# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command: run"""

import signal

import click

from ociedoo import check, complete, lib


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    short_help="Run Odoo with default options.",
)
@click.argument(
    "database",
    callback=check.check_database_exist,
    autocompletion=complete.databases_complete,
)
@click.argument("odoo_args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "modules",
    "-u",
    "--update",
    metavar="MODULES",
    autocompletion=complete.modules_complete_list,
    help="Update MODULES.",
)
@click.pass_context
def run(ctx, database, modules, odoo_args):
    """
    Run Odoo with some default options.

    Defaults can be a special port, some default debug options, special
    odoo configuration file, etc. and are defined in a profile (see the main
    --profile option).

    DATABASE is the database on witch module can be updated and on which
    odoo will be launched.

    ODOO_ARGS is arguments directly given to the odoo command.
    """
    profile = ctx.obj["profile"]

    if modules:
        update_option = ("-u", modules)
    else:
        update_option = ()

    try:
        process = lib.run_odoo(
            profile=profile,
            database=database,
            other_args=update_option + odoo_args,
        )
        if process.wait():
            ctx.fail("Error: Odoo terminate with code %d" % process.returncode)
    except KeyboardInterrupt:
        click.echo("CTRL-C: program will terminate properly.", err=True)
        try:
            process.send_signal(signal.SIGINT)
            process.wait()
        except KeyboardInterrupt:
            click.echo("CTRL-C: program will exit now.", err=True)
            process.kill()
            ctx.exit(101)
        ctx.exit(100)
    ctx.exit()
