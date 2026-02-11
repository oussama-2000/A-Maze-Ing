from collections import deque
from mazegen.coordinates import Coordinates
from mazegen.ascii_render import AsciiRenderer
from typing import List, Tuple, Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from mazegen.generator import MazeGenerator
import os
import time


class Solver:

    @staticmethod
    def solve_bfs(
                  maze: "MazeGenerator",
                  entry: Tuple[int, int],
                  exit: Tuple[int, int]
                  ) -> List:
        start = entry
        goal = exit

        queue = deque([start])
        visited = set([start])
        parent = {}
        # {'reached cell(x, y)' : ('from which cell(x, y), 'wich direction') }

        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                break

            cell = maze.get_cell(x, y)

            # iterating directions to expand neighbors
            for direction, (dx, dy) in Coordinates.directions.items():

                if cell and cell.walls[direction]:
                    continue  # wall is closed

                # compute neighbor coordinates
                nx, ny = x + dx, y + dy

                if not maze.in_bounds(nx, ny):
                    continue

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y, direction)
                    queue.append((nx, ny))
                    # add it to queue for next exploration

        return Solver.generate_path(
                            maze,
                            parent,
                            entry,
                            exit
                            )

    @staticmethod
    def generate_path(
                maze: "MazeGenerator",
                parent: Dict,
                entry: Tuple[int, int],
                exit: Tuple[int, int]
                ) -> List:
        path = []
        current = exit

        while current != entry:
            x, y, direction = parent[current]
            path.append(direction)
            current = (x, y)

        path.reverse()
        return path

    @staticmethod
    def path_to_cells(
                entry: Tuple[int, int],
                path: List
                ) -> List:

        x, y = entry
        cell_pos = [(x, y)]

        for direction in path:
            dx, dy = Coordinates.directions[direction]
            x += dx
            y += dy
            cell_pos.append((x, y))
        return cell_pos

    @staticmethod
    def show_path(
            maze: "MazeGenerator",
            entry: Tuple[int, int],
            exit: Tuple[int, int],
            path: List,
            animate: bool = True,
            show: bool = True
            ) -> None:

        renderer = AsciiRenderer(maze, entry, exit)

        if animate:
            visible_path = set()

            for cell in path:
                visible_path.add(cell)
                os.system('cls' if os.name == 'nt' else 'clear')
                print(renderer.render(path=visible_path, show=show))
                if show:
                    time.sleep(0.05)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(renderer.render(path=set(path), show=show))
