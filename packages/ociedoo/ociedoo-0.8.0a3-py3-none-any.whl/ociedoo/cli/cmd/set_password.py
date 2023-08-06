# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command: set-password"""

import click
import sh
from passlib.context import CryptContext

from ociedoo import check, complete, lib


@click.command(short_help="Set password for a user.")
@click.argument(
    "database",
    callback=check.check_database_exist,
    autocompletion=complete.databases_complete,
)
@click.option(
    "--login",
    metavar="LOGIN",
    default="admin",
    help="Specify the user for who the password should be set. "
    "Default to 'admin'.",
)
@click.option(
    "--password",
    metavar="PASSWORD",
    prompt="New password",
    hide_input=True,
    confirmation_prompt=True,
    help="Set the admin password to PASSWORD.",
)
@click.pass_context
def set_password(ctx, database, login, password):
    """
    Set the password for a user of DATABASE. The default user is
    'admin', but can be specified with the --login option. The password
    is stored in the database in an encrypted way.

    When running this command you will be prompt to type the password,
    except if the --password is used. --password option should be used
    for scripting. DO NOT not use --password option when using
    interactive shell.

    Setting password for an odoo database version less than 8.0 is not
    supported.
    """
    # Check that login exist in database
    raw_query = "SELECT count(*) FROM res_users WHERE login = '%s'"
    query = raw_query % login
    try:
        nb_login = sh.psql(
            "--no-psqlrc",
            "--no-align",
            "--tuples-only",
            "--dbname",
            database,
            "--command",
            query,
        )
    except sh.ErrorReturnCode as err:
        click.echo(err, err=True)
        ctx.exit(1)
    if not int(nb_login.strip()):
        click.echo(
            "Error: Login '%s' does not exists in database '%s'. "
            "No password changed." % (login, database),
            err=True,
        )
        ctx.exit(1)

    # Get database version
    version = lib.get_odoo_version(database=database)
    if not version:
        click.echo(
            "Error: Could not find Odoo version in %s" % database, err=True
        )
        ctx.exit(1)

    # Encrypt password
    new_pwd_crypt = CryptContext(["pbkdf2_sha512"]).encrypt(password)

    # Set password
    if version >= 12:
        raw_query = "UPDATE res_users SET password='%s' WHERE login='%s';"
        query = raw_query % (new_pwd_crypt, login)
    elif version >= 8:
        raw_query = (
            "UPDATE res_users SET password='', password_crypt='%s' "
            "WHERE login='%s';"
        )
        query = raw_query % (new_pwd_crypt, login)
    else:
        click.echo(
            "Error: Password setting not supported for Odoo version %s"
            % version,
            err=True,
        )
        ctx.exit(1)
    try:
        sh.psql(
            "--dbname",
            database,
            "--command",
            query,
        )
    except sh.ErrorReturnCode as err:
        click.echo(err, err=True)
        ctx.exit(1)
