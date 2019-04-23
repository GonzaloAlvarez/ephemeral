# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json, os, tempfile
from io import open
from ephemeral.lang import SynchronizedObject

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace

class ContextManager(object):
    MAIN_CONFIG_NAME = "epher.json"
    def __init__(self, epherstore):
        object.__setattr__(self, 'epherstore', epherstore)
        config_path = os.path.join(self.epherstore.get_store_path(), self.MAIN_CONFIG_NAME)
        config_path = os.path.realpath(config_path)
        object.__setattr__(self, 'config_path', config_path)
        object.__setattr__(self, 'session', type('', (), {})())
        self.config = SynchronizedObject.loadFromFile(self.config_path)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        if name in self.session.__dict__:
            return self.session.__dict__[name]
        return None

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
        else:
            self.__dict__['session'].__dict__[name] = value
