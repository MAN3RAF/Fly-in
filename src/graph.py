from typing import List, Dict, Any
from zone import Zone


class Graph():
	def __init__(
			self, nb_drones: int, hubs: List[Dict],
			connections: List[Dict]) -> None:
		
		self.nb_drones = nb_drones
		self.hubs = hubs
		self.connections = connections
		self.zones: List[Zone] = []

	def get_hubs(self):

		for hub in self.hubs:
			
			name = hub['name']
			coords = (hub['x'], hub['y'])
			color = "none"
			max_drones = 1
			type = "normal"

			if 'color' in hub:
				color = hub['color']
			if 'max_drones' in hub:
				max_drones = hub['max_drones']
			if 'type' in hub:
				type = hub["type"]

			zone = Zone(name, coords, color, max_drones, type)

			self.zones.append(zone)

		return self.zones
