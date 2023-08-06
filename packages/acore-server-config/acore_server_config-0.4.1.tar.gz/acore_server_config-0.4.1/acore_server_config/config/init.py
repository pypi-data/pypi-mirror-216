# -*- coding: utf-8 -*-

"""
注, 这个模块不属于公开 API 的一部分, 仅仅用于在 acore_server_config 项目本身内部用于部署
配置数据. 如果你在其他项目中引用了这个项目, 请使用 acore_server_config.api 模块中的内容.
"""

import json

from ..paths import path_config_json, path_config_secret_json
from ..runtime import IS_LOCAL

from .define import EnvEnum, Env, Config

if IS_LOCAL:
    # ensure that the config-secret.json file exists
    # it should be at the ${HOME}/.projects/wserver_infra/config-secret.json
    # this code block is only used to onboard first time user of this
    # project template. Once you know about how to handle the config-secret.json file,
    # you can delete this code block.
    if not path_config_secret_json.exists():  # pragma: no cover
        path_config_secret_json.parent.mkdir(parents=True, exist_ok=True)
        path_config_secret_json.write_text(
            json.dumps(
                {
                    "_shared": {},
                    EnvEnum.sbx.value: {"password": f"{EnvEnum.sbx.value}.password"},
                    EnvEnum.tst.value: {"password": f"{EnvEnum.tst.value}.password"},
                    EnvEnum.prd.value: {"password": f"{EnvEnum.prd.value}.password"},
                },
                indent=4,
            )
        )

    # read non-sensitive config and sensitive config from local file system
    config = Config.read(
        env_class=Env,
        env_enum_class=EnvEnum,
        path_config=path_config_json,
        path_secret_config=path_config_secret_json,
    )
else:
    raise NotImplementedError
