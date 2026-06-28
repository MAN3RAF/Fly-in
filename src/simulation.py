from collections import deque
from typing import List, Dict, Any
from zone import Zone
from drone import Drone
from connection import Connection
from parser import Map
from graph import Graph
from algo import Algo


class Simulation:
    def __init__(self, graph: Graph, algo: Algo) -> None:
        self.graph = graph
        self.current_turn = 0
        self.algo = algo
    
    def assign_drones_path(self, paths: List[List[Zone]]) -> None:
        usable_paths = self.algo.get_usable_paths(paths)
        nb_paths = len(usable_paths)

        for i, drone in enumerate(self.graph.drones):
            drone.path = usable_paths[i % nb_paths]
			# print(f"{drone.id}: {[x.name for x in drone.path]} ")
			# print()

    def run_turn(self) -> str:
        """
        Executes exactly ONE simulation turn.
        Returns the formatted string for this turn (e.g., 'D1-zoneA D2-zoneB').
        """
        # 1. Track current zone occupancies at the start of this turn
        # Start and End hubs have infinite capacity, so we don't limit them.
        occupancy: dict[Zone, int] = {zone: 0 for zone in self.graph.zones}
        for drone in self.graph.drones:
            occupancy[drone.current_zone] += 1

        moving_drones: List[Drone] = []
        output_parts: List[str] = []

        # 2. Phase 1: Determine which drones want to move and free up capacity immediately
        for drone in self.graph.drones:
            next_zone = drone.get_next_zone()
            if next_zone is not None:
                # INSTANT CAPACITY RELEASE: 
                # This drone plans to leave its current zone, so we subtract its capacity footprint right now.
                # This allows an incoming drone to claim this slot during this exact same turn.
                if drone.current_zone.name not in ("start", "goal"):
                    occupancy[drone.current_zone] -= 1
                moving_drones.append(drone)

        # 3. Phase 2: Validate destinations against capacity rules
        for drone in moving_drones:
            next_zone = drone.get_next_zone()
            
            # Safe check: Is there room at the destination? (Or is it an infinite capacity hub?)
            is_infinite_hub = "start" in next_zone.name or "goal" in next_zone.name
            has_capacity = occupancy[next_zone] < next_zone.max_drones

            if is_infinite_hub or has_capacity:
                # Approve the move! Update our tracking occupancy mapping
                if not is_infinite_hub:
                    occupancy[next_zone] += 1

                # Format the output string block based on requirements
                output_parts.append(f"D{drone.id}-{next_zone.name}")

                # Execute the movement step on the drone object.

                drone.move()
            else:
                # CONGESTION MANAGEMENT: No space available. 
                # The drone is forced to wait. Revert its freed capacity since it's staying.
                if drone.current_zone.name not in ("start", "goal"):
                    occupancy[drone.current_zone] += 1

        self.current_turn += 1
        return " ".join(output_parts)
    









