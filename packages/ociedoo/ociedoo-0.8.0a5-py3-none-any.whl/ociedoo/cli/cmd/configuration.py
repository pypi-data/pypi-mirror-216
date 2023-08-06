# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command: config"""

from pprint import pformat

import click


@click.command("config")
@click.option(
    "--source-files",
    is_flag=True,
    default=False,
    help="Show only configuration files that are loaded from "
    "the most important to the less important. Fail if there "
    "is no configuration file loaded.",
)
@click.option(
    "--pager", is_flag=True, default=False, help="Send output to a pager."
)
@click.pass_context
def configuration(ctx, source_files, pager):
    """
    Show the current configuration.
    """
    cfg = ctx.obj["cfg"]

    if source_files:
        file_list = cfg.config_sources
        if not file_list:
            ctx.exit(1)  # No config file loaded
        # To get file from the most important to the less, we need to
        # reverse the list
        file_list.reverse()
        file_list_str = "\n".join(str(path) for path in file_list)
        if pager:
            click.echo_via_pager(file_list_str)
        else:
            click.echo(file_list_str)
    else:
        if pager:
            click.echo_via_pager(pformat(cfg))
        else:
            click.echo(pformat(cfg))
