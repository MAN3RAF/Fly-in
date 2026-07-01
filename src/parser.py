from typing import List, Dict, Any
from zone import Zone
from drone import Drone
from connection import Connection
from exceptions import ParsingError
import pygame


class Map():
    def __init__(
                    self, nb_drones: int, hubs: List[Dict],
                    connections: List[Dict], start_hub: Dict,
                    end_hub: Dict) -> None:

            self.nb_drones = nb_drones         # int
            self.hubs = hubs                           # Dict
            self.connections = connections # List[dict[str, str]]
            self.zones: List[Zone] = []
            self.start_hub: Dict = start_hub
            self.end_hub: Dict = end_hub
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
                    if (not 'max_drones' in hub) and hub['name'] == self.end_hub['name']:
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
            # print(self.connections)

            for conn in self.connections:
                    source_name: str | None = None
                    target_name: str | None = None

                    for key, value in conn.items():
                            if key == "max_link_capacity":
                                    continue
                            
                            # print(key, value)

                            source_name = key
                            target_name = value
                            break

                    # if source_name is None or target_name is None:
                    #       raise ValueError(f"Invalid connection: {conn}")

                    # print(zones_by_name)
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
                            if self.start_hub['name'] == zone.name:
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
            self.coords: List[tuple] = []


    def parse_drones(self, line: str) -> None:

        parts = line.split()
        
        if not parts[0] == "nb_drones:":
            raise ParsingError("Invalid nb_drones.")

        if len(parts) != 2:
            raise ParsingError(
                f"Invalid nb_drones format. Expected 'nb_drones: <number>'.")

        value = parts[1].strip()


        try:
            int(value)
        except:
            raise ParsingError(
                f"nb_drones must be a positive integer."
            )

        if int(value) < 1:
            raise ParsingError(
                f"nb_drones must be a positive integer."
            )

        self.nb_drones = int(value)


    def parse_start(self, line: str) -> None:

        if self.start_hub:
            raise ParsingError("Start hub has already been defined.")

        mandatory = line
        meta_data = ""
        seen_keys = set()

        if "[" not in line and "]" not in line:
            pass

        elif "[" not in line or "]" not in line:
            raise ParsingError("Metadata block must start with '[' and end with ']'.")

        else:

            valid_keys = {
                "color",
                "zone",
                "max_drones",
            }

            valid_zones = {
                "normal",
                "restricted",
                "blocked",
                "priority",
            }

            open_idx = line.index("[")
            close_idx = line.index("]")

            if open_idx > close_idx:
                raise ParsingError("Opening '[' must appear before closing ']'.")

            if close_idx != len(line) - 1:
                raise ParsingError("Unexpected characters found after the metadata block.")

            if line[open_idx - 1] != ' ':
                raise ParsingError("Metadata block must be preceded by a space.")

            mandatory = line[:open_idx].strip()
            meta_data = line[open_idx + 1:close_idx]

            if meta_data.strip() == "":
                raise ParsingError("Metadata block cannot be empty.")

            for data in meta_data.split():

                if "=" not in data:
                    raise ParsingError(
                        "Invalid metadata entry. Expected the format 'key=value'."
                    )

                if data.count("=") != 1:
                    raise ParsingError(
                        f"Invalid metadata entry '{data}'. Expected exactly one '='."
                    )

                key, value = data.split("=")

                if key not in valid_keys:
                    raise ParsingError(
                        f"Unknown metadata key '{key}'."
                    )
                if key in seen_keys:
                    raise ParsingError(f"Duplicate metadata key '{key}'.")

                seen_keys.add(key)

                if value == "":
                    raise ParsingError(
                        f"Metadata key '{key}' is missing a value."
                    )

                if key == "zone":
                    if value not in valid_zones:
                        raise ParsingError(
                            f"Invalid zone type '{value}'. "
                            "Expected one of: normal, restricted, blocked, priority."
                        )

                    if value == "blocked":
                        raise ParsingError(
                            "The start hub cannot have zone type 'blocked'."
                        )

                elif key == "max_drones":
                    if not value.isdigit() or int(value) < 1:
                        raise ParsingError(
                            "'max_drones' must be a positive integer."
                        )

                    if int(value) < self.nb_drones:
                        raise ParsingError(
                            "'max_drones' cannot be smaller than the number of drones."
                        )

                elif key == "color":
                    try:
                        pygame.Color(value)
                    except:
                        raise ParsingError(
                            f"Unknown color '{value}'."
                        )

        items = mandatory.split()

        if len(items) != 4:
            raise ParsingError(
                "Invalid start_hub definition. Expected: "
                "'start_hub: <name> <x> <y> [metadata]'."
            )

        _, zone_name, x, y = items

        if "-" in zone_name:
            raise ParsingError(
                "Zone names cannot contain '-' characters."
            )
        
        for hub in self.hubs:
            if hub["name"] == zone_name:
                raise ParsingError(
                    "Zone names must be unique."
                )

        if (x, y) in self.coords:
            raise ParsingError(
                "Zone coordinates must be unique."
            )
        else:
            self.coords.append((x, y))

        try:
            x = float(x)
        except:
            raise ParsingError(
                "The x coordinate must be a valid number."
            )

        try:
            y = float(y)
        except:
            raise ParsingError(
                "The y coordinate must be a valid number."
            )

        hub: Dict = {}
        hub["name"] = items[1]
        hub["x"] = x
        hub["y"] = y

        if meta_data:
            meta_data = meta_data.strip("[]")
            meta_data = meta_data.split()
            for data in meta_data:
                key, value = data.split("=")
                hub[key] = int(value) if value.isdigit() else value

        self.start_hub = hub
        self.hubs.append(hub)


    def parse_hub(self, line: str) -> None:

        mandatory = line
        meta_data = ""
        seen_keys = set()

        if "[" not in line and "]" not in line:
            pass

        elif "[" not in line or "]" not in line:
            raise ParsingError("Metadata block must start with '[' and end with ']'.")

        else:

            valid_keys = {
                "color",
                "zone",
                "max_drones",
            }

            valid_zones = {
                "normal",
                "restricted",
                "blocked",
                "priority",
            }

            open_idx = line.index("[")
            close_idx = line.index("]")

            if open_idx > close_idx:
                raise ParsingError("Opening '[' must appear before closing ']'.")

            if close_idx != len(line) - 1:
                raise ParsingError("Unexpected characters found after the metadata block.")

            if line[open_idx - 1] != " ":
                raise ParsingError("Metadata block must be preceded by a space.")

            mandatory = line[:open_idx].strip()
            meta_data = line[open_idx + 1:close_idx]

            if meta_data.strip() == "":
                raise ParsingError("Metadata block cannot be empty.")

            for data in meta_data.split():

                if "=" not in data:
                    raise ParsingError(
                        "Invalid metadata entry. Expected the format 'key=value'."
                    )

                if data.count("=") != 1:
                    raise ParsingError(
                        f"Invalid metadata entry '{data}'. Expected exactly one '='."
                    )

                key, value = data.split("=")

                if key not in valid_keys:
                    raise ParsingError(
                        f"Unknown metadata key '{key}'."
                    )

                if key in seen_keys:
                    raise ParsingError(
                        f"Duplicate metadata key '{key}'."
                    )

                seen_keys.add(key)

                if value == "":
                    raise ParsingError(
                        f"Metadata key '{key}' is missing a value."
                    )

                if key == "zone":
                    if value not in valid_zones:
                        raise ParsingError(
                            f"Invalid zone type '{value}'. "
                            "Expected one of: normal, restricted, blocked, priority."
                        )

                elif key == "max_drones":
                    if not value.isdigit() or int(value) < 1:
                        raise ParsingError(
                            "'max_drones' must be a positive integer."
                        )

                elif key == "color":
                    try:
                        pygame.Color(value)
                    except:
                        raise ParsingError(
                            f"Unknown color '{value}'."
                        )

        items = mandatory.split()

        if len(items) != 4:
            raise ParsingError(
                "Invalid hub definition. Expected: "
                "'hub: <name> <x> <y> [metadata]'."
            )

        _, zone_name, x, y = items

        if "-" in zone_name:
            raise ParsingError(
                "Zone names cannot contain '-' characters."
            )

        for hub in self.hubs:
            if hub["name"] == zone_name:
                raise ParsingError(
                    "Zone names must be unique."
                )

        try:
            x = float(x)
        except:
            raise ParsingError(
                "The x coordinate must be a valid number."
            )

        try:
            y = float(y)
        except:
            raise ParsingError(
                "The y coordinate must be a valid number."
            )

        if (x, y) in self.coords:
            raise ParsingError(
                "Zone coordinates must be unique."
            )
        else:
            self.coords.append((x, y))

        hub: Dict = {}
        hub["name"] = zone_name
        hub["x"] = x
        hub["y"] = y

        if meta_data:
            for data in meta_data.split():
                key, value = data.split("=")

                if key == "zone":
                    hub["type"] = value
                else:
                    hub[key] = int(value) if value.isdigit() else value

        self.hubs.append(hub)

    def parse_end(self, line: str) -> None:

        if self.end_hub:
            raise ParsingError("End hub has already been defined.")

        mandatory = line
        meta_data = ""
        seen_keys = set()

        if "[" not in line and "]" not in line:
            pass

        elif "[" not in line or "]" not in line:
            raise ParsingError("Metadata block must start with '[' and end with ']'.")

        else:

            valid_keys = {
                "color",
                "zone",
                "max_drones",
            }

            valid_zones = {
                "normal",
                "restricted",
                "blocked",
                "priority",
            }

            open_idx = line.index("[")
            close_idx = line.index("]")

            if open_idx > close_idx:
                raise ParsingError("Opening '[' must appear before closing ']'.")

            if close_idx != len(line) - 1:
                raise ParsingError("Unexpected characters found after the metadata block.")

            if line[open_idx - 1] != " ":
                raise ParsingError("Metadata block must be preceded by a space.")

            mandatory = line[:open_idx].strip()
            meta_data = line[open_idx + 1:close_idx]

            if meta_data.strip() == "":
                raise ParsingError("Metadata block cannot be empty.")

            for data in meta_data.split():

                if "=" not in data:
                    raise ParsingError(
                        "Invalid metadata entry. Expected the format 'key=value'."
                    )

                if data.count("=") != 1:
                    raise ParsingError(
                        f"Invalid metadata entry '{data}'. Expected exactly one '='."
                    )

                key, value = data.split("=")

                if key not in valid_keys:
                    raise ParsingError(
                        f"Unknown metadata key '{key}'."
                    )

                if key in seen_keys:
                    raise ParsingError(
                        f"Duplicate metadata key '{key}'."
                    )

                seen_keys.add(key)

                if value == "":
                    raise ParsingError(
                        f"Metadata key '{key}' is missing a value."
                    )

                if key == "zone":
                    if value not in valid_zones:
                        raise ParsingError(
                            f"Invalid zone type '{value}'. "
                            "Expected one of: normal, restricted, blocked, priority."
                        )

                    if value == "blocked":
                        raise ParsingError(
                            "The end hub cannot have zone type 'blocked'."
                        )

                elif key == "max_drones":
                    if not value.isdigit() or int(value) < 1:
                        raise ParsingError(
                            "'max_drones' must be a positive integer."
                        )

                elif key == "color":
                    try:
                        pygame.Color(value)
                    except:
                        raise ParsingError(
                            f"Unknown color '{value}'."
                        )

        items = mandatory.split()

        if len(items) != 4:
            raise ParsingError(
                "Invalid end_hub definition. Expected: "
                "'end_hub: <name> <x> <y> [metadata]'."
            )

        _, zone_name, x, y = items

        if "-" in zone_name:
            raise ParsingError(
                "Zone names cannot contain '-' characters."
            )

        for hub in self.hubs:
            if hub["name"] == zone_name:
                raise ParsingError(
                    "Zone names must be unique."
                )

        try:
            x = float(x)
        except:
            raise ParsingError(
                "The x coordinate must be a valid number."
            )

        try:
            y = float(y)
        except:
            raise ParsingError(
                "The y coordinate must be a valid number."
            )

        if (x, y) in self.coords:
            raise ParsingError(
                "Zone coordinates must be unique."
            )
        else:
            self.coords.append((x, y))

        hub: Dict = {}
        hub["name"] = zone_name
        hub["x"] = x
        hub["y"] = y

        if meta_data:
            for data in meta_data.split():
                key, value = data.split("=")

                if key == "zone":
                    hub["type"] = value
                else:
                    hub[key] = int(value) if value.isdigit() else value

        self.end_hub = hub
        self.hubs.append(hub)

    def parse_connection(self, line: str) -> None:

        mandatory = line
        meta_data = ""
        seen_keys = set()

        if "[" not in line and "]" not in line:
            pass

        elif "[" not in line or "]" not in line:
            raise ParsingError("Metadata block must start with '[' and end with ']'.")

        else:

            open_idx = line.index("[")
            close_idx = line.index("]")

            if open_idx > close_idx:
                raise ParsingError("Opening '[' must appear before closing ']'.")

            if close_idx != len(line) - 1:
                raise ParsingError("Unexpected characters found after the metadata block.")

            if line[open_idx - 1] != " ":
                raise ParsingError("Metadata block must be preceded by a space.")

            mandatory = line[:open_idx].strip()
            meta_data = line[open_idx + 1:close_idx]

            if meta_data.strip() == "":
                raise ParsingError("Metadata block cannot be empty.")

            for data in meta_data.split():

                if "=" not in data:
                    raise ParsingError(
                        "Invalid metadata entry. Expected the format 'key=value'."
                    )

                if data.count("=") != 1:
                    raise ParsingError(
                        f"Invalid metadata entry '{data}'. Expected exactly one '='."
                    )

                key, value = data.split("=")

                if key != "max_link_capacity":
                    raise ParsingError(
                        f"Unknown metadata key '{key}'."
                    )

                if key in seen_keys:
                    raise ParsingError(
                        f"Duplicate metadata key '{key}'."
                    )

                seen_keys.add(key)

                if not value.isdigit() or int(value) < 1:
                    raise ParsingError(
                        "'max_link_capacity' must be a positive integer."
                    )

        parts = mandatory.split()

        if len(parts) != 2:
            raise ParsingError(
                "Invalid connection definition. Expected: "
                "'connection: <hub1>-<hub2> [metadata]'."
            )

        if parts[0] != "connection:":
            raise ParsingError(
                "Connection must start with 'connection:'."
            )

        if parts[1].count("-") != 1:
            raise ParsingError(
                "Connection must connect exactly two hubs using a single '-'."
            )

        source, target = parts[1].split("-")

        if source == "" or target == "":
            raise ParsingError(
                "Connection endpoints cannot be empty."
            )

        if source == target:
            raise ParsingError(
                "A hub cannot be connected to itself."
            )

        names = {hub["name"] for hub in self.hubs}

        if source not in names:
            raise ParsingError(f"Unknown hub '{source}'.")

        if target not in names:
            raise ParsingError(f"Unknown hub '{target}'.")

        for connection in self.connections:
            for a, b in connection.items():
                if a == "max_link_capacity":
                    continue

                if (a == source and b == target) or (a == target and b == source):
                    raise ParsingError(
                        "Duplicate connection."
                    )

        conn: Dict = {}
        conn[source] = target

        if meta_data:
            for data in meta_data.split():
                key, value = data.split("=")
                conn[key] = int(value)

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
                        self.parse_drones(line)
                        has_parsed_drones = True
                        continue
                    else:
                        raise ParsingError(f"'nb_drones: <nuber>' must appear on the first line.")

                if line.startswith("start_hub:"):
                    self.parse_start(line)
                elif line.startswith("hub:"):
                    self.parse_hub(line)
                elif line.startswith("end_hub:"):
                    self.parse_end(line)
                elif line.startswith("connection:"):
                    self.parse_connection(line)
                else:
                    raise ParsingError(f"Unrecognized prefix syntax structure: '{line}'")

        # if self.start_count != 1 or self.end_count != 1:
        #     raise ParsingError("Parsing Error: Map must contain exactly one 'start_hub:' and one 'end_hub:'.")
        if not self.start_hub:
              raise ParsingError("No Start_hub was provided.")
        if not self.end_hub:
              raise ParsingError("No end_hub was probided")

        map = Map(self.nb_drones, self.hubs, self.connections, self.start_hub, self.end_hub)
        map.init_map()

        return map


