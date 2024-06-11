from pathlib import Path


WORKSPACE = Path.cwd()

INSTANCE_PATH = WORKSPACE / 'instance'
LOG_PATH = INSTANCE_PATH / 'logs'

DB_PATH = INSTANCE_PATH
DB_FILE = INSTANCE_PATH / 'data_handler.db'
DB_URI = f'sqlite:///{DB_FILE}'