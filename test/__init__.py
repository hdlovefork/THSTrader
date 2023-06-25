import time

from dynaconf import Dynaconf

env = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=['.env.toml'],
)


def measure_time(func, *args, **kwargs):
        start_time = time.time()
        r = func(*args, **kwargs)
        end_time = time.time()
        print("执行时间为：{} 秒".format(end_time - start_time))
        return r