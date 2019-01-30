# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

#### also will work with py23, py24 without 'encoding' arg
import os
import logging
import logging.handlers

LOGFILE_NAME = 'epher.log'
LOG_FORMAT = '%(asctime)s %(module)s [%(levelname)s]: %(message)s'
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def configure_logging(log_path):
    logfile = os.path.join(log_path, LOGFILE_NAME)
    fmtr = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    fileHandler = logging.handlers.RotatingFileHandler(logfile, encoding='utf8', maxBytes=100000, backupCount=1, mode='a')
    fileHandler.setFormatter(fmtr)
    fileHandler.setLevel(logging.DEBUG)
    root_logger.addHandler(fileHandler)

    consoleFormatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(fmtr)
    consoleHandler.setLevel(logging.WARN)
    root_logger.addHandler(consoleHandler)
