# -*- coding: utf-8 -*-

"""
该模块为使用 ``acore_server_config`` 库的外部项目提供了一套能读取服务器 config 的接口.
相比之下 ``acore_server_config.config.init`` 模块是为 ``acore_server_config`` 库
内部用来从本地文件系统读取配置数据的, 外部项目不应该使用它.

该模块有两个 Public API:

- :class:`Ec2ConfigLoader`: 用于在 EC2 上运行脚本, 用 "自省" 的方式获得自己的配置数据.
- :class:`ConfigLoader`: 用于在任意其他环境显式的加载配置数据.
"""

import dataclasses
import typing as T

from s3pathlib import S3Path
from simple_aws_ec2.api import Ec2Instance
from acore_constants.api import TagKey

from ..boto_ses import bsm as default_bsm

from .define import EnvEnum, Env, Config, Server


if T.TYPE_CHECKING:  # pragma: no cover
    from boto_session_manager import BotoSesManager


def _get_default_s3folder_config(bsm: "BotoSesManager") -> str:
    """
    获得默认的 S3 配置数据的根目录.
    """
    return (
        S3Path(f"s3://{bsm.aws_account_id}-{bsm.aws_region}-artifacts")
        .joinpath(
            "projects",
            "acore_server_config",
            "config",
        )
        .to_dir()
    ).uri


def _get_default_parameter_name_prefix() -> str:
    """
    获得默认的 AWS Parameter Store 的参数名前缀. 这取决于我们 deploy 的时候用的前缀是什么.
    """
    return "acore_server_config"


def get_this_server_id(bsm: "BotoSesManager") -> str:  # pragma: no cover
    """
    在 EC2 上通过 "自省", 获得这个服务器的 server_id. 它的 naming convention 是
    ``${env_name}-${server_name}``.
    """
    ec2_inst = Ec2Instance.from_ec2_inside(bsm.ec2_client)
    server_id = ec2_inst.tags[TagKey.SERVER_ID]
    return server_id


def parse_server_id(server_id: str) -> T.Tuple[str, str]:
    """
    解析 server_id, 返回 (env_name, server_name) 的 tuple.
    """
    env_name, server_name = server_id.split("-", 1)
    return env_name, server_name


def get_config(
    bsm: "BotoSesManager" = default_bsm,
    parameter_name_prefix: T.Optional[str] = None,
    env_name: T.Optional[str] = None,
    s3folder_config: T.Optional[str] = None,
) -> Config:
    """
    获取这个 ``Config`` 对象的数据. 详细的数据结构请参考
    :class:`acore_server_config.config.main.Config`.

    :param bsm: BotoSesManager 实例.
    :param parameter_name_prefix: the parameter name prefix, the full name will
        be ${parameter_name_prefix}-${env_name}.
    :param env_name: the environment name of the env specific config you want to
        load from, stx, tst, prd, etc. If None, then load the master config.
    :param s3folder_config: S3 配置数据的根目录, 默认为
        s3://aws_account_id}-{aws_region}-artifacts/projects/acore_server_config/config/
    """
    if parameter_name_prefix is None:
        parameter_name_prefix = _get_default_parameter_name_prefix()
    if env_name is None:  # pragma: no cover
        parameter_name = parameter_name_prefix
    else:
        parameter_name = f"{parameter_name_prefix}-{env_name}"

    if s3folder_config is None:
        s3folder_config = _get_default_s3folder_config(bsm=bsm)

    config = Config.read(
        env_class=Env,
        env_enum_class=EnvEnum,
        bsm=bsm,
        parameter_name=parameter_name,
        s3folder_config=s3folder_config,
    )

    return config


@dataclasses.dataclass
class Ec2ConfigLoader:
    """
    用于在 EC2 上运行脚本, 用 "自省" 的方式获得自己的配置数据. 开始时请使用
    :meth:`Ec2ConfigLoader.load` 方法获得当前 EC2 的配置数据.

    用法:

    .. code-block:: python

        >>> server = Ec2ConfigLoader.load(...)
        >>> server
        Server(id='sbx-blue', db_admin_password='sbx*dummy4test', db_username='myuser', db_password='sbx*dummy4test')
    """

    @classmethod
    def load(
        cls,
        parameter_name_prefix: T.Optional[str] = None,
        s3folder_config: T.Optional[str] = None,
        server_id: T.Optional[str] = None,
        bsm: "BotoSesManager" = default_bsm,
    ) -> Server:
        """
        获得当前 EC2 的配置数据, 返回一个
        :class:`~acore_server_config.config.define.server.Server` 对象.

        :param parameter_name_prefix: the parameter name prefix, the full name will
            be ${parameter_name_prefix}-${env_name}.
        :param s3folder_config: S3 配置数据的根目录, 默认为
            s3://aws_account_id}-{aws_region}-artifacts/projects/acore_server_config/config/
        :param server_id: 强制指定 server_id, 跳过 "自省" 阶段. 常用于测试. 这个 server_id
            的格式为: ${env_name}-${server_name}, 例如: sbx-blue
        :param bsm: ``boto_session_manager.BotoSesManager`` object, if not provided,
            then use the current runtime default AWS CLI profile.
        """
        if server_id is None:  # pragma: no cover
            server_id = get_this_server_id(bsm=bsm)
        env_name, server_name = parse_server_id(server_id=server_id)
        config = get_config(
            bsm=bsm,
            parameter_name_prefix=parameter_name_prefix,
            env_name=env_name,
            s3folder_config=s3folder_config,
        )
        env = config.get_env(env_name)
        return env.servers[server_name]


@dataclasses.dataclass
class ConfigLoader:
    """
    用于在任意其他环境显式的加载配置数据. 开始时请使用 :meth:`ConfigLoader.new` 方法创建
    一个新的 Loader 对象, 将配置数据加载到内存中. 然后再对特定的 Server 的配置数据进行访问.

    用法:

    .. code-block:: python

        >>> config_loader = ConfigLoader.new(...)
        >>> for server_name, server in config_loader.iter_servers():
        ...
        >>> server = config_loader.get_server(server_name="blue")
        >>> server
        Server(id='sbx-blue', db_admin_password='sbx*dummy4test', db_username='myuser', db_password='sbx*dummy4test')
    """

    _env: Env = dataclasses.field(init=False)  # a cache of the env specific config

    @classmethod
    def new(
        cls,
        env_name: str,
        parameter_name_prefix: T.Optional[str] = None,
        s3folder_config: T.Optional[str] = None,
        bsm: "BotoSesManager" = default_bsm,
    ) -> "ConfigLoader":
        """
        创建一个新的 ConfigLoader 对象,

        :param env_name: the environment name of the env specific config you want to
            load from, stx, tst, prd, etc. If None, then load the master config.
        :param parameter_name_prefix: the parameter name prefix, the full name will
            be ${parameter_name_prefix}-${env_name}.
        :param s3folder_config: S3 配置数据的根目录, 默认为
            s3://aws_account_id}-{aws_region}-artifacts/projects/acore_server_config/config/
        :param bsm: ``boto_session_manager.BotoSesManager`` object, if not provided,
            then use the current runtime default AWS CLI profile.
        """
        config = get_config(
            bsm=bsm,
            parameter_name_prefix=parameter_name_prefix,
            env_name=env_name,
            s3folder_config=s3folder_config,
        )
        env = config.get_env(env_name)
        config_loader = cls()
        config_loader._env = env
        return config_loader

    def iter_servers(self) -> T.Iterable[T.Tuple[str, Server]]:
        """
        遍历所有的 server. 返回许多 (server_name, server) 的 tuple. 这类似于字典中的
        ``dict.items()`` 方法
        """
        return self._env.servers.items()

    def get_server(self, server_name: str) -> Server:
        """
        获得特定 server 的配置数据.

        :param server_name: 服务器的名字 (不包括环境名, 包括环境名的字符串是 server_id).
            例如 "blue", "green" 等.
        """
        return self._env.servers[server_name]
