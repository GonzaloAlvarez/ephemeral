# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import logging
import json
import os
from ephemeral.shell import cout

def conf(context):
    if context.session.cli.action:
        if context.session.cli.action == 'localoverride':
            if len(context.session.cli.args) > 2:
                logging.error('Wrong number of arguments for "localoverride". Expecting PACKAGE_NAME PATH.')
            elif len(context.session.cli.args) == 1:
                package_name = context.session.cli.args[0]
                context.config.__delattr__(package_name + '.source')
            else:
                package_name = context.session.cli.args[0]
                override_path = context.session.cli.args[1]
                cout('{} -> {}'.format(package_name, override_path))
                context.config.__setattr__(package_name + '.source', os.path.abspath(override_path))
        elif context.session.cli.action == 'show':
            cout(json.dumps(context.config.__dict__, indent = 2, separators=(',', ': ')))
        else:
            logging.error('The action provided [{}] is not supported.'.format(context.session.cli.action))

