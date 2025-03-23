"""Module creating custom Exceptions for special needs"""


class BadRequestError(Exception):
    """Exception raised in case of bad input parameters"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class BadResponseError(Exception):
    """Exception raised in case of bad response from an API call"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InternalServerError(Exception):
    """Exception raised in case of an error
    occuring wile dealing with the request"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
