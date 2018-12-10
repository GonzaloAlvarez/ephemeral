#!/usr/bin/env python

import importlib
from .setup import setup
from pylib import shell

def run(context):
    setup(context)
    if context.session.cli.package:
        run_method = importlib.import_module('packages.' + context.session.cli.package).run
        run_method(context)
