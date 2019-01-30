# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os, sys

def self_relaunch(py_interpreter):
    os.execl(py_interpreter, py_interpreter, *sys.argv)

