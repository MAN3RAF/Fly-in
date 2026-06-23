from typing import List, Dict, Any
from zone import Zone
from drone import Drone


class Graph():
	def __init__(
			self, nb_drones: int, hubs: List[Dict],
			connections: List[Dict]) -> None:
		
		self.nb_drones = nb_drones
		self.hubs = hubs
		self.connections = connections
		self.zones: List[Zone] = []
		self.connects: Dict[Zone,Zone] = {}
		self.drones: List[Drone] = []

	def get_hubs(self) -> List[Zone]:

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

	def get_connections(self) -> Dict[Zone, Zone]:

		for conn in self.connections:
			if not self.zones:
				self.zones = self.get_hubs()
			for zone in self.zones:
				if zone.name in conn: #if name of zone in connection in our zones.
					link_1: Zone = zone
					break
			for zone in self.zones:
				if zone.name in conn.values(): #if name of zone in connection in our zones.
					link_2: Zone = zone
					break
			self.connects[link_1] = link_2

		return self.connects
	
	def get_drones(self):

		for zone in self.zones:
			if "start" in zone.name:
				coords: tuple[int] = zone.coords
		for zone in self.zones:
			if "goal" in zone.name:
				end_zone = zone

		for i in range(1, self.nb_drones):
			drone = Drone(i, coords, [], end_zone)
			self.drones.append(drone)
		return 

