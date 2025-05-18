"""Main module that will be called by the cloud function"""

import functions_framework

from clients.binance import BinanceApi

from utils.exceptions import (
    BadRequestError, BadResponseError, InternalServerError,
    SecretNotFoundError
    )
from utils.logging_conf import init_logging
from utils.validator import args_validator, input_request_checker
from utils.secrets import get_secret
from utils.constants import (PROJECT_ID,
    SECRET_KEY_SECRET_ID, API_KEY_SECRET_ID,
    QUOTE_ASSET, COINS_TO_TRADE, PROJECT_ENV)

init_logging()


# Register an HTTP function with the Functions Framework
@functions_framework.http
def run(request):
    """Entrypoint of the cloud function
    It will handle the incoming request
    Args:
        request (_type_): Incoming request

    Returns:
        Tuple: Tuple containing the response and the status code
    """
    try:
        input_request_checker(request=request)
        args_validator(request.json)
        secret_key = get_secret(
            project_id=PROJECT_ID,
            secret_id=SECRET_KEY_SECRET_ID
        )
        api_key = get_secret(
            project_id=PROJECT_ID,
            secret_id=API_KEY_SECRET_ID
        )
        binance_client = BinanceApi(
            api_key=api_key,
            secret_key=secret_key,
            quote_asset=QUOTE_ASSET,
            coins_to_trade=COINS_TO_TRADE[PROJECT_ENV.upper()]
        )
        binance_client.get_account_wallet(conversion_asset="USDT")

    except BadRequestError as error:
        return f"Bad request : {error}", 400
    except BadResponseError as error:
        return f"Bad response : {error}", 400
    except SecretNotFoundError as error:
        return f"{error}", 400
    except InternalServerError as error:
        return f"Internal server error : {error}", 500

    return "OK", 200
