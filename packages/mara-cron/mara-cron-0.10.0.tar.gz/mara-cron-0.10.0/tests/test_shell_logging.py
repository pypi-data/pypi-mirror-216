import pytest
import subprocess
import pathlib

import mara_cron.config
from mara_app.monkey_patch import patch
from mara_cron.job import CronJob


ECHO_HELLO_WORLD_TEXT = 'Hello World!'
ECHO_HELLO_WORLD_COMMAND = f'echo "{ECHO_HELLO_WORLD_TEXT}"'
MARA_LOG_FILE_PATTERN = 'mara-cron_*.log'


@pytest.fixture
def job_echo_hello_world() -> CronJob:
    return CronJob(id='test_job',
                   description="",
                   default_time_pattern="00 1 * * *",
                   command=ECHO_HELLO_WORLD_COMMAND)


def test_log_path_does_not_exist(job_echo_hello_world: CronJob):
    patch(mara_cron.config.log_path)(lambda: 'tests/logs_folder_which_does_not_exist')
    job = job_echo_hello_world

    assert job.command == ECHO_HELLO_WORLD_COMMAND

    # since the log folder does not exist, the shell_command should be equal to the command
    assert job.shell_command == job.command


def test_execute_job_without_log(job_echo_hello_world: CronJob):
    patch(mara_cron.config.log_path)(lambda: None)
    job = job_echo_hello_world

    # validate internal fields
    assert job.command == ECHO_HELLO_WORLD_COMMAND
    assert job.shell_command == job.command

    # exec job
    (exitcode, stdout) = subprocess.getstatusoutput(job.shell_command)
    assert exitcode == 0
    assert stdout == ECHO_HELLO_WORLD_TEXT



def test_execute_job_with_logging(job_echo_hello_world: CronJob):
    patch(mara_cron.config.log_path)(lambda: 'tests/logs')
    job = job_echo_hello_world

    # Debug output
    print(f'job command: {job.command}')
    print(f'job shell command: {job.shell_command}')

    assert job.command == ECHO_HELLO_WORLD_COMMAND
    assert job.shell_command != job.command

    # exec job
    log_path = pathlib.Path(mara_cron.config.log_path())

    log_files = set(log_path.glob(MARA_LOG_FILE_PATTERN))

    (exitcode, stdout) = subprocess.getstatusoutput(job.shell_command)
    assert exitcode == 0
    assert not stdout

    new_log_files = set(log_path.glob(MARA_LOG_FILE_PATTERN))
    assert len(log_files) + 1 == len(new_log_files)

    log_file, = (new_log_files.difference(log_files))

    # test if we get a real file
    assert pathlib.Path(log_file).exists()

    # test if log file contains the stdout content
    found = False
    with open(log_file, 'r') as f:
        if ECHO_HELLO_WORLD_TEXT in f.read():
            found = True

    assert found
