# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command: drop-db"""

import shutil
import subprocess

import click

from ociedoo import check, cli, complete, lib


@click.command(short_help="Delete databases.")
@click.argument(
    "dbname",
    callback=check.check_database_exist,
    autocompletion=complete.databases_complete,
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Delete DBNAME even if it has opened connections.",
)
@click.option(
    "--with-filestore/--without-filestore",
    default=True,
    show_default="with filestore",
    help="Also remove the filestore if it exists.",
)
@click.pass_context
def drop_db(ctx, dbname, force, with_filestore):
    """
    Delete DBNAME.
    """
    if force:
        lib.close_connections(dbname)
    result = subprocess.run(
        ["dropdb", dbname],
        check=False,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        click.echo("Error: {}".format(result.stderr), err=True)
        ctx.exit(result.returncode)
    if with_filestore:
        filestore_path = cli.tool.get_filestore_path(ctx, dbname)
        if filestore_path.exists():
            shutil.rmtree(filestore_path)
