# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from importlib import resources

import os
from os.path import expanduser
from es7s import data
from es7s import APP_NAME
from es7s.shared import format_attrs, get_color, get_config, get_logger, run_subprocess
from es7s.shared.exception import SubprocessExitCodeError
from es7s.shared.path import SHELL_COMMONS_FILE, SHELL_PATH, USER_ES7S_BIN_DIR


class _Invoker:
    def __init__(self, target: str):
        self._target = target

    def spawn(self, *args: str) -> None:
        cmd_target, cmd_args = self._get_spawn_cmd(*args)
        get_logger().info(f"Launching: {cmd_target} {format_attrs(cmd_args)}")
        code = os.spawnvpe(os.P_WAIT, cmd_target, cmd_args, self._build_env())
        #if code == 127:
        #    raise ExecutableNotFoundError(self._target)
        if code != 0:
            raise SubprocessExitCodeError(code, args)

    def _get_spawn_cmd(self, *args: str) -> tuple[str, list]:
        return self._target, [self._target, *args]

    def get_help(self) -> str:
        cmd_target, cmd_args, cmd_shell = self._get_help_cmd()
        cp = run_subprocess(
            " ".join(cmd_args),
            executable=cmd_target,
            shell=cmd_shell,
            env=self._build_env(),
            timeout=10,
        )
        if cp.stderr:
            get_logger().non_fatal_exception(cp.stderr)
        return cp.stdout

    def _get_help_cmd(self) -> tuple[str, list, bool]:
        return SHELL_PATH, [self._target, "--help"], True

    def _build_env(self) -> dict:
        logger = get_logger()
        commons_path = resources.path(data, SHELL_COMMONS_FILE)
        user_repos_path = get_config().get("general", "user-repos-path", fallback="")
        theme_seq = get_color().get_theme_color().to_sgr()
        result = {
            # ---[@temp]--- filter out all G1/G2 es7s env vars:
            **{k: v for (k, v) in os.environ.items() if not k.lower().startswith("es7s")},
            # ---[@temp]---
            "PATH": self._build_path(),
            #"COLORTERM": os.environ.get("COLORTERM"),
            #"TERM": os.environ.get("TERM"),
            "ES7S_SHELL_COMMONS": commons_path,
            "ES7S_USER_REPOS_PATH": user_repos_path,
            "ES7S_THEME_COLOR_SGR": ";".join(map(str, theme_seq.params)),
        }
        logger.debug("Setting up the environment")
        for k, v in sorted(result.items(), key=lambda k: k):
            logger.trace(format_attrs(v), k, out_plain=False, out_sanitized=True)
        return result

    def _build_path(self) -> str:
        current = os.environ.get("PATH", "").split(":")
        filtered = ":".join(
            [
                # ---[@temp]----- remove all deprecated es7s parts from PATH:
                *filter(lambda s: "es7s" not in s, current),
                expanduser("~/bin/es7s"),
                # ---[@temp]----- ^ restore legacy path
                USER_ES7S_BIN_DIR,  # add G3 path
            ]
        )
        return filtered


class AutoInvoker(_Invoker):
    pass


class ShellInvoker(_Invoker):
    pass
