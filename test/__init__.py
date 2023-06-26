import logging
import time

from dynaconf import Dynaconf
from log import log

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
log.addHandler(ch)

def measure_time(func, *args, **kwargs):
        start_time = time.time()
        r = func(*args, **kwargs)
        end_time = time.time()
        print("执行时间为：{} 秒".format(end_time - start_time))
        return r