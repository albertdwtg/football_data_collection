"""Module creating custom Exceptions for special needs"""

class ExecutionError(Exception):
    """Exception raised in case of an error
    occuring wile dealing with the request"""
    def __init__(self, message: str, status_code: int = 500) -> None:
        """Init of the ExecutionError

        Args:
            message (str): Message to display
            status_code (int, optional): Status code to return. Defaults to 500.
        """
        super().__init__(self.message)
        self.message = message
        self.status_code = status_code

class BadRequestError(ExecutionError):
    """Exception raised in case of bad input parameters"""

    def __init__(self, message: str) -> None:
        """Init of the BadRequestError

        Args:
            message (str): Message to display
        """
        self.message = message
        self.status_code = 400
        super().__init__(self.message, self.status_code)


class BadResponseError(ExecutionError):
    """Exception raised in case of bad response from an API call"""

    def __init__(self, message: str) -> None:
        """Init of the BadResponseError

        Args:
            message (str): Message to display
        """
        self.message = message
        self.status_code = 422
        super().__init__(self.message, self.status_code)

class InternalServerError(ExecutionError):
    """Exception raised in case of an error
    occuring wile dealing with the request"""

    def __init__(self, message: str) -> None:
        """Init of the InternalServerError

        Args:
            message (str): Message to display
        """
        self.message = message
        self.status_code = 500
        super().__init__(self.message, self.status_code)

class SecretNotFoundError(ExecutionError):
    """Custom exception raised when a secret is not found."""
    def __init__(self, secret_name: str) -> None:
        """Init of the SecretNotFoundError

        Args:
            secret_name (str): Name of the secret that was not found
        """
        self.secret_name = secret_name
        self.message = f"Secret '{secret_name}' not found."
        self.status_code = 404
        super().__init__(self.message, self.status_code)
