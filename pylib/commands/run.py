#!/usr/bin/env python

from .setup import setup
from pylib import shell

def run(context):
    setup(context)
    for instruction in context.session.package_manager.get_instructions():
        shell.run_command(instruction['command'].split())
