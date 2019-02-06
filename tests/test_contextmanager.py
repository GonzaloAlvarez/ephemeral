# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os, json
from ephemeral.contextmanager import (SynchronizedObject, load_file)

def test_SynchronizedObject_basic_test(tmpdir):
    sync_file = tmpdir.mkdir('test').join('config.json')
    filename = os.path.join(sync_file.dirname, sync_file.basename)
    syncobj = load_file(filename)
    syncobj.data = 'test'
    with open(filename) as f:
        object_loaded = json.load(f)
        __import__('pprint').pprint(object_loaded)
        assert object_loaded['__path'] == filename
        assert object_loaded['data'] == 'test'
