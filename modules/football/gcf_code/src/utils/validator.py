"""Module to handle input requests parameters"""

import requests

from utils.exceptions import BadRequestError


def input_request_checker(request: requests.request):
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

def args_validator(request_body: dict):
    """Function that checks if input request body
    respect format

    Args:
        request_body (dict): body coming from input HTTP request

    Raises:
        BadRequestError: if a condition is not met
    """
    mandatory_keys = ["target"]
    for key in mandatory_keys:
        if key not in request_body:
            raise BadRequestError(f"'{key}' is a mandatory input key")

    possible_targets = ["last_round_season_stats", "round_season_stats"]
    if request_body["target"] not in possible_targets:
        raise BadRequestError(f"'target' must be in {possible_targets}")

    int_args = ["tournament_id", "season_id", "round"]
    for arg in int_args:
        # ruff: noqa: SIM102
        if arg in request_body and isinstance(request_body[arg], str):
            if request_body[arg].isdigit() is False:
                raise BadRequestError(f"'{arg}' must contain only digits")

    mandatory_keys_by_target = {
        "last_round_season_stats": ["tournament_id", "season_id"],
        "round_season_stats": ["tournament_id", "season_id", "round"],
    }

    for key in mandatory_keys_by_target[request_body["target"]]:
        if key not in request_body:
            raise BadRequestError(
                f"'{key}' is a mandatory input key for target {request_body['target']}"
            )
