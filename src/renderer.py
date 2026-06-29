import pygame
from typing import List, Dict
from zone import Zone
from graph import Graph
from simulation import Simulation

class Renderer:
    MARGIN = 50

    def __init__(
        self,
        graph: Graph,
        sim: Simulation,
        drone_image: pygame.Surface,
        width: int = 1920,
        height: int = 1080,
    ) -> None:

        self.graph = graph

        self.width = width
        self.height = height

        xs = [zone.coords[0] for zone in graph.zones]
        ys = [zone.coords[1] for zone in graph.zones]

        self.min_x = min(xs)
        self.max_x = max(xs)

        self.min_y = min(ys)
        self.max_y = max(ys)

        self.compute_scale()

        self.sim = sim

        self.zoom = 1
        self.pose_x = 0
        self.pose_y = 0

        self.drone_image = drone_image

    def compute_scale(self) -> None:

        map_width = max(self.max_x - self.min_x, 1)
        map_height = max(self.max_y - self.min_y, 1)

        scale_x = (
            self.width - 2 * self.MARGIN
        ) / map_width

        scale_y = (
            self.height - 2 * self.MARGIN
        ) / map_height

        self.scale = min(scale_x, scale_y)

    def resize(
        self,
        width: int,
        height: int
    ) -> None:

        self.width = width
        self.height = height

        self.compute_scale()

    def to_screen(
        self,
        zone: Zone
    ) -> tuple[int, int]:

        graph_center_x = (
            self.min_x + self.max_x
        ) / 2

        graph_center_y = (
            self.min_y + self.max_y
        ) / 2

        x = int(
            (zone.coords[0] - graph_center_x)
            * self.scale
            + self.width / 2
        )

        y = int(
            (zone.coords[1] - graph_center_y)
            * self.scale
            + self.height / 2
        )

        return x * self.zoom + self.pose_x, y * self.zoom + self.pose_y

    def get_color(
        self,
        zone: Zone
    ) -> pygame.Color:

        try:
            return pygame.Color(zone.color)
        except ValueError:
            return pygame.Color("white")

    def scale_down(self, drone_image: pygame.Surface) -> pygame.Surface:

        original_width, original_height = drone_image.get_size()

        scale_factor = 0.04

        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        scaled_drone = pygame.transform.scale(drone_image, (new_width, new_height))

        return scaled_drone
    
    def draw_tick(self, font, screen):
        text = font.render(f"Turns: {self.sim.current_turn}", True, (255, 255, 255))
        screen.blit(text, (1, 1))


    def draw(
        self,
        screen: pygame.Surface,
        font: pygame.font
    ) -> None:

        # Connections
        for conn in self.graph.connections:

            x1, y1 = self.to_screen(conn.zone_1)
            x2, y2 = self.to_screen(conn.zone_2)

            pygame.draw.line(
                screen,
                (255, 255, 255),
                (x1, y1),
                (x2, y2),
                int(3 * self.zoom)
            )
            # image = pygame.font.Font(None, 30).render(f"{conn.max_capacity}", True, (125, 0, 0))
            # screen.blit(image, ((x1 + x2 / 2), (y1 + y2 / 2)))

        # Zones
        for zone in self.graph.zones:

            x, y = self.to_screen(zone)

            zone_color = self.get_color(zone)

            pygame.draw.circle(
                screen,
                pygame.Color("white"),
                (x, y),
                22 * self.zoom
            )

            pygame.draw.circle(
                screen,
                zone_color,
                (x, y),
                20 * self.zoom
            )
            image = pygame.font.Font(None, 25).render(f"{zone.name}", True, (255, 255, 255))
            screen.blit(image, (x + 5, y + 20))

        # --- DRONES ADDITION ---
        for drone in self.graph.drones:
            # Calculate position based on state
            if drone.in_transit:
                next_zone = drone.get_next_zone()
                if next_zone is not None:
                    x1, y1 = self.to_screen(drone.current_zone)
                    x2, y2 = self.to_screen(next_zone)
                    # Midpoint interpolation for flying transits
                    drone_x = int((x1 + x2) / 2)
                    drone_y = int((y1 + y2) / 2)
                else:
                    drone_x, drone_y = self.to_screen(drone.current_zone)
            else:
                drone_x, drone_y = self.to_screen(drone.current_zone)

            image = self.scale_down(self.drone_image)
            image_rect = image.get_rect(center=(drone_x, drone_y))
            screen.blit(image, (image_rect))

            text_surface = pygame.font.Font(None, 50).render(f"{drone.id}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(drone_x, drone_y))
            screen.blit(text_surface, text_rect)

        self.draw_tick(font, screen)




