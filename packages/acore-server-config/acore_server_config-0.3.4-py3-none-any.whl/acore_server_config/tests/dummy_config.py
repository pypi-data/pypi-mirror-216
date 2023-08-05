# -*- coding: utf-8 -*-

from ..paths import dir_unit_test, path_config_json
from ..config.define import Env, EnvEnum, Config

path_config_secret_json = dir_unit_test.joinpath("config", "config-secret.json")

config = Config.read(
    env_class=Env,
    env_enum_class=EnvEnum,
    path_config=path_config_json,
    path_secret_config=path_config_secret_json,
)
