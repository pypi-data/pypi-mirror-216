################################################################################
# Copyright (C) 2023 Kostiantyn Klochko <kostya_klochko@ukr.net>               #
#                                                                              #
# This file is part of tui-rsync.                                              #
#                                                                              #
# tui-rsync is free software: you can redistribute it and/or modify it under   #
# uthe terms of the GNU General Public License as published by the Free        #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# tui-rsync is distributed in the hope that it will be useful, but WITHOUT ANY #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS    #
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more        #
# details.                                                                     #
#                                                                              #
# You should have received a copy of the GNU General Public License along with #
# tui-rsync. If not, see <https://www.gnu.org/licenses/>.                      #
################################################################################

from rich.console import Console
from rich.prompt import Prompt
from typing import List, Optional
import typer

from tui_rsync.models.models import Group, GroupSource
from tui_rsync.cli.groups.group_prompt import GroupPrompt

console = Console()
group_show = typer.Typer()

@group_show.command()
def one(
    group_label: str = typer.Option(
        None, "--group-label", "-l",
        help="[b]The label[/] is a uniq identification of a [b]group[/].",
        show_default=False
    ),
):
    """
    [green b]Show[/] an [yellow]existing group[/].
    """
    if group_label is None:
        console.print("What is the [yellow b]label of the group[/]? ")
        group_label = GroupPrompt.get_label_fzf()

    if not Group.is_exist(group_label):
        console.print("[red b][ERROR][/] Source does not exists!!!")
        return

    group = Group.get_group(group_label)

    console.print(group.show_format())

