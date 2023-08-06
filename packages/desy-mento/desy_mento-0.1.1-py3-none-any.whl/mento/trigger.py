#!/usr/bin/env python

# SPDX-FileCopyrightText: 2021 S. Vijay Kartik <vijay.kartik@desy.de>, DESY
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Main interface to online analysis functionality

Provides two classes to create triggers that can, well, automatically
trigger processes while data taking is going on. These processes may
be local programs or Bash scripts, or programs run on a remote machine
via SSH, or SLURM jobs submitted to reserved HPC nodes via SSH+sbatch.

Classes
-------

Trigger:
    Simple class containing information about:
    1. Type of processing to run (local, remote, SLURM, etc.)
    2. Beamtime metadata (computing resource allocation,
       temporary authentication accounts/tokens for remote connection, etc.)

TriggerMethod:
    Simple enumerator listing all possible triggering methods

    Local Bash script, Remote call via SSH, SLURM job submission via sbatch,
    SLURM job submission via REST API, etc.

Functions
---------

get_ssh_command(bt_info, destination=None):
    get the full SSH command to connect to an allocated remote node

def get_sbatch_command(bt_info, job_name, job_dependency, logfile_path):
    get the full sbatch command to submit a batch job to the allocated SLURM reservation
"""

from mento.utils import run_subprocess
from mento.metadata import get_beamtime_metadata
from mento.metadata import BeamtimeMetadata  # Just for type hinting

import os
from enum import IntEnum, unique, auto


@unique
class TriggerMethod(IntEnum):
    """
    Supported triggering methods.
    """
    SLURM_REST_API = auto()
    REMOTE_COMMAND = auto()
    REMOTE_SBATCH_SCRIPT = auto()
    LOCAL_BASH_SCRIPT = auto()


class Trigger:
    """
    Collective information needed to trigger an online analysis run.

    Information about access to remote online computing resources
    """
    # Unclear what type hint to provide when a function argument is a path. typing.Union[str, bytes, os.Pathlike]?
    def __init__(self, trigger_method=TriggerMethod.REMOTE_SBATCH_SCRIPT, beamline_root_dir='/gpfs/current'):
        """
        Construct a Trigger object with relevant information for remote computing resource access.

        :param trigger_method: method to use for triggering processing, either locally or remotely
        :param beamline_root_dir: full path to root directory of beamline filesystem
        """
        self.bt_info = get_beamtime_metadata(root_dir=beamline_root_dir)
        if trigger_method not in TriggerMethod:  # TODO: This doesn't work at the moment
            raise RuntimeError(f'Trigger method not known: {str(trigger_method)}')
        self.trigger_method = trigger_method

    # Unclear what type hint to provide when a function argument is a path. typing.Union[str, bytes, os.Pathlike]?
    def run(self, arg_list=None,
            destination: str = None,
            job_name: str = None, job_time: str = None,
            job_dependency: str = None, log_file=None) -> None:
        """
        Function to trigger processing on remote nodes.

        :param arg_list: list containing command (or script file path),
                         and commandline arguments for different trigger methods
        :param destination: name of compute node on which to perform (or submit)
                            the processing job (if None (default), chooses a node from the reserved nodes)
        :param job_name: name of processing job (will appear in the Slurm queue)
                        (if None (default), a name will be auto-generated)
        :param job_time: time limit for processing job (if None (default), time limit set to one day through Slurm)
        :param job_dependency: Slurm dependency (if None, the processing job will be run independent of other jobs)
        :param log_file: file to write logs from the job as recorded by Slurm (if None, no logs will be saved)
        :returns: None
        """
        if arg_list is None:
            arg_list = []
        if not arg_list:
            raise RuntimeError('Command (or executable script) not provided')
        cmd = retrieve_cmd(arg_list)
        cmd_args = retrieve_arg_list(arg_list)
        if self.trigger_method is TriggerMethod.LOCAL_BASH_SCRIPT:
            script_file = cmd
            script_args = cmd_args
            if not os.path.exists(script_file):
                raise FileNotFoundError(f'File not found: {script_file}')
            if not os.access(script_file, os.X_OK):
                raise RuntimeError(f'File not executable: {script_file}')
            run_subprocess([script_file] + script_args)
        elif self.trigger_method in [TriggerMethod.REMOTE_COMMAND, TriggerMethod.REMOTE_SBATCH_SCRIPT]:
            remote_command = cmd
            remote_command_args = cmd_args
            ssh_command = get_ssh_command(self.bt_info, destination=destination)
            if self.trigger_method is TriggerMethod.REMOTE_SBATCH_SCRIPT:
                sbatch_file = remote_command
                sbatch_command = get_sbatch_command(self.bt_info,
                                                    job_name=job_name,
                                                    job_dependency=job_dependency,
                                                    job_maxtime=job_time,
                                                    logfile_path=log_file)
                remote_command = f'{sbatch_command} {sbatch_file}'
            # The local command to run looks like this: ssh -o options hostname "sbatch sbatchoptions sbatchfile sbatchargs" &
            # The last entry in the argument list is to finish the command to run on the remote node, and push the SSH call to the background
            run_subprocess([ssh_command, f'"{remote_command}'] + remote_command_args + ['" &'])
            # TODO: Check if & is needed when using subprocess.Popen with start_new_session=True
        elif self.trigger_method is TriggerMethod.SLURM_REST_API:
            raise NotImplementedError('SLURM REST API not available')
        else:
            raise RuntimeError('Trigger method not known')


def get_ssh_command(bt_info: BeamtimeMetadata, destination: str = None) -> str:
    """
    Prepare SSH command to be run on the local node, including all options for accessing remote computing resources.

    Put together temporary online analysis user, access keys, and job submission node in one SSH call.

    :param bt_info: BeamtimeMetada object with information about current beamtime (including SSH credentials)
    :param destination: name of SSH destination node. If None, picks the first reserved node
    :returns: prepared SSH command with all required options for remote connections
    """
    ssh_command = '/usr/bin/ssh'
    ssh_opts_general = (' -o BatchMode=yes'  # Leading space in SSH options is important!
                        ' -o CheckHostIP=no'
                        ' -o StrictHostKeyChecking=no'
                        ' -o GSSAPIAuthentication=no'
                        ' -o GSSAPIDelegateCredentials=no'
                        ' -o PasswordAuthentication=no'
                        ' -o PubkeyAuthentication=yes'
                        ' -o PreferredAuthentications=publickey'
                        ' -o IdentitiesOnly=yes'
                        ' -o ConnectTimeout=10')
    online_info = bt_info.online
    ssh_opts_user = f' -l {online_info.ssh.user}'
    ssh_opts_key = f' -i {online_info.ssh.key}'
    # When no SSH host specified, just use the first reserved node, should be ok (e.g., for SLURM)
    ssh_opts_host = destination if destination else str(online_info.nodes[0])
    ssh_command += f'{ssh_opts_general}{ssh_opts_key}{ssh_opts_user} {ssh_opts_host}'
    return ssh_command


# Unclear what type hint to provide when a function argument is a path. typing.Union[str, bytes, os.Pathlike]?
def get_sbatch_command(bt_info: BeamtimeMetadata,
                       job_name: str = None,
                       job_maxtime: str = None,
                       job_dependency: str = None,
                       logfile_path: str = None) -> str:
    """
    Prepare SLURM sbatch command to be run on the remote node, including all Slurm reservation parameters.

    :param bt_info: BeamtimeMetada object with information about current beamtime (including Slurm resources)
    :param job_name: Slurm job name, for identification (if None (default), uses 'mento_beamline_beamtime')
    :param job_maxtime: Time limit for a Slurm job (if None (default), time limit set to one day)
    :param job_dependency: Slurm job dependency, to influence job queue handling (and better utilize CPU/Memory)
                           (if None (default), no dependency between submitted jobs)
    :param logfile_path: full path to logfile containing standard output and standard error from Slurm job
                            (if None (default), produces no Slurm output file)
    :returns: prepared sbatch command with all required options for job submission
    """
    sbatch_command = '/usr/bin/sbatch'
    sbatch_opts_jobname = job_name if job_name else f'mento_{bt_info.beamline}_{bt_info.beamtime}'
    sbatch_opts_dependency = job_dependency if job_dependency else ''
    sbatch_opts_maxtime = job_maxtime if job_maxtime else '1-0'  # Default time limit set to 1 day
    sbatch_opts_logfile = logfile_path if logfile_path else os.devnull  # No slurm output file if os.devnull
    sbatch_opts = (f' --partition={bt_info.online.slurm.partition}'
                   f' --reservation={bt_info.online.slurm.reservation}'
                   f' --job-name={sbatch_opts_jobname}'
                   f' --dependency={sbatch_opts_dependency}'
                   f' --time={sbatch_opts_maxtime}'
                   f' --output={sbatch_opts_logfile}'
                   f' --error={sbatch_opts_logfile}')
    sbatch_command += sbatch_opts
    return sbatch_command


def retrieve_cmd(arg_list: list):
    """
    Internal function.

    Extract string containing command (or path to script file) from the argument list arg_list provided to Trigger.run.
    The command (or script file) is expected to appear first in the argument list.

    :param arg_list: list containing command and arguments
    :returns: command, given as first entry in the argument list
    """
    # TODO: This doesn't account for script file names which include spaces!
    # arg_list can look like one of these (empty lists not expected):
    # 1. ['cmd']
    # 2. ['cmd arg1 arg2 ... argN']
    # 3. ['cmd', [arg1, arg2, ..., argN]]
    # 4. ['cmd', arg1, arg2, ..., argN]
    if not arg_list:
        raise RuntimeError('Empty list input not supported')
    cmd = str(arg_list[0]).split(None, 1)[0]

    return cmd


def retrieve_arg_list(arg_list: list):
    """
    Internal function.

    Extract list of arguments for the command also given in the argument list arg_list provided to Trigger.run.

    :param arg_list: list containing command (or script file path) and command (or script) arguments
    :returns: list of arguments to be forwarded to the command (or script)
    """
    # TODO: This doesn't account for script file names which include spaces!
    # arg_list can look like one of these (empty lists not expected):
    # 1. ['cmd']
    # 2. ['cmd arg1 arg2 ... argN']
    # 3. ['cmd', [arg1, arg2, ..., argN]]
    # 4. ['cmd', arg1, arg2, ..., argN]
    if not arg_list:
        raise RuntimeError('Empty list input not supported')
    if len(arg_list) == 1:  # Cases 1. and 2.
        if arg_list[0] == retrieve_cmd(arg_list):  # Case 1.
            cmd_args = []
        else:  # Case 2.
            cmd_args = str(arg_list[0]).split()[1:]  # BEWARE!! Wrong if script_file has spaces
    elif len(arg_list) == 2 and isinstance(arg_list[0], str) and isinstance(arg_list[1], list):  # Case 3, probably most commonly occurring
        cmd_args = arg_list[1]
    else:  # Case 4.
        cmd_args = arg_list[1:]

    return cmd_args
