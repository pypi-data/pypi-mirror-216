# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import importlib.resources
import typing as t
from collections.abc import Iterator
from importlib.abc import Traversable
from pathlib import Path

from .path import RESOURCE_DIR
from .. import APP_NAME


def get_res_dir(subpath: str|Path = None) -> Traversable:
    path = Path(RESOURCE_DIR)
    if subpath:
        path /= Path(subpath)
    return importlib.resources.files(APP_NAME).joinpath(path)


class DemoHilightNumText:
    @classmethod
    def open(cls) -> t.TextIO:
        subpath = Path('demo', "demo-text.txt")
        return get_res_dir(subpath).open('rt')


class DemoGradients:
    @classmethod
    def iter(cls) -> Iterator[t.TextIO]:
        for file in get_res_dir('demo').iterdir():
            if file.name.startswith('demo-gradient'):
                yield file.open('rt')
