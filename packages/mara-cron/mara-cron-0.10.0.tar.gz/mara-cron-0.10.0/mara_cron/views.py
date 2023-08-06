"""Mara admin views"""

import copy
import functools
import html
import sys
import typing

import flask
from mara_page import acl, navigation, response, _, bootstrap, xml
from . import config

from .job import CronJob

blueprint = flask.Blueprint('mara_cron', __name__, url_prefix='/mara-cron', static_folder='static')

acl_resource = acl.AclResource('Cron')


def _cronjob_modules(with_cronjobs=True):
    """Gathers all cron jobs from modules"""
    import inspect

    cronjob_modules = {}
    for name, module in copy.copy(sys.modules).items():
        if 'MARA_CRON_JOBS' in dir(module):
            cronjobs = getattr(module, 'MARA_CRON_JOBS')
            if isinstance(cronjobs, typing.Callable):
                cronjobs = cronjobs()
            assert (isinstance(cronjobs, typing.Iterable))
            cronjob_modules[f"{name}.crontab"] = {
                'doc': f'Module {name}' if name != 'app' else 'Main app',
                'cronjobs': {}
            }
            if with_cronjobs:
                for cronjob in cronjobs:
                    assert (isinstance(cronjob, CronJob))

                    cronjob_modules[f"{name}.crontab"]['cronjobs'][cronjob.id] = \
                        {
                            'doc': cronjob.description,
                            'time_pattern': cronjob.time_pattern,
                            'enabled': cronjob.enabled,
                            'command': cronjob.command
                        }

    return cronjob_modules


@blueprint.route('/crontab')
def crontab_page():
    import pprint

    # gather all cronjobs by package

    current_user_has_permission = acl.current_user_has_permission(acl_resource)

    return response.Response(
        html=[(bootstrap.card(id=module_name,
                              header_left=html.escape(module_name),
                              body=[_.p[_.em[html.escape(str(module['doc']))]],
                                    bootstrap.table(
                                        ['ID', 'Description', 'Status', 'Time pattern', 'Command', 'Actions'],
                                        [_.tr[
                                             _.td[html.escape(cronjob_id)],
                                             _.td[_.em[html.escape(cronjob['doc'])]],
                                             _.td[
                                                 _.span[
                                                     _.div(class_='fa fa-fw fa-play', style='color: green')[''],
                                                     'enabled'
                                                 ] if cronjob['enabled'] == True else _.span[
                                                     _.div(class_='fa fa-fw fa-stop', style='color: red')[''],
                                                     'disabled'
                                                 ]
                                             ],
                                             _.td[_.pre[html.escape(cronjob['time_pattern'] or '')]],
                                             _.td[
                                                 _.pre[html.escape(pprint.pformat(cronjob['command']))]
                                                 if current_user_has_permission
                                                 else acl.inline_permission_denied_message()
                                             ],
                                             _.td[
                                                 _.span[
                                                    bootstrap.button(url=flask.url_for('mara_cron.do_schedule_run', job_id=cronjob_id),
                                                                    label='Schedule run', icon='play',
                                                                    title='Schedule this task to run in less then 1 minute')
                                                        if config.allow_run_from_web_ui() else '',
                                                 ] if current_user_has_permission
                                                 else acl.inline_permission_denied_message()
                                             ]] for cronjob_id, cronjob in module['cronjobs'].items()])
                                    ]) if module['cronjobs'] else '')
              for module_name, module in sorted(_cronjob_modules().items())],
        title='Mara Crontab')


def package_cronjobs_navigation_entry():
    return navigation.NavigationEntry(
        label='Cron', icon='calendar', rank=100,
        description='Package cronjobs',
        uri_fn=lambda: flask.url_for('mara_cron.crontab_page'),
        children=[
            navigation.NavigationEntry(
                label=module_name, icon='list', description=module['doc'],
                uri_fn=lambda _module_name=module_name: flask.url_for('mara_cron.crontab_page',
                                                                      _anchor=_module_name))
            for module_name, module in sorted(_cronjob_modules(with_cronjobs=False).items())]
    )


@blueprint.route('/navigation-bar')
@functools.lru_cache(maxsize=None)
def navigation_bar() -> [str]:
    from . import app
    # The navigation sidebar is loaded asynchronously for better rendering experience
    def render_entries(entries: [navigation.NavigationEntry] = [], level: int = 1):
        def render_entry(entry: navigation.NavigationEntry, level: int = 1):
            attrs = {}
            if entry.children:
                attrs['onClick'] = 'toggleNavigationEntry(this)'
            else:
                attrs['href'] = entry.uri_fn()

            if entry.description:
                attrs.update({'title': entry.description, 'data-toggle': 'tooltip',
                              'data-container': 'body', 'data-placement': 'right'})
            return _.div(class_='mara-nav-entry level-' + str(level),
                         style='display:none' if level > 1 else '')[
                _.a(**attrs)[
                    _.div(class_='mara-nav-entry-icon fa fa-fw fa-' + entry.icon + (' fa-lg' if level == 1 else ''))[
                        ''] if entry.icon else '',
                    _.div(class_='mara-nav-entry-text')[entry.label.replace('_', '_<wbr>')],
                    _.div(class_='mara-caret fa fa-caret-down')[''] if entry.children else ''],
                render_entries(entry.children, level + 1)
            ]

        return [functools.partial(render_entry, level=level)(entry)
                for entry in sorted([entry for entry in entries if entry.visible], key=lambda x: x.rank)]

    return flask.Response(''.join(list(xml.render(render_entries(app.combine_navigation_entries().children)))))
