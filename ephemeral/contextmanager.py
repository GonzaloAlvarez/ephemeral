# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json, os, tempfile
from io import open

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace

def json2obj(data): return json.loads(data, object_hook=lambda d: SynchronizedObject(**d))
def load_file(file):
    if os.path.isfile(file):
        with open(file, 'r', encoding='utf-8') as f:
            obj = json2obj(f.read())
    else:
        obj = SynchronizedObject()
    object.__setattr__(obj, '__path', file)
    return obj

def save_obj(obj):
    if hasattr(obj, '__path') and obj.__path is not None:
        with tempfile.NamedTemporaryFile('w', dir=os.path.dirname(obj.__path), delete=False) as tf:
            tf.write(json.dumps(obj.__dict__, ensure_ascii=False, sort_keys = True, indent = 4))
            tempfile_path = tf.name
        os.rename(tempfile_path, obj.__path)

class SynchronizedObject(Namespace):
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        return None

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        save_obj(self)

class ContextManager(object):
    MAIN_CONFIG_NAME = "epher.json"
    def __init__(self, epherstore):
        object.__setattr__(self, 'epherstore', epherstore)
        config_path = os.path.join(self.epherstore.get_store_path(), self.MAIN_CONFIG_NAME)
        config_path = os.path.realpath(config_path)
        object.__setattr__(self, 'config_path', config_path)
        object.__setattr__(self, 'session', type('', (), {})())
        self.config = load_file(self.config_path)

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
