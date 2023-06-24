from dynaconf import Dynaconf

env = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=['.env.toml'],
)

if __name__ == '__main__':
    from script.app import App
    App().run()
