import env
from log import log
from script.app import App

if __name__ == '__main__':
    try:
        env = env.load()
        App(env).run()
    except Exception as e:
        log.exception(e)
