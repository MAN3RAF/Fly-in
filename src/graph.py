from typing import List
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
