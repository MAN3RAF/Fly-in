from collections import deque
from typing import List, Dict, Any
from zone import Zone
from drone import Drone
from connection import Connection
from parser import Map
from graph import Graph



class simulation():

    def __init__(self):
        pass


    def get_next_zone(self, drone: Drone) -> Zone | None:
        path = drone.path
        for i, zone in enumerate(path[:-1]):  # exclude last zone, it has no next
            if zone == drone.current_zone:
                return path[i + 1]
        return None

    def assign_drones(self, paths: List[List[Zone]]) -> None:
		
		usable_paths = self.get_usable_paths(paths)
		nb_paths = len(usable_paths)

		for i, drone in enumerate(self.graph.drones):
			drone.path = usable_paths[i % nb_paths]
			# print(f"{drone.id}: {[x.name for x in drone.path]} ")
			# print()
    
    def run():
        """Runs the simulation 1 turn."""
        pass

    









