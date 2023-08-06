# SPDX-FileCopyrightText: 2021 S. Vijay Kartik <vijay.kartik@desy.de>, DESY
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mento.utils import *
# Explicitly import internal functions to be able to test them here
from mento.utils import _map_local_to_remote_path, _name_resultfile_with_suffix, _name_resultdir

import os
import pytest


def test_map_local_to_remote_path():
    input_data_file = 'tests/data/gpfs/current/processed/onlineanalysis/dummy/scan/data_test_util_funcs.h5'
    assert _map_local_to_remote_path(os.path.abspath(input_data_file), '/beamline/pXX', 'processed') == '/beamline/pXX/processed/onlineanalysis/dummy/scan/data_test_util_funcs.h5'


def test_name_resultfile_with_suffix():
    input_data_file = 'tests/data/gpfs/current/raw/dummy/scan/data.h5'
    result_suffix = '_test_util_funcs'
    assert _name_resultfile_with_suffix(os.path.abspath(input_data_file), result_suffix) == 'data_test_util_funcs.h5'


def test_name_result_dir():
    input_data_file = 'tests/data/gpfs/current/raw/dummy/scan/data.h5'
    assert _name_resultdir(os.path.abspath(input_data_file)) == os.path.abspath('tests/data/gpfs/current/processed/onlineanalysis/dummy/scan')


def test_make_writable_dir_success(tmp_beamtime_dirtree):
    tmp_beamtime_root = tmp_beamtime_dirtree('scratch')  # temporary copy of beamtime directory, can write inside at will
    dir_name = tmp_beamtime_root / 'processed/test_dir'
    file_name = dir_name / 'test_file.h5'

    # Test that directory creation works
    make_writable_dir(dir_name)
    assert os.access(dir_name, os.W_OK)

    # Test that file creation is allowed
    # i.e., the directory was created with the
    # appropriate write permissions
    with open(file_name, 'a'):
        os.utime(file_name, None)
    assert file_name.exists()


@pytest.mark.skip(reason='Test fails in CI because we are root in the Docker image, so permission is not denied')
def test_make_writable_dir_permission_denied():
    dir_name = '/sbin/data/gpfs/test_dir'
    with pytest.raises(PermissionError):
        make_writable_dir(dir_name)


def test_prepare_results_filename(tmp_beamtime_dirtree):
    tmp_beamtime_root = tmp_beamtime_dirtree('scratch')  # temporary copy of beamtime directory, can write inside at will
    input_data_file = tmp_beamtime_root / 'raw/dummy/scan/data.h5'
    expected_results_dir = tmp_beamtime_root / 'processed/onlineanalysis/dummy/scan/'
    expected_results_file = expected_results_dir / 'data_results.h5'
    assert prepare_results_filename(str(input_data_file)) == str(expected_results_file)
    # Note: prepare_results_filename implicitly CREATES expected_results_dir
    assert os.access(expected_results_dir, os.W_OK)
    # File only created by processing program, not MENTO module
    assert not expected_results_file.exists()


def test_flatten_arg_list():
    flat_list = ['/path/to/script.sh', 'arg1', 'arg2', 1.0, 2, 3.0, 'arg3', 4, 'arg4', 5]
    assert list(flatten_arg_list([['/path/to/script.sh', ['arg1', 'arg2'], 1.0, 2, [3.0, ['arg3', 4, 'arg4'], 5]]])) == flat_list
    assert list(flatten_arg_list(['/path/to/script.sh', ['arg1', 'arg2'], 1.0, 2, [3.0, ['arg3', 4, 'arg4'], 5]])) == flat_list
    assert list(flatten_arg_list(['/path/to/script.sh', ['arg1', 'arg2'], 1.0, 2, [3.0, 'arg3', 4, 'arg4'], 5])) == flat_list
    assert list(flatten_arg_list(['/path/to/script.sh', ['arg1', 'arg2', 1.0, 2, [3.0, 'arg3', 4, 'arg4'], 5]])) == flat_list
    assert list(flatten_arg_list(['/path/to/script.sh', 'arg1', 'arg2', 1.0, 2, [3.0, 'arg3', 4, 'arg4'], 5])) == flat_list
    assert list(flatten_arg_list(['/path/to/script.sh', 'arg1', 'arg2', 1.0, 2, 3.0, 'arg3', 4, 'arg4', 5])) == flat_list
