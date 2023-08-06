# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command: list-module"""

import click
import sh

from ociedoo import check, complete, lib


@click.command(short_help="List installed modules on a database.")
@click.argument(
    "database",
    callback=check.check_database_exist,
    autocompletion=complete.databases_complete,
)
@click.pass_context
def list_module(ctx, database):
    """
    List all installed modules in the database named DATABASE.
    """
    try:
        modules = lib.get_installed_modules(database)
    except sh.ErrorReturnCode as err:
        click.echo(err, err=True)
        ctx.exit(1)
    for mod in modules:
        click.echo(mod)
