# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Tool function for click commands"""

import click

from ociedoo import lib


def cb_print_cmd(cmd, success, exit_code):
    """Print the command that has been run on stdout"""
    click.echo("Running: %s" % cmd.ran)


def get_filestore_path(ctx, database):
    """
    Return the filestore path of the provided database as a pathlib.Path
    object
    """
    # the filestore directory is stored in odoo's "data_dir", which is
    # configurable (--data-dir command-line option and data_dir property in
    # the configuration file) and whose default value depends on multiple
    # factors (user's home directory or platform) (see
    # odoo.tools.config._get_default_datadir()). since we don't use odoo's
    # code in here, and will not reimplement the function, we will assume the
    # most common default value, while making it overridable in the
    # configuration file.
    profile = ctx.obj["profile"]
    data_dir = profile.get("data-dir")
    return lib.get_filestore_path(database, data_dir)
