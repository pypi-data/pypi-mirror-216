#!/usr/bin/env python

# SPDX-FileCopyrightText: 2021 S. Vijay Kartik <vijay.kartik@desy.de>, DESY
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Metadata objects and related functions for use by MENTO modules.

Classes
-------

BeamtimeMetadata:
    Contains all relevant metadata about current beamtime,
    and computing resources allocated to the beamtime for
    online processing

SSHInfo:
    Contains authentication information for remotely connecting
    to reserved nodes via SSH

SlurmInfo:
    Contains details of Slurm resource allocation, including
    reservation and partition

AsapoInfo:
    Contains connection details for ASAPO

OnlineInfo:
    Contains SSH, Slurm, temporary beamline filesystem info,
    names of reserved nodes for online processing

Functions
---------

get_beamtime_metadata(root_dir):
    Load all beamtime metadata required to access remote computing resources.

locate_metadata_file(root_dir):
    Guess the location of the metadata file for current beamtime.

parse_metadata_file(metadata_file):
    Read metadata file located at the root of every beamtime directory.
    Get information about online analysis, like temporary account name,
    credentials, slurm reservations etc.
"""

from pathlib import Path
import json  # To parse the beamtime metadata file
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SSHInfo:
    """
    Contains authentication information for remotely connecting
    to reserved nodes via SSH
    """
    user: str  # Temporary user, only available during beamtime (if reserved)
    key: str  # SSH access only through public key authentication


@dataclass
class SlurmInfo:
    """
    Contains details of Slurm resource allocation, including
    reservation and partition
    """
    partition: str
    reservation: str


@dataclass
class AsapoInfo:
    """
    Contains connection details for ASAPO
    """
    endpoint: str
    token_ro: str
    token_rw: str


@dataclass
class OnlineInfo:
    """
    Contains SSH, Slurm, temporary beamline filesystem info,
    names of reserved nodes for online processing
    """
    ssh: SSHInfo
    slurm: SlurmInfo
    nodes: list = field(default_factory=list)  # Nodes reserved for beamtime duration
    blfs_mountpoint: str = None  # Beamline filesystem is temporarily mounted on reserved nodes


@dataclass
class BeamtimeMetadata:
    """
    Contains all relevant metadata about current beamtime,
    and computing resources allocated to the beamtime for
    online processing
    """
    beamline: str
    beamtime: str
    corefs_path: str
    tag: str  # 'current' or 'commissioning'
    online: Optional[OnlineInfo] = None
    asapo: Optional[AsapoInfo] = None


# Unclear what type hint to provide when a function argument is a path. typing.Union[str, bytes, os.Pathlike]?
def locate_metadata_file(root_dir='/gpfs/current') -> str:
    """
    Get the path to the metadata JSON file for the current beamtime

    This function only works in the online situation where there is a currently
    running beamtime.

    :param root_dir: top directory of beamtime
    :returns: full path to metadata JSON file provided for the current beamtime
    """
    # root_dir for beamline filesystems is, AFAIK, always '/gpfs' at PETRA III
    # /gpfs/local is always present, we want to ignore it. Normally there should be
    # either a /gpfs/current, or /gpfs/commissioning subdirectory (sometimes both).
    # The metadata file should be located directly in this subdirectory
    # When both 'current' and 'commissioning' directories are present, we usually want the 'current'
    # directory corresponding to the user beamtime. Hence the default parameter value.
    root_dir = Path(root_dir)
    try:
        beamtime_dirs = [path for path in root_dir.iterdir()
                         if path.is_dir() and (path.name != 'local')]
    except FileNotFoundError:  # if root_dir does not exist
        raise FileNotFoundError(f'Root directory not found: {root_dir}')
    metadata_files = []
    for curr_dir in beamtime_dirs + [root_dir]:  # also check root_dir, in case the root directory contains a metadata file (e..g when root_dir = '/gpfs/current')
        curr_dir_metadata_files = list(curr_dir.glob('*metadata*.json'))
        metadata_files.extend(curr_dir_metadata_files)  # if there happens to be more than one directory with a metadata json file - which is BAD
    num_metadata_files = len(metadata_files)
    if num_metadata_files == 1:  # Desired case, with specific user or commissioning run
        return str(metadata_files[0])
    elif num_metadata_files == 0:  # No metadata file is found
        raise FileNotFoundError(f'Metadata file not found under {root_dir}')
    elif num_metadata_files > 1:  # Both user run and commissioning directories present, AND root=/gpfs
        # A more specific root_dir is needed, to have a unique metadata file
        raise RuntimeError(f'Multiple metadata files found under {root_dir}')


# Unclear what type hint to provide when a function argument is a path. typing.Union[str, bytes, os.Pathlike]?
def parse_metadata_file(metadatafile_path) -> BeamtimeMetadata:
    """
    Parse beamtime metadata file to get information relevant to current beamtime and online analysis.

    :param metadatafile_path: full path to metadata file
    :returns: tuple containing variables relevant for online analysis
    """
    # DESY-IT has switched to a fully valid JSON file for the beamtime metadata file (since 2020.06.12).
    metadatafile_path = Path(metadatafile_path)
    if not metadatafile_path.exists():
        raise FileNotFoundError(f'Metadata file not found: {metadatafile_path}')
    with open(metadatafile_path, 'r') as mdfile:
        try:
            md = json.load(mdfile)
            beamline = str(md['beamline'])
            if 'beamtimeId' in md:  # For user run
                beamtime = str(md['beamtimeId'])
                tag = 'current'
            elif 'id' in md:  # For commissioning run
                beamtime = str(md['id'])
                tag = 'commissioning'
            else:
                raise ValueError('Required metadata not found: Beamtime/Commissioning ID')
            corefs_path = str(md['corePath'])
            if 'onlineAnalysis' not in md:
                print('Online analysis resources not found in metadata file')
                online_info = None
            else:
                online_meta = md['onlineAnalysis']
                reserved_nodes = online_meta['reservedNodes']
                slurm_reservation = str(online_meta['slurmReservation'])
                slurm_partition = str(online_meta['slurmPartition'])
                temp_user_name = str(online_meta['userAccount'])
                # Store absolute path of SSH key, to ensure it
                # can be used from anywhere
                # (who knows where a third-party SSH call is made from)
                temp_user_sshkeyfile = _make_path_absolute(metadatafile_path,
                                                           str(online_meta['sshPrivateKeyPath']))
                # TODO: Strictly speaking, specifying blfs_mountpoint isn't
                #  part of parsing the metadata file
                # Results are written to the beamline filesystem through
                # a temporary mountpoint on reserved cluster nodes
                # Hardcoded mountpoint, current location as per IT
                blfs_mountpoint = str(Path('/beamline', beamline))

                ssh_info = SSHInfo(user=temp_user_name,
                                   key=temp_user_sshkeyfile)
                slurm_info = SlurmInfo(partition=slurm_partition,
                                       reservation=slurm_reservation)
                online_info = OnlineInfo(ssh=ssh_info,
                                         slurm=slurm_info,
                                         nodes=reserved_nodes,
                                         blfs_mountpoint=blfs_mountpoint)
            if 'asapo' not in md:
                print('ASAP::O resources not found in metadata file')
                asapo_info = None
            else:
                asapo_meta = md['asapo']
                asapo_endpoint = str(asapo_meta['endpoint'])
                # Store absolute path of tokens, to ensure they
                # can be used from anywhere
                asapo_token_ro = _make_path_absolute(metadatafile_path,
                                                     str(asapo_meta['beamtimeClbtTokenPath']))
                asapo_token_rw = _make_path_absolute(metadatafile_path,
                                                     str(asapo_meta['beamtimeTokenPath']))
                asapo_info = AsapoInfo(endpoint=asapo_endpoint,
                                       token_ro=asapo_token_ro,
                                       token_rw=asapo_token_rw)
        except KeyError as e:
            raise ValueError(f'Required metadata not found: {e}')
        except json.JSONDecodeError:
            raise ValueError(f'Parsing of metadata file failed (invalid JSON content): {metadatafile_path}')

    # TODO: Rethink whether checking the files' existence is this function's responsibility or not
    # Check that the files mentioned in the metadata file do exist
    if online_info is not None:
        if not Path(online_info.ssh.key).exists():
            raise FileNotFoundError(f'File not found (but mentioned in metadata): {online_info.ssh.key}')
    if asapo_info is not None:
        if not Path(asapo_info.token_ro).exists():
            raise FileNotFoundError(f'File not found (but mentioned in metadata): {asapo_info.token_ro}')
        if not Path(asapo_info.token_rw).exists():
            raise FileNotFoundError(f'File not found (but mentioned in metadata): {asapo_info.token_rw}')
    return BeamtimeMetadata(beamline=beamline, beamtime=beamtime,
                            corefs_path=corefs_path, tag=tag,
                            online=online_info, asapo=asapo_info)


# Unclear what type hint to provide when a function argument is a path. typing.Union[str, bytes, os.Pathlike]?
def get_beamtime_metadata(root_dir='/gpfs/current') -> BeamtimeMetadata:
    """
    Convenience function to load partial beamtime metadata relevant for online analysis.

    Automatically finds a metadata file and parses it for information required for online analysis.

    :param root_dir: top directory for beamtime
    :returns: tuple containing 'relevant' metadata for later use in online analysis
    """
    metadata_file = locate_metadata_file(root_dir)
    return parse_metadata_file(metadata_file)


# Unclear what type hint to provide when a function argument is a path. typing.Union[str, bytes, os.Pathlike]?
def _make_path_absolute(metadatafile_path, file_path) -> str:
    """
    Internal function.

    The file paths provided in the metadata file are relative
    to the location of the metadata file itself. Having absolute
    paths for these files would be useful, because then these files
    can be used from any position in the directory tree.
    :param metadatafile_path: path to metadata file (can be either relative or absolute,
                              must simply be reachable from wherever this function is called)
    :param file_path: file path as mentioned in metadata file, assumed to be relative to it
    :returns: absolute path to the file mentioned in the metadata file
    """
    metadatafile_dir_abs = Path(metadatafile_path).resolve().parent
    return str(metadatafile_dir_abs / file_path)
