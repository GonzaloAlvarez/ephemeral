# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import importlib
from ephemeral import bootstrap

def setup_internal(context, package):
    setup_method = importlib.import_module('packages.' + package).setup
    setup_method(context)

def setup(context):
    bootstrap.python_bootstrap(context)
    bootstrap.context_bootstrap(context)
    if context.session.cli.package:
        setup_method = importlib.import_module('packages.' + context.session.cli.package).setup
        setup_method(context)
