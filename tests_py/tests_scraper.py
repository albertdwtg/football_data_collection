import sys
import os

sys.path.append(os.path.abspath("../src"))
from clients.scraper import Scraper


class TestClassScraper:
    def test_get_call(self):
        scraper_client = Scraper()
        request_uuid, json_response = scraper_client.make_call(
            method="GET", url="https://reqbin.com/echo"
        )
        assert len(request_uuid) == 8
        assert isinstance(json_response, dict)
