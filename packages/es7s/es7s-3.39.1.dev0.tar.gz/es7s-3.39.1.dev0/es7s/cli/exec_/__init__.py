# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import click

from . import (
    _apps,
    edit_image,
    get_socket,
    hilight_num,
    ls,
    lingvini,
    notify,
    pgreks,
    sun,
    switch_wspace,
    wrap,
    geoip,
    esqdb,
)
from .._decorators import _catch_and_log_and_exit, cli_group, cli_pass_context


@cli_group(__file__, short_help="run an embed or external component")
@cli_pass_context
@_catch_and_log_and_exit
def group(ctx: click.Context, **kwargs):
    """
    Commands that invoke one of es7s subsystems that has been made available
    for standalone manual launching via CLI.
    """


group.add_commands(
    get_socket.GetSocketCommand,
    hilight_num.HighlightNumbersCommand,
    edit_image.EditImageCommand,
    ls.ListDirCommand,
    notify.NotifyCommand,
    sun.SunCommand,
    switch_wspace.SwitchWorkspaceCommand,
    wrap.WrapCommand,
    *_apps.make_commands(),  # @TODO можно выпилить yaml для ускорения загрузки
    pgreks.PgreksCommand,
    geoip.ResolveGeoCommand,
    esqdb.EscSeqDebuggerCommand,
    lingvini.LangBreakdownCommand,
)
