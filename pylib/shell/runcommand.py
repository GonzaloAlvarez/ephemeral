#!/usr/bin/env python
import os, sys
import subprocess

def run_command(*popenargs, **kwargs):
    if "check_output" in dir(subprocess):
        return subprocess.check_output(*popenargs, **kwargs)
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

