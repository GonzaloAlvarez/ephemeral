#!/usr/bin/env python
import os
import sys
import shlex
import shutil
import logging
import signal
import subprocess
import termios
import fcntl
import struct

from pylib import pexpect

try:
    from CStringIO import StringIO 
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import BytesIO as StringIO

# Include `unicode` in STR_TYPES for Python 2.X
try:
    STR_TYPES = (str, unicode)
except NameError:
    STR_TYPES = (str,)

def sigwinch_passthrough(sig, data):
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912 # assume
    s = struct.pack ("HHHH", 0, 0, 0, 0)
    a = struct.unpack ('HHHH', fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ , s))
    global global_pexpect_instance
    global_pexpect_instance.setwinsize(a[0],a[1])

class CommandExecutionMode():
    SUBPROCESS = 1
    PEXPECT = 2
    SYSTEM = 3

def run_subprocess(command, env):
    popen_kwargs = {"env": env}
    popen_kwargs["stdout"] = subprocess.PIPE
    popen_kwargs["stderr"] = subprocess.STDOUT
    popen_kwargs["close_fds"] = False
    if isinstance(command, STR_TYPES):
        command = shlex.split(command)
    process = subprocess.Popen(command, **popen_kwargs)
    process_output = ""
    with process.stdout as output:
        for line in iter(output.readline, b''):
            logging.debug("> {}".format(line))
            process_output += "{}\n".format(line)
    process.wait()
    return process_output

def run_pexpect(command, env):
    _original_signal = signal.getsignal(signal.SIGWINCH)
    try:
        pexpect_kwargs = {"env": env}
        columns, lines = shutil.get_terminal_size()
        logging.debug("columns {} lines {}".format(columns, lines))
        process_output = StringIO()
        pexpect_kwargs["logfile"] = process_output
        child = pexpect.spawn(command, **pexpect_kwargs)
        global global_pexpect_instance
        global_pexpect_instance = child
        signal.signal(signal.SIGWINCH, sigwinch_passthrough)
        child.interact(chr(29))
        return process_output.getvalue().decode('UTF-8')
    finally:
        signal.signal(signal.SIGWINCH, _original_signal)

def run_system(command, env):
    _environ = os.environ.copy()
    try:
        os.environ.clear()
        os.environ.update(env)
        os.system(command)
    finally:
        os.environ.clear()
        os.environ.update(_environ)

class CommandExecutionMode():
    SUBPROCESS = {"func": run_subprocess, "name": "subprocess"}
    PEXPECT = {"func": run_pexpect, "name": "pexpect"}
    SYSTEM = {"func": run_system, "name": "system"}

def run(command, mode=CommandExecutionMode.PEXPECT):
    env = os.environ.copy()
    if "__PYVENV_LAUNCHER__" in env:
        del env["__PYVENV_LAUNCHER__"]
    env["PYTHONUNBUFFERED"] = "1"
    env["TERM"] = "screen-256color"

    logging.info('Executing [{}] as {} call'.format(command, mode["name"]))
    return mode["func"](command, env)

def self_relaunch(py_interpreter):
    os.execl(py_interpreter, py_interpreter, *sys.argv)

