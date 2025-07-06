"""Main module that will be called by the cloud function"""

import functions_framework
import os

from clients.coros import Coros
from clients.data_writter import DataWritter

from utils.exceptions import (
    BadRequestError, BadResponseError, InternalServerError,
    SecretNotFoundError
    )
from utils.logging_conf import init_logging
from utils.validator import args_validator, input_request_checker
from utils.secrets import get_secret
from utils.constants import PROJECT_ID, COROS_PWD_SECRET_ID, get_request_uuid


# Register an HTTP function with the Functions Framework
@functions_framework.http
def run(request):
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
        contents = coros_client.get_all_activities(
            size = 200
        )
        data_writter.write_contents(
            directory="activities_details",
            content=contents,
            file_type="json"
        )

    except BadRequestError as error:
        return f"Bad request : {error}", 400
    except BadResponseError as error:
        return f"Bad response : {error}", 400
    except SecretNotFoundError as error:
        return f"{error}", 400
    except InternalServerError as error:
        return f"Internal server error : {error}", 500

    return "OK", 200
