"""Module collecting constants and ENV variables"""

import os
import secrets
import string

from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.environ["PROJECT_ID"]
PROJECT_ENV = os.environ["PROJECT_ENV"]
GCS_BUCKET = f"cdp_gcs_coros_ew1_{PROJECT_ENV.lower()}"

POSSIBLE_BROWSERS = [
    "chrome99",
    "chrome100",
    "chrome101",
    "chrome104",
    "chrome107",
    "chrome110",
    "chrome116",
    "chrome119",
    "chrome120",
]

# pylint: disable=line-too-long
POSSIBLE_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36", # noqa: E501
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36", # noqa: E501
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36", # noqa: E501
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36", # noqa: E501
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36", # noqa: E501
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36", # noqa: E501
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36", # noqa: E501
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17", # noqa: E501
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15", # noqa: E501
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14", # noqa: E501
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13", # noqa: E501
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13", # noqa: E501
]

TIMEOUT = 10

COROS_PWD_SECRET_ID = f"cdp_srt_coros_{PROJECT_ENV.lower()}"

def get_request_uuid() -> str:
    """Function to generate a request uuid

    Returns:
        str: Generated uuid
    """
    uuid = "".join(
        [secrets.choice(string.ascii_letters + string.digits) for i in range(8)]
    )
    return uuid.lower()
