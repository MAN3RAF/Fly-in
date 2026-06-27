from collections import deque
from typing import List, Dict, Any
from zone import Zone
from drone import Drone
from connection import Connection
from parser import Map
from graph import Graph

class Algo():

	def get_all_paths(self, zones:List[Zone], graph: Graph) -> List[List[Zone]]:
		"""Get all posible paths."""

		all_paths: List[List[Zone]] = []
		queue: deque[List[Zone]] = deque()

		start = [zone for zone in zones if zone.name == "start"][0]
		all_paths: List[List[Zone]] = []
		queue: deque[List[Zone]] = deque([[start]])
		
		while queue:
			path = queue.popleft()
			current_zone = path[-1]

			if current_zone.name == "goal":
				all_paths.append(path)
				continue

			neighbors = graph.get_neighbors(current_zone)

			for neighbor in neighbors:
				if neighbor in path or neighbor.type == "blocked":
					continue
				queue.append(path + [neighbor])

		return all_paths


	def get_cost(self, path: List[Zone]) -> float | int:
		"""Calculate the cost."""

		cost = 0

		for p in path:
			if p.type == "normal":
				cost += 1
			elif p.type == "restricted":
				cost += 2
			elif p.type == "priority":
				cost += 0.5

		return cost
	
	def get_useable_paths(self, paths: List[List[Zone]]) -> List[List[Zone]]:
		"""Get usable most paths"""

		if not paths:
			raise ValueError("[ERROR] No seable paths!")

		sorted_paths = sorted(paths, key=lambda x: self.get_cost(x))
		
		cheapest_cost = self.get_cost(sorted_paths[0])
		second_cheap = cheapest_cost + 1

		return [path for path in sorted_paths if self.get_cost(path) <= second_cheap]

	# def asign_drones(self, )
