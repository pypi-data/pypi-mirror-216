import json
import typing
from crontab import CronTab, CronItem
from datetime import datetime, timedelta

from . import config
from .job import CronJob, _iterate_cronjobs


def current() -> CronTab:
    tabfile = config.tabfile()
    if tabfile:
        cron = CronTab(tabfile=tabfile)
    else:
        cron = CronTab(user=config.user())

    return cron


def _build_job_comment(job_id: str, module_name: str = None, run_type: str = None) -> str:
    job_comment_dict = {}
    instance = config.instance_name()
    if instance:
        job_comment_dict['instance'] = instance

    if module_name:
        job_comment_dict['module'] = module_name

    job_comment_dict['job_id'] = job_id

    if run_type:
        job_comment_dict['run_type'] = run_type

    return f'mara {json.dumps(job_comment_dict)}'


def get_job(cron: CronTab, job_id: str, module_name: str = None) -> typing.Optional[CronItem]:
    job_comment = _build_job_comment(job_id, module_name)

    for j in cron.find_comment(job_comment):
        return j


def generate() -> CronTab:
    cron = current()

    # iterate through defined cron jobs

    for module_name, cronjob in _iterate_cronjobs():
        job_comment = _build_job_comment(
                            job_id=cronjob.id,
                            module_name=(module_name if module_name != 'app' else None))

        job = None
        for j in cron.find_comment(job_comment):
            job = j
            job.set_command(cronjob.shell_command)
            break

        if not job:
            if not cronjob.time_pattern:
                continue
            job = cron.new(command=cronjob.shell_command, comment=job_comment)

        enabled = cronjob.enabled and config.enabled()

        if cronjob.time_pattern:
            job.setall(cronjob.time_pattern)
        else:
            # time pattern not set, keep the current time pattern and disable the cronjob
            enabled = False

        job.enable(enabled)

    return cron


def cronjob_time_pattern_from_datetime(datetime: datetime):
    """
    Generates a cron time pattern from a datetime object.

    Note:
        CRON does not support placing the year into the time pattern.
        We assume here that at least once a year the crontab is rewritten.
    """
    return f"{datetime.minute} {datetime.hour} {datetime.day} {datetime.month} *"


def append_single_execution_job(cronjob: CronJob):
    """Appends a new cron job for a single execution"""
    cron = current()

    job_comment_dict = {}
    instance = config.instance_name()
    if instance:
        job_comment_dict['instance'] = instance

    #if module_name:
    #    job_comment_dict['module'] = module_name

    job_comment_dict['job_id'] = cronjob.id
    job_comment_dict['type'] = 'single_execution'

    job = cron.new(command=cronjob.shell_command,
                   comment=_build_job_comment(cronjob.id, run_type='manual_scheduled'))

    # This job will run each year. We assume here that you will rewrite the cronjob task list before that time.
    time_pattern = str(cronjob_time_pattern_from_datetime(datetime.now() + timedelta(minutes=1)))
    job.setall(time_pattern)

    cron.write()
