class FlyInError(Exception):
    def __init__(self, msg):
        super().__init__(f"FlyInError: {msg}")


class ParsingError(FlyInError):
    """Raised when the parsing has an error."""
    def __init__(self, msg):
        super().__init__(f"ParsingError: {msg}")


class PathNotFoundError(FlyInError):
    """
    Raised when the pathfinding algorithm
    cannot find a valid route to the goal.
    """
    def __init__(self, msg):
        super().__init__(f"PathNotFoundError: {msg}")
