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

        self.nb_drones = nb_drones     # int
        self.hubs = hubs               # Dict
        self.connections = connections # List[dict[str, str]]
        self.zones: List[Zone] = []
        self.start_hub: Dict = None
        self.end_hub: Dict = None
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


class InputParser():
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.hubs: List[Dict] = []
        self.connections: List[Dict[str, str]] = []
        self.start_hub: Dict = None
        self.end_hub: Dict = None
        
        # Validation trackers for VII.4 constraints
        self.seen_names = set()
        self.seen_connections = set()
        self.start_count = 0
        self.end_count = 0

    def _is_valid_int(self, value_str: str) -> bool:
        """Handles negative/positive integer parsing, rejecting signed zeros."""
        cleaned = value_str.strip()
        # Reject signed zeros like -0, +0, -00, +00, etc.
        if (cleaned.startswith('-') or cleaned.startswith('+')) and all(
            c == '0' for c in cleaned[1:]
        ):
            return False
        if cleaned.startswith(('-', '+')):
            cleaned = cleaned[1:]
        return cleaned.isdigit()

    def _validate_metadata(
        self, key: str, value: str, line_idx: int, is_connection: bool
    ) -> None:
        """Enforces type and capacity constraints on metadata blocks."""
        if is_connection:
            valid_keys = {"max_link_capacity"}
        else:
            valid_keys = {"zone", "color", "max_drones"}

        if key not in valid_keys:
            raise ParsingError(
                f"Line {line_idx}: Invalid metadata key '{key}'. "
                f"Allowed keys are {valid_keys}."
            )

        if key == "zone":
            if value not in {"normal", "blocked", "restricted", "priority"}:
                raise ParsingError(
                    f"Line {line_idx}: Invalid zone type '{value}'. "
                    "Must be normal, blocked, restricted, or priority."
                )
        if key == "color":
            if not value or any(c in value for c in "[]= "):
                raise ParsingError(
                    f"Line {line_idx}: Invalid color value '{value}'."
                )
        if key in ("max_drones", "max_link_capacity"):
            if not value.isdigit() or int(value) <= 0:
                raise ParsingError(
                    f"Line {line_idx}: Capacity values must be positive "
                    f"integers. Got '{value}'."
                )

    def _parse_meta_block(
        self, meta_data: str, line_idx: int, is_connection: bool
    ) -> Dict:
        """Safely tokens out and validates any trailing bracket string."""
        if not meta_data.startswith("[") or not meta_data.endswith("]"):
            raise ParsingError(
                f"Line {line_idx}: Malformed metadata framing syntax."
            )
            
        content = meta_data[1:-1].strip()
        if not content:
            raise ParsingError(
                f"Line {line_idx}: Empty metadata block '[]'."
            )

        meta_dict = {}
        chunks = content.split()
        for chunk in chunks:
            if "=" not in chunk or chunk.startswith("=") or chunk.endswith("="):
                raise ParsingError(
                    f"Line {line_idx}: Malformed metadata formatting "
                    f"near '{chunk}'."
                )
            
            key, value = chunk.split("=", 1)
            key = key.strip()
            value = value.strip()
            
            self._validate_metadata(key, value, line_idx, is_connection)
            if key == "zone":
                meta_dict["type"] = value
            else:
                meta_dict[key] = int(value) if value.isdigit() else value
        return meta_dict

    def validate_name(self, name: str, line_idx: int) -> None:
        """Enforces name uniqueness and character constraints."""
        if not name or "-" in name or " " in name or "[" in name or "]" in name:
            raise ParsingError(
                f"Line {line_idx}: Zone name '{name}' contains "
                "invalid characters."
            )
        if name in self.seen_names:
            raise ParsingError(
                f"Line {line_idx}: Zone name '{name}' is not unique."
            )
        self.seen_names.add(name)

    def parse_drones(self, line: str, line_idx: int) -> None:
        """Parses the nb_drones line and validates positive integer format."""

        parts = line.split()

        if len(parts) != 2:
            raise ParsingError(
                f"Line {line_idx}: Invalid nb_drones")

        value = parts[1].strip()

        if not value.isdigit() or int(value) < 1:
            raise ParsingError(
                f"Line {line_idx}: nb_drones must be a positive integer."
            )

        self.nb_drones = int(value)

    def parse_start(self, line: str, line_idx: int) -> None:
        """Parses the start_hub definition and metadata."""

        if self.start_hub:
            raise ParsingError("start zone allreay defined") #have to be edited

        # if self.start_count > 1:
        #     raise ParsingError(
        #         f"Line {line_idx}: Multiple start_hubs defined."
        #     )

        line = line.strip()
        mandatory = line
        meta_data = ""

# No metadata
        if "[" not in line and "]" not in line:
            pass

        # Malformed cases
        elif line.count("[") != 1 or line.count("]") != 1:
            raise ValueError("Invalid metadata: expected exactly one '[' and one ']'.")

        # Valid metadata
        else:
            open_idx = line.index("[")
            close_idx = line.index("]")

            if open_idx > close_idx:
                raise ValueError("']' appears before '['.")

            if close_idx != len(line) - 1:
                raise ValueError("Unexpected characters after ']'.")

            mandatory = line[:open_idx].rstrip()
            meta_data = line[open_idx + 1:close_idx]

        items = mandatory.split()
        if len(items) != 4:
            raise ParsingError(
                f"Line {line_idx}: Malformed start_hub line. "
                "Expected prefix, name, and coordinates."
            )
        # if items[0] != "start_hub:":
        #     raise ParsingError(
        #         f"Line {line_idx}: Invalid prefix '{items[0]}'. "
        #         "Expected 'start_hub:'."
        #     )
            
        hub: Dict = {}
        hub["name"] = items[1]
        self.validate_name(hub["name"], line_idx)
        
        if not self._is_valid_int(items[2]) or not self._is_valid_int(items[3]):
            raise ParsingError(
                f"Line {line_idx}: Coordinates must be valid integers."
            )
        hub["x"] = int(items[2])
        hub["y"] = int(items[3])

        if meta_data:
            meta_dict = self._parse_meta_block(
                meta_data, line_idx, is_connection=False
            )
            for k, v in meta_dict.items():
                hub[k] = v

        self.start_hub = hub
        self.hubs.append(hub)

    def parse_hub(self, line: str, line_idx: int) -> None:
        """Parses a hub definition and metadata."""
        if '[' in line:
            idx = line.find('[')
            mandatory = line[:idx]
            meta_data = line[idx:].strip()
        else:
            mandatory = line
            meta_data = ""

        items = mandatory.split()
        if len(items) != 4:
            raise ParsingError(
                f"Line {line_idx}: Malformed hub line. "
                "Expected prefix, name, and coordinates."
            )
        if items[0] != "hub:":
            raise ParsingError(
                f"Line {line_idx}: Invalid prefix '{items[0]}'. "
                "Expected 'hub:'."
            )
            
        hub: Dict = {}
        hub["name"] = items[1]
        self.validate_name(hub["name"], line_idx)
        
        if not self._is_valid_int(items[2]) or not self._is_valid_int(items[3]):
            raise ParsingError(
                f"Line {line_idx}: Coordinates must be valid integers."
            )
        hub["x"] = int(items[2])
        hub["y"] = int(items[3])

        if meta_data:
            meta_dict = self._parse_meta_block(
                meta_data, line_idx, is_connection=False
            )
            for k, v in meta_dict.items():
                hub[k] = v

        self.hubs.append(hub)

    def parse_end(self, line: str, line_idx: int) -> None:
        """Parses the end_hub definition and metadata."""
        self.end_count += 1
        if self.end_count > 1:
            raise ParsingError(
                f"Line {line_idx}: Multiple end_hubs defined. "
                "Exactly one is required."
            )

        if '[' in line:
            idx = line.find('[')
            mandatory = line[:idx]
            meta_data = line[idx:].strip()
        else:
            mandatory = line
            meta_data = ""

        items = mandatory.split()
        if len(items) != 4:
            raise ParsingError(
                f"Line {line_idx}: Malformed end_hub line. "
                "Expected prefix, name, and coordinates."
            )
        if items[0] != "end_hub:":
            raise ParsingError(
                f"Line {line_idx}: Invalid prefix '{items[0]}'. "
                "Expected 'end_hub:'."
            )
            
        hub: Dict = {}
        hub["name"] = items[1]
        self.validate_name(hub["name"], line_idx)
        
        if not self._is_valid_int(items[2]) or not self._is_valid_int(items[3]):
            raise ParsingError(
                f"Line {line_idx}: Coordinates must be valid integers."
            )
        hub["x"] = int(items[2])
        hub["y"] = int(items[3])

        if meta_data:
            meta_dict = self._parse_meta_block(
                meta_data, line_idx, is_connection=False
            )
            for k, v in meta_dict.items():
                hub[k] = v

        self.end_hub = hub
        self.hubs.append(hub)

    def parse_connection(self, line: str, line_idx: int) -> None:
        """Parses a connection definition and metadata."""
        if '[' in line:
            idx = line.find('[')
            mandatory = line[:idx]
            meta_data = line[idx:].strip()
        else:
            mandatory = line
            meta_data = ""

        splited = mandatory.split()
        if len(splited) != 2:
            raise ParsingError(
                f"Line {line_idx}: Malformed connection line. "
                "Expected prefix and connection details."
            )
        if splited[0] != "connection:":
            raise ParsingError(
                f"Line {line_idx}: Invalid prefix '{splited[0]}'. "
                "Expected 'connection:'."
            )

        value = splited[1]
        if "-" not in value or value.startswith("-") or value.endswith("-"):
            raise ParsingError(
                f"Line {line_idx}: Connection missing expected '-' separator."
            )
        if value.count("-") != 1:
            raise ParsingError(
                f"Line {line_idx}: Connection must link exactly two zones "
                "with a single '-' character."
            )
            
        items = value.split("-", 1)
        source, target = items[0], items[1]
        
        if source not in self.seen_names or target not in self.seen_names:
            raise ParsingError(
                f"Line {line_idx}: Connection links an undefined zone "
                f"('{source}' or '{target}')."
            )

        conn_key = tuple(sorted([source, target]))
        if conn_key in self.seen_connections:
            raise ParsingError(
                f"Line {line_idx}: Connection between '{source}' and "
                f"'{target}' is a duplicate."
            )
        self.seen_connections.add(conn_key)

        conn: Dict = {}
        conn[source] = target 

        if meta_data:
            meta_dict = self._parse_meta_block(
                meta_data, line_idx, is_connection=True
            )
            for k, v in meta_dict.items():
                conn[k] = v

        self.connections.append(conn)

    def parse_map(self, path: str) -> Map:

        has_parsed_drones = False

        with open(path, 'r') as fp:
            for line_idx, line in enumerate(fp, 1):
                line: str = line.strip()

                if line.startswith("#") or not line:
                    continue
                if "#" in line:
                    line = line.split("#")[0].strip()

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