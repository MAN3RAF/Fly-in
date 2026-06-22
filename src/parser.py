class Parser():
	def __init__(self):
		pass


	def parse_map(self, fp):

		for line in fp:
			print(line, end=" ")


p = Parser()

with open("maps/easy/01_linear_path.txt", 'r') as fp:
	p.parse_map(fp)
