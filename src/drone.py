from typing import List, Dict, Any
from zone import Zone

class Drone():
	def __init__(
			self, id: int, coords: tuple[int],
			path: List, destination: Zone) -> None:
		
		self.id = id
		self.coords = coords
		self.path = path
		self.destination = destination
