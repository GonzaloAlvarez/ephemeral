# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

def find_file(search_path, filename):
    for dirpath, dirnames, filenames in os.walk(search_path):
        if filename in filenames:
            return os.path.join(dirpath, filename)

    return None
