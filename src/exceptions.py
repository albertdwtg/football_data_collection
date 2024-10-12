class BadRequest(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class BadResponse(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
