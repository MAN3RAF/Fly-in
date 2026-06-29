from typing import List, Dict
from zone import Zone
from drone import Drone
from connection import Connection
from exceptions import ParsingError


class Map():
	def __init__(
			self, nb_drones: int, hubs: List[Dict],
			connections: List[Dict], start_hub: Dict,
			end_hub: Dict) -> None:

		self.nb_drones = nb_drones 	   # int
		self.hubs = hubs			   # Dict
		self.connections = connections # List[dict[str, str]]
		self.zones: List[Zone] = []
		self.start_hub: Zone = start_hub
		self.end_hub: Zone = end_hub
		self.connects: List[Connection] = []
		self.drones: List[Drone] = []


	def init_map(self) -> None:
		self.get_hubs()
		self.get_drones()
		self.get_connections()


	def get_hubs(self) -> None:

		for hub in self.hubs:
			
			name = hub['name']
			coords = (hub['x'], hub['y'])
			color = "none"
			max_drones = 1
			type = "normal"

			if 'color' in hub:
				color = hub['color']
			if 'max_drones' in hub:
				max_drones = hub['max_drones']
			if (not 'max_drones' in hub) and hub['name'] == 'goal':
				max_drones = self.nb_drones
			if 'type' in hub:
				type = hub["type"]

			zone = Zone(name, coords, color, max_drones, type)

			self.zones.append(zone)


	def get_connections(self) -> None:
		if not self.zones:
			self.get_hubs()

		zones_by_name: dict[str, Zone] = {
			zone.name: zone
			for zone in self.zones
		}

		for conn in self.connections:
			source_name: str | None = None
			target_name: str | None = None

			for key, value in conn.items():
				if key == "max_link_capacity":
					continue

				source_name = key
				target_name = value
				break

			# if source_name is None or target_name is None:
			# 	raise ValueError(f"Invalid connection: {conn}")

			source_zone = zones_by_name[source_name]
			target_zone = zones_by_name[target_name]

			capacity = conn.get("max_link_capacity", 1)

			self.connects.append(
				Connection(
					source_zone,
					target_zone,
					capacity
				)
			)


	def get_drones(self) -> None:

		for i in range(0, self.nb_drones):
			for zone in self.zones:
				if "start" in zone.name:
					start_zone: Zone = zone
			for zone in self.zones:
				if "goal" in zone.name:
					end_zone = zone

			
			drone = Drone(i, start_zone, [], end_zone)
			self.drones.append(drone)


class Parser():
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.hubs: List[Dict] = []
        self.connections: List[Dict[str, str]] = []
        self.start_hub: Dict = {}
        self.end_hub: Dict = {}
        
        # Validation trackers for VII.4 constraints
        self.seen_names = set()
        self.seen_connections = set()
        self.start_count = 0
        self.end_count = 0

    def _validate_metadata(self, key: str, value: str, line_idx: int) -> None:
        """Enforces type and capacity constraints on metadata."""
        if key == "zone":
            if value not in {"normal", "blocked", "restricted", "priority"}:
                raise ParsingError(f"Line {line_idx}: Invalid zone type '{value}'. Must be normal, blocked, restricted, or priority.")
        if key in ("max_drones", "max_link_capacity"):
            if not value.isdigit() or int(value) <= 0:
                raise ParsingError(f"Line {line_idx}: Capacity values must be positive integers. Got '{value}'.")

    def _validate_name(self, name: str, line_idx: int) -> None:
        """Enforces name uniqueness and character constraints."""
        if "-" in name or " " in name:
            raise ParsingError(f"Line {line_idx}: Zone name '{name}' contains invalid characters (no dashes or spaces allowed).")
        if name in self.seen_names:
            raise ParsingError(f"Line {line_idx}: Zone name '{name}' is not unique.")
        self.seen_names.add(name)

    def parse_drones(self, line: str, line_idx: int) -> None:
        if ":" not in line:
            raise ParsingError(f"Line {line_idx}: Missing ':' separator in nb_drones line.")
        _, second = line.split(":", 1)
        second = second.strip()

        if not second.isdigit() or int(second) < 1:
            raise ParsingError(f"Line {line_idx}: nb_drones must be a positive integer.")

        self.nb_drones = int(second)

    def parse_start(self, line: str, line_idx: int) -> None:
        self.start_count += 1
        if self.start_count > 1:
            raise ParsingError(f"Line {line_idx}: Multiple start_hubs defined. Exactly one is required.")

        if '[' in line:
            mandatory, meta_data = line.split("[", 1)
        else:
            mandatory = line
            meta_data = ""

        items = mandatory.split()
        if len(items) < 4:
            raise ParsingError(f"Line {line_idx}: Malformed start_hub line. Missing name or coordinates.")
            
        hub: Dict = {}
        hub["name"] = items[1]
        self._validate_name(hub["name"], line_idx)
        
        if not items[2].replace('-', '', 1).isdigit() or not items[3].replace('-', '', 1).isdigit():
            raise ParsingError(f"Line {line_idx}: Coordinates must be valid integers.")
        hub["x"] = int(items[2])
        hub["y"] = int(items[3])

        if meta_data:
            meta_data = meta_data.strip("[]")
            meta_data = meta_data.split()
            for data in meta_data:
                if "=" not in data:
                    raise ParsingError(f"Line {line_idx}: Malformed metadata formatting near '{data}'.")
                key, value = data.split("=", 1)
                self._validate_metadata(key, value, line_idx)
                if key == "zone":
                    hub["type"] = value
                else:
                    hub[key] = int(value) if value.isdigit() else value

        self.start_hub = hub
        self.hubs.append(hub)

    def parse_hub(self, line: str, line_idx: int) -> None:
        if '[' in line:
            mandatory, meta_data = line.split("[", 1)
        else:
            mandatory = line
            meta_data = ""

        items = mandatory.split()
        if len(items) < 4:
            raise ParsingError(f"Line {line_idx}: Malformed hub line. Missing name or coordinates.")
            
        hub: Dict = {}
        hub["name"] = items[1]
        self._validate_name(hub["name"], line_idx)
        
        if not items[2].replace('-', '', 1).isdigit() or not items[3].replace('-', '', 1).isdigit():
            raise ParsingError(f"Line {line_idx}: Coordinates must be valid integers.")
        hub["x"] = int(items[2])
        hub["y"] = int(items[3])

        if meta_data:
            meta_data = meta_data.strip("[]")
            meta_data = meta_data.split()
            for data in meta_data:
                if "=" not in data:
                    raise ParsingError(f"Line {line_idx}: Malformed metadata formatting near '{data}'.")
                key, value = data.split("=", 1)
                self._validate_metadata(key, value, line_idx)
                if key == "zone":
                    hub["type"] = value
                else:
                    hub[key] = int(value) if value.isdigit() else value

        self.hubs.append(hub)

    def parse_end(self, line: str, line_idx: int) -> None:
        self.end_count += 1
        if self.end_count > 1:
            raise ParsingError(f"Line {line_idx}: Multiple end_hubs defined. Exactly one is required.")

        if '[' in line:
            mandatory, meta_data = line.split("[", 1)
        else:
            mandatory = line
            meta_data = ""

        items = mandatory.split()
        if len(items) < 4:
            raise ParsingError(f"Line {line_idx}: Malformed end_hub line. Missing name or coordinates.")
            
        hub: Dict = {}
        hub["name"] = items[1]
        self._validate_name(hub["name"], line_idx)
        
        if not items[2].replace('-', '', 1).isdigit() or not items[3].replace('-', '', 1).isdigit():
            raise ParsingError(f"Line {line_idx}: Coordinates must be valid integers.")
        hub["x"] = int(items[2])
        hub["y"] = int(items[3])

        if meta_data:
            meta_data = meta_data.strip("[]")
            meta_data = meta_data.split()
            for data in meta_data:
                if "=" not in data:
                    raise ParsingError(f"Line {line_idx}: Malformed metadata formatting near '{data}'.")
                key, value = data.split("=", 1)
                self._validate_metadata(key, value, line_idx)
                if key == "zone":
                    hub["type"] = value
                else:
                    hub[key] = int(value) if value.isdigit() else value

        self.end_hub = hub
        self.hubs.append(hub)

    def parse_connection(self, line: str, line_idx: int):
        if '[' in line:
            mandatory, meta_data = line.split("[", 1)
        else:
            mandatory = line
            meta_data = ""

        tokens = mandatory.split()
        if len(tokens) < 2:
            raise ParsingError(f"Line {line_idx}: Connection details are missing.")
        
        value = tokens[1]
        if "-" not in value:
            raise ParsingError(f"Line {line_idx}: Connection missing expected '-' separator notation.")
            
        items = value.split("-", 1)
        source, target = items[0], items[1]
        
        if source not in self.seen_names or target not in self.seen_names:
            raise ParsingError(f"Line {line_idx}: Connection links an undefined zone ('{source}' or '{target}').")

        # Handle duplicates bidirectionally via sorted tuple key validation
        conn_key = tuple(sorted([source, target]))
        if conn_key in self.seen_connections:
            raise ParsingError(f"Line {line_idx}: Connection between '{source}' and '{target}' is a duplicate.")
        self.seen_connections.add(conn_key)

        conn: Dict = {}
        conn[source] = target 

        if meta_raw := meta_data:
            meta_raw = meta_raw.strip("[]")
            meta_raw = meta_raw.split()
            for data in meta_raw:
                if "=" not in data:
                    raise ParsingError(f"Line {line_idx}: Malformed metadata formatting near '{data}'.")
                key, val = data.split("=", 1)
                self._validate_metadata(key, val, line_idx)
                conn[key] = int(val) if val.isdigit() else val

        self.connections.append(conn)

    def parse_map(self, path: str) -> Map:
        line_idx = 0
        has_parsed_drones = False

        with open(path, 'r') as fp:
            for line in fp:
                line_idx += 1
                line: str = line.strip()

                if line.startswith("#") or not line:
                    continue

                if not has_parsed_drones:
                    if line.startswith("nb_drones:"):
                        self.parse_drones(line, line_idx)
                        has_parsed_drones = True
                        continue
                    else:
                        raise ParsingError(f"Line {line_idx}: Structural error. 'nb_drones:' must appear on the first line.")

                if line.startswith("start_hub:"):
                    self.parse_start(line, line_idx)
                elif line.startswith("hub:"):
                    self.parse_hub(line, line_idx)
                elif line.startswith("end_hub:"):
                    self.parse_end(line, line_idx)
                elif line.startswith("connection:"):
                    self.parse_connection(line, line_idx)
                else:
                    raise ParsingError(f"Line {line_idx}: Unrecognized prefix syntax structure: '{line}'")

        if self.start_count != 1 or self.end_count != 1:
            raise ParsingError("Parsing Error: Map must contain exactly one 'start_hub:' and one 'end_hub:'.")

        map = Map(self.nb_drones, self.hubs, self.connections, self.start_hub, self.end_hub)
        map.init_map()

        return map