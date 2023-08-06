# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Entry point for all subcommand"""

import click

import ociedoo
from ociedoo import PGRNAME, check, complete, config, lib

# Context settings
CONTEXT_SETTINGS = {"auto_envvar_prefix": PGRNAME.upper()}


@click.group(
    context_settings=CONTEXT_SETTINGS,
    short_help="Simplify the management of Odoo instances.",
)
@click.option(
    "conf",
    "--config",
    "-c",
    type=click.Path(exists=True),
    autocompletion=complete.file_completion,
    metavar="CONFIG-FILE",
    help="ociedoo config file.",
)
@click.option(
    "profile_name",
    "--profile",
    "-p",
    autocompletion=complete.profile_complete,
    metavar="PROFILE",
    help="""name of a profile defined in the ociedoo config file.
    [default: (first profile found)].""",
)
@click.version_option(version=ociedoo.__version__)
@click.pass_context
def main(ctx, conf, profile_name):
    """
    This is a CLI tool to simplify the management of Odoo instances.

    To get help on a particular command run:

        ociedoo COMMAND --help

    This program needs a configuration file to work properly. This file
    can be referenced via the `--config` or found in the following
    locations: .ociedoo.conf, XDG_CONFIG_HOME/ociedoo/config,
    ~/.ociedoo.conf, XDG_CONFIG_DIRS/ociedoo/config,
    /etc/ociedoo/config. This list is from the more important to the
    less important. Also the environment variable OCIEDOO_CONF act as
    using `--config`. In such a case only the specified config file is
    read, else all files found are merged.

    PROFILE is the name of a profile given in the configuration file of
    ociedoo. In the configuration file, profiles are defined as sections
    that begins with 'profile-'. For example, section '[profile-simple]'
    is the section named 'simple'.

    Options always beats the configuration file.
    """
    if not isinstance(ctx.obj, dict):
        ctx.obj = {}
    if conf:
        config.config_file_path = [conf]
    config.load()
    ctx.obj["cfg"] = config
    check.check_profile_exists(ctx, "profile_name", profile_name)
    profile = lib.get_profile(config, profile_name)
    ctx.obj["profile"] = profile
