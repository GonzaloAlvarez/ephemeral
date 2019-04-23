# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os
import tempfile
from io import open

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace

try:
    basestring
except NameError:
    basestring = str

class SynchronizedObject(Namespace):
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        return None

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        self.__update()

    def __delattr__(self, name):
        object.__delattr__(self, name)
        self.__update()

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __update(self):
        if '__path' in self.__dict__ and self['__path'] is not None:
            with tempfile.NamedTemporaryFile('w', dir=os.path.dirname(self['__path']), delete=False) as tf:
                tf.write(json.dumps(self.__dict__, ensure_ascii=False, sort_keys = True, indent = 4))
                tempfile_path = tf.name
            os.rename(tempfile_path, self['__path'])

    @staticmethod
    def loadFromFile(filename):
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.loads(f.read(), object_hook = lambda d: SynchronizedObject(**d))
            except Exception as e:
                raise ValueError('Failed to use file attribute, although it exists', e)
        elif os.access(os.path.dirname(args[0]), os.W_OK):
            obj = SynchronizedObject()
            object.__setattr__(obj, '__path', filename)
        else:
            raise ValueError('Argument provided is a string but not a path. Aborting')

