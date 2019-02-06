# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import argparse
import copy

from ephemeral.commands import build_subparsers
from ephemeral.lang import NamedObject

class AliasedSubParsersAction(argparse._SubParsersAction):
    class _AliasedPseudoAction(argparse.Action):
        def __init__(self, name, aliases, help):
            dest = name
            if aliases:
                dest += ', %s' % ', '.join(aliases)
            sup = super(AliasedSubParsersAction._AliasedPseudoAction, self)
            sup.__init__(option_strings=[], dest=dest, help=help) 

    def add_parser(self, name, **kwargs):
        aliases = kwargs.pop('aliases', [])

        parser = super(AliasedSubParsersAction, self).add_parser(name, **kwargs)

        # Make the aliases work.
        for alias in aliases:
            self._name_parser_map[alias] = parser
        # Make the help text reflect them, first removing old help entry.
        if 'help' in kwargs:
            help = kwargs.pop('help')
            self._choices_actions.pop()
            pseudo_action = self._AliasedPseudoAction(name, aliases, help)
            self._choices_actions.append(pseudo_action)

        return parser

class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_action(self, action):
        parts = super(argparse.RawDescriptionHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts

class DictAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            k, v = values.split("=", 1)
        except ValueError:
            raise argparse.ArgumentError(self, "Format must be key=value")

        # Implementation is from argparse._AppendAction
        items = copy.copy(argparse._ensure_value(namespace, self.dest, {}))  # Default mutables, use copy!
        items[k] = v
        setattr(namespace, self.dest, items)

class CommandLineManager(object):

    def __init__(self):
        self.session_object = NamedObject()
        self.parser = argparse.ArgumentParser(formatter_class=SubcommandHelpFormatter)
        self.parser.register('action', 'parsers', AliasedSubParsersAction)
        self.parser.add_argument('-v', '--verbose', action='count', default=0)
        self.parser.add_argument('-c', '--config', action=DictAction)
        subparser = self.parser.add_subparsers(title = 'commands', metavar='<command>')
        build_subparsers(subparser)

        self.parsed_args = self.parser.parse_args()

    def get_args(self):
        return self.parsed_args
