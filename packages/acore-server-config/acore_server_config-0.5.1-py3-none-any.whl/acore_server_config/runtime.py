# -*- coding: utf-8 -*-

"""
**"Runtime" Definition**

Runtime is where you execute your code. For example, if this code is running
in a CI build environment, then the runtime is "ci". If this code is running
on your local laptop, then the runtime is "local". If this code is running on
AWS Lambda, then the runtime is "lambda"

This module automatically detect what is the current runtime.

.. note::

    This module is "ZERO-DEPENDENCY".
"""

import os
import enum

IS_LOCAL = False
IS_GITHUB_CI = False
IS_EC2 = False
IS_CODEBUILD_CI = False
IS_LAMBDA = False
IS_BATCH = False
IS_FARGATE = False


class RunTimeEnum(str, enum.Enum):
    local = "loc"
    github_ci = "github_ci"
    ec2 = "ec2"
    codebuild_ci = "codebuild_ci"
    awslambda = "awslambda"
    batch = "batch"
    fargate = "fargate"
    unknown = "unknown"


CURRENT_RUNTIME: str = RunTimeEnum.unknown.value

# don't rely on $HOME env var, you may on EC2 and use sudo, then the $HOME is /root
# but actually you are on EC2
if os.path.exists("/home/ubuntu"):
    IS_EC2 = True
    CURRENT_RUNTIME = RunTimeEnum.ec2.value
# if you use AWS CodeBuild for CI/CD
# ref: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html
elif "CODEBUILD_CI" in os.environ:  # pragma: no cover
    IS_CODEBUILD_CI = True
    CURRENT_RUNTIME = RunTimeEnum.codebuild_ci.value
# if you use GitHub CI for CI/CD
# ref: https://docs.github.com/en/actions/learn-github-actions/variables
elif "CI" in os.environ:  # pragma: no cover
    IS_GITHUB_CI = True
    CURRENT_RUNTIME = RunTimeEnum.github_ci.value
# ref: https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html
elif "AWS_LAMBDA_FUNCTION_NAME" in os.environ:  # pragma: no cover
    IS_LAMBDA = True
    CURRENT_RUNTIME = RunTimeEnum.awslambda.value
# ref: https://docs.aws.amazon.com/batch/latest/userguide/job_env_vars.html
elif "AWS_BATCH_JOB_ID" in os.environ:  # pragma: no cover
    IS_BATCH = True
    CURRENT_RUNTIME = RunTimeEnum.batch.value
# ref: https://docs.aws.amazon.com/AmazonECS/latest/userguide/task-metadata-endpoint-v4-fargate.html
elif "ECS_CONTAINER_METADATA_URI_V4" in os.environ or "ECS_CONTAINER_METADATA_URI" in os.environ:  # pragma: no cover
    IS_FARGATE = True
    CURRENT_RUNTIME = RunTimeEnum.fargate.value
else:  # pragma: no cover
    IS_LOCAL = True
    CURRENT_RUNTIME = RunTimeEnum.local.value
