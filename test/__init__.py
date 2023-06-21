from dynaconf import Dynaconf

env = Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=['.env.toml'],
        )