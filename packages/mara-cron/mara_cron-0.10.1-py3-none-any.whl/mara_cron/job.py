import copy
import os
import pathlib
import shlex
import sys
import typing

from . import config


class CronJob():
    """ A cron job configuration """
    def __init__(self, id: str, description: str, command: str,
                 default_time_pattern: str = None, default_enabled: bool = True,
                 max_retries: int = None):
        self.id = id
        self.description = description
        self.time_pattern = default_time_pattern
        self.command = command
        self.enabled = default_enabled
        self.max_retries = max_retries

    @property
    def shell_command(self):
        max_retries = self.max_retries
        if max_retries is None:
            max_retries = config.default_job_max_retries()

        if config.log_path():
            if max_retries:
                raise ValueError('ERROR: Logging of a cron job cannot be combined with max_retries in the current version of mara_cron!')
            log_path = pathlib.Path(config.log_path())

            log_full_path = None
            if log_path.is_file():
                log_full_path = str(log_path.absolute())
            elif log_path.is_dir():
                log_full_path = str((log_path / 'mara-cron_$(date "+%Y%m%d_%H%M%S").log').absolute())

            if log_full_path:
                log_command = f'{{ echo "MARA CRON JOB {self.id} START $(date)"; {self.command}; echo "MARA CRON JOB {self.id} END $(date)" ; }}'

                if '$' not in log_full_path:
                    log_full_path = shlex.quote(log_full_path)

                return f'{log_command} >> {log_full_path} 2>&1'

        if max_retries:
            return f"for i in {' '.join([str(2**(i+3)) for i in range(max_retries+1)])} 0; do ({self.command}) && break || sleep $i; done"

        return self.command


class MaraJob(CronJob):
    """ A configuration for a mara job"""
    def __init__(self, id: str, description: str, command: str, args: dict = None,
                 default_time_pattern: str = None, default_enabled = True,
                 max_retries: int = None):
        virtual_env_path = os.environ['VIRTUAL_ENV']
        if not virtual_env_path:
            raise Exception('Could not determine virtual environment path. VIRTUAL_ENV not set')

        mara_root_path = pathlib.Path(virtual_env_path).parent.resolve()

        job_command = f'cd {mara_root_path} ; . ./.venv/bin/activate ; flask {command}'

        if args:
            for param, value in args.items() if args else {}:
                job_command += f' {param}' \
                                + (f' {value}' if value and not isinstance(value, bool) else '')

        super().__init__(id=id, description=description, command=job_command,
                         default_time_pattern=default_time_pattern, default_enabled=default_enabled,
                         max_retries=max_retries)


class RunPipelineJob(MaraJob):
    """ A configuration for a job executing a mara pipeline"""
    def __init__(self, id: str, description: str, path: str = None, nodes: [str] = None, with_upstreams: bool = False,
                 default_time_pattern: str = None, default_enabled = True,
                 max_retries: int = None):
        """
        A job running a mara pipeline.
        """
        command = 'mara_pipelines.ui.run'
        args = {
            '--disable-colors': False
        }
        if path:
            args['--path'] = path
        if nodes:
            args['--nodes'] = ','.join(nodes)
        if with_upstreams:
            args['--with_upstreams'] = with_upstreams

        super().__init__(id=id, description=description, command=command, args=args,
                         default_time_pattern=default_time_pattern, default_enabled=default_enabled,
                         max_retries=max_retries)


def _iterate_cronjobs() -> typing.Dict[str, typing.List[CronJob]]:
    for module_name, module in copy.copy(sys.modules).items():
        if 'MARA_CRON_JOBS' in dir(module):
            cronjobs = getattr(module, 'MARA_CRON_JOBS')
            if isinstance(cronjobs, typing.Callable):
                cronjobs = cronjobs()
            assert (isinstance(cronjobs, typing.Iterable))
            for cronjob in cronjobs:
                assert (isinstance(cronjob, CronJob))
                yield module_name, cronjob


def find_job(id: str, module_name: str = None) -> CronJob:
    """
    Retrieves a job by the the job id
    Args:
        module_name: The name of the module
        id: The id of the job

    Returns:
        A CronJob object or None when the job was not found
    """
    if module_name:
        raise ValueError('Arg. module_name is not yet supported')

    for _, cronjob in _iterate_cronjobs():
        if cronjob.id == id:
            return cronjob

    return None
