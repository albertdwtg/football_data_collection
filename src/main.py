"""Main module that will be called by the cloud function"""

import functions_framework

from clients.data_formatter import DataFormatter
from utils.exceptions import BadRequest, BadResponse
from utils.logging_conf import init_logging
from utils.validator import args_validator, input_request_checker

formatter_client = DataFormatter(data_writter_mode="LOCAL")
init_logging()


# Register an HTTP function with the Functions Framework
@functions_framework.http
def run(request):
    """Entrypoint of the cloud function
    It will handle the incoming request
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        input_request_checker(request=request)
        args_validator(request.json)
        request_body = request.json
        if request_body["target"] == "last_round_season_stats":
            formatter_client.load_round_statistics(
                tournament_id=request_body["tournament_id"],
                season_id=request_body["season_id"],
            )
        if request_body["target"] == "round_season_stats":
            formatter_client.load_round_statistics(
                tournament_id=request_body["tournament_id"],
                season_id=request_body["season_id"],
                round_id=request_body["round"],
            )
    except BadRequest as error:
        return f"Bad request : {error}", 400 
    except BadResponse as error:
        return f"Bad response : {error}", 400 
    except Exception as error:
        return f"Internal server error : {error}", 500
        
    return "OK", 200
