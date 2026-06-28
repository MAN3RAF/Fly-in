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

        self.conn: dict[tuple[Zone, Zone], Connection] = {}

        for c in self.graph.connections:
            self.conn[(c.zone_1, c.zone_2)] = c
            self.conn[(c.zone_2, c.zone_1)] = c

    def assign_drones_path(self, paths: List[List[Zone]]) -> None:
        usable_paths = self.algo.get_usable_paths(paths)
        nb_paths = len(usable_paths)

        for i, drone in enumerate(self.graph.drones):
            drone.path = usable_paths[i % nb_paths]

    def is_connection_available(self, drone: Drone, next_zone: Zone) -> bool:

        conn = [
            c for c in self.graph.connections 
            if (c.zone_1 == drone.current_zone and c.zone_2 == next_zone) or 
               (c.zone_2 == drone.current_zone and c.zone_1 == next_zone)
        ][0]

        in_conn = sum(
            1 for d in self.graph.drones 
            if d.in_transit and (
                (d.current_zone == conn.zone_1 and d.get_next_zone() == conn.zone_2) or
                (d.current_zone == conn.zone_2 and d.get_next_zone() == conn.zone_1)
            )
        )
        return in_conn < conn.max_capacity

    def is_zone_available(self, next_zone: Zone) -> bool:
        in_zone_only = sum(1 for d in self.graph.drones if d.current_zone == next_zone and (not d.in_transit))
        
        in_transit = sum(1 for d in self.graph.drones if d.in_transit and d.get_next_zone() == next_zone)
        
        return (in_zone_only + in_transit) < next_zone.max_drones

    def run_turn(self) -> str:
        """
        Executes exactly ONE simulation turn with connection and zone caps.
        """
        output_parts: List[str] = []

        for drone in self.graph.drones:
            if drone.in_transit:
                drone.in_transit = False
                drone.move()
                drone.moved = True
            if drone.current_zone == drone.destination:
                continue

        for drone in self.graph.drones:
            next_zone = drone.get_next_zone()
            if next_zone is None:
                continue

            conn_av = self.is_connection_available(drone, next_zone)
            zone_av = self.is_zone_available(next_zone)

            if (not drone.moved) and conn_av and zone_av:

                if next_zone.type == "restricted":
                    drone.in_transit = True
                else:
                    drone.move()

                # output_parts.append(f"D{drone.id}-{drone.current_zone.name}")

            drone.moved = False

        self.current_turn += 1
        return " ".join(output_parts)

    def is_finished(self) -> bool:
        return all(drone.current_zone == drone.destination for drone in self.graph.drones)





