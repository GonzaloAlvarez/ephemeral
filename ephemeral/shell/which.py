# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

def which(*executables):
    """
    Generic bash-like which command, to find an executable in PATH. Unlike
    the similar 'distutils.spawn.find_executable', this one does not look in the current
    directory.

    :param executables: The list of files or executables that we want to find
    :returns: A list of the real paths of all found executables, without duplicates.
    """
    path = os.environ['PATH']
    paths = path.split(os.pathsep)
    results = []
    for executable in executables:
        for p in paths:
            f = os.path.join(p, executable)
            if os.path.isfile(f) and os.access(f, os.X_OK):
                results.append(os.path.realpath(f))
    return list(set(results))


