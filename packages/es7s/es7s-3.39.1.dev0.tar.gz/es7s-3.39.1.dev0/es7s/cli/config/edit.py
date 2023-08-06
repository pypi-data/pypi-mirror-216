# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import os

from es7s.shared.sub import run_detached
from .._decorators import cli_command, _catch_and_log_and_exit
from es7s.shared import get_user_config_filepath, get_stdout, get_logger


@cli_command(name=__file__, short_help="open current user config in text editor")
@_catch_and_log_and_exit
class EditCommand:
    """
    Open current user config in text editor.\n\n

    Note that this command ignores the common option '--default'.
    """

    def __init__(self):
        self._run()

    def _run(self):
        logger = get_logger()

        user_config_filepath = get_user_config_filepath()
        editor = os.getenv("EDITOR", "xdg-open")
        logger.debug(f"Selected the editor executable: '{editor}'")

        run_detached([editor, user_config_filepath])
        get_stdout().echo("Done")
