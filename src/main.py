"""Main module that will be called by the cloud function"""

import functions_framework

from clients.data_formatter import DataFormatter
from utils.exceptions import BadRequest
from utils.logging_conf import init_logging
from utils.validator import args_validator

formatter_client = DataFormatter(data_writter_mode="LOCAL")
init_logging()


# Register an HTTP function with the Functions Framework
@functions_framework.http
def run(request):
    """Entrypoint of the cloud function

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Your code here
    if request.method != "POST":
        raise BadRequest("POST is the only autorized method")
    init_logging()

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
    return "OK", 200
