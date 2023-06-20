from dynaconf import Dynaconf


settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=['config.toml'],
)

if __name__ == '__main__':
    from script.app import App
    App().run()
