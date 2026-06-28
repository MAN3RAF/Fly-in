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

        self.connection_lookup: dict[tuple[Zone, Zone], Connection] = {}

        for conn in self.graph.connections:
            self.connection_lookup[(conn.zone_1, conn.zone_2)] = conn
            self.connection_lookup[(conn.zone_2, conn.zone_1)] = conn
    
    def assign_drones_path(self, paths: List[List[Zone]]) -> None:
        usable_paths = self.algo.get_usable_paths(paths)
        nb_paths = len(usable_paths)

        for i, drone in enumerate(self.graph.drones):
            drone.path = usable_paths[i % nb_paths]

    def is_connection_available(
            self, drone: Drone,
            conn_capacity: dict[Connection, int]) -> bool:
        
        next_zone = drone.get_next_zone()
        if next_zone is None:
            return False

        conn = self.connection_lookup.get((drone.current_zone, next_zone))
        if conn is None:
            return False

        return conn_capacity[conn] < conn.max_capacity

    def is_zone_available(
            self, next_zone: Zone, 
            zones_capacity: Dict[Zone, int]
            ) -> bool:

        if "goal" in next_zone.name:
            return True
        return zones_capacity[next_zone] < next_zone.max_drones

    def run_turn(self) -> str:
        """
        Executes exactly ONE simulation turn with connection and zone caps.
        """
        zones_capacity: Dict[Zone, int] = {zone: 0 for zone in self.graph.zones}
        for d in self.graph.drones:
            zones_capacity[d.current_zone] += 1

        conn_capacity: Dict[Connection, int] = {conn: 0 for conn in self.graph.connections}
        output_parts: List[str] = []

        for drone in self.graph.drones:
            if drone.in_transit:
                drone.in_transit = False
                drone.move()
                drone.moved = True

            if drone.current_zone == drone.destination:
                continue

            next_zone = drone.get_next_zone()
            if next_zone is not None and not drone.in_transit:
                zones_capacity[drone.current_zone] -= 1

        for drone in self.graph.drones:
            next_zone = drone.get_next_zone()
            if next_zone is None:
                continue

            conn_av = self.is_connection_available(drone, conn_capacity)
            zone_av = self.is_zone_available(next_zone, zones_capacity)

            if (not drone.moved) and conn_av and zone_av:
                conn = self.connection_lookup[(drone.current_zone, next_zone)]
                conn_capacity[conn] += 1

                zones_capacity[next_zone] += 1

                drone.move()
                output_parts.append(f"D{drone.id}-{drone.current_zone.name}")
            else:
                zones_capacity[drone.current_zone] += 1

        self.current_turn += 1
        return " ".join(output_parts)









