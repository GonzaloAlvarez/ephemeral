"""
Command Methods
"""

import argparse
from .run import run
from .setup import setup
from .pyinfo import pyinfo

__all__ = [
    "run",
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

    pyinfo_parser = subparser.add_parser('pyinfo')
    pyinfo_parser.set_defaults(command=pyinfo)
        
