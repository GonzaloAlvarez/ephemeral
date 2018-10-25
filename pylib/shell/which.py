#!/usr/bin/env python
import os

def which(*executables):
    """
    This is a generic bash-like which command, to find an executable in PATH. Unlike
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


