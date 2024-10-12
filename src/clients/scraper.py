from curl_cffi import requests
import logging
import random
import string

from constants import POSSIBLE_BROWSERS, POSSIBLE_USER_AGENTS, TIMEOUT
from exceptions import BadRequest, BadResponse


class Scraper:
    def __init__(self):
        self.user_agent = random.choice(POSSIBLE_USER_AGENTS)
        self.browser = random.choice(POSSIBLE_BROWSERS)
        self.nb_calls = 0

    def _get_request_uuid(self):
        uuid = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        return uuid.lower()

    def make_call(
        self, method: str, url: str, query_params: dict = {}, body: dict = {}
    ):
        headers = {"User-Agent": self.user_agent}
        self.nb_calls += 1
        request_uuid = self._get_request_uuid()
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
        if response.status_code == 200:
            logging.info("Succesfull request")
            if response.headers["content-type"] == "application/json":
                return request_uuid, response.json()
        elif response.status_code != 200 and "error" in response.json():
            raise BadResponse(f"{response.json()['error']}")
        else:
            raise BadResponse(f"Bad response : {response.text}")

    def _update_attributes(self):
        if self.nb_calls >= 3:
            self.user_agent = random.choice(POSSIBLE_USER_AGENTS)
            self.browser = random.choice(POSSIBLE_BROWSERS)
            self.nb_calls = 0
            logging.debug("New attributes for Scraper")
