from collections import deque
from typing import List, Dict, Any
from zone import Zone
from drone import Drone
from connection import Connection
from parser import Map
from graph import Graph

class Algo():

	def get_all_paths(self, zones:List[Zone], graph: Graph) -> List[List[Zone]]:

		all_paths: List[List[Zone]] = []
		queue: deque[List[Zone]] = deque()

		start = [zone for zone in zones if zone.name == "start"][0]
		queue.append([start])

		while queue:
			path = queue.popleft()
			current_zone = path[-1]

			# print(path)

			if current_zone.name == "goal":
				all_paths.append(path)
				continue

			neighbors = graph.get_neighbors(current_zone)

			for n in neighbors:

				if n in path:
					continue
				if n.type == "blocked":
					continue

				queue.append(path + [n])

		return all_paths


	def get_cost(self, path: List[Zone]) -> int:

		cost = 0

		for p in path:
			if p.type == "normal" or p.type == "priority":
				cost += 1
			elif p.type == "restricted":
				cost += 2

		return cost
