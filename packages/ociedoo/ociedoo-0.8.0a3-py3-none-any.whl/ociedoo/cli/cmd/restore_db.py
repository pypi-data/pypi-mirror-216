# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command: restore-db"""

import datetime
from pathlib import Path

import click
import sh

from ociedoo import check, cli, complete, lib


@click.command(short_help="Restore database.")
@click.argument("database", autocompletion=complete.databases_complete)
@click.argument(
    "backup",
    type=click.Path(exists=True),
    autocompletion=complete.file_completion([".sql", ".sql.gz"]),
)
@click.argument(
    "filestore_backup",
    required=False,
    type=click.Path(exists=True),
    autocompletion=complete.file_completion([".tar", ".tar.*"]),
)
@click.option(
    "--force", "-f", is_flag=True, help="Delete DATABASE if it exist."
)
@click.option(
    "--autosave/--no-autosave",
    default=None,
    help="Backup DATABASE to a new name with pattern "
    "DATABASE-save-YYYY-MM-DD before restoring BACKUP to "
    "DATABASE. Beats --force.",
)
@click.option(
    "--save",
    metavar="SAVENAME",
    callback=check.check_database_not_exist,
    help="Rename DATABASE to SAVENAME instead of deleting it. "
    "Beats --autosave.",
)
@click.option(
    "--login",
    metavar="LOGIN",
    default="admin",
    help="Specify the user for who the password should be set. "
    "Default to 'admin'.",
)
@click.option(
    "pwd",
    "--set-password",
    metavar="PASSWORD",
    required=False,
    help="Prompt for a new user password for DATABASE. "
    "Default user is 'admin'. Set user with --login.",
)
@click.option(
    "no_pwd",
    "--no-set-password",
    is_flag=True,
    help="Do not ask to change a user password. " "Beats --set-password.",
)
@click.option(
    "--posthook",
    type=click.Path(exists=True),
    autocompletion=complete.file_completion([".sql", ".sql.gz"]),
    metavar="POSTHOOK",
    help="""
    POSTHOOK is a regular sql file or a gzipped version of it that
    contains sql instructions that will be executed on DATABASE after
    the restoration of the BACKUP. POSTHOOK can be configured in the
    configuration file. The value of POSTHOOK will replace the one in
    the configuration file. POSTHOOK is not executed if option
    `--disable-posthook` is given, or if POSTHOOK is empty.
    """,
)
@click.option(
    "--disable-posthook",
    is_flag=True,
    default=False,
    help="Disable POSTHOOK execution.",
)
@click.pass_context
def restore_db(
    ctx,
    database,
    backup,
    filestore_backup,
    force,
    autosave,
    save,
    login,
    pwd,
    no_pwd,
    posthook,
    disable_posthook,
):
    """
    Restore BACKUP on DATABASE.

    BACKUP is a regular sql file or a gzipped version of a regular sql
    file.

    FILESTORE_BACKUP is an optionally-compressed tar file containing the
    filestore. It should contain a top-level directory called "filestore".

    DATABASE can be a new database name or an existing one. If database
    is an existing one see options `--autosave`, `--save` and `--force`.

    A new password for the 'admin' user will be asked. Use
    --no-set-password to not change password. Use --login if the login
    of the admin is not 'admin'.
    """
    profile = ctx.obj["profile"]

    # Get value from config if not provided in the command line
    if autosave is None:
        autosave = profile["restore"].get("autosave")
    if not posthook:
        posthook = profile["restore"].get("posthook", "").strip()
        if posthook and not Path(posthook).expanduser().exists():
            ctx.echo(
                "Error: file '%s' given in as 'posthook' in the "
                "configuration file does not exist." % posthook,
                err=True,
            )
            ctx.exit(1)

    if filestore_backup:
        filestore_path = cli.tool.get_filestore_path(ctx, database)
        if filestore_path.exists():
            ctx.fail("A filestore named {0} already exists.".format(database))

    # Ask for a password if needed
    if not no_pwd:
        pwd = click.prompt(
            "New password for user '%s'" % login,
            hide_input=True,
            confirmation_prompt=True,
        )

    # Save or drop db
    if database in lib.get_all_db():
        if save:
            try:
                ctx.invoke(cli.rename_db, oldname=database, newname=save)
            except click.exceptions.Exit as err:
                if err.exit_code:
                    raise
        elif autosave:
            newname = "%s-save-%s" % (database, str(datetime.date.today()))
            try:
                ctx.invoke(cli.rename_db, oldname=database, newname=newname)
            except click.exceptions.Exit as err:
                if err.exit_code:
                    click.echo(
                        "Take a look at --no-autosave or --save", err=True
                    )
                    raise
        elif force:
            try:
                sh.dropdb(database, _done=cli.tool.cb_print_cmd)
            except sh.ErrorReturnCode as err:
                click.echo("Error: ", nl=False, err=True)
                click.echo(err.stderr, err=True)
                ctx.exit(1)
        else:
            ctx.fail(
                "Database '%s' already exists. Look at --force, "
                "--autosave or --save options." % database
            )
    # Create new db
    try:
        sh.createdb(database, _done=cli.tool.cb_print_cmd)
    except sh.ErrorReturnCode as err:
        click.echo("Error: ", nl=False, err=True)
        click.echo(err.stderr, err=True)
        ctx.exit(1)
    # Import db from a sql file with progression bar
    with click.progressbar(
        length=lib.linecount(backup), label="Restoring database"
    ) as pbar:
        psqlproc = sh.psql(
            database,
            _in=lib.get_file_content(backup, pbar),
            _bg=True,
        )
        psqlproc.wait()

    # Apply posthook
    if not disable_posthook and posthook:
        with click.progressbar(
            length=lib.linecount(posthook), label="Applying posthook"
        ) as pbar:
            try:
                sh.psql(
                    database,
                    _in=lib.get_file_content(posthook, pbar),
                )
            except sh.ErrorReturnCode as err:
                click.echo(err, err=True)
                ctx.exit(1)

    # Set admin password and admin login
    if not no_pwd:
        ctx.invoke(
            cli.set_password, database=database, login=login, password=pwd
        )

    if filestore_backup:
        click.echo("Restoring filestore...")
        try:
            lib.restore_filestore_backup(filestore_backup, filestore_path)
        except ValueError as e:
            ctx.fail(e)
