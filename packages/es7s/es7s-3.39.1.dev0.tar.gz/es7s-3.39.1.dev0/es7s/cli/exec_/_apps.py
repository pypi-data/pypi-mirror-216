# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import os.path

from es7s.shared.config import get_app_config_yaml
from .._base_opts_params import EpilogPart, CommandAttribute
from .._decorators import cli_pass_context, _catch_and_log_and_exit, cli_command
from .._invoker import AutoInvoker
from es7s.shared.path import USER_ES7S_BIN_DIR


class AppCommand:
    """
    Launch the external/intergrated component. PASSARGS are the arguments that
    will be passed to an external app. Long options can also be used, but make
    sure to prepend the "transit" options with "--" to help `click` library to
    distinguish them from its own options. Short options are known to be buggy,
    better just avoid using them on indirect invocations of standalone apps.
    """


EPILOG_PARTS = [
    EpilogPart(
        "This first command will result in 'es7s' command help text, along with embedded help from "
        "the external component, while the second will result in 'watson's direct call and only its "
        "own usage being displayed:",
        title="Invocation (generic):",
        group="ex1",
    ),
    EpilogPart("  (1) 'es7s exec watson --help'", group="ex1"),
    EpilogPart("  (2) 'es7s exec watson -- --help'", group="ex1"),
    EpilogPart("Another way to invoke an external component is to call it directly:", group="ex2"),
    EpilogPart("  (3) 'watson --help'", group="ex2"),
]


def make_commands():
    for name, data in get_app_config_yaml("apps").items():
        is_integrated = os.path.exists(os.path.join(USER_ES7S_BIN_DIR, name))
        invoker = AutoInvoker(name)
        cmd = lambda ctx, inv=invoker: inv.spawn(*ctx.args)
        cmd = _catch_and_log_and_exit(cmd)
        cmd = cli_pass_context(cmd)
        cmd = cli_command(
            name=name,
            type=CommandAttribute.get(data.get('type')),
            short_help=data.get('short-help'),
            help=AppCommand.__doc__,
            epilog=EPILOG_PARTS,
            ignore_unknown_options=True,
            allow_extra_args=True,
            ext_help_invoker=lambda ctx, inv=invoker: inv.get_help(),
            usage_section_name="Usage (generic)",
            include_common_options_epilog=False,
        )(cmd)
        yield cmd
