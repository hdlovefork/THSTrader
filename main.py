import env
from log import log
from script.app import App

if __name__ == '__main__':
    try:
        env = env.load()
        App(env).run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log.exception(e)
    finally:
        log.info("程序已退出")
