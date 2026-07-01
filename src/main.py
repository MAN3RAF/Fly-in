import sys
from typing import List

import pygame

from algo import Algo
from exceptions import FlyInError
from graph import Graph
from parser import InputParser
from renderer import Renderer
from simulation import Simulation


class MainProgram:
    def __init__(self, argv: List[str]) -> None:
        self.argv = argv
        self.path = ""

        if len(self.argv) != 2:
            if len(self.argv) == 1:
                self.path = "maps/challenger/01_the_impossible_dream.txt"
            else:
                raise ValueError("Input must be exactly 2 arguments.")
        else:
            self.path = argv[1]

    def main(self) -> None:
        parser = InputParser()
        map_data = parser.parse_map(self.path)

        graph = Graph(map_data)
        algo = Algo(graph)
        sim = Simulation(graph, algo)

        paths = algo.get_all_paths(graph.zones)
        sim.assign_drones_path(paths)

        try:
            drone_image = pygame.image.load("drone.png")
        except FileNotFoundError:
            raise FlyInError("Drone image was not found.")

        renderer = Renderer(
            graph,
            sim,
            drone_image,
            1920,
            1080,
        )
        renderer.fly_the_drones(sim)


if __name__ == "__main__":
    try:
        m = MainProgram(sys.argv)
        m.main()
    except FlyInError as e:
        print(e)
    # except Exception as e:
    #     print(f"Unixpected Error\n{e}")
