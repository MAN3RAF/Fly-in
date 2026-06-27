# import pygame

from parser import Parser
from graph import Graph
# from renderer import Renderer
from algo import Algo

# pygame.init()

parser = Parser()

map_data = parser.parse_map(
    "maps/easy/01_linear_path.txt"
)

graph = Graph(map_data)
algo = Algo(graph)

paths = algo.get_all_paths(graph.zones)
# print(paths)
print(algo.get_usable_paths(paths))


# renderer = Renderer(graph)
# pygame.init()

# screen = pygame.display.set_mode(
#     (1920, 1080),
#     pygame.RESIZABLE
# )

# renderer = Renderer(
#     graph,
#     1920,
#     1080
# )

# running = True

# while running:

#     for event in pygame.event.get():

#         if event.type == pygame.QUIT:
#             running = False

#         elif event.type == pygame.VIDEORESIZE:

#             screen = pygame.display.set_mode(
#                 (event.w, event.h),
#                 pygame.RESIZABLE
#             )

#             renderer.resize(
#                 event.w,
#                 event.h
#             )

#     screen.fill((30, 30, 30))

#     renderer.draw(screen)

#     pygame.display.flip()

# pygame.quit()