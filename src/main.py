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
# print(graph.connections)

# print(drone.coords, drone.destination.color, drone.id, drone.path)



import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 30)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (200, 200),
        20
    )

    text = font.render(
        "start",
        True,
        (255, 255, 255)
    )

    screen.blit(text, (180, 150))

    pygame.display.flip()

pygame.quit()






# # Initialize all imported pygame modules
# pygame.init()

# # Create a display window
# screen = pygame.display.set_mode((800, 600))

# # Game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         pygame.draw.line(...)
#         if event.type == pygame.QUIT:
#             running = False

# pygame.quit()