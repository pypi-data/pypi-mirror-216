import sys
import click
from mara_cron import config

from . import crontab, job


@click.command()
@click.option('--job-id', required=True,
              help='The id of of the cron job.')
@click.option('--module', default=None,
              help='The module name the cron job.')
def disable(job_id: str, module_name: str):
    """ disables a specific cronjob """
    cron = crontab.generate()

    job = crontab.get_job(cron, job_id=job_id, module_name=module_name)

    if not job:
        print(f'Could not find cronjob "{job_id}"', file=sys.stderr)
        sys.exit(1)

    job.enable(False)
    cron.write()
    sys.exit(0)


@click.command()
@click.option('--job-id', required=True,
              help='The id of of the cron job.')
@click.option('--module', default=None,
              help='The module name the cron job.')
def enable(job_id: str, module_name: str):
    """ enables a specific cronjob """
    if not config.enabled():
        print('WARNING: The global parameter mara_cron.config.enabled is not set. The job will be enabled nevertheless')

    cron = crontab.generate()

    job = crontab.get_job(cron, job_id=job_id, module_name=module_name)

    if not job:
        print(f'Could not find cronjob "{job_id}"', file=sys.stderr)
        sys.exit(1)

    job.enable(True)

    cron.write()
    sys.exit(0)


@click.command()
@click.option('--job-id', required=True,
              help='The id of of the cron job.')
def schedule_job(job_id: str):
    """ Schedules a job to run. """
    cronjob = job.find_job(job_id)
    if not cronjob:
        print(f'Could not find job with id "{job_id}"', file=sys.stderr)
        sys.exit(1)

    crontab.append_single_execution_job(cronjob)

    print(f'Job {job_id} is scheduled to run in less than 1 minute')
    sys.exit(0)


@click.command()
@click.option('--with-changes', default=False, is_flag=True,
              help='Lists the current crontab including the not written changes.')
def list_crontab(with_changes: bool):
    """ List the crontab content """

    if with_changes:
        cron = crontab.generate()
    else:
        cron = crontab.current()

    print(cron)


@click.command()
def write_crontab():
    """ Updates the current crontab """
    cron = crontab.generate()

    cron.write()


@click.command()
def clear_crontab():
    """ Removes all mara jobs from the crontab """
    cron = crontab.current()

    for job in cron:
        if job.comment.lstrip().startswith('mara'):
            print(f'Delted cron job: {job}')
            job.delete()

    cron.write()
