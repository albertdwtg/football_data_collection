"""Module creating custom Exceptions for special needs"""


class BadRequest(Exception):
    """Exception raised in case of bad input parameters"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class BadResponse(Exception):
    """Exception raised in case of bad response from an API call"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
