[![pipeline status](https://gitlab.com/coopiteasy/ociedoo/badges/master/pipeline.svg)](https://gitlab.com/coopiteasy/ociedoo)

ociedoo
=======

ociedoo is a cli collection of tools to simplify the management of odoo
on a server.

See help for more info.


Installation
------------

ociedoo needs python version >= 3.5. So ensure `pip` points to a correct
version of python. To do this run:
```shell
pip --version
```

It should return something like:
```
pip xx.y from /path/to/pip (python 3.5)
```

If `pip` doesn't run python >=3.5, try running `pip3` which is on
certain distribution the `pip` for python >=3.


### Dependencies

ociedoo uses external programs via the shell. Be sure they are installed
and accessible for the current user.

- psql
- createdb
- dropdb
- systemctl


### Install for a specific user


#### Installation with pipx (recommended python >= 3.6)

```shell
pipx install ociedoo
```


#### Installation with pipsi (recommended python < 3.5)

```shell
pipsi install ociedoo
```


#### Install with pip

```shell
pip install --user ociedoo
```


### Install system wide (for all users)


#### Install with pipx (recommended python >= 3.6)

First install pipx if not already installed:
```shell
sudo pip install pipx
```

Then install ociedoo:
```shell
sudo PIPX_HOME=/usr/local PIPX_BIN_DIR=/usr/local/bin pipx install ociedoo
```


#### Install with pipsi (recommended python < 3.6)

First install pipsi, if not already installed:
```shell
sudo curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | sudo python3 - --bin-dir /usr/local/bin --home /usr/local/venvs --no-modify-path
```

Then install ociedoo:
```shell
sudo pipsi --bin-dir /usr/local/bin --home /usr/local/venvs install ociedoo
```


#### Install with pip
```shell
sudo pip install ociedoo
```


### Enable bash completion


#### Bash completion for a specific user

To enable bash completion add the following in your `.bashrc`:

```shell
# ociedoo
# =======
if command -v ociedoo >/dev/null; then
    eval "$(_OCIEDOO_COMPLETE=source ociedoo)"
fi
```

Or if you use zsh, add this to your `.zshrc`:
```shell
# ociedoo
# =======
if command -v ociedoo >/dev/null; then
    eval "$(_OCIEDOO_COMPLETE=source_zsh ociedoo)"
fi
```


#### Bash completion system wide (for all users)

To enable bash completion add the following in `/etc/bash.bashrc`:
```shell
# ociedoo
# =======
if command -v ociedoo >/dev/null; then
    eval "$(_OCIEDOO_COMPLETE=source ociedoo)"
fi
```

Or if you use zsh, add this to your `/etc/zsh/zshrc`:
```shell
# ociedoo
# =======
if command -v ociedoo >/dev/null; then
    eval "$(_OCIEDOO_COMPLETE=source_zsh ociedoo)"
fi
```


Upgrade
-------


### Upgrade for a specific user


#### Upgrade with pipx (recommended python >= 3.6)

```shell
pipx upgrade ociedoo
```


#### Upgrade with pipsi (recommended python < 3.5)

```shell
pipsi upgrade ociedoo
```


#### Upgrade with pip

```shell
pip install --user --upgrade ociedoo
```


### Upgrade system wide (for all users)


#### Upgrade with pipx (recommended python >= 3.6)

```shell
sudo PIPX_HOME=/usr/local PIPX_BIN_DIR=/usr/local/bin pipx upgrade ociedoo
```


#### Upgrade with pipsi (recommended python < 3.5)

```shell
sudo pipsi --bin-dir /usr/local/bin --home /usr/local/venvs upgrade ociedoo
```


#### Upgrade with pip

```shell
sudo pip install --upgrade ociedoo
```

Build and publish
-----------------

First do not forget to upgrade version. Then:

```shell
poetry build
poetry publish -u coopiteasy
