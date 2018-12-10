#!/usr/bin/env python
from __future__ import print_function
import __main__
import os
import sys
import json
import logging
import pkg_resources
from pylib.clint.textui import puts
from pylib import shell
from pylib import github

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace

def gather_python_info(*executables):
    # https://stackoverflow.com/a/13240524
    eph_path = os.path.realpath(__main__.__file__)
    py_results = []
    for executable in executables:
        json_out = shell.run(' '.join([executable, eph_path, 'pyinfo']), mode=shell.CommandExecutionMode.SUBPROCESS)
        py_info_obj = json.loads(json_out)
        py_results.append(py_info_obj)
    return py_results

def pick_python(py_versions):
    py_filtered_versions = list(filter(lambda py_version: 'TLSv1_2' in py_version['ssl_protocols'], py_versions))
    py_sorted_versions = sorted(py_filtered_versions, key=lambda py_version: py_version['version_major'], reverse=True)
    if len(py_sorted_versions) > 0:
        return py_sorted_versions[0]
    return None

def get_best_python():
    python_execs = shell.which(*['python', 'python2', 'python2.7', 'python3', 'python3.7'])
    py_versions = gather_python_info(*python_execs)
    py_chosen = pick_python(py_versions)
    if py_chosen != None:
        return py_chosen['executable']
    return None

def pip_install(context, package, extra_args = None):
    try:
        pkg = pkg_resources.get_distribution(package)
    except:
        puts('Installing dependency [{}]'.format(package))
        run_attributes = [context.config.pip_path, 'install', '-I', '--verbose', package]
        if extra_args:
            run_attributes = run_attributes + extra_args.split(' ')
        shell.run(' '.join(run_attributes), mode=shell.CommandExecutionMode.SUBPROCESS)

def init_python(context):
    virtualenv_zipball = github.download_latest('pypa', 'virtualenv')
    virtualenv_path = os.path.join(context.epherstore.get_store_path(), 'venv')
    shell.unpack_zipball(virtualenv_zipball, context.epherstore.get_store_path())
    virtualenv_py_path = shell.find_file(context.epherstore.get_store_path(), "virtualenv.py")
    shell.run([context.config.system_python, virtualenv_py_path, '-q', '--no-site-packages', context.epherstore.get_store_path()], mode=shell.CommandExecutionMode.SUBPROCESS)
    context.config.python_path = os.path.realpath(os.path.join(context.epherstore.get_store_path(), 'bin', 'python'))
    context.config.pip_path = os.path.realpath(os.path.join(context.epherstore.get_store_path(), 'bin', 'pip'))

def init_virtualenv(context):
    if not hasattr(sys, 'real_prefix'):
        logging.debug('Outside of virtualenv')
        if not 'python_path' in context.config.__dict__:
            logging.debug('Unknown python exectuable')
            if sys.executable != context.config.system_python:
                logging.debug('Discovering python version')
                best_sys_python = get_best_python()
                logging.debug('Python version [{}]'.format(best_sys_python))
                context.config.system_python = best_sys_python
                if sys.executable != best_sys_python:
                    logging.debug('Relaunching with new python')
                    shell.self_relaunch(best_sys_python) # Relaunch with a 'hopefully' better python

            puts('Initializing virtual environment')
            init_python(context)

        logging.debug('Relaunching inside virtualenv')
        shell.self_relaunch(context.config.python_path) # Relaunch within VirtualEnv
    elif not context.config.python_lib:
        python_lib_options = [k for k in sys.path if context.epherstore.get_store_path() in k and 'site-packages' in k]
        context.config.python_lib = [k for k in sys.path if context.epherstore.get_store_path() in k and 'site-packages' in k][0]

def populate_context(context):
    context.vars = Namespace()
    context.vars.python = context.config.python_path
    context.vars.bin_path = os.path.realpath(os.path.join(context.epherstore.get_store_path(), 'bin'))
    context.vars.vargs = context.session.cli.args
    context.func = Namespace()
    context.func.pip_install = pip_install
    context.func.run = shell.run
    context.func.run_sys = lambda x: shell.run(x, shell.CommandExecutionMode.SYSTEM)
