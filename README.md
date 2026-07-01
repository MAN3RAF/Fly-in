
*This project has been created as part of the 42 curriculum by <lsebar>.*

# Fly-in

## Description

Fly-in is a Python project about routing a fleet of drones through a graph of connected zones.

The goal is to:

- parse a custom map file,
- build a zone graph,
- find efficient drone routes,
- simulate movement turn by turn,
- respect zone and connection capacity constraints,
- provide a visual representation of the simulation.

The project focuses on minimizing the total number of turns needed to deliver every drone from the start zone to the end zone.

## Instructions

### Requirements

- Python 3.10 or later
- `pygame`

### Run

From the root of the repository:

```bash
python3 src/main.py
```

By default, the program loads the challenger map:

- `maps/challenger/01_the_impossible_dream.txt`

To use another map:

```bash
python3 src/main.py path/to/your_map.txt
```

### Input format

The map file describes:

- the number of drones,
- one start zone,
- one end zone,
- regular zones,
- bidirectional connections,
- optional metadata such as zone type, color, and capacities.

## Algorithm strategy

The implementation is structured in several stages:

1. **Parsing**

   - Read the input file.
   - Validate zone definitions, connections, and metadata.
   - Reject invalid syntax and conflicting definitions.
2. **Graph construction**

   - Build an object-oriented graph representation.
   - Store zones, connections, capacities, and movement costs.
3. **Pathfinding**

   - Compute candidate routes from start to end.
   - Prefer paths with lower movement cost and better throughput.
   - Avoid blocked zones and invalid connections.
4. **Drone allocation**

   - Distribute drones across available paths.
   - Balance load to reduce waiting time.
   - Respect zone occupancy and connection capacity rules.
5. **Simulation**

   - Advance drones turn by turn.
   - Handle movement delays for restricted zones.
   - Stop when all drones reach the end zone.

### Design choices

- The code is organized into separate modules for parsing, graph handling, algorithm logic, simulation, and rendering.
- The simulation uses turn-based scheduling to keep movement valid at every step.
- Path assignment is computed before the simulation to avoid unnecessary recalculation during runtime.

## Visual representation

The project uses a graphical renderer to display:

- zones and connections,
- drone positions,
- color metadata from the input file,
- simulation progress over time.

This improves readability by making path conflicts, congestion, and delivery progress easier to follow.

## Resources

### References

- Python documentation: https://docs.python.org/3/
- Pygame documentation: https://www.pygame.org/docs/
- Graph theory basics: https://en.wikipedia.org/wiki/Graph_theory
- Shortest path algorithms: https://en.wikipedia.org/wiki/Shortest_path_problem

### AI usage

AI was used to:

- draft the README structure,
- improve wording and readability,
- organize the project description into clear sections.

AI was not used as a source of truth for project logic. All implementation details must be reviewed and understood manually.

## Notes

- The project must remain typesafe and flake8-compatible.
- The input parser must fail cleanly on invalid maps.
- The simulation output must follow the required turn-by-turn format.
- Bonus performance depends on minimizing total turns and improving path allocation quality.
