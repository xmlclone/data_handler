import os
import logging
import logging.config


def config_log(path, console_log_level='info'):
    print(f"The log path is {path}")
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                # 'format': '%(asctime)s - %(levelname)s - %(message)s',
                'format': '%(asctime)s - %(levelname)s - %(name)s[%(lineno)d] - %(message)s',
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
            'mgtg_msgntf': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(path, 'mgtg_msgntf.log'),
                'when': 'midnight',
                'backupCount': 7,
                'encoding': 'utf-8',
                'formatter': 'file',
                'level': 'DEBUG',
            },
            'root': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(path, 'fw.log'),
                'when': 'midnight',
                'backupCount': 7,
                'encoding': 'utf-8',
                'formatter': 'file',
                'level': 'DEBUG',
            }
        },
        'loggers': {
            'mgtg_msgntf': {
                'handlers': ['mgtg_msgntf', 'console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
        'root': {
            'handlers': ['root'],
            'level': 'INFO',
        },
    })