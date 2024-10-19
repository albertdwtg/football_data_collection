"""Module to handle loggers based on environments"""

import logging
from constants import PROJECT_ENV


def init_logging():
    """Initialization of loggers"""
    if PROJECT_ENV.upper() == "DEV":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    loggers_infos = ["watchdog.observers.inotify_buffer"]
    for logger in loggers_infos:
        logging.getLogger(logger).setLevel(logging.INFO)
