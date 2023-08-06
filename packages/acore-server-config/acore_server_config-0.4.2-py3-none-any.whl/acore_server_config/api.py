# -*- coding: utf-8 -*-

from .runtime import IS_LOCAL
from .runtime import IS_GITHUB_CI
from .runtime import IS_EC2
from .runtime import IS_CODEBUILD_CI
from .config.define import EnvEnum
from .config.define import Env
from .config.define import Config
from .config.define import Server
from .config.loader import Ec2ConfigLoader
from .config.loader import ConfigLoader
from .in_ec2 import get_server

try:
    from .boto_ses import bsm
except ImportError as e:  # pragma: no cover
    pass
