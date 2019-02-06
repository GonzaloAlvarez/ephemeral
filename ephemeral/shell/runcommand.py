# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import sys
import shlex
import logging
import subprocess

# Include `unicode` in STR_TYPES for Python 2.X
try:
    STR_TYPES = (str, unicode)
except NameError:
    STR_TYPES = (str,)

ENV_DEFAULTS = {
    "PYTHONUNBUFFERED": "1",
    "TERM": "screen-256color",
    "LC_ALL": "en_US.UTF-8",
    "LANG": "en_US.UTF-8"
}

def brun(command, _env={}):
    env = os.environ.copy()
    env.update(_env)
    env.update(ENV_DEFAULTS)
    if "__PYVENV_LAUNCHER__" in env:
        del env["__PYVENV_LAUNCHER__"]
    popen_kwargs = {"env": env}
    popen_kwargs["stdout"] = subprocess.PIPE
    popen_kwargs["stderr"] = subprocess.PIPE
    popen_kwargs["close_fds"] = False
    if isinstance(command, STR_TYPES):
        command = shlex.split(command)

    logging.info('Executing [{}] in the background'.format(command))

    process = subprocess.Popen(command, **popen_kwargs)
    process_stdout, process_stderr = process.communicate()
    logging.debug('STDOUT: [{}]'.format(process_stdout))
    logging.debug('STDERR: [{}]'.format(process_stderr))
    return process_stdout, process_stderr, int(process.returncode)

def run(command, _env={}):
    _environ = os.environ.copy()
    try:
        os.environ.clear()
        os.environ.update(_env)
        os.environ.update(ENV_DEFAULTS)

        logging.info('Executing [{}] in the foreground'.format(command))
        cmd = os.system(command)
        return None, None, os.WEXITSTATUS(cmd)
    finally:
        os.environ.clear()
        os.environ.update(_environ)
