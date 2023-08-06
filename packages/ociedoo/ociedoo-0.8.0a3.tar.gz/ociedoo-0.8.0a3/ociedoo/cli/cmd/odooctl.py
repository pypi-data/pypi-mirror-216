# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command related to manage odoo daemon"""

import click
import sh

from ociedoo import lib


@click.command()
@click.pass_context
def start_odoo(ctx):
    """
    Start odoo daemon.
    """
    profile = ctx.obj["profile"]
    odoo_daemon_name = profile.get("daemon-name")
    if not lib.is_daemon_running(odoo_daemon_name):
        if not lib.start_daemon(odoo_daemon_name):
            ctx.fail(
                "Fail to start %s daemon. To do so try: sudo "
                "systemctl start %s" % (odoo_daemon_name, odoo_daemon_name)
            )


@click.command()
@click.pass_context
def status_odoo(ctx):
    """
    Status of tho odoo daemon.
    """
    profile = ctx.obj["profile"]
    odoo_daemon_name = profile.get("daemon-name")
    try:
        sh.systemctl.status(odoo_daemon_name, _fg=True)
    except sh.ErrorReturnCode as err:
        ctx.exit(err.exit_code)


@click.command()
@click.pass_context
def stop_odoo(ctx):
    """
    Stop odoo daemon.
    """
    profile = ctx.obj["profile"]
    odoo_daemon_name = profile.get("daemon-name")
    if lib.is_daemon_running(odoo_daemon_name):
        if not lib.stop_daemon(odoo_daemon_name):
            ctx.fail(
                "Fail to stop %s daemon. To do so try: sudo "
                "systemctl stop %s" % (odoo_daemon_name, odoo_daemon_name)
            )
