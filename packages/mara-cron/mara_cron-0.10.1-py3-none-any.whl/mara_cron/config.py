import typing as t


def enabled() -> bool:
    """
    A global parameter which lets you disable/activate all cron jobs

    Default value: False.
    """
    return False


def instance_name() -> t.Optional[str]:
    """
    Lets you define a name of your mara instance.

    Cron jobs will be executed per instance.
    """
    return None


def user() -> t.Union[bool, str]:
    """
    The crontab user:
    - you can return the name of crontab user
    - you can enter 'true' in case you want to get the crontab of the current user

    By default the current user is taken
    """
    return True


def tabfile() -> t.Optional[str]:
    """
    The crontab file. Use '/etc/crontab' in order to use

    By default not set. This will override the user() config.
    """
    return None


def allow_run_from_web_ui() -> bool:
    """When false, then it is not possible to start a cron job manually via the web UI"""
    return True


def log_path(): # -> t.Optional[t.Union[str, pathlib.Path]]:
    """
    The log path to which to log the command output.

    When the sign '$' is used in the path, shell quotation is disabled, otherwise the path name
    will be quoted.

    Note: You will have to ensure that the folder exist, otherwise logging will be skipped.

    It is recommended to use a different log path per instance e.g. '/var/log/mara/my_instance_name/'

    Possible options:
        Use a path to a folder e.g. '/var/log/mara'. You will have to make sure that the folder exists.
        Mara will automatically generate a log file named '$(date +%Y%m%d_%H%M%S).log',
        e.g. mara-cron_20211124_152800.log

        Alternatively you can define the name of the file as well by adding it to the path. You can add
        e.g. the date to a log file by using the following path: '/var/log/mara/mara_$(date +%Y%m%d).log'

        Each execution will append to the file. NOTE: When several jobs run at the same time, it will be
        maybe hard to determine to which execution the log line belongs.

    WARNING: Make sure that the user cron runs on has write access to the log_path. Otherwise the whole
             job will break with the error: Permission denied
    """
    return None


def default_job_max_retries() -> int:
    """How many times a cron job is retried when it fails by default"""
    return 0
