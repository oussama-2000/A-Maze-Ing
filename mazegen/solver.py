from mazegen.coordinates import Coordinates
from mazegen.ascii_render import AsciiRenderer
from typing import List, Tuple, Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from mazegen.generator import MazeGenerator
import os
import time


class Solver:
    """
    this class represent the maze solve
    for generate the solution path
    """
    @staticmethod
    def solve_bfs(
                  maze: "MazeGenerator",
                  entry: Tuple[int, int],
                  exit: Tuple[int, int]
                  ) -> List:
        """
        Docstring for solve_bfs
        the method that responsible for solve the maze using BFS algorithm
        :param maze: the maze object
        :type maze: "MazeGenerator"
        :param entry: the maze entry
        :type entry: Tuple[int, int]
        :param exit: the maze exit
        :type exit: Tuple[int, int]
        :return: it returns a list of directions that solve the maze
            using the helper function generate_path
        :rtype: List
        """

        start = entry
        goal = exit

        cells_to_explore = [start]
        visited = set([start])
        parent = {}

        while cells_to_explore:
            x, y = cells_to_explore.pop(0)

            if (x, y) == goal:
                break

            cell = maze.get_cell(x, y)

            for direction, (dx, dy) in Coordinates.directions.items():

                if cell and cell.walls[direction]:
                    continue

                nx, ny = x + dx, y + dy

                if not maze.in_bounds(nx, ny):
                    continue

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y, direction)
                    cells_to_explore.append((nx, ny))

        return Solver.generate_path(
                            parent,
                            entry,
                            exit
                            )

    @staticmethod
    def generate_path(
                parent: Dict,
                entry: Tuple[int, int],
                exit: Tuple[int, int]
                ) -> List:
        """
        Docstring for generate_path
        helper function for extract directions from the given dictionary
        :param parent: dictionary as this form:
         {'reached cell(x, y)' : ('from which cell(x, y), 'wich direction') }
        :type parent: Dict
        :param entry: maze entry
        :type entry: Tuple[int, int]
        :param exit: maze exit
        :type exit: Tuple[int, int]
        :return: it return a list of the solution directions
        :rtype: List
        """

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
        """
        Docstring for path_to_cells
        this method used to return solution directions into
        reel maze coordinates to move
        :param entry: maze entry
        :type entry: Tuple[int, int]
        :param path: list of solution directions
        :type path: List
        """

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
        """
        Docstring for show_path
        shows the solution path on the maze using the AsciiRender class
        :param maze: the maze object
        :type maze: "MazeGenerator"
        :param entry: the maze entry
        :type entry: Tuple[int, int]
        :param exit: the maze exit
        :type exit: Tuple[int, int]
        :param path: the solution path coordinates
        :type path: List
        :param animate: flage for animate when showing the path or not
        :type animate: bool
        :param show: show or hide
        :type show: bool
        """

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
