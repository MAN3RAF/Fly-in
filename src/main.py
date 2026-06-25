import pygame

from parser import Parser
from graph import Graph
from renderer import Renderer


pygame.init()

parser = Parser()

map_data = parser.parse_map(
    "maps/challenger/01_the_impossible_dream.txt"
)

graph = Graph(map_data)
graph.get_neighbors()

renderer = Renderer(graph)

screen = pygame.display.set_mode(
    (Renderer.WIDTH, Renderer.HEIGHT)
)

pygame.display.set_caption("Fly-in")

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((25, 25, 25))

    renderer.draw(screen)

    pygame.display.flip()

pygame.quit()