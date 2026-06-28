from typing import List, Dict, Any
from zone import Zone

class Drone:
    def __init__(
        self, id: int, zone: Zone,
        path: list[Zone], destination: Zone
    ) -> None:
        
        self.id = id
        self.current_zone = zone
        self.destination = destination
        self.path: list[Zone] = path
        
        self.path_index = 0
        self.steps = 0
        
        # Transit state tracking for restricted connections
        self.in_transit = False
        self.transit_turns_left = 0

    def get_next_zone(self) -> Zone | None:
        """Looks ahead to the next step in the assigned path."""
        if self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None

    def move(self) -> None:
        """Advances the drone to its next planned path node."""
        next_zone = self.get_next_zone()
        if next_zone is not None:
            self.current_zone = next_zone
            self.path_index += 1
            self.steps += 1

