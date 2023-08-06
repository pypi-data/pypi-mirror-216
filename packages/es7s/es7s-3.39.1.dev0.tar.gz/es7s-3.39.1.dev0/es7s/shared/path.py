# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os.path
import tempfile

SHELL_PATH = '/bin/bash'
LS_PATH = '/bin/ls'
ENV_PATH = '/bin/env'
GIT_PATH = '/usr/bin/git'
WMCTRL_PATH = '/bin/wmctrl'
DOCKER_PATH = "/bin/docker"
TMUX_PATH = "/usr/local/bin/tmux"
GH_LINGUIST_PATH = "/usr/local/bin/github-linguist"

RESOURCE_DIR = 'data'
GIT_LSTAT_DIR = 'lstat-cache'

USER_ES7S_BIN_DIR = os.path.expanduser("~/.es7s/bin")
USER_ES7S_DATA_DIR = os.path.expanduser("~/.es7s/data")
USER_XBINDKEYS_RC_FILE = os.path.expanduser("~/.xbindkeysrc")

SHELL_COMMONS_FILE = "es7s-shell-commons.sh"

ESQDB_DATA_PIPE = os.path.join(tempfile.gettempdir(), 'es7s-esqdb-pipe')
