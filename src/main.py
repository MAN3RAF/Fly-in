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

drone_image = pygame.image.load("drone.png")
renderer = Renderer(graph, sim, drone_image)


pygame.init()

screen = pygame.display.set_mode(
    (1920, 1080),
    pygame.RESIZABLE
)

font = pygame.font.Font(None, 48)

renderer = Renderer(
    graph,
    sim,
    drone_image,
    1920,
    1080
)

running = True
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                sim.run()
        if event.type == pygame.MOUSEWHEEL:
            renderer.zoom += event.y * 0.1
            renderer.zoom = max(0.5, min(3.0, renderer.zoom))

        elif event.type == pygame.VIDEORESIZE:

            screen = pygame.display.set_mode(
                (event.w, event.h),
                pygame.RESIZABLE
            )

            renderer.resize(
                event.w,
                event.h
            )

    keys = pygame.key.get_pressed()
    pan_speed = 10 * renderer.zoom
    if keys[pygame.K_LEFT]:
        renderer.pose_x += pan_speed
    if keys[pygame.K_RIGHT]:
        renderer.pose_x -= pan_speed
    if keys[pygame.K_UP]:
        renderer.pose_y += pan_speed
    if keys[pygame.K_DOWN]:
        renderer.pose_y -= pan_speed

    screen.fill((36, 36, 36))


    renderer.draw(screen, font)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()