
class ParsingError(Exception):
	"""Raised when the parsing has an error."""
	pass


class PathNotFoundError(Exception):
    """Raised when the pathfinding algorithm cannot find a valid route to the goal."""
    pass
