# -*- coding: utf-8 -*-

from acore_server_config import api


def test():
    _ = api

    _ = api.IS_LOCAL
    _ = api.IS_GITHUB_CI
    _ = api.IS_EC2
    _ = api.IS_CODEBUILD_CI
    _ = api.EnvEnum
    _ = api.Env
    _ = api.Config
    _ = api.Server
    _ = api.get_server
    _ = api.Ec2ConfigLoader
    _ = api.ConfigLoader
    _ = api.bsm


if __name__ == "__main__":
    from acore_server_config.tests import run_cov_test

    run_cov_test(__file__, "acore_server_config.api", preview=False)
