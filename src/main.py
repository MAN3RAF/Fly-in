import pygame
from parser import Parser
from zone import Zone
from graph import Graph
from drone import Drone
from connection import Connection


parser = Parser()

graph = parser.parse_map("maps/easy/01_linear_path.txt")

print(graph.get_hubs()[1].name)
print(graph.get_connections())
print(graph.get_drones())













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