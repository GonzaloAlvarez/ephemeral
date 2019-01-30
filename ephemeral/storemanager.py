# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import __main__
import os

class EphemeralStoreManager(object):
    ENV_FOLDER_NAME = ".venv"
    def __init__(self):
        main_path = os.path.dirname(__main__.__file__)
        self.store_path = os.path.join(main_path, self.ENV_FOLDER_NAME)
        if not os.path.exists(self.store_path):
            os.makedirs(self.store_path)

    def get_store_path(self):
        return os.path.realpath(self.store_path)
