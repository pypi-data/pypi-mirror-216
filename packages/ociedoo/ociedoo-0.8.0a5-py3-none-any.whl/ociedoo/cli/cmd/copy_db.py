# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command: copy-db"""

import shutil

import click
import sh

from ociedoo import check, cli, complete


@click.command(short_help="Copy databases.")
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
    help="Also copy the filestore if it exists.",
)
@click.pass_context
def copy_db(ctx, oldname, newname, with_filestore):
    """
    Copy OLDNAME database to NEWNAME.
    """
    if with_filestore:
        new_filestore_path = cli.tool.get_filestore_path(ctx, newname)
        if new_filestore_path.exists():
            ctx.fail("A filestore named {0} already exists.".format(newname))
    try:
        sh.createdb("--template", oldname, newname)
    except sh.ErrorReturnCode as err:
        click.echo("Error: ", nl=False, err=True)
        click.echo(err.stderr, err=True)
        ctx.exit(1)
    if with_filestore:
        old_filestore_path = cli.tool.get_filestore_path(ctx, oldname)
        if old_filestore_path.exists():
            shutil.copytree(
                old_filestore_path, new_filestore_path, symlinks=True
            )
