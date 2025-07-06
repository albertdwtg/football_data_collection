from clients.scraper import Scraper
import json
from datetime import datetime
import os
import logging
from utils.models import DataExport

scraper = Scraper()

class Coros:
    def __init__(self, account: str, pwd: str):
        self.account = account
        self.pwd = pwd

    def get_access_token(self):
        json_response = scraper.make_call(
            method="POST", url="https://teameuapi.coros.com/account/login",
            body=json.dumps(
                {
                    "account": self.account, 
                    "pwd": self.pwd, 
                    "accountType": 2
                }
            )
        )
        self.access_token = json_response["data"]["accessToken"]

    def get_account_info(self):
        json_response = scraper.make_call(
            method="GET", url="https://teameuapi.coros.com/account/query",
            headers={"Accesstoken": self.access_token}
        )
        return json_response["data"]

    def get_all_activities(self, size: int):
        content = []
        page_number = 1
        total_page = 1000
        while page_number <= total_page:
            method = "GET"
            url = "https://teameuapi.coros.com/activity/query"
            query_params = {"pageNumber": page_number, "size": size}

            json_response = scraper.make_call(
                method=method, url=url,
                headers={"Accesstoken": self.access_token},
                query_params=query_params
            )
            export = DataExport(
                file_name=f"{os.environ['REQUEST_UUID']}_{page_number}",
                data=json_response["data"],
                metadata={
                    "method": method, 
                    "url": url,
                    "request_uuid": os.environ["REQUEST_UUID"],
                    "file_name": f"{os.environ['REQUEST_UUID']}_{page_number}",
                    "query_params": query_params,
                    "ingestion_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            content.append(dict(export))
            page_number += 1
            total_page = json_response["data"]["totalPage"]
        return content
    
    def get_all_activities_details(self):
        all_activities = self.get_all_activities(size=200)
        content = []
        activity_number = 1
        for response in all_activities:
            for activity in response["data"]["dataList"]:
                label_id = activity["labelId"]
                logging.debug(
                    "Loading activity number %s: %s", activity_number, label_id
                )
                url = "https://teameuapi.coros.com/activity/detail/query"
                query_params = {"labelId": label_id, "sportType": 100}
                method = "POST"
                json_response = scraper.make_call(
                    method=method, 
                    url=url,
                    query_params=query_params,
                    headers={"Accesstoken": self.access_token}
                )
                content.append(
                    {
                        "file_name": f"{os.environ['REQUEST_UUID']}_{activity_number}",
                        "data": json_response["data"],
                        "metadata": {
                            "method": method, 
                            "url": url,
                            "query_params": query_params,
                            "request_uuid": os.environ["REQUEST_UUID"],
                            "file_name":(
                                f"{os.environ['REQUEST_UUID']}_{activity_number}"
                            ),
                            "ingestion_time": datetime.now()\
                                .strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
                )
                activity_number += 1
        return content
