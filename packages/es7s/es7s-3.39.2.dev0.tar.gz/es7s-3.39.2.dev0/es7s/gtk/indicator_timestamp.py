# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import time

import pytermor as pt

from ._base import _BaseIndicator, _BoolState, CheckMenuItemConfig
from es7s.shared import SocketMessage, get_config
from es7s.shared.dto import TimestampInfo


class IndicatorTimestamp(_BaseIndicator[TimestampInfo]):
    """
    ╭──────────╮                         ╭────────────╮
    │ Δ │ PAST │                         │ ∇ │ FUTURE │
    ╰──────────╯                         ╰────────────╯
             -1h  -30min   ṇọẉ   +30min  +1h
         ▁▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁
       ⠄⠢⠲░░░░│▁│░░░░│▃│░░░░│█│░░░░│▀│░░░░│▔│░⣊⠈⣁⢉⠠⠂⠄
          ▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔
             ← 0%   +50%   +100%    |      |
                           -100%  -50%    -0% →
    """

    def __init__(self):
        self.config_section = "indicator.timestamp"
        self._formatter = pt.dual_registry.get_by_max_len(6)
        self._formatter._allow_fractional = False  # @FIXME (?) copied from monitor

        self._show_value = _BoolState(config_var=(self.config_section, "label-value"))

        super().__init__(
            "timestamp",
            icon_subpath="delta",
            icon_name_default="default.png",
            icon_path_dynamic_tpl="%s.png",
            title="Time delta",
        )

    def _init_state(self):
        super()._init_state()
        self._state_map.update(
            {
                CheckMenuItemConfig("Show numeric value", separator_before=True): self._show_value,
            }
        )

    def _render(self, msg: SocketMessage[TimestampInfo]):
        now = time.time()
        if (remote := msg.data.ts) is None:
            self._render_result("N/A", "N/A", True, self._get_icon("nodata", msg.network_comm))
            return

        icon_subtype = self._get_icon_subtype(now, remote)
        icon = self._get_icon(icon_subtype, msg.network_comm)

        delta_str = ""
        if self._show_value:
            delta_str = self._formatter.format(now - remote)
            if get_config().get_indicator_debug_mode():
                delta_str += '|'+icon

        self._render_result(delta_str, delta_str, False, icon=icon)

    # noinspection PyMethodMayBeStatic
    def _get_icon_subtype(self, now: float, remote: int) -> str:
        prefix = "" if now > remote else "-"
        adiff = abs(now - remote)
        if adiff < 300:  # @TODO to config
            return "5m"
        if adiff < 3600:
            return f"{prefix}1h"
        if adiff < 3 * 3600:
            return f"{prefix}3h"
        if now < remote:
            return "future"
        return "default"

    def _get_icon(self, icon_subtype: str, network_comm: bool = None) -> str:
        return self._icon_path_dynamic_tpl % (icon_subtype + ("-nc" if network_comm else ""))
