"""Module to handle input requests parameters"""

import requests

from utils.exceptions import BadRequestError
from utils.models import InputRequest

def input_request_checker(request: requests.request) -> None:
    """Function that checks if input request is valid

    Args:
        request (requests.request): request object

    Raises:
        BadRequestError: If request method is not POST
        BadRequestError: If content type is not application/json
    """
    if request.method != "POST":
        raise BadRequestError("POST is the only authorized method")
    if request.headers.get("Content-Type") != "application/json":
        raise BadRequestError("'application/json' is the only content authorized")

def args_validator(request_body: dict) -> None:
    """Function that checks if input request body
    respect format

    Args:
        request_body (dict): body coming from input HTTP request

    Raises:
        BadRequestError: if a condition is not met
    """
    # Validate the request body against the InputRequest model
    InputRequest.model_validate(request_body)
