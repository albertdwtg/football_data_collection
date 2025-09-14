"""Main module that will be called by the cloud function"""

import functions_framework
import os
import logging
from datetime import datetime
from pydantic import ValidationError
import requests

from clients.coros import Coros
from clients.data_writter import DataWritter

from utils.exceptions import ExecutionError
from utils.logging_conf import init_logging
from utils.validator import args_validator, input_request_checker
from utils.secrets import get_secret
from utils.constants import PROJECT_ID, COROS_PWD_SECRET_ID, get_request_uuid


# Register an HTTP function with the Functions Framework
@functions_framework.http
def run(request: requests.request) -> tuple[str, int]:
    """Entrypoint of the cloud function
    It will handle the incoming request
    Args:
        request (requests.request): Incoming request

    Returns:
        Tuple: Tuple containing the response and the status code
    """
    os.environ["REQUEST_UUID"] = get_request_uuid()
    init_logging()
    try:
        input_request_checker(request=request)
        args_validator(request.json)
        request_body = request.json
        pwd = get_secret(
            project_id=PROJECT_ID, 
            secret_id=COROS_PWD_SECRET_ID
        )

        coros_client = Coros(
            account=request_body["account"],
            pwd=pwd
        )
        data_writter = DataWritter()
        coros_client.get_access_token()
        contents = coros_client.get_all_activities_details(
            from_date=request_body["from_date"],
            to_date=request_body["to_date"]
        )
        directory = f"activities_details/{datetime.now().strftime('%Y-%m-%d')}"
        data_writter.write_contents(
            directory=directory,
            content=contents,
            file_type="json"
        )
    except ValidationError as error:
        logging.error("Error of data validation: %s", str(error.errors()[0]))
        return str(error.errors()[0]), 500
    except ExecutionError as error:
        logging.error(error.message)
        return error.message, error.status_code

    return os.environ["REQUEST_UUID"], 200
