# SPDX-FileCopyrightText: 2021 S. Vijay Kartik <vijay.kartik@desy.de>, DESY
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mento.trigger import get_ssh_command, get_sbatch_command
from mento.trigger import retrieve_cmd, retrieve_arg_list
from mento import Trigger, TriggerMethod, get_beamtime_metadata

from pathlib import Path
from shutil import copy
import time
import pytest

# Different possible inputs from module users
arg_list_only_script = ['/path/to/script.sh']
arg_list_single_entry_everything = ['/path/to/script.sh arg1 arg2 1.0 2 3.0']
arg_list_script_arg_list = ['/path/to/script.sh', ['arg1', 'arg2', 1.0, 2, 3.0]]
arg_list_flat_list = ['/path/to/script.sh', 'arg1', 'arg2', 1.0, 2, 3.0]


def _poll_with_timeout(predicate, interval: float = 0.1, timeout: float = 10.0):
    start = time.time()
    while (time.time() - start) < timeout:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()


def test_trigger_default_construction():
    assert Trigger(beamline_root_dir='tests/data/gpfs')


def test_trigger_construction():
    assert Trigger(TriggerMethod.REMOTE_SBATCH_SCRIPT, 'tests/data/gpfs')


@pytest.mark.skip(reason='Have to still figure out how to handle non-existent Enum members')
def test_trigger_incorrect_construction():
    with pytest.raises(RuntimeError, match='Unknown triggering method'):
        _ = Trigger(TriggerMethod.DOESNOTEXIST, 'tests/data/gpfs')


def test_get_ssh_command():
    bt_info = get_beamtime_metadata(root_dir='tests/data/gpfs')
    ssh_command_string = get_ssh_command(bt_info)
    assert ssh_command_string.startswith('/usr/bin/ssh')
    assert bt_info.online.nodes[0] in ssh_command_string
    assert bt_info.online.ssh.user in ssh_command_string
    assert bt_info.online.ssh.key in ssh_command_string


def test_get_sbatch_command():
    bt_info = get_beamtime_metadata(root_dir='tests/data/gpfs')
    sbatch_command_string = get_sbatch_command(bt_info)
    assert sbatch_command_string.startswith('/usr/bin/sbatch')
    assert bt_info.online.slurm.reservation in sbatch_command_string
    assert bt_info.online.slurm.partition in sbatch_command_string


def test_trigger_run_local_bash_script_nonexistent():
    test_trigger = Trigger(trigger_method=TriggerMethod.LOCAL_BASH_SCRIPT,
                           beamline_root_dir='tests/data/gpfs')
    script_file = 'non/existent/file/name.sh'
    with pytest.raises(FileNotFoundError):
        test_trigger.run([script_file])


def test_trigger_run_local_bash_script_success(tmp_beamtime_dirtree):
    sample_bash_script = 'tests/data/gpfs/local/dump_args_to_file_bash.sh'
    # Create temporary directory tree as scratch space for bash script, output, etc.
    tmp_beamtime_root = tmp_beamtime_dirtree('scratch')
    local_bash_script = copy(sample_bash_script, tmp_beamtime_root)
    local_bash_log = Path(local_bash_script).with_suffix('.log')
    local_args = [5, 'dummy', 'arguments', 'to script', 0]
    arg_list_string = ' '.join(str(item) for item in local_args)

    test_trigger = Trigger(trigger_method=TriggerMethod.LOCAL_BASH_SCRIPT,
                           beamline_root_dir=tmp_beamtime_root)
    test_trigger.run([local_bash_script, local_args])

    # Let the bash script finish before asserting if script log file exists
    assert _poll_with_timeout(lambda: local_bash_log.exists())
    with open(local_bash_log, 'r') as f:
        local_bash_output = f.readline().rstrip()
    assert local_bash_output == arg_list_string


def test_trigger_run_remote_sbatch_script():
    test_trigger = Trigger(trigger_method=TriggerMethod.REMOTE_SBATCH_SCRIPT,
                           beamline_root_dir='tests/data/gpfs')
    # TODO: Write tests checking if job submission is possible at all (unrelated to online analysis)


def test_trigger_run_slurm_api():
    test_trigger = Trigger(trigger_method=TriggerMethod.SLURM_REST_API,
                           beamline_root_dir='tests/data/gpfs')
    with pytest.raises(NotImplementedError, match='SLURM REST API not available'):
        test_trigger.run(['some_valid_rest_api', 'with', 'args', 0])


def test_trigger_run_unknown_trigger_method():
    test_trigger = Trigger(beamline_root_dir='tests/data/gpfs')
    DOESNOTEXIST = 999
    test_trigger.trigger_method = DOESNOTEXIST  # TODO: Disallow changing trigger method like this, on existing triggers
    with pytest.raises(RuntimeError, match='Trigger method not known'):
        test_trigger.run(['bad_call'])


@pytest.mark.parametrize('input_list', [arg_list_only_script,
                                        arg_list_single_entry_everything,
                                        arg_list_script_arg_list,
                                        arg_list_flat_list])
def test_retrieve_cmd(input_list):
    script_path = '/path/to/script.sh'
    assert retrieve_cmd(input_list) == script_path


def test_retrieve_arg_list():
    assert retrieve_arg_list(arg_list_only_script) == []
    assert retrieve_arg_list(arg_list_single_entry_everything) == ['arg1', 'arg2', '1.0', '2', '3.0']
    assert retrieve_arg_list(arg_list_script_arg_list) == ['arg1', 'arg2', 1.0, 2, 3.0]
    assert retrieve_arg_list(arg_list_flat_list) == ['arg1', 'arg2', 1.0, 2, 3.0]
