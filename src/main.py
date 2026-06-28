import pygame
from parser import Parser
from graph import Graph
from renderer import Renderer
from algo import Algo
from simulation import Simulation
import sys

parser = Parser()


map_data = parser.parse_map(sys.argv[1])

graph = Graph(map_data)
algo = Algo(graph)
sim = Simulation(graph, algo)

paths = algo.get_all_paths(graph.zones)
# print(paths)
sim.assign_drones_path(paths)


renderer = Renderer(graph)


pygame.init()

screen = pygame.display.set_mode(
    (1920, 1080),
    pygame.RESIZABLE
)

renderer = Renderer(
    graph,
    1920,
    1080
)

running = True
tick = "0"

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                sim.run_turn()
                print(sim.current_turn)


        elif event.type == pygame.VIDEORESIZE:

            screen = pygame.display.set_mode(
                (event.w, event.h),
                pygame.RESIZABLE
            )

            renderer.resize(
                event.w,
                event.h
            )

    screen.fill((36, 36, 36))


    renderer.draw(screen)

    pygame.display.flip()

pygame.quit()