

class Zone():
	def __init__(
			self, name: str, coords: tuple[int],
			color: str="none", max_drones: int=1,
			type: str="normal") -> None:
		
		self.name: str = name
		self.coords: tuple[int] = coords
		self.color: str = color
		self.max_drones: int = max_drones
		self.type: str = type
		self.neighbors: set[Zone] = set()
