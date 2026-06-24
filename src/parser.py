from typing import List, Dict, Any
from zone import Zone
from drone import Drone
from connection import Connection


class Map():
	def __init__(
			self, nb_drones: int, hubs: List[Dict],
			connections: List[Dict], start_hub: Zone,
			end_hub: Zone) -> None:
		
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
					coords: tuple[int] = zone.coords
			for zone in self.zones:
				if "goal" in zone.name:
					end_zone = zone

			
			drone = Drone(i, coords, [], end_zone)
			self.drones.append(drone)


class Parser():
	def __init__(self) -> None:
		self.nb_drones: int = 0
		self.hubs: List[Dict] = []
		self.connections: List[Dict[str, str]] = []
		self.start_hub: Dict = {}
		self.end_hub: Dict = {}


	def parse_drones(self, line: str) -> None:

		_, second = line.split(":")
		second = second.strip()

		if not second.isdigit():
			raise ValueError("[ERROR] Invalid Number of drones!")
		if int(second) < 1:
			raise ValueError("[ERROR] Invalid Number of drones!")

		self.nb_drones = int(second)


	def parse_start(self, line: str) -> None:

		if '[' in line:
			mandatory, meta_data = line.split("[")
		else:
			mandatory = line
			meta_data = ""

		# items: List = []
		items = mandatory.split()
		hub: Dict = {}
		hub["name"] = items[1]
		hub["x"] = int(items[2]) #Later parse
		hub["y"] = int(items[3])	#Later parse

		if meta_data:
			meta_data = meta_data.strip("[]")
			meta_data = meta_data.split()
			for data in meta_data:
				key, value = data.split("=")
				hub[key] = int(value) if value.isdigit() else value

		self.start_hub = hub
		self.hubs.append(hub)


	def parse_hub(self, line: str) -> None:
		
		if '[' in line:
			mandatory, meta_data = line.split("[")
		else:
			mandatory = line
			meta_data = ""

		# items: List = []
		items = mandatory.split()
		hub: Dict = {}
		hub["name"] = items[1]
		hub["x"] = int(items[2]) #Later parse
		hub["y"] = int(items[3]) #Later parse

		if meta_data:
			meta_data = meta_data.strip("[]")
			meta_data = meta_data.split()
			for data in meta_data:
				key, value = data.split("=")
				hub[key] = int(value) if value.isdigit() else value

		self.hubs.append(hub)


	def parse_end(self, line: str) -> None:
		
		if '[' in line:
			mandatory, meta_data = line.split("[")
		else:
			mandatory = line
			meta_data = ""

		# items: List = []
		items = mandatory.split()
		hub: Dict = {}
		hub["name"] = items[1]
		hub["x"] = int(items[2]) #Later parse
		hub["y"] = int(items[3]) #Later parse

		if meta_data:
			meta_data = meta_data.strip("[]")
			meta_data = meta_data.split()
			for data in meta_data:
				key, value = data.split("=")
				hub[key] = int(value) if value.isdigit() else value

		self.end_hub = hub
		self.hubs.append(hub)


	def parse_connection(self, line: str):

		if '[' in line:
			mandatory, meta_data = line.split("[")
		else:
			mandatory = line
			meta_data = ""

		# items: List = []
		_, value = mandatory.split()
		items = value.split("-")
		conn: Dict = {}
		conn[items[0]] = items[1] #Later parse

		if meta_data:
			meta_data = meta_data.strip("[]")
			meta_data = meta_data.split()
			for data in meta_data:
				key, value = data.split("=")
				conn[key] = int(value) if value.isdigit() else value

		self.connections.append(conn)


	def parse_map(self, path: str) -> Map:

		i = 0
		with open(path, 'r') as fp:
			for line in fp:
				line: str = line.strip()

				if line.startswith("#") or not line:
					continue

				if i == 0 and line.startswith("nb_drones:"):
					self.parse_drones(line)
				elif i == 0 and not line.startswith("nb_drones:"):
					raise ValueError("[ERROR] nb_drones was not found!")

				if line.startswith("start_hub:"):
					self.parse_start(line)
					
				
				if line.startswith("hub:"):
					self.parse_hub(line)
				
				if line.startswith("end_hub:"):
					self.parse_end(line)
				
				if line.startswith("connection:"):
					self.parse_connection(line)

				i += 1

		map = Map(self.nb_drones, self.hubs, self.connections, self.start_hub, self.end_hub)
		map.init_map()

		return map
