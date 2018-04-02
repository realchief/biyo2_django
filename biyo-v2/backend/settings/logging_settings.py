# -*- coding: utf-8 -*-


def get_logging_config(app_name, log_folder, apps=None, debug=False):
    apps = apps or []
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': log_folder + '/webdebug.log',
                'formatter': 'verbose',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file', ],
                'level': 'INFO',
                'propagate': True,
            },
            'main': {
                'handlers': ['file', ],
                'level': 'DEBUG',
                'propagate': True,
            },
            'utils': {
                'handlers': ['file', ],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

    # define loggers for every app
    for app in apps:
        if app not in LOGGING['loggers']:
            LOGGING['loggers'][app] = LOGGING['loggers']['main']

    return LOGGING
