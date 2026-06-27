class Zone():
	def __init__(
			self, name: str, coords: tuple[int],
			color: str="none", max_drones: int=1,
			type: str="normal") -> None:
		
		self.name = name
		self.coords = coords
		self.color = color
		self.max_drones = max_drones
		self.type = type
		self.neighbors = set()


	