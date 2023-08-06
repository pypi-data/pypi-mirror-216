# -*- coding: utf-8 -*-

import dataclasses
import os

from config_patterns.patterns.multi_env_json.api import (
    BaseEnvEnum,
    BaseEnv,
    BaseConfig,
)

from ...runtime import IS_LOCAL, IS_GITHUB_CI, IS_EC2, IS_CODEBUILD_CI
from ...compat import cached_property


class EnvEnum(BaseEnvEnum):
    """
    In this project, we have three environment:

    - sbx: represent the developer's local laptop, and the sandbox environment
        the change you made on your local laptop can be applied to sandbox.
    - tst: a long living integration test environment. before releasing to
        production, the app has to be deployed to test environment for QA.
    - prd: the production environment. can only be deployed from release branch.
    """

    sbx = "sbx"
    tst = "tst"
    prd = "prd"


# You may have a long list of config field definition
# put them in different module and use Mixin class
from .server import Server, ServerMixin


@dataclasses.dataclass
class Env(
    BaseEnv,
    ServerMixin,
):
    @classmethod
    def from_dict(cls, data: dict):
        data["servers"] = {
            name: Server(
                id="{}-{}".format(
                    data["env_name"],
                    name,
                ),
                **dct,
            )
            for name, dct in data.get("servers", {}).items()
        }
        env = cls(**data)
        return env


class Config(BaseConfig):
    @classmethod
    def get_current_env(cls) -> str:  # pragma: no cover
        # you can uncomment this line to force to use certain env
        # from your local laptop to run application code, tests, ...
        # return EnvEnum.sbx.value
        if IS_LOCAL:
            if "USER_ENV_NAME" in os.environ:
                return os.environ["USER_ENV_NAME"]
            return EnvEnum.sbx.value
        elif IS_GITHUB_CI or IS_CODEBUILD_CI:
            if "USER_ENV_NAME" in os.environ:
                return os.environ["USER_ENV_NAME"]
            return EnvEnum.sbx.value
        elif IS_EC2:
            if "USER_ENV_NAME" in os.environ:
                return os.environ["USER_ENV_NAME"]
            return EnvEnum.sbx.value
        else:
            raise NotImplementedError

    @cached_property
    def sbx(self) -> Env:  # pragma: no cover
        return self.get_env(env_name=EnvEnum.sbx)

    @cached_property
    def tst(self) -> Env:  # pragma: no cover
        return self.get_env(env_name=EnvEnum.tst)

    @cached_property
    def prd(self) -> Env:  # pragma: no cover
        return self.get_env(env_name=EnvEnum.prd)

    @cached_property
    def env(self) -> Env:
        return self.get_env(env_name=self.get_current_env())
