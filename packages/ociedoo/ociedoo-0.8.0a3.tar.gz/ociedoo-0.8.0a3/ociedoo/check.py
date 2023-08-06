# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Checks for arguments of the CLI"""

import re

import click

from ociedoo import REDBNAME, lib


def check_database_valid_name(ctx, param, value):
    """
    Raise an exception if :value: is not a valid database name.
    """
    if value:
        if not re.match(REDBNAME, value):
            raise click.BadParameter(
                "'%s' is not a valid database name." % value
            )
    return value


def check_database_exist(ctx, param, value):
    """
    Raise an exception if database named :value: does not exit and if
    :value: is not a valid database name.
    """
    if value:
        if value not in lib.get_all_db():
            raise click.BadParameter("Database '%s' does not exist." % value)
    check_database_valid_name(ctx, param, value)
    return value


def check_database_not_exist(ctx, param, value):
    """
    Raise an exception if database named :value: already exists and if
    :value: is not a valid database name.
    """
    if value:
        if value in lib.get_all_db():
            raise click.BadParameter("Database '%s' already exists." % value)
    check_database_valid_name(ctx, param, value)
    return value


def check_profile_exists(ctx, param, value):
    """
    Raise an exception if profile named :value: does not exit.
    """
    if value:
        cfg = ctx.obj["cfg"]
        if "profile" not in cfg:
            raise click.BadParameter(
                "Configuration file does not contains profiles."
            )
        if value not in (
            prof["name"] for prof in cfg["profile"] if "name" in prof
        ):
            raise click.BadParameter("Profile '%s' does not exists." % value)
    return value
