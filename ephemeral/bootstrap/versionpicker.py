# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import __main__
import json
import os
from ephemeral import shell

def gather_python_info(*executables):
    # https://stackoverflow.com/a/13240524
    eph_path = os.path.realpath(__main__.__file__)
    py_results = []
    for executable in executables:
        json_out, err, exit_code = shell.brun(' '.join([executable, eph_path, 'pyinfo']))
        py_info_obj = json.loads(json_out)
        py_results.append(py_info_obj)
    return py_results

def pick_python(py_versions):
    py_filtered_versions = list(filter(lambda py_version: 'TLSv1_2' in py_version['ssl_protocols'], py_versions))
    py_sorted_versions = sorted(py_filtered_versions, key=lambda py_version: py_version['version_major'], reverse=True)
    if len(py_sorted_versions) > 0:
        return py_sorted_versions[0]
    return None

def get_best_python():
    python_execs = shell.which(*['python', 'python2', 'python2.7', 'python3', 'python3.7'])
    py_versions = gather_python_info(*python_execs)
    py_chosen = pick_python(py_versions)
    if py_chosen != None:
        return py_chosen['executable']
    return None
