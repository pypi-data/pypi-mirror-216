"""UI for manually scheduling a cron job"""

import flask

from mara_page import _, bootstrap, response, acl
from .. import views, job, crontab

@views.blueprint.route('/<path:job_id>/schedule-run')
@acl.require_permission(views.acl_resource)
def do_schedule_run(job_id: str):
    cronjob = job.find_job(job_id)
    if not cronjob:
        flask.abort(404, f'Job "{job_id}" not found')

    crontab.append_single_execution_job(cronjob)

    print(f'schedule {job_id}')

    return response.Response(
        title=f'Job scheduled',
        html=bootstrap.card(
            body=_.div[
                    _.p[
                        """The job is scheduled to run in less then 1 minute."""
                    ],
                    bootstrap.button(url='javascript:history.back()',
                                     label='Go to last page', icon='play',
                                     title='Returns to the last page')
                ]))
