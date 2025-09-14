"""Module to handle loggers based on environments"""

import logging
import os

from utils.constants import PROJECT_ENV


def init_logging() -> None:
    """Initialization of loggers"""
    logs_format = f"request_uuid:{os.environ.get("REQUEST_UUID")} "
    logs_format += "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    if PROJECT_ENV.upper() == "DEV":
        logging.basicConfig(
            level=logging.DEBUG, 
            format=logs_format,
            datefmt=date_format
        )
    else:
        logging.basicConfig(
            level=logging.INFO, 
            format=logs_format,
            datefmt=date_format
        )
    loggers_infos = [
        "watchdog.observers.inotify_buffer",
        "urllib3.connectionpool",
        "urllib3.util",
        "google.auth"
    ]
    for logger in loggers_infos:
        logging.getLogger(logger).setLevel(logging.INFO)
    logging.info("Logging initialized")
