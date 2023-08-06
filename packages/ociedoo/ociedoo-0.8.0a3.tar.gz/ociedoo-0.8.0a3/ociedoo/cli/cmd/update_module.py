# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command: update-module"""

import datetime
import os
import signal
import subprocess
import time
from pathlib import Path

import click

from ociedoo import complete, lib


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    short_help="Update odoo modules on databases.",
)
@click.argument("modules", autocompletion=complete.modules_complete_list)
@click.argument("odoo_args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "databases",
    "--dbname",
    "-d",
    autocompletion=complete.databases_complete_list,
    metavar="DBNAMES",
    help="""names of the database to update.
    [Default: databases where MODULES are installed].""",
)
@click.option(
    "restart_mode",
    "--restart-before",
    "--ninja",
    flag_value="restart-before",
    help="Restart Odoo daemon before performing updates.",
)
@click.option(
    "restart_mode",
    "--no-restart",
    flag_value="no-restart",
    help="Do not restart Odoo daemon for performing updates.",
)
@click.option(
    "restart_mode",
    "--stop-before-start-after",
    flag_value="stop-odoo",
    help="Stop Odoo before performing updates and restart it after.",
)
@click.option("-y", "--yes", is_flag=True, help="Answer yes to questions.")
@click.pass_context
def update_module(ctx, modules, odoo_args, databases, restart_mode, yes):
    """
    Update MODULES on each database where at least one of MODULES are
    installed.

    Odoo is run with some default options in order to update MODULES.

    Several databases are updated simultaneously.

    When running Odoo, the defaults options are:

        - write log in a new file (one for each database)

        - stop after init

        - multithread mode (workers = 0)

        - No cron threads (max-cron-threads = 0)

    More options can be given to Odoo via ODOO_ARGS.

    MODULES can contain 'all' to update all modules or a coma separated
    list of modules name. MODULES list cannot contain spaces.

    DBNAMES can contain 'all' to update all databases or a list of
    database name separated by a coma and without spaces. 'all' refers
    to all databases that belongs to the user defined in the
    `database_user` field in the configuration file. Only databases that
    belongs to this user can be used, others will be ignored.

    ODOO_ARGS standard options that the Odoo binary accepts. For example
    it is useful to supply debug option when something goes wrong.
    """
    profile = ctx.obj["profile"]
    db_user = profile.get("database-user")
    odoo_daemon_name = profile.get("daemon-name")
    logdir = Path(profile.get("odoo-log-dir")).expanduser()
    update_options = ["-u", modules, "--stop-after-init"]

    version = lib.get_bin_odoo_version(profile)
    if version > 10:
        update_options.append("--no-http")
    else:
        update_options.append("--no-xmlrpc")

    if databases:
        if databases.strip() == "all":
            dbs = lib.get_all_db(db_user)
        else:
            arg_dbs = [db.strip() for db in databases.split(",")]
            dbs = [db for db in lib.get_all_db(db_user) if db in arg_dbs]
            ignored_dbs = set(arg_dbs) - set(dbs)
            for db in ignored_dbs:
                click.echo(
                    "Warning: Ignore '%s' because it is not a database that "
                    "belongs to %s." % (db, db_user)
                )
    else:
        alldbs = lib.get_all_db(db_user)
        args_modules = {mod.strip() for mod in modules.split(",")}
        dbs = []
        for db in alldbs:
            installed_modules = set(lib.get_installed_modules(db))
            if args_modules & installed_modules:
                dbs.append(db)
        click.echo(
            "Info: The following databases will be updated: %s" % ",".join(dbs)
        )

    if restart_mode == "restart-before":
        question = (
            "%s will be restarted. Do you want to continue ?"
            % odoo_daemon_name
        )
        if yes or click.confirm(question):
            # Restart odoo daemon
            if lib.is_daemon_running(odoo_daemon_name) and not lib.stop_daemon(
                odoo_daemon_name
            ):
                ctx.fail(
                    "Fail to stop %s daemon. To do so try: sudo "
                    "systemctl stop %s" % (odoo_daemon_name, odoo_daemon_name)
                )
            if not lib.start_daemon(odoo_daemon_name):
                ctx.fail(
                    "Fail to start %s daemon. To do so try: sudo "
                    "systemctl start %s" % (odoo_daemon_name, odoo_daemon_name)
                )
    elif restart_mode == "stop-odoo":
        # Stop odoo daemon
        if lib.is_daemon_running(odoo_daemon_name):
            question = (
                "%s is running do you want to stop it ?" % odoo_daemon_name
            )
            if yes or click.confirm(question):
                if not lib.stop_daemon(odoo_daemon_name):
                    ctx.fail(
                        "Fail to stop %s daemon. To do so try: sudo "
                        "systemctl stop %s"
                        % (odoo_daemon_name, odoo_daemon_name)
                    )
            else:
                click.echo(
                    "%s is running. Cannot perform updates." % odoo_daemon_name
                )
                ctx.abort()

    processes = []
    for db in dbs:
        processes.append(
            {
                "db": db,
                "fun": lib.run_odoo,
                "kwargs": {
                    "profile": profile,
                    "database": db,
                    "logfile": (
                        logdir
                        / "update-{}-{}.log".format(
                            db,
                            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"),
                        )
                    ),
                    "other_args": update_options + list(odoo_args),
                    "stdout": subprocess.DEVNULL,
                    "stderr": subprocess.DEVNULL,
                    "stdin": subprocess.DEVNULL,
                },
                "proc": None,
            }
        )

    def all_proc_done(processes):
        """Return True if all processes are done."""
        all_proc_done = True
        for process in processes:
            if process["proc"] is None or process["proc"].poll() is None:
                all_proc_done = False
                break
        return all_proc_done

    def all_proc_success(processes):
        """Return True if all processes are done and success."""
        all_proc_success = True
        for process in processes:
            if (
                process["proc"] is None
                or process["proc"].poll() is None
                or process["proc"].poll()
            ):
                all_proc_success = False
                break
        return all_proc_success

    def prune_failed_proc(processes):
        """Delete failed processes as there where not executed."""
        for process in processes:
            if process["proc"].returncode:
                process["proc"] = None

    def count_running_proc(processes):
        """Return the number of running processes."""
        nb_running_proc = 0
        for process in processes:
            if process["proc"] is not None and process["proc"].poll() is None:
                nb_running_proc += 1
        return nb_running_proc

    def proc_status(processes):
        """Return a list of string representation of proc status."""
        status = []
        for process in processes:
            state = " "
            if process["proc"] is not None:
                if process["proc"].poll() is None:
                    state = "."
                elif process["proc"].poll():
                    state = "x"
                else:
                    state = "v"
            status.append("[{}] {}".format(state, process["db"]))
        return status

    max_proc = os.cpu_count() if os.cpu_count() else 1
    try:
        while not all_proc_success(processes):
            if count_running_proc(processes) < max_proc:
                if all_proc_done(processes):
                    click.echo()
                    if yes or click.confirm(
                        "There is failed jobs. Do you want to try again ?"
                    ):
                        prune_failed_proc(processes)
                    else:
                        break
                # Launch next proc
                for process in processes:
                    if process["proc"] is None:
                        process["proc"] = process["fun"](**process["kwargs"])
                        break
            # Show status on stdout
            click.echo("\r" + ", ".join(proc_status(processes)), nl=False)
            time.sleep(0.1)
        click.echo("\r" + ", ".join(proc_status(processes)), nl=False)
    except KeyboardInterrupt:
        click.echo()
        click.echo("CTRL-C: program will terminate properly.", err=True)
        try:
            for process in processes:
                if (
                    process["proc"] is not None
                    and process["proc"].poll() is None
                ):
                    process["proc"].send_signal(signal.SIGINT)
                    process["proc"].wait()
        except KeyboardInterrupt:
            click.echo("CTRL-C: program will exit now.", err=True)
            for process in processes:
                if (
                    process["proc"] is not None
                    and process["proc"].poll() is None
                ):
                    process["proc"].kill()
            ctx.exit(101)
        ctx.exit(100)
    click.echo()
    if not all_proc_success(processes):
        ctx.fail(
            "Errors when updatating the following databases: {}".format(
                ",".join(
                    process["db"]
                    for process in processes
                    if process["proc"].returncode
                )
            )
        )

    if restart_mode == "stop-odoo":
        # Start odoo daemon
        if not lib.is_daemon_running(odoo_daemon_name):
            question = (
                "%s is not running do you want to start it ?"
                % odoo_daemon_name
            )
            if yes or click.confirm(question):
                if not lib.start_daemon(odoo_daemon_name):
                    ctx.fail(
                        "Fail to start %s daemon. To do so try: sudo "
                        "systemctl start %s"
                        % (odoo_daemon_name, odoo_daemon_name)
                    )
