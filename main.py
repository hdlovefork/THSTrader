import os
from dynaconf import Dynaconf

env = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['.env.toml'],
)
os.environ['APPENV'] = env.appenv
os.environ['LOGLEVEL'] = env.loglevel

from log import log
from script.app import App

if __name__ == '__main__':
    try:
        App(env).run()
    except Exception as e:
        log.exception(e)
