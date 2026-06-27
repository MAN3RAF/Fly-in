from typing import List, Dict, Any
from zone import Zone
from drone import Drone
from connection import Connection
from parser import Map

class Graph():
	def __init__(self, map: Map) -> None:
		
		self.map: Map = map
		self.drones: List[Drone] = map.drones
		self.connections: List[Connection] = map.connects
		self.zones: List[Zone] = map.zones
		# self.neighbors: Dict[Zone, List[Zone]] = {}
	

	def get_neighbors(self, zone: Zone) -> List[Zone]:

		neighbors = [] #neighbor list, left neighbor and right neighbor.
		for conn in self.connections:
			if zone.name == conn.zone_1.name: #if zone in conn left.
				if conn.zone_2 not in neighbors: #if that neighbor not in list yet.
					neighbors.append(conn.zone_2)
			if zone.name == conn.zone_2.name: #if zone in conn right.
				if conn.zone_1 not in neighbors: #if that neighbor not in list yet.
					neighbors.append(conn.zone_1)
		
		return neighbors

