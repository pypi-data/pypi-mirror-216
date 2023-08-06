# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command: rename-db"""

import subprocess

import click

from ociedoo import check, cli, complete, lib


@click.command(short_help="Rename databases.")
@click.argument(
    "oldname",
    callback=check.check_database_exist,
    autocompletion=complete.databases_complete,
)
@click.argument("newname", callback=check.check_database_not_exist)
@click.option(
    "--with-filestore/--without-filestore",
    default=True,
    show_default="with filestore",
    help="Also rename the filestore if it exists.",
)
@click.pass_context
def rename_db(ctx, oldname, newname, with_filestore):
    """
    Rename OLDNAME database to NEWNAME.
    """
    try:
        query_to_rename = lib.sql_rename_db(oldname, newname)
    except ValueError as e:
        ctx.fail(e)
    if with_filestore:
        new_filestore_path = cli.tool.get_filestore_path(ctx, newname)
        if new_filestore_path.exists():
            ctx.fail("A filestore named {0} already exists.".format(newname))
    lib.close_connections(oldname)
    if with_filestore:
        old_filestore_path = cli.tool.get_filestore_path(ctx, oldname)
        if old_filestore_path.exists():
            old_filestore_path.rename(new_filestore_path)
    result = subprocess.run(
        ["psql", "postgres", "-c", query_to_rename],
        check=False,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        click.echo("Error: {}".format(result.stderr), err=True)
    ctx.exit(result.returncode)
