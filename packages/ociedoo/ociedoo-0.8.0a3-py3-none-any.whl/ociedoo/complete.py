# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Completion functions for CLI"""

import os
from pathlib import Path

from ociedoo import config, lib


def read_config(ctx, args):
    """
    Return config object based on context and args.
    If ctx is empty then args should be parsed.
    If ctx is not empty then it means that config as already been loaded
    """
    # Check and read config file given in args if specified
    args = args if args else []
    cfg = None
    if ctx.obj is not None:
        cfg = ctx.obj.get("cfg")
    if not cfg:
        cfg = config
        config_filename = None
        optflags = ("-c", "--config")
        for optflag in optflags:
            if optflag in args:
                optindex = args.index(optflag)
                try:
                    config_filename = Path(args[optindex + 1])
                except IndexError:
                    pass
        if config_filename:
            cfg.config_file_path = [config_filename]
        cfg.load()
    return cfg


def databases_complete(ctx, args, incomplete):
    """
    List available database name matching :incomplete:.
    """
    cfg = read_config(ctx, args)
    if not ("profile" in cfg and cfg["profile"]):
        return []
    # TODO: chose profile based on arguments
    profile = cfg["profile"][0]
    return [
        db
        for db in lib.get_all_db(profile["database-user"])
        if db.startswith(incomplete)
    ]


def databases_complete_list(ctx, args, incomplete):
    """
    List available database matching the last element of :incomplete:
    list. :incomplete: is coma separated string of database name.
    """
    incompletes = incomplete.split(",")
    last_incomplete = incompletes[-1]
    found_db = databases_complete(ctx, args, last_incomplete)
    if incompletes[:-1]:
        return ["%s,%s" % (",".join(incompletes[:-1]), db) for db in found_db]
    return found_db


def modules_complete(ctx, args, incomplete):
    """
    List available modules matching :incomplete:.
    """
    cfg = read_config(ctx, args)
    if not ("profile" in cfg and cfg["profile"]):
        return []
    # TODO: chose profile based on arguments
    profile = cfg["profile"][0]
    addons_p = [
        Path(path).expanduser()
        for path in lib.get_addons_path(
            profile["odoo-config-path"],
            profile["working-directory"],
        )
    ]
    modules = []
    for p in addons_p:
        for mod in p.iterdir():
            if mod.is_dir() and (
                mod / Path("__manifest__.py") in mod.iterdir()
                or mod / Path("__openerp__.py") in mod.iterdir()
            ):
                modules.append(mod.name)
    match_modules = [mod for mod in modules if mod.startswith(incomplete)]
    match_modules.sort()
    return match_modules


def modules_complete_list(ctx, args, incomplete):
    """
    List available modules matching the last element of :incomplete:
    list. :incomplete: is coma separated string of module name.
    """
    incompletes = incomplete.split(",")
    last_incomplete = incompletes[-1]
    found_mod = modules_complete(ctx, args, last_incomplete)
    if incompletes[:-1]:
        return [
            "%s,%s" % (",".join(incompletes[:-1]), mod) for mod in found_mod
        ]
    return found_mod


def profile_complete(ctx, args, incomplete):
    """
    List available profile in the config file matching :incomplete:.
    """
    cfg = read_config(ctx, args)
    return [
        profile["name"]
        for profile in cfg["profile"]
        if "name" in profile and profile["name"].startswith(incomplete)
    ]


def file_completion(suffixes=None):
    """
    Generate a function that can be used as completion for click.
    """

    def file_complete(ctx, args, incomplete):
        """
        List files in parent of :incomplete: that have at least one of
        the :suffixes: and that match :incomplete: name.
        """
        raw_hidden = incomplete.endswith(os.sep + ".")
        raw_p = Path(incomplete)
        p = Path(incomplete).expanduser()
        is_p_exp = raw_p != p
        is_hidden = str(p.name).startswith(".") or raw_hidden

        def has_suffix(file, suffixes):
            """
            Return True if file has one of the suffixes.
            If suffixes is empty, return always true.
            """
            if not suffixes:
                return True
            for suffix in suffixes:
                if file.match("*" + suffix) or file.match("**/*" + suffix):
                    return True
            return False

        if p.is_dir():
            rawres = (
                file if not is_p_exp else Path(raw_p, file.name)
                for file in p.iterdir()
                if (
                    (has_suffix(file, suffixes) or file.is_dir())
                    and not str(file.name).startswith(".") ^ is_hidden
                )
            )
            return [
                str(file) + os.sep if file.expanduser().is_dir() else str(file)
                for file in rawres
            ]
        rawres = (
            file if not is_p_exp else Path(raw_p.parent, file.name)
            for file in p.parent.iterdir()
            if (
                (has_suffix(file, suffixes) or file.is_dir())
                and p.name in file.name
                and not str(file.name).startswith(".") ^ is_hidden
            )
        )
        return [
            str(file) + os.sep if file.expanduser().is_dir() else str(file)
            for file in rawres
        ]

    return file_complete
