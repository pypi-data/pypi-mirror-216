#!/usr/bin/env python

# SPDX-FileCopyrightText: 2021 S. Vijay Kartik <vijay.kartik@desy.de>, DESY
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Utility functions for internal use by online analysis triggering modules at different beamlines.

Functions
---------

_map_local_to_remote_path(beamline_local_path, remote_rootdir, remote_subdir):
    Generate file path on the remote cluster corresponding to a local file path as shown at the beamline.

_name_resultfile_with_suffix(datafile_path, result_suffix):
    Generate result file name on local beamline filesystem, derived from input data file.

_name_resultdir(datafile_path):
    Get the full path of the location to store results corresponding to the input data file.

make_writable_dir(dir_name):
    Create a directory and make it world-writable, world-readable.

run_subprocess():
    Run command either on local machine with Bash, or after connecting to remote machine with SSH

run_slurm():
    Not yet implemented

retrieve_script_path(arg_list):
    Get the path to the local/remote script to be run by the trigger

retrieve_arg_list(arg_list):
    Get the arguments to be fed to the local/remote script
    to be run by the trigger

flatten_arg_list(arg_list):
    Flatten all nested lists inside a list to present a
    one-level list (with no list element being a list itself)
"""

import sys
import re  # To fix up concatenated remote command string
import shlex  # To tokenize arguments for subprocess
import subprocess
from pathlib import Path

assert sys.version_info >= (3, 7), 'Python version too old'  # If Python version < 3.7 no point going further


# Unclear what type hint to provide when function returns a path. typing.Union[str, bytes, os.Pathlike]?
def _map_local_to_remote_path(beamline_local_path, remote_rootdir, remote_subdir):
    """
    Generate file path on the remote cluster corresponding to a local file path as shown at the beamline.

    This generates the right path, for files either in the core filesystem, or a mountpoint for the
    beamline filesystem present on a Maxwell node.

    :param beamline_local_path: full path of a file as seen at the beamline
    :param remote_rootdir: full path of the root directory for the file in the cluster
                            (core-fs for data, beamline mountpoint for results)
    :param remote_subdir: subdirectory name, 'raw' for data files, 'processed' for result and log files
    :returns: full path to the file, valid on the remote cluster
    """
    local_path_parts = Path(beamline_local_path).parts
    if remote_subdir not in local_path_parts:
        raise FileNotFoundError('Directory in desired remote path has no equivalent in local path')
    subdir_index = local_path_parts.index(remote_subdir)  # get the first occurrence of remote_subdir
    remote_path = Path(remote_rootdir, *local_path_parts[subdir_index:])
    return str(remote_path)


# Unclear what type hint to provide when function returns a path. typing.Union[str, bytes, os.Pathlike]?
def _name_resultfile_with_suffix(datafile_path, result_suffix):
    """
    Make up the name of a result file, derived from the input data file name.

    :param datafile_path: full path to data file
    :param result_suffix: suffix to use to generate result filename
    :returns: name of result file (Note: not the full path). The file is not guaranteed to exist at this point.
    """
    datafile_path = Path(datafile_path)
    result_suffix = result_suffix if result_suffix.startswith('_') else ('_' + result_suffix)

    result_filename_stem = datafile_path.stem + result_suffix
    # with_stem is only available from Python 3.9 onwards
    # result_filename = datafile_path.with_stem(result_filename_stem)
    # return result_filename.name
    # manually build up new stem+suffix for filename (works in all Python versions)
    result_filename = result_filename_stem + datafile_path.suffix
    return result_filename


# Unclear what type hint to provide when function returns a path. typing.Union[str, bytes, os.Pathlike]?
def _name_resultdir(datafile_path, data_root=None, results_root=None):
    """
    Make up a directory name to store result files corresponding to the input data file.

    :param datafile_path: path to data file
    :param data_root: top directory name under which data file is present (if None (default), uses 'raw')
    :param results_root: path to root directory for all results (if None (default), makes up a path
                         using 'processed/onlineanalysis' in place of `data_root` present in `datafile_path`)
    :returns: path to results directory. The directory is not guaranteed to exist at this point.
    """
    data_dir = Path(datafile_path).parent
    data_root = data_root if data_root else 'raw'
    results_root = results_root if results_root else 'processed/onlineanalysis'

    data_dir_parts = data_dir.parts
    if data_root not in data_dir_parts:
        raise FileNotFoundError(f'Expected "{data_root}" directory not found within path: {datafile_path}')
    data_root_index = data_dir_parts.index(data_root)  # get the first occurrence of data_root

    results_dir = Path(*data_dir_parts[:data_root_index], results_root, *data_dir_parts[data_root_index+1:])
    return str(results_dir)


# Unclear what type hint to provide when a function argument is a path. typing.Union[str, bytes, os.Pathlike]?
def make_writable_dir(dir_name) -> None:
    """
    Create a directory and make it world-writable, world-readable.

    :param dir_name: path to directory to be created
    :returns: None
    """
    dir_name = Path(dir_name)
    # Default mode of leaf directory is supposed to 0o77, but it may be
    # ignored, depending on the umask. Set the mode explicitly later
    dir_name.mkdir(mode=0o777, parents=True, exist_ok=True)
    # In case the results directory is created with permissions that forbid the beamtime account from writing to it.
    # Tests show this does indeed happen, and is probably due to the
    # umask inherited from the Macroserver executing the MENTO module functions
    dir_name.chmod(0o777)


def prepare_results_filename(data_file_path, data_root=None, results_root=None):
    """
    Make up the name of a result file, derived from the input data file name.
    Create the appropriate directory tree to store this result file in.
    :param data_file_path: path to data file
    :param data_root: top directory name under which data file is present (if None (default), uses 'raw')
    :param results_root: path to root directory for all results (if None (default), makes up a path
                         using 'processed/onlineanalysis' in place of `data_root` present in `datafile_path`)
    :return:
    """
    # Create directory for storing analysis results
    results_dir = _name_resultdir(data_file_path, data_root, results_root)
    make_writable_dir(results_dir)  # creates directory with 777 permissions
    results_filename = _name_resultfile_with_suffix(data_file_path, '_results')
    results_file_path = Path(results_dir, results_filename)  # Note: results_filename doesn't exist at this point

    return str(results_file_path)


def get_path_core(local_path, remote_dir):
    return _map_local_to_remote_path(local_path, remote_dir, 'raw')


def get_path_mountpoint(local_path, remote_dir, tag='current'):
    remote_dir = Path(remote_dir, tag)
    return _map_local_to_remote_path(local_path, str(remote_dir), 'processed')


def run_subprocess(arg_list: list) -> None:
    """
    Use Python's subprocess module to run a command with arguments.

    :param arg_list: list comprising the command (+ arguments) to be run
    :returns: None
    """
    flattened_arg_list = list(flatten_arg_list(arg_list))  # In case there are lists inside arg_list, and not just 'plain' entries
    single_string_of_args = ' '.join(str(entry) for entry in flattened_arg_list)  # No input sanitization done here
    # Remove the extraneous space between the last argument to the remote program
    # and the ending double-quote that defines the remote command, and keep the & at the end
    # to immediately send the remote command to the background
    single_string_of_args = re.sub(' " &$', '" &', single_string_of_args)
    tokenized_args_list = shlex.split(single_string_of_args, posix=True)  # posix=True needed to allow parsing quoted empty strings
    try:
        subprocess.Popen(tokenized_args_list, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    except ValueError as e:
        print(e, file=sys.stderr)
        print('Did not trigger analysis - invalid args to subprocess.Popen()', file=sys.stderr)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        print('Did not trigger analysis - no trigger script found', file=sys.stderr)
    except OSError as e:
        print(e, file=sys.stderr)
        print('Did not trigger analysis', file=sys.stderr)


def run_slurm():
    """
    Use Slurm REST API to submit a batch job directly from the local machine.
    :returns: None
    """
    raise NotImplementedError('No implementation exists')


def flatten_arg_list(arg_list: list):
    """
    Internal function.

    Flattens any internal lists present in arg_list.

    :param arg_list: a list containing 'scalar' entries and list entries
    :returns: a flattened list only containing 'scalar' (i.e., non-list) entries
    """
    for maybe_list in arg_list:
        if isinstance(maybe_list, list) and not isinstance(maybe_list, str):  # May not work for non-latin encodings
            for sub_list in flatten_arg_list(maybe_list):
                yield sub_list
        else:
            yield maybe_list
