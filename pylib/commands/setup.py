#!/usr/bin/env python

from pylib import bootstrap
from pylib import shell
from pylib.epher import PackageManager

def setup(context):
    bootstrap.init_virtualenv(context)
    if context.session.cli.package:
        context.session.package_manager = PackageManager(context)

    if context.session.package_manager.get_dependencies():
        for package_dependency in context.session.package_manager.get_dependencies():
            shell.run_command(package_dependency['command'].split())

