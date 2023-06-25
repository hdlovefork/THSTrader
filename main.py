import logging

from dynaconf import Dynaconf
from log import log

env = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['.env.toml'],
)

if __name__ == '__main__':
    from script.app import App

    log.setLevel(env.LOGLEVEL)
    ch = logging.StreamHandler()
    ch.setLevel(env.LOGLEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    log.addHandler(ch)

    App().run()
