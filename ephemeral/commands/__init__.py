"""
Command Methods
"""

import argparse
from .run import run
from .setup import setup, setup_internal
from .pyinfo import pyinfo
from .conf import conf

__all__ = [
    "run",
    "setup_internal",
    "build_subparsers"
]

def build_subparsers(subparser):
    run_parser = subparser.add_parser('run', aliases=['r'], help='execute package')
    run_parser.add_argument('package')
    run_parser.set_defaults(command=run)
    run_parser.add_argument('args', nargs=argparse.REMAINDER)

    setup_parser = subparser.add_parser('setup', help='setup command')
    setup_parser.add_argument('package')
    setup_parser.set_defaults(command=setup)
    setup_parser.add_argument('args', nargs=argparse.REMAINDER)

    conf_parser = subparser.add_parser('conf', help='configuration command')
    conf_parser.add_argument('action')
    conf_parser.set_defaults(command=conf)
    conf_parser.add_argument('args', nargs=argparse.REMAINDER)

    pyinfo_parser = subparser.add_parser('pyinfo')
    pyinfo_parser.set_defaults(command=pyinfo)
        
