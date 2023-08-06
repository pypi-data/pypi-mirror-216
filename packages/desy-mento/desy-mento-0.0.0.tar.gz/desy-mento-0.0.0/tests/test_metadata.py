# SPDX-FileCopyrightText: 2021 S. Vijay Kartik <vijay.kartik@desy.de>, DESY
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mento.metadata import *

from pathlib import Path
import pytest

bad_files_root = Path('tests/data/gpfs/local')
incomplete_metadata_file = bad_files_root / 'incomplete-metadata-12345678.json'
noonline_metadata_file = bad_files_root / 'noonline-metadata-12345678.json'
noonlinenoasapo_metadata_file = bad_files_root / 'noonlinenoasapo-metadata-12345678.json'

beamtime_root = Path('tests/data/gpfs/current')
complete_metadata_file = 'beamtime-metadata-12345678.json'
sshkey_path = 'shared/id_rsa'
asapo_token_ro = 'shared/asapo-token-clbt.txt'
asapo_token_rw = 'shared/asapo-token.txt'

ssh = SSHInfo(user='bttest01', key=str((beamtime_root / sshkey_path).resolve()))
slurm = SlurmInfo(partition='ponline', reservation='12345678')
asapo = AsapoInfo(token_ro=str((beamtime_root / asapo_token_ro).resolve()),
                  token_rw=str((beamtime_root / asapo_token_rw).resolve()),
                  endpoint='asapo-ps-0.desy.de:8400')
online = OnlineInfo(ssh=ssh, slurm=slurm,
                    nodes=['hpc01', 'hpc02'],
                    blfs_mountpoint='/beamline/p9999')
bt_info = BeamtimeMetadata(beamline='p9999', beamtime='12345678',
                           corefs_path='/asap3/petra3/gpfs/', tag='current',
                           online=online, asapo=asapo)


def test_sshinfo_construction_default():
    with pytest.raises(TypeError):
        _ = SSHInfo()


def test_slurminfo_construction_default():
    with pytest.raises(TypeError):
        _ = SlurmInfo()


def test_asapoinfo_construction_default():
    with pytest.raises(TypeError):
        _ = AsapoInfo()


def test_onlineinfo_construction_default():
    with pytest.raises(TypeError):
        _ = OnlineInfo()


def test_onlineinfo_construction_optionalargs():
    test_online = OnlineInfo(ssh=ssh, slurm=slurm)
    assert not test_online.nodes  # Default-constructed list is empty
    assert not test_online.blfs_mountpoint  # Default constructed str is None


def test_beamtimemetadata_construction_default():
    with pytest.raises(TypeError):
        _ = BeamtimeMetadata()


def test_beamtimemetadata_construction_optionalargs():
    test_bt_info = BeamtimeMetadata(beamline='p00', beamtime='1234567890',
                                    corefs_path='remote/data/dir', tag='current')
    assert test_bt_info.online is None
    assert test_bt_info.asapo is None


def test_beamtimemetadata_construction_allargs():
    test_bt_info = BeamtimeMetadata(beamline='p00', beamtime='1234567890',
                                    corefs_path='remote/data/dir', tag='current',
                                    online=OnlineInfo(ssh=ssh, slurm=slurm,
                                                      nodes=['node01', 'node02'],
                                                      blfs_mountpoint='/temp/remote/p00'),
                                    asapo=asapo)
    assert test_bt_info.beamline == 'p00'
    assert test_bt_info.beamtime == '1234567890'
    assert test_bt_info.corefs_path == 'remote/data/dir'
    assert test_bt_info.tag == 'current'
    bt_online = test_bt_info.online
    assert bt_online.ssh == ssh
    assert bt_online.slurm == slurm
    assert bt_online.nodes == ['node01', 'node02']
    assert bt_online.blfs_mountpoint == '/temp/remote/p00'
    bt_asapo = test_bt_info.asapo
    assert bt_asapo == asapo


def test_beamtimemetadata_construction_kwargs():
    test_bt_info_01 = BeamtimeMetadata(beamline='p00', beamtime='1234567890',
                                       corefs_path='remote/data/dir', tag='current',
                                       online=online)

    test_bt_info_02 = BeamtimeMetadata(online=online, beamline='p00', beamtime='1234567890',
                                       corefs_path='remote/data/dir', tag='current')

    # Shows keyword args keep the code robust, users don't need to remember positions
    assert test_bt_info_01 == test_bt_info_02


def test_locate_metadata_file_success():
    root_dir = 'tests/data/gpfs'
    assert locate_metadata_file(root_dir) == str(beamtime_root / complete_metadata_file)


def test_locate_metadata_file_bad_root():
    bad_root_dir = '/non/existent/path'
    with pytest.raises(FileNotFoundError, match='Root directory not found'):
        _ = locate_metadata_file(bad_root_dir)


def test_locate_metadata_file_no_file():
    bad_root_dir = 'tests/data'
    with pytest.raises(FileNotFoundError, match='Metadata file not found'):
        _ = locate_metadata_file(bad_root_dir)


def test_locate_metadata_file_multiple_files(tmp_beamtime_dirtree, tmp_path):
    # Ensure multiple metadata files appear under tmp_path
    # by temporarily duplicating entire directory tree
    tmp_beamtime_dirtree('current')
    tmp_beamtime_dirtree('commissioning')
    with pytest.raises(RuntimeError, match='Multiple metadata files found'):
        _ = locate_metadata_file(tmp_path)


def test_locate_metadata_file_ignore_local_dir(tmp_beamtime_dirtree, tmp_path):
    # Ensure multiple metadata files appear under tmp_path
    # by temporarily duplicating entire directory tree
    # But the directory tree under 'local' should be ignored
    tmp_beamtime_dirtree('current')
    tmp_beamtime_dirtree('local')
    assert locate_metadata_file(tmp_path) == str(tmp_path / 'current' / complete_metadata_file)


def test_parse_metadata_file_success():
    test_bt_info = parse_metadata_file(beamtime_root / complete_metadata_file)
    assert test_bt_info == bt_info


def test_parse_metadata_file_no_online_no_asapo():
    test_bt_info = parse_metadata_file(noonlinenoasapo_metadata_file)
    assert test_bt_info.online is None  # valid field value for BeamtimeMetadata.online
    assert test_bt_info.asapo is None  # valid field value for BeamtimeMetadata.asapo
    assert test_bt_info.beamline == 'p9999'
    assert test_bt_info.beamtime == '12345678'
    assert test_bt_info.corefs_path == '/asap3/petra3/gpfs/'
    assert test_bt_info.tag == 'current'


def test_parse_metadata_file_no_online():
    # Because ASAPO is in metadata file, but no ASAPO token files are
    # present under 'local/shared', no BeamtimeMetadata object will be created.
    # This is only because of missing token files in the test directory.
    # There will be a BeamtimeMetada object under real conditions
    # (with token files under 'current/shared').
    with pytest.raises(FileNotFoundError, match=r'File not found \(but mentioned in metadata\)'):
        _ = parse_metadata_file(noonline_metadata_file)


def test_parse_metadata_file_no_file():
    nonexistent_file = '/does/not/exist.json'
    with pytest.raises(FileNotFoundError, match='Metadata file not found'):
        _ = parse_metadata_file(nonexistent_file)


def test_parse_metadata_file_bad_format():
    not_json_file = sshkey_path  # empty file, obviously not JSON
    with pytest.raises(ValueError, match='Parsing of metadata file failed'):
        _ = parse_metadata_file(beamtime_root / not_json_file)


def test_parse_metadata_file_missing_keys():
    with pytest.raises(ValueError, match='Required metadata not found'):
        _ = parse_metadata_file(incomplete_metadata_file)


@pytest.mark.parametrize('file_path', [sshkey_path,
                                       asapo_token_ro,
                                       asapo_token_rw])
def test_parse_metadata_file_missing_mentioned_file(file_path, tmp_beamtime_dirtree):
    # "missing mentioned file" means the metadata file claims
    # that the file exists at the given path (e.g. SSH key,
    # ASAP::O token), but there is no such file at the path

    # Make a temporary copy of the beamline directory tree,
    # so that we can safely delete files for testing
    tmp_beamtime_root = tmp_beamtime_dirtree('current')
    # Find full path of metadafile in the copied beamline directory tree
    metadata_file = tmp_beamtime_root / complete_metadata_file
    # Delete file, so metadata file will contain a path to a non-existent file
    file_to_delete = tmp_beamtime_root / file_path
    file_to_delete.unlink()

    with pytest.raises(FileNotFoundError, match=r'File not found \(but mentioned in metadata\)'):
        _ = parse_metadata_file(metadata_file)
