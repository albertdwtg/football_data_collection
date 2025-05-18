from clients.scraper import Scraper
import json
from datetime import datetime

scraper = Scraper()

class Coros:
    def __init__(self, account: str, pwd: str):
        self.account = account
        self.pwd = pwd

    def get_access_token(self):
        request_uuid, json_response = scraper.make_call(
            method="POST", url="https://teameuapi.coros.com/account/login",
            body=json.dumps({"account": self.account, "pwd": self.pwd, "accountType": 2})
        )
        self.access_token = json_response["data"]["accessToken"]

    def get_account_info(self):
        request_uuid, json_response = scraper.make_call(
            method="GET", url="https://teameuapi.coros.com/account/query",
            headers={"Accesstoken": self.access_token}
        )
        return request_uuid, json_response["data"]

    def get_all_activities(self):
        content = []
        page_number = 1
        total_page = 1000
        while page_number <= total_page:
            method = "GET"
            url = "https://teameuapi.coros.com/activity/query"
            query_params = {"pageNumber": page_number, "size": 20}

            request_uuid, json_response = scraper.make_call(
                method=method, url=url,
                headers={"Accesstoken": self.access_token},
                query_params=query_params
            )
            content.append(
                {
                    "request_uuid": request_uuid,
                    "data": json_response["data"],
                    "metadata": {
                        "method": method, 
                        "url": url,
                        "query_params": query_params,
                        "ingestion_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
            )
            page_number += 1
            total_page = json_response["data"]["totalPage"]
        return content
    
    # def get_all_activities_details(self):
