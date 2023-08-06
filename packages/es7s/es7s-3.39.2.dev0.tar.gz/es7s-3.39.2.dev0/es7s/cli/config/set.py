# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ._base import split_name
from .._decorators import _catch_and_log_and_exit, cli_argument, cli_command
from es7s.shared import get_stdout
from es7s.shared.config import rewrite_user_config_value


@cli_command(name=__file__, short_help="set config variable value")
@cli_argument("name")
@cli_argument("value")
@_catch_and_log_and_exit
class SetCommand:
    """
    Set config variable value. NAME should be in format
    "<<SECTION>>.<<OPTION>>".
    """

    def __init__(self, name: str, value: str):
        self._run(name, value)

    def _run(self, name: str, value: str):
        section, option = split_name(name)
        rewrite_user_config_value(section, option, value)
        get_stdout().echo("Done")
