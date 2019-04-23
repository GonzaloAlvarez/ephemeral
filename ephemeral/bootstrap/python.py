# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import sys
import logging
import pkg_resources

from ephemeral import (shell, github)
from ephemeral.shell import cout
from ephemeral.lang import NamedObject
from ephemeral.bootstrap import (versionpicker, virtenv, pip)

def python_bootstrap(context):
    store_path = context.epherstore.get_store_path()

    if not hasattr(sys, 'real_prefix'):
        logging.debug('Outside of virtualenv')
        if not 'python_path' in context.config.__dict__:
            logging.debug('Unknown python exectuable')
            if sys.executable != context.config.system_python:
                logging.debug('Discovering python version')
                best_sys_python = versionpicker.get_best_python()
                logging.debug('Python version [{}]'.format(best_sys_python))
                context.config.system_python = best_sys_python
                if sys.executable != best_sys_python:
                    logging.debug('Relaunching with new python')
                    shell.self_relaunch(best_sys_python) # Relaunch with a 'hopefully' better python

            cout('Initializing virtual environment')
            virtenv.install_virtualenv(store_path, context.config.system_python)
            context.config.python_path = os.path.realpath(os.path.join(store_path, 'bin', 'python'))
            context.config.pip_path = os.path.realpath(os.path.join(store_path, 'bin', 'pip'))

        logging.debug('Relaunching inside virtualenv')
        shell.self_relaunch(context.config.python_path) # Relaunch within VirtualEnv
    elif not context.config.python_lib:
        python_lib_options = [k for k in sys.path if store_path in k and 'site-packages' in k]
        context.config.python_lib = [k for k in sys.path if store_path in k and 'site-packages' in k][0]

def context_bootstrap(context):
    context.vars = NamedObject()
    context.vars.python = context.config.python_path
    context.vars.bin_path = os.path.realpath(os.path.join(context.epherstore.get_store_path(), 'bin'))
    context.vars.local_path = context.epherstore.get_store_path()
    context.vars.vargs = context.session.cli.args
    context.vars.config = context.config

    context.func = NamedObject()
    context.func.pip_install = pip.pip_install
    context.func.run_background = shell.brun
    context.func.run = shell.run
    context.func.puts = cout
    from ephemeral.commands import setup_internal
    context.func.pkg_install = setup_internal
