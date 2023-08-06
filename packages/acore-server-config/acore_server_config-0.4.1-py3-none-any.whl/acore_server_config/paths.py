# -*- coding: utf-8 -*-

from pathlib import Path

dir_here = Path(__file__).absolute().parent
PACKAGE_NAME = dir_here.name

dir_project_root = dir_here.parent

# ------------------------------------------------------------------------------
# Virtual Environment Related
# ------------------------------------------------------------------------------
dir_venv = dir_project_root / ".venv"
dir_venv_bin = dir_venv / "bin"

# virtualenv executable paths
bin_pytest = dir_venv_bin / "pytest"

# test related
dir_htmlcov = dir_project_root / "htmlcov"
path_cov_index_html = dir_htmlcov / "index.html"
dir_unit_test = dir_project_root / "tests"


# ------------------------------------------------------------------------------
# Config Management Related
# ------------------------------------------------------------------------------
dir_home = Path.home()  # ${HOME}
dir_home_project_root = dir_home / ".projects" / PACKAGE_NAME

dir_config = dir_project_root / "config"
# where you store the non-sensitive config data
path_config_json = dir_config / "config.json"
# where you store the sensitive config dat
path_config_secret_json = dir_home_project_root / "config-secret.json"
