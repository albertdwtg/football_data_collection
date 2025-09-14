"""Module to make generic API calls"""

import logging
import secrets
from typing import Optional

from curl_cffi import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from utils.constants import POSSIBLE_BROWSERS, POSSIBLE_USER_AGENTS, TIMEOUT
from utils.exceptions import BadResponseError

SUCCESS_STATUS_CODE = 200
NB_CALLS_BEFORE_ROTATION = 3

# pylint: disable = too-few-public-methods
class Scraper:
    """Objects handling generic calls and responses to APIs"""

    def __init__(self) -> None:
        """Init of the Scraper object
        """
        self.user_agent = secrets.choice(POSSIBLE_USER_AGENTS)
        self.browser = secrets.choice(POSSIBLE_BROWSERS)
        self.nb_calls = 0

    @retry(
        stop = stop_after_attempt(3),
        wait = wait_exponential(multiplier=3),
        reraise = True
    )
    def make_call(
        self, method: str, url: str,
        query_params: Optional[dict] = None, body: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> dict:
        """Function making HTTP request and handling JSON response

        Args:
            method (str): HTTP method to use
            url (str): base target url
            query_params (dict, optional): additional query params. Defaults to None.
            body (dict, optional): additional request body. Defaults to None.
            headers (dict, optional): additional request headers. Defaults to None.

        Raises:
            BadResponseError: If response is not what is expected

        Returns:
            Dict: JSON response
        """
        if headers is None:
            headers = {"User-Agent": self.user_agent}
        else:
            headers["User-Agent"] = self.user_agent
        self.nb_calls += 1
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=body,
            params=query_params,
            impersonate=self.browser,
            timeout=TIMEOUT,
        )
        logging.debug("Request headers : %s", response.request.headers)
        logging.debug("Request url : %s", response.request.url)
        logging.debug("Browser : %s", self.browser)
        logging.debug("Response headers : %s", response.headers)
        self._update_attributes()
        json_response = {}
        if response.status_code == SUCCESS_STATUS_CODE:
            logging.info("Succesfull request")
            json_response = response.json()
        elif response.status_code != SUCCESS_STATUS_CODE and "error" in response.json():
            raise BadResponseError(f"{response.json()['error']}")
        else:
            raise BadResponseError(f"Bad response : {response.text}")
        return json_response

    def _update_attributes(self) -> None:
        """Function to update attributes of the scraper
        to avoid being blocked by the API
        """
        if self.nb_calls >= NB_CALLS_BEFORE_ROTATION:
            self.user_agent = secrets.choice(POSSIBLE_USER_AGENTS)
            self.browser = secrets.choice(POSSIBLE_BROWSERS)
            self.nb_calls = 0
            logging.debug("New attributes for Scraper")
