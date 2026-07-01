from typing import Set, Tuple


class Zone:
    def __init__(
        self,
        name: str,
        coords: Tuple[int],
        color: str = "none",
        max_drones: int = 1,
        type: str = "normal",
    ) -> None:
        self.name: str = name
        self.coords: Tuple[int] = coords
        self.color: str = color
        self.max_drones: int = max_drones
        self.type: str = type
        self.neighbors: Set[Zone] = set()
