# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import os
import shutil
import typing as t
from configparser import ConfigParser as BaseConfigParser
from contextlib import contextmanager
from dataclasses import dataclass
from importlib import resources
from os import makedirs, path
from os.path import dirname, isfile

from .log import get_logger
from .path import RESOURCE_DIR, USER_ES7S_DATA_DIR
from .. import APP_NAME, data

_merged_user_config: ConfigParser | None = None
_default_config: ConfigParser | None = None


@dataclass
class ConfigLoaderParams:
    default: bool = False


class ConfigParser(BaseConfigParser):
    def __init__(self, *args, **kwargs):
        self.cfg_loader_params = kwargs.pop("cfg_loader_params", None)
        super().__init__(*args, **kwargs)

        self._invalid: RuntimeError | None = None
        self._already_logged_options: t.Set[t.Tuple[str, str]] = set()
        self._logging_enabled = True

    def get(self, section: str, option: str, *args, **kwargs) -> t.Any:
        self.ensure_validity()
        log_msg = f"Getting config value: {section}.{option}"
        result = None
        try:
            result = super().get(section, option, *args, **kwargs)
        except Exception:
            raise
        finally:
            if self._logging_enabled:
                log_msg += f" = " + (
                    '"' + result.replace("\n", " ") + '"' if result else str(result)
                )
                get_logger().debug(log_msg)
        return result

    def getintlist(self, section: str, option: str, *args, **kwargs) -> list[int]:
        try:
            return [*map(int, filter(None, self.get(section, option).splitlines()))]
        except ValueError as e:
            raise RuntimeError(f"Conversion to [int] failed for: {section}.{option}") from e

    def get_monitor_debug_mode(self) -> bool:
        if (env_var := os.getenv("ES7S_MONITOR_DEBUG", None)) is not None:
            return True if env_var != "" else False
        return self.getboolean("monitor", "debug", fallback=False)

    def get_indicator_debug_mode(self) -> bool:
        if (env_var := os.getenv("ES7S_INDICATOR_DEBUG", None)) is not None:
            return True if env_var != "" else False
        return self.getboolean("indicator", "debug", fallback=False)

    def get_cli_debug_io_mode(self) -> bool:
        if (env_var := os.getenv("ES7S_CLI_DEBUG_IO", None)) is not None:
            return True if env_var != "" else False
        with self._disabled_logging():
            return self.getboolean("cli", "debug-io", fallback=False)

    def invalidate(self):
        self._invalid = True

    def ensure_validity(self):
        if self._invalid:
            raise RuntimeError(
                "Config can be outdated. Do not cache config instances (at most "
                "-- store as local variables in the scope of the single function), "
                "call get_config() to get the fresh one instead."
            )

    def set(self, section: str, option: str, value: str | None = ...) -> None:
        raise RuntimeError(
            "Do not call set() directly, use rewrite_user_value(). "
            "Setting config values directly can lead to writing default "
            "values into user's config even if they weren't there at "
            "the first place."
        )

    def _set(self, section: str, option: str, value: str | None = ...) -> None:
        self.ensure_validity()
        if self._logging_enabled:
            log_msg = f'Setting config value: {section}.{option} = "{value}"'
            get_logger().info(log_msg)

        super().set(section, option, value)

    @contextmanager
    def _disabled_logging(self, **kwargs):
        self._logging_enabled = False
        try:
            yield
        finally:
            self._logging_enabled = True


def get_app_config_yaml(name: str) -> dict | list:
    import yaml

    filename = f"{name}.yml"
    user_path = os.path.join(USER_ES7S_DATA_DIR, filename)

    if os.path.isfile(user_path):
        with open(user_path, "rt") as f:
            return yaml.safe_load(f.read())
    else:
        app_path = os.path.join(RESOURCE_DIR, filename)
        f = resources.open_text(data, app_path)
        return yaml.safe_load(f)


def get_default_config_filepath() -> str:
    filename = "es7s.conf.d"
    user_path = os.path.join(USER_ES7S_DATA_DIR, filename)

    if os.path.isfile(user_path):
        if os.path.islink(user_path):
            return os.readlink(user_path)
        return user_path
    else:
        dc_filepath = str(resources.path(APP_NAME, "es7s.conf.d"))
        get_logger(False).warning(
            f"Default config not found in user data dir, "
            f"loading from app data dir instead: '{dc_filepath}'"
        )
        return dc_filepath


def get_user_config_filepath() -> str:
    import click

    user_config_path = click.get_app_dir(APP_NAME)
    return path.join(user_config_path, f"{APP_NAME}.conf")


def get_config(require=True) -> ConfigParser | None:
    if not _merged_user_config:
        if require:
            raise RuntimeError("Config is uninitialized")
        return None
    return _merged_user_config


def get_default_config() -> ConfigParser | None:
    return _default_config


def init_config(cfg_params=ConfigLoaderParams()):
    global _default_config, _merged_user_config

    if _default_config:
        _default_config.invalidate()
    _default_config = ConfigParser(interpolation=None)
    _read_config(_default_config, get_default_config_filepath())

    user_config_filepath = get_user_config_filepath()
    if not isfile(user_config_filepath):
        reset_config(False)

    config_filepaths = [get_default_config_filepath()]
    if not cfg_params.default:
        config_filepaths += [user_config_filepath]

    if _merged_user_config:
        _merged_user_config.invalidate()
    _merged_user_config = ConfigParser(interpolation=None, cfg_loader_params=cfg_params)
    _read_config(_merged_user_config, *config_filepaths)


def _read_config(config: ConfigParser, *filepaths: str) -> None:
    read_ok = config.read(filepaths)
    get_logger().info("Reading configs files from: " + ", ".join(f'"{fp}"' for fp in filepaths))

    if len(read_ok) != len(filepaths):
        read_failed = set(filepaths) - set(read_ok)
        get_logger().warning("Failed to read config(s): " + ", ".join(read_failed))
    if len(read_ok) == 0:
        raise RuntimeError(f"Failed to initialize config")


def reset_config(backup: bool = True) -> str | None:
    """Return path to backup file, if any."""
    user_config_filepath = get_user_config_filepath()
    makedirs(dirname(user_config_filepath), exist_ok=True)
    get_logger().debug(f'Making default config in: "{user_config_filepath}"')

    user_backup_filepath = None
    if backup and os.path.exists(user_config_filepath):
        user_backup_filepath = user_config_filepath + ".bak"
        os.rename(user_config_filepath, user_backup_filepath)
        get_logger().info(f'Original file renamed to: "{user_backup_filepath}"')

    header = True
    with open(user_config_filepath, "wt") as user_cfg:
        with open(get_default_config_filepath(), "rt") as default_cfg:
            for idx, line in enumerate(default_cfg.readlines()):
                if header and line.startswith(("#", ";", "\n")):
                    continue  # remove default config header comments
                header = False

                if line.startswith(('#', "\n")):  # remove section separators
                    continue                      # and empty lines
                elif line.startswith("["):  # keep section definitions, and
                    if user_cfg.tell():     # prepend the first one with a newline
                        line = "\n" + line
                elif line.startswith("syntax-version"):  # keep syntax-version
                    pass
                elif line.startswith(";"):  # keep examples, triple-comment out to distinguish
                    line = "###" + line.removeprefix(';')
                else:  # keep default values as commented out examples
                    line = "# " + line

                user_cfg.write(line)
                get_logger().trace(line.strip(), f"{idx+1}| ")

    return user_backup_filepath


def rewrite_user_config_value(section: str, option: str, value: str | None) -> None:
    user_config_filepath = get_user_config_filepath()
    source_user_config = ConfigParser(interpolation=None)

    _read_config(source_user_config, user_config_filepath)
    if not source_user_config.has_section(section):
        source_user_config.add_section(section)
    source_user_config._set(section, option, value)  # noqa

    get_logger().debug(f'Writing config to: "{user_config_filepath}"')
    with open(user_config_filepath, "wt") as user_cfg:
        source_user_config.write(user_cfg)

    init_config(_merged_user_config.cfg_loader_params)
