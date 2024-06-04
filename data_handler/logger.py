import os
import logging
import logging.config


def config_log(path, console_log_level='info'):
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '%(asctime)s - %(levelname)s - %(message)s',
            },
            'file': {
                'format': '%(asctime)s - %(levelname)s - %(name)s[%(lineno)d] - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
                'level': console_log_level.upper(),
            },
            'data_handler': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(path, 'data_handler.log'),
                'when': 'midnight',
                'backupCount': 7,
                'encoding': 'utf-8',
                'formatter': 'file',
                'level': 'DEBUG',
            },
        },
        'loggers': {
            'data_handler': {
                'handlers': ['data_handler', 'console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    })