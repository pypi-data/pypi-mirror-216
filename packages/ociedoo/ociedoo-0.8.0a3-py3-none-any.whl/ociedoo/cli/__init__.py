# SPDX-FileCopyrightText: 2018 Coop IT Easy SC <https://coopiteasy.be>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""CLI commands"""

from ociedoo.cli.cmd.configuration import configuration
from ociedoo.cli.cmd.copy_db import copy_db
from ociedoo.cli.cmd.drop_db import drop_db
from ociedoo.cli.cmd.list_db import list_db
from ociedoo.cli.cmd.list_module import list_module
from ociedoo.cli.cmd.main import main
from ociedoo.cli.cmd.odooctl import start_odoo, status_odoo, stop_odoo
from ociedoo.cli.cmd.rename_db import rename_db
from ociedoo.cli.cmd.restore_db import restore_db
from ociedoo.cli.cmd.run import run
from ociedoo.cli.cmd.set_password import set_password
from ociedoo.cli.cmd.update_module import update_module

main.add_command(configuration)
main.add_command(copy_db)
main.add_command(drop_db)
main.add_command(list_db)
main.add_command(list_module)
main.add_command(start_odoo)
main.add_command(status_odoo)
main.add_command(stop_odoo)
main.add_command(rename_db)
main.add_command(restore_db)
main.add_command(run)
main.add_command(set_password)
main.add_command(update_module)
