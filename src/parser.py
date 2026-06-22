from typing import List, Dict, Any
from graph import Graph


class Parser():
	def __init__(self) -> None:
		self.nb_drones: int = 0
		self.hubs: List[Dict] = []
		self.connections: List[Dict] = []
		# self.start_hub: Dict = {}
		# self.hub: Dict = {}
		# self.end_hub: Dict = {}


	def parse_drones(self, line: str) -> None:

		_, second = line.split(":")
		second = second.strip()

		if not second.isdigit():
			raise ValueError("[ERROR] Invalid Number of drones!")
		if int(second) < 1:
			raise ValueError("[ERROR] Invalid Number of drones!")

		self.nb_drones = second

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

	def parse_map(self, path: str) -> Graph:

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

		graph = Graph(self.nb_drones, self.hubs, self.connections)

		return graph
