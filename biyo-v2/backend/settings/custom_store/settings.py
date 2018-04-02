# -*- coding: utf-8 -*-

from ..base_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'biyo_dev',
        'USER': 'biyo',
        'PASSWORD': 'biyo',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB;',
            'charset': 'utf8',
            'use_unicode': True,
        }
    }
}

TIME_ZONE = 'Europe/Moscow'

DEBUG_TOOLBAR_PANELS = [
    # 'ddt_request_history.panels.request_history.RequestHistoryPanel',  # Here it is
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    # 'SHOW_TOOLBAR_CALLBACK': 'ddt_request_history.panels.request_history.allow_ajax',
    'SHOW_TEMPLATE_CONTEXT': True,
}
DEBUG_TOOLBAR_PATCH_SETTINGS = True
# gunicorn complains about it
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    ),
}

JENKINS_TASKS = ('django_jenkins.tasks.with_coverage',
                 'django_jenkins.tasks.run_pylint',
                 )

SESSION_COOKIE_AGE = 60 * 60 * 24 * 365

from ..logging_settings import get_logging_config

LOGGING = get_logging_config('my_local_biyo_app', '/var/log/pulsewallet')

if True:  # DEBUG
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        if 'console' not in LOGGING['loggers'][logger]['handlers']:
            LOGGING['loggers'][logger]['handlers'] += ['console']
