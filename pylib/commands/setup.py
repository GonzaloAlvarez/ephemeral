#!/usr/bin/env python

import importlib
from pylib import bootstrap

def setup_internal(context, package):
    setup_method = importlib.import_module('packages.' + package).setup
    setup_method(context)

def setup(context):
    bootstrap.init_virtualenv(context)
    bootstrap.populate_context(context)
    if context.session.cli.package:
        setup_method = importlib.import_module('packages.' + context.session.cli.package).setup
        setup_method(context)
