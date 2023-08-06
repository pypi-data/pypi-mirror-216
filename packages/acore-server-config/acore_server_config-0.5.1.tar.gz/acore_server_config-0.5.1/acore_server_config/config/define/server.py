# -*- coding: utf-8 -*-

"""
todo: doc string
"""

import typing as T
import dataclasses

from acore_constants.api import ServerLifeCycle

if T.TYPE_CHECKING:  # pragma: no cover
    from .main import Env


@dataclasses.dataclass
class Server:
    """
    Per Game Server configuration.

    :param id: Server id, the naming convention is ``${env_name}-${server_name}``.
    :param ec2_ami_id: the AMI id for the game server.
    :param ec2_instance_type: the EC2 instance type for the game server.
    :param ec2_subnet_id: the EC2 subnet id for the game server.
    :param ec2_key_name: the EC2 ssh key name for the game server.
    :param ec2_eip_allocation_id: if you need a static IP, then create
        an Elastic IP address and put the allocation id here. otherwise,
        use the automatic public IP address.
    :param acore_soap_app_version: the acore_soap_app-project git tag for bootstrap.
    :param acore_server_bootstrap_version: the acore_server_bootstrap-project
        git tag for bootstrap.
    :param db_snapshot_id: the snapshot id to create the RDS DB instance.
    :param db_instance_class: the RDS instance class for the game database.
    :param db_admin_password: the RDS admin password, we need this password.
        to create the database user for game server.
    :param db_username: the database user for game server.
    :param db_password: the database password for game server.
    :param lifecycle: the logic "game server (both EC2 and RDS)" lifecycle definition.
    :param authserver_conf: custom config for authserver.conf.
    :param worldserver_conf: custom config for worldserver.conf.
    :param mod_lua_engine_conf: custom config for mod_LuaEngine.conf.
    """

    id: T.Optional[str] = dataclasses.field(default=None)
    # EC2 related
    ec2_ami_id: T.Optional[str] = dataclasses.field(default=None)
    ec2_instance_type: T.Optional[str] = dataclasses.field(default=None)
    ec2_subnet_id: T.Optional[str] = dataclasses.field(default=None)
    ec2_key_name: T.Optional[str] = dataclasses.field(default=None)
    ec2_eip_allocation_id: T.Optional[str] = dataclasses.field(default=None)
    acore_soap_app_version: T.Optional[str] = dataclasses.field(default=None)
    acore_db_app_version: T.Optional[str] = dataclasses.field(default=None)
    acore_server_bootstrap_version: T.Optional[str] = dataclasses.field(default=None)
    # RDS related
    db_snapshot_id: T.Optional[str] = dataclasses.field(default=None)
    db_instance_class: T.Optional[str] = dataclasses.field(default=None)
    db_admin_password: T.Optional[str] = dataclasses.field(default=None)
    db_username: T.Optional[str] = dataclasses.field(default=None)
    db_password: T.Optional[str] = dataclasses.field(default=None)
    # EC2 and RDS related
    lifecycle: T.Optional[str] = dataclasses.field(default=None)
    # authserver.conf, worldserver.conf, ...
    authserver_conf: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    worldserver_conf: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    mod_lua_engine_conf: T.Dict[str, str] = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        if self.lifecycle not in [
            ServerLifeCycle.running,
            ServerLifeCycle.smart_running,
            ServerLifeCycle.stopped,
            ServerLifeCycle.deleted,
        ]:  # pragma: no cover
            raise ValueError(f"{self.lifecycle!r} is not a valid lifecycle definition!")


@dataclasses.dataclass
class ServerMixin:
    servers: T.Dict[str, Server] = dataclasses.field(default_factory=dict)

    @property
    def server_blue(self) -> Server:
        return self.servers["blue"]

    @property
    def server_green(self) -> Server:
        return self.servers["green"]
