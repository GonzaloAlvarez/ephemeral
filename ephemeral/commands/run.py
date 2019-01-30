# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import importlib
from .setup import setup

def run(context):
    setup(context)
    if context.session.cli.package:
        run_method = importlib.import_module('packages.' + context.session.cli.package).run
        run_method(context)
