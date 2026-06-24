import pygame
from parser import Parser
from zone import Zone
from graph import Graph
from drone import Drone
from connection import Connection


parser = Parser()

# zone = Zone("Man", (0, 1), "red", 1)

# drone = Drone(1, (1, 2), [], zone)

map = parser.parse_map("maps/hard/01_maze_nightmare.txt") #try/except.
graph = Graph(map)
graph.get_neighbors()
print(graph.neighbors)

# print(drone.coords, drone.destination.color, drone.id, drone.path)












# # Initialize all imported pygame modules
# pygame.init()

# # Create a display window
# screen = pygame.display.set_mode((800, 600))

# # Game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

# pygame.quit()