#!/usr/bin/env python
from __future__ import (print_function)
__metaclass__ = type

import os
import select
import shlex
import subprocess
import sys

from pylib.util.six import PY2, PY3
from pylib.util.text import to_bytes


def run_cmd(context, cmd):

    readsize = 10

    # On python2, shlex needs byte strings
    if PY2:
        cmd = to_bytes(cmd, errors='surrogate_or_strict')
    cmdargs = shlex.split(cmd)

    # subprocess should be passed byte strings.  (on python2.6 it must be
    # passed byte strtings)
    cmdargs = [to_bytes(a, errors='surrogate_or_strict') for a in cmdargs]

    environment = []
    if hasattr(context.session, 'env'):
        environment = context.session.env

    p = subprocess.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment)

    stdout = b''
    stderr = b''
    rpipes = [p.stdout, p.stderr]
    while True:
        rfd, wfd, efd = select.select(rpipes, [], rpipes, 1)

        if p.stdout in rfd:
            dat = os.read(p.stdout.fileno(), readsize)
            if hasattr(context.session, 'verbose') and context.session.verbose:
                # On python3, stdout has a codec to go from text type to bytes
                if PY3:
                    sys.stdout.buffer.write(dat)
                else:
                    sys.stdout.write(dat)
            stdout += dat
            if dat == b'':
                rpipes.remove(p.stdout)
        if p.stderr in rfd:
            dat = os.read(p.stderr.fileno(), readsize)
            stderr += dat
            if hasattr(context.session, 'verbose') and context.session.verbose:
                # On python3, stdout has a codec to go from text type to bytes
                if PY3:
                    sys.stdout.buffer.write(dat)
                else:
                    sys.stdout.write(dat)
            if dat == b'':
                rpipes.remove(p.stderr)
        # only break out if we've emptied the pipes, or there is nothing to
        # read from and the process has finished.
        if (not rpipes or not rfd) and p.poll() is not None:
            break
        # Calling wait while there are still pipes to read can cause a lock
        elif not rpipes and p.poll() is None:
            p.wait()

    return p.returncode, stdout, stderr

def run_command(*popenargs, **kwargs):
    if "check_output" in dir(subprocess):
        try:
            out = subprocess.check_output(*popenargs, **kwargs)
            print(out)
            return out
        except Exception as e:
            print(e.output)
        return ""
    else:
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output

def self_relaunch(py_interpreter):
    os.execl(py_interpreter, py_interpreter, *sys.argv)

