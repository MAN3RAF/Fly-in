from collections import deque
from typing import List, Dict, Any
from zone import Zone
from drone import Drone
from connection import Connection
from parser import Map
from graph import Graph

class Algo():
    def __init__(self, graph:Graph):
        self.graph = graph

    def get_all_paths(self, zones:List[Zone]) -> List[List[Zone]]:
        """Get all posible paths."""

        all_paths: List[List[Zone]] = []
        queue: deque[List[Zone]] = deque()

        start = [zone for zone in zones if zone.name == "start"][0]
        end = [d for d in self.graph.drones if d.current_zone][0].destination
        all_paths: List[List[Zone]] = []
        queue: deque[List[Zone]] = deque([[start]])

        while queue:
            path = queue.popleft()
            current_zone = path[-1]

            if current_zone.name == end.name:
                all_paths.append(path)
                continue

            for neighbor in current_zone.neighbors:
                if neighbor in path or neighbor.type == "blocked":
                    continue
                queue.append(path + [neighbor])

        # print(all_paths)
        return all_paths


    def get_cost(self, path: List[Zone]) -> float | int:
        """Calculate the cost."""

        cost = 0

        for p in path[1:]:
            if p.type == "normal":
                cost += 1
            elif p.type == "restricted":
                cost += 2
            elif p.type == "priority":
                cost += 1
        return cost
    
    def get_usable_paths(self, paths: List[List[Zone]]) -> List[List[Zone]]:
        """Get usable most paths"""

        if not paths:
            raise ValueError("[ERROR] No seable paths!")

        sorted_paths = sorted(paths, key=lambda x: self.get_cost(x)) #sort by cost

        # print(sorted_paths[0])
        
        # cheapest_cost = self.get_cost(sorted_paths[0])
        best_turn_cost = self.get_cost(sorted_paths[0])
        
        # 3. Return ALL paths that share this optimal minimum turn cost.
        # This gives your drone fleet multiple distinct lanes if they exist, 
        # but ensures nobody wastes time taking a longer route.
        # print([path for path in sorted_paths if self.get_cost(path) == best_turn_cost])

        return [path for path in sorted_paths if self.get_cost(path) <= best_turn_cost + 1]


