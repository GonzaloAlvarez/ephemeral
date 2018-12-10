#!/usr/bin/env python

#### also will work with py23, py24 without 'encoding' arg
import logging
import logging.handlers

LOG_FORMAT = '%(asctime)s %(module)s [%(levelname)s]: %(message)s'
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
def configure_logging(logfile):
    fmtr = logging.Formatter(fmt = LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    fileHandler = logging.handlers.RotatingFileHandler(logfile, encoding='utf8', maxBytes=100000, backupCount=1)
    fileHandler.setFormatter(fmtr)
    fileHandler.setLevel(logging.DEBUG)
    root_logger.addHandler(fileHandler)

    consoleFormatter = logging.Formatter(fmt = LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(fmtr)
    consoleHandler.setLevel(logging.WARN)
    root_logger.addHandler(consoleHandler)
