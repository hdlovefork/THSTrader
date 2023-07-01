import time
import env as env

env = env.load()

def measure_time(func, *args, **kwargs):
        start_time = time.time()
        r = func(*args, **kwargs)
        end_time = time.time()
        print("执行时间为：{} 秒".format(end_time - start_time))
        return r