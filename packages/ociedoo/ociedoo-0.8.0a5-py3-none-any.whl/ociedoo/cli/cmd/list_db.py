# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command: list-db"""

import click

from ociedoo import lib


@click.command(short_help="List existing databases.")
@click.argument("user", required=False)
@click.option(
    "all_user",
    "--all",
    is_flag=True,
    help="Ignore USER and show all databases",
)
@click.option(
    "--module",
    metavar="MODULE",
    help="List only database with MODULE installed.",
)
@click.option(
    "separator",
    "--sep",
    metavar="SEPARATOR",
    default="\n",
    help="Separator between databases names on. Default new line.",
)
@click.pass_context
def list_db(ctx, user, all_user, module, separator):
    """
    List all the database names that belongs to USER. If USER is not
    specified, the USER from the field `database_user` in the
    configuration file is used.
    """
    profile = ctx.obj["profile"]
    if all_user:
        dbs = lib.get_all_db()
    elif user:
        dbs = lib.get_all_db(user)
    else:
        dbs = lib.get_all_db(profile["database-user"])
    # Filter dbs if module is given
    if module:
        dbs = (db for db in dbs if module in lib.get_installed_modules(db))
    # Two different case for the same thing, because if separator is new
    # line then the output can be feed in real time, not all in a block
    # like when using, for example, a coma as separator.
    if separator in ("\n", "\\n"):
        for db in dbs:
            click.echo(db)
    else:
        click.echo(separator.join(dbs))
