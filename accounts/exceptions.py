# exceptions.py


class UserAlreadyExists(Exception):
    """Custom exception for when a user already exists."""

    def __init__(self, message="user already exists"):
        self.message = message
        super().__init__(self.message)


class UserDoesNotExist(Exception):
    """Custom exception for when a user does not exist."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)