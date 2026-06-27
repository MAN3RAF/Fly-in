from typing import List, Dict, Any
from zone import Zone

class Drone():
	def __init__(
			self, id: int, zone: Zone,
			path: List, destination: Zone) -> None:
		
		self.id = id
		self.current_zone = zone
		self.steps = 0
		self.path = path
		self.destination = destination
		self.in_trasit = False




