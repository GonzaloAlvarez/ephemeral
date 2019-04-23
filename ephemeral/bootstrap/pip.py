# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pkg_resources
from ephemeral import shell
from ephemeral.shell import cout

def pip_install(context, package, extra_args = None):
    try:
        pkg = pkg_resources.get_distribution(package)
    except:
        cout('Installing dependency [{}]'.format(package))
        if context.vars.config and package + '.source' in context.vars.config.__dict__:
            package_source = context.vars.config.__dict__[package + '.source']
            cout('Installing the package from [{}]'.format(package_source))
            run_attributes = [context.config.pip_path, 'install', '-I', '--verbose', '-e', package_source]
            #run_attributes = [context.config.pip_path, 'install', '-I', '--verbose', package, '--no-index', '--find-links', package_source]
        else:
            run_attributes = [context.config.pip_path, 'install', '-I', '--verbose', package]
        if extra_args:
            run_attributes = run_attributes + extra_args.split(' ')
        shell.brun(' '.join(run_attributes))

