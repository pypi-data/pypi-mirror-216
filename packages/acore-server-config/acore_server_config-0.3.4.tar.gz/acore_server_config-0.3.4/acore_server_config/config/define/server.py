# -*- coding: utf-8 -*-

"""
todo: doc string
"""

import typing as T
import dataclasses

if T.TYPE_CHECKING:  # pragma: no cover
    from .main import Env


@dataclasses.dataclass
class Server:
    """
    Per Game Server configuration.

    :param id: Server id, the naming convention is ``${env_name}-${server_name}``
    :param db_admin_password: the RDS admin password, we need this password
        to create the database user.
    :param db_username: the database user for game server
    :param db_password: the database password for game server
    :param authserver_conf: custom config for authserver.conf
    :param worldserver_conf: custom config for worldserver.conf
    :param mod_lua_engine_conf: custom config for mod_LuaEngine.conf
    """

    id: T.Optional[str] = dataclasses.field(default=None)
    db_admin_password: T.Optional[str] = dataclasses.field(default=None)
    db_username: T.Optional[str] = dataclasses.field(default=None)
    db_password: T.Optional[str] = dataclasses.field(default=None)
    authserver_conf: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    worldserver_conf: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    mod_lua_engine_conf: T.Dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class ServerMixin:
    servers: T.Dict[str, Server] = dataclasses.field(default_factory=dict)

    @property
    def server_blue(self) -> Server:
        return self.servers["blue"]

    @property
    def server_green(self) -> Server:
        return self.servers["green"]
