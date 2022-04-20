LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default_formatter': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'stream_handler': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },
    'loggers': {
        'page_loader': {
            'handlers': ['stream_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
