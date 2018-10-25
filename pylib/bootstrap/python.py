#!/usr/bin/env python
import __main__
import os
import sys
import json
from pylib import shell
from pylib import github

def gather_python_info(*executables):
    # https://stackoverflow.com/a/13240524
    eph_path = os.path.realpath(__main__.__file__)
    py_results = []
    for executable in executables:
        json_out = shell.run_command([executable, eph_path, 'pyinfo'])
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

def pip_install(context, package):
    shell.run_command([context.config.pip_path, 'install', package])

def init_python(context):
    virtualenv_zipball = github.download_latest('pypa', 'virtualenv')
    virtualenv_path = os.path.join(context.epherstore.get_store_path(), 'venv')
    shell.unpack_zipball(virtualenv_zipball, context.epherstore.get_store_path())
    virtualenv_py_path = shell.find_file(context.epherstore.get_store_path(), "virtualenv.py")
    shell.run_command([context.config.system_python, virtualenv_py_path, '-q', context.epherstore.get_store_path()])
    context.config.python_path = os.path.realpath(os.path.join(context.epherstore.get_store_path(), 'bin', 'python'))
    context.config.pip_path = os.path.realpath(os.path.join(context.epherstore.get_store_path(), 'bin', 'pip'))
    pip_install(context, 'ruamel.yaml')
    pip_install(context, 'ruamel.yaml[jinja2]')
    pip_install(context, 'jinja2')

def init_virtualenv(context):
    if not hasattr(sys, 'real_prefix'):
        if not 'python_path' in context.config.__dict__:
            if sys.executable != context.config.system_python:
                best_sys_python = get_best_python()
                context.config.system_python = best_sys_python
                if sys.executable != best_sys_python:
                    shell.self_relaunch(best_sys_python) # Relaunch with a 'hopefully' better python

            init_python(context)

        shell.self_relaunch(context.config.python_path) # Relaunch within VirtualEnv
    elif not context.config.python_lib:
        python_lib_options = [k for k in sys.path if context.epherstore.get_store_path() in k and 'site-packages' in k]
        context.config.python_lib = [k for k in sys.path if context.epherstore.get_store_path() in k and 'site-packages' in k][0]

