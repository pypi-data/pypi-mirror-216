# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t
import pytermor as pt

from ._base import CheckMenuItemConfig, _BaseIndicator, _BoolState, _State
from es7s.shared import SocketMessage
from es7s.shared.dto import NetworkUsageInfo, NetworkUsageInfoStats


class IndicatorNetworkUsage(_BaseIndicator[NetworkUsageInfo]):
    def __init__(self):
        self.config_section = "indicator.network-usage"

        self._show_rate = _BoolState(config_var=(self.config_section, "label"))

        super().__init__(
            "network-usage",
            "network-usage",
            icon_subpath='network-usage',
            icon_name_default="off.svg",
            icon_path_dynamic_tpl="%s-%s.svg",
            title="Network usage",
        )
        self._formatter = pt.StaticFormatter(
            pt.formatter_bytes_human,
            max_value_len=4,
            auto_color=False,
            allow_negative=False,
            allow_fractional=True,
            discrete_input=False,
            unit="",
            unit_separator="",
            pad=True,
        )

    def _init_state(self, state_map: t.Mapping[CheckMenuItemConfig, _State] = None):
        super()._init_state()
        self._state_map.update(
            {
                CheckMenuItemConfig("Show rate ([kM]bit/s)", separator_before=True): self._show_rate,
            }
        )

    def _render(self, msg: SocketMessage[NetworkUsageInfo]):
        if not msg.data.isup:
            self._render_result(
                "N/A",
                "N/A",
                icon=self._icon_name_default,
            )
            return

        frames, bpss = [], []
        for dto in (msg.data.sent, msg.data.recv):
            if not dto:
                frames.append('0')
                bpss.append(None)
                continue
            frames.append(self._get_icon_frame(dto))
            bpss.append(dto.bps)

        icon = self._icon_path_dynamic_tpl % (*frames,)
        self._render_result(
            self._format_result(*bpss),
            self._format_result(*bpss),
            icon=icon
        )

    def _get_icon_frame(self, dto: NetworkUsageInfoStats) -> str:
        if dto.errors:
            return 'e'
        if dto.drops:
            return 'w'
        if dto.ratio:
            if dto.ratio > 0.4:
                return '4'
            if dto.ratio > 0.2:
                return '3'
            if dto.ratio > 0.1:
                return '2'
            if dto.ratio > 0.01:
                return '1'
        return '0'

    def _format_result(self, *bps_values: float|None) -> str:
        if not self._show_rate:
            return ''
        if not any(bps_values):
            return "  0k"
        val = max(bps_values)
        if val < 1000:
            return " <1k"
        return self._formatter.format(val)
