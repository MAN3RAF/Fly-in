from zone import Zone


class Connection():
    def __init__(self, zone_1: Zone, zone_2: Zone, max_capacity: int = 1):
        self.zone_1 = zone_1
        self.zone_2 = zone_2
        self.max_capacity = max_capacity

        zone_1.neighbors.add(zone_2)
        zone_2.neighbors.add(zone_1)
