# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import logging
from ephemeral import (shell, github)

def install_virtualenv(dest_path, python_exec):
    virtualenv_zipball = github.download_latest('pypa', 'virtualenv')
    logging.debug('Unpacking virtualenv from [{}] to [{}]'.format(virtualenv_zipball, dest_path))
    shell.unpack_zipball(virtualenv_zipball, dest_path)
    virtualenv_py_path = shell.find_file(dest_path, "virtualenv.py")
    shell.brun([python_exec, virtualenv_py_path, '-q', '--no-site-packages', dest_path])

