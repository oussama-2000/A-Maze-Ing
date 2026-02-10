from collections import deque
from mazegen.coordinates import Coordinates
from mazegen.ascii_render import AsciiRenderer
import os
import time
from typing import List, Tuple, Dict, Any


class Solver:
    @staticmethod
    def solve_bfs(maze: Any, entry: Tuple[int, int],
                  exit: Tuple[int, int]) -> List[str]:
        start = entry
        goal = exit

        queue = deque([start])
        visited = {start}
        parent: Dict[Tuple[int, int], Tuple[int, int, str]] = {}

        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                break

            cell = maze.get_cell(x, y)
            if not cell:
                continue

            for direction, (dx, dy) in Coordinates.directions.items():
                if cell.walls[direction]:
                    continue

                nx, ny = x + dx, y + dy

                if not maze.in_bounds(nx, ny):
                    continue

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y, direction)
                    queue.append((nx, ny))

        return Solver.generate_path(maze, parent, entry, exit)

    @staticmethod
    def generate_path(maze: Any, parent: Dict[Tuple[int, int],
                                              Tuple[int, int, str]],
                      entry: Tuple[int, int],
                      exit: Tuple[int, int]) -> List[str]:
        path = []
        current = exit

        while current != entry:
            x, y, direction = parent[current]
            path.append(direction)
            current = (x, y)

        path.reverse()
        return path

    @staticmethod
    def path_to_cells(maze: Any, entry: Tuple[int, int],
                      path: List[str]) -> List[Tuple[int, int]]:
        x, y = entry
        cell_pos = [(x, y)]

        for direction in path:
            dx, dy = Coordinates.directions[direction]
            x += dx
            y += dy
            cell_pos.append((x, y))
        return cell_pos

    @staticmethod
    def show_path(maze: Any, entry: Tuple[int, int], exit: Tuple[int, int],
                  path: List[Tuple[int, int]], animate: bool = True,
                  show: bool = True) -> None:
        renderer = AsciiRenderer(maze, entry, exit)

        if animate:
            visible_path: List[Tuple[int, int]] = []

            for cell in path:
                visible_path.append(cell)
                os.system('cls' if os.name == 'nt' else 'clear')
                print(renderer.render(path=visible_path, show=show))
                if show:
                    time.sleep(0.05)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(renderer.render(path=list(path), show=show))
