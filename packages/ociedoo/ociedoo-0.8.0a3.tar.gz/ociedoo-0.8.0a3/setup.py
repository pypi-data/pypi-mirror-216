# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ociedoo', 'ociedoo.cli', 'ociedoo.cli.cmd']

package_data = \
{'': ['*'], 'ociedoo': ['defaults/*']}

install_requires = \
['click>=7.0,<8.0',
 'passlib>=1.7.4,<2.0.0',
 'prgconfig>=1.0.0-beta.2,<2.0.0',
 'sh>=1.12,<2.0']

entry_points = \
{'console_scripts': ['ociedoo = ociedoo.cli:main']}

setup_kwargs = {
    'name': 'ociedoo',
    'version': '0.8.0a3',
    'description': 'CLI tool to simplify the management of Odoo',
    'long_description': '[![pipeline status](https://gitlab.com/coopiteasy/ociedoo/badges/master/pipeline.svg)](https://gitlab.com/coopiteasy/ociedoo)\n\nociedoo\n=======\n\nociedoo is a cli collection of tools to simplify the management of odoo\non a server.\n\nSee help for more info.\n\n\nInstallation\n------------\n\nociedoo needs python version >= 3.5. So ensure `pip` points to a correct\nversion of python. To do this run:\n```shell\npip --version\n```\n\nIt should return something like:\n```\npip xx.y from /path/to/pip (python 3.5)\n```\n\nIf `pip` doesn\'t run python >=3.5, try running `pip3` which is on\ncertain distribution the `pip` for python >=3.\n\n\n### Dependencies\n\nociedoo uses external programs via the shell. Be sure they are installed\nand accessible for the current user.\n\n- psql\n- createdb\n- dropdb\n- systemctl\n\n\n### Install for a specific user\n\n\n#### Installation with pipx (recommended python >= 3.6)\n\n```shell\npipx install ociedoo\n```\n\n\n#### Installation with pipsi (recommended python < 3.5)\n\n```shell\npipsi install ociedoo\n```\n\n\n#### Install with pip\n\n```shell\npip install --user ociedoo\n```\n\n\n### Install system wide (for all users)\n\n\n#### Install with pipx (recommended python >= 3.6)\n\nFirst install pipx if not already installed:\n```shell\nsudo pip install pipx\n```\n\nThen install ociedoo:\n```shell\nsudo PIPX_HOME=/usr/local PIPX_BIN_DIR=/usr/local/bin pipx install ociedoo\n```\n\n\n#### Install with pipsi (recommended python < 3.6)\n\nFirst install pipsi, if not already installed:\n```shell\nsudo curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | sudo python3 - --bin-dir /usr/local/bin --home /usr/local/venvs --no-modify-path\n```\n\nThen install ociedoo:\n```shell\nsudo pipsi --bin-dir /usr/local/bin --home /usr/local/venvs install ociedoo\n```\n\n\n#### Install with pip\n```shell\nsudo pip install ociedoo\n```\n\n\n### Enable bash completion\n\n\n#### Bash completion for a specific user\n\nTo enable bash completion add the following in your `.bashrc`:\n\n```shell\n# ociedoo\n# =======\nif command -v ociedoo >/dev/null; then\n    eval "$(_OCIEDOO_COMPLETE=source ociedoo)"\nfi\n```\n\nOr if you use zsh, add this to your `.zshrc`:\n```shell\n# ociedoo\n# =======\nif command -v ociedoo >/dev/null; then\n    eval "$(_OCIEDOO_COMPLETE=source_zsh ociedoo)"\nfi\n```\n\n\n#### Bash completion system wide (for all users)\n\nTo enable bash completion add the following in `/etc/bash.bashrc`:\n```shell\n# ociedoo\n# =======\nif command -v ociedoo >/dev/null; then\n    eval "$(_OCIEDOO_COMPLETE=source ociedoo)"\nfi\n```\n\nOr if you use zsh, add this to your `/etc/zsh/zshrc`:\n```shell\n# ociedoo\n# =======\nif command -v ociedoo >/dev/null; then\n    eval "$(_OCIEDOO_COMPLETE=source_zsh ociedoo)"\nfi\n```\n\n\nUpgrade\n-------\n\n\n### Upgrade for a specific user\n\n\n#### Upgrade with pipx (recommended python >= 3.6)\n\n```shell\npipx upgrade ociedoo\n```\n\n\n#### Upgrade with pipsi (recommended python < 3.5)\n\n```shell\npipsi upgrade ociedoo\n```\n\n\n#### Upgrade with pip\n\n```shell\npip install --user --upgrade ociedoo\n```\n\n\n### Upgrade system wide (for all users)\n\n\n#### Upgrade with pipx (recommended python >= 3.6)\n\n```shell\nsudo PIPX_HOME=/usr/local PIPX_BIN_DIR=/usr/local/bin pipx upgrade ociedoo\n```\n\n\n#### Upgrade with pipsi (recommended python < 3.5)\n\n```shell\nsudo pipsi --bin-dir /usr/local/bin --home /usr/local/venvs upgrade ociedoo\n```\n\n\n#### Upgrade with pip\n\n```shell\nsudo pip install --upgrade ociedoo\n```\n\nBuild and publish\n-----------------\n\nFirst do not forget to upgrade version. Then:\n\n```shell\npoetry build\npoetry publish -u coopiteasy\n',
    'author': 'Coop IT Easy SCRLfs',
    'author_email': 'remy@coopiteasy.be',
    'maintainer': 'Rémy Taymans',
    'maintainer_email': 'remy@coopiteasy.be',
    'url': 'https://gitlab.com/coopiteasy/ociedoo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
