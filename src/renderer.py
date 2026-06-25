import pygame
from zone import Zone
from graph import Graph


class Renderer:
    WIDTH = 1920
    HEIGHT = 1080
    MARGIN = 50

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

        xs = [zone.coords[0] for zone in graph.zones]
        ys = [zone.coords[1] for zone in graph.zones]

        self.min_x = min(xs)
        self.max_x = max(xs)

        self.min_y = min(ys)
        self.max_y = max(ys)

        map_width = max(self.max_x - self.min_x, 1)
        map_height = max(self.max_y - self.min_y, 1)

        scale_x = (self.WIDTH - 2 * self.MARGIN) / map_width
        scale_y = (self.HEIGHT - 2 * self.MARGIN) / map_height

        self.scale = min(scale_x, scale_y)

        graph_width = map_width * self.scale
        graph_height = map_height * self.scale

        self.offset_x = (self.WIDTH - graph_width) / 2
        self.offset_y = (self.HEIGHT - graph_height) / 2

    def to_screen(self, zone: Zone) -> tuple[int, int]:

        graph_center_x = (self.min_x + self.max_x) / 2
        graph_center_y = (self.min_y + self.max_y) / 2

        x = int(
            (zone.coords[0] - graph_center_x)
            * self.scale
            + self.WIDTH / 2
        )

        y = int(
            (zone.coords[1] - graph_center_y)
            * self.scale
            + self.HEIGHT / 2
        )

        return x, y

    def draw(self, screen: pygame.Surface) -> None:

        for conn in self.graph.connections:

            x1, y1 = self.to_screen(conn.zone_1)
            x2, y2 = self.to_screen(conn.zone_2)

            pygame.draw.line(
                screen,
                (255, 255, 255),
                (x1, y1),
                (x2, y2),
                3
            )

        for zone in self.graph.zones:

            x, y = self.to_screen(zone)
            
            zone_color = self.get_color(zone)

            # Outline
            outline = pygame.Color("white")
            pygame.draw.circle(
                screen,
                outline,      # black outline
                (x, y),
                22              # larger radius
            )

            # Zone
            pygame.draw.circle(
                screen,
                zone_color,
                (x, y),
                20
            )

    def get_color(self, zone: Zone) -> pygame.Color:
        try:
            return pygame.Color(zone.color)
        except ValueError:
            return pygame.Color("white")