import os
from dynaconf import Dynaconf


def load():
    env = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=['.env.toml'],
    )
    os.environ['SERIAL_NO'] = str(env.get('SERIAL_NO', '127.0.0.1:62001'))
    os.environ['APP_ENV'] = str(env.get('APP_ENV', 'prod'))
    os.environ['LOG_LEVEL'] = str(env.get('LOG_LEVEL', 'INFO'))
    os.environ['LOG_FILE_SIZE_LIMIT'] = str(env.get('LOG_FILE_SIZE_LIMIT', '10'))
    os.environ['LOG_FILE_COUNT_LIMIT'] = str(env.get('LOG_FILE_COUNT_LIMIT', '10'))
    return env
