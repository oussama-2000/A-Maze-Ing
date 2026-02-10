from collections import deque
from maze.coordinates import Coordinates
from maze.ascii_render import AsciiRenderer
import os
import time


class Solver:
    def solve_bfs(maze, entry, exit) -> list:
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

                if cell.walls[direction]:
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

        return Solver.generate_path(maze, parent, entry, exit)

    def generate_path(maze, parent, entry, exit) -> list:
        path = []
        current = exit

        while current != entry:
            x, y, direction = parent[current]
            path.append(direction)
            current = (x, y)

        path.reverse()
        return path

    def path_to_cells(maze, entry, path) -> list:
        x, y = entry
        cell_pos = [(x, y)]

        for direction in path:
            dx, dy = Coordinates.directions[direction]
            x += dx
            y += dy
            cell_pos.append((x, y))
        return cell_pos

    def show_path(maze, entry, exit, path, animate=True, show=True) -> None:
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
