import logging

from dynaconf import Dynaconf
from log import log
from script.app import App

if __name__ == '__main__':
    env = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=['.env.toml'],
    )
    log.setLevel(env.LOGLEVEL)
    ch = logging.StreamHandler()
    ch.setLevel(env.LOGLEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)

    App().run()

