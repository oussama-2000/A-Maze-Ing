import random
import time
import os
from typing import List, Tuple, Optional
from mazegen.cell import Cell
from mazegen.coordinates import Coordinates
from mazegen.ascii_render import AsciiRenderer


class MazeGenerator:
    """
        Instantiation :
            instance_name = MazeGenerator(width, height)
            for example:
                maze = MazeGenerator(15, 17)
        Access :
            To access a maze solution you can do:
                solution_path = Solver.solve_bfs(instance_name, entry, exit)

    """
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.grid: List[List[Cell]] = self.create_grid()

    def create_grid(self) -> List[List[Cell]]:
        """creates the maze grid (x, y)"""
        grid: List[List[Cell]] = []
        for _ in range(self.height):
            row: List[Cell] = []
            for _ in range(self.width):
                row.append(Cell())
            grid.append(row)
        return grid

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Security check to ensure coordinates are within the grid.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """
        Retrieves the Cell object at the given (x, y) coordinates.
        """
        if not self.in_bounds(x, y):
            return None
        return self.grid[y][x]

    def carve(self, x1: int, y1: int, x2: int, y2: int,
              direction: str) -> None:
        current: Optional[Cell] = self.get_cell(x1, y1)
        neighbor: Optional[Cell] = self.get_cell(x2, y2)

        if current and neighbor:
            current.walls[direction] = False

            opp: str = Coordinates.opposite[direction]
            neighbor.walls[opp] = False

    def generate_DFS(self,
                     animate: bool = False,
                     entry: Optional[Tuple[int, int]] = None,
                     exit: Optional[Tuple[int, int]] = None,
                     perfect_flag: bool = False
                     ) -> None:

        # when the 42 block should shows up
        if self.width >= 9 and self.height >= 7:
            ftc = Coordinates.forty_two_cells(self.width, self.height)
            blocked_positions: List[Tuple[int, int]] = ftc
            for bx, by in blocked_positions:
                blocked_cell: Optional[Cell] = self.get_cell(bx, by)
                if blocked_cell:
                    blocked_cell.blocked = True

        if entry is None:
            return

        px, py = entry
        stack: List[Tuple[int, int]] = [(px, py)]

        cell: Optional[Cell] = self.get_cell(px, py)
        if cell:
            cell.visited = True

        renderer: AsciiRenderer = AsciiRenderer(self, entry=entry, exit=exit)

        while stack:
            if animate:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(renderer.render(player_pos=stack[-1]))
                time.sleep(0.01)

            x, y = stack[-1]
            unvisited_neighbors: List[Tuple[str, int, int]] = []

            for direction, (dx, dy) in Coordinates.directions.items():
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny):
                    neighbor: Optional[Cell] = self.get_cell(nx, ny)

                    if neighbor:
                        nb_short: bool = neighbor.blocked
                        nv_short: bool = neighbor.visited
                        if not nv_short and not nb_short:
                            unvisited_neighbors.append((direction, nx, ny))

            if unvisited_neighbors:
                val: Tuple[str, int, int] = random.choice(unvisited_neighbors)
                chosen_dir, next_x, next_y = val
                self.carve(x, y, next_x, next_y, chosen_dir)

                if animate:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(renderer.render(player_pos=(next_x, next_y)))
                    time.sleep(0.01)

                neighbor_cell: Optional[Cell] = self.get_cell(next_x, next_y)
                if neighbor_cell:
                    neighbor_cell.visited = True
                    stack.append((next_x, next_y))
            else:
                stack.pop()

        if not perfect_flag:
            extra_walls_to_break: int = int((self.width * self.height) / 10)
            for _ in range(extra_walls_to_break):
                rx: int = random.randint(0, self.width-1)
                ry: int = random.randint(0, self.height-1)

                random_val = random.choice(list(Coordinates.directions.keys()))
                random_dir: str = random_val
                dx, dy = Coordinates.directions[random_dir]
                nx, ny = rx + dx, ry + dy

                curent_cell: Optional[Cell] = self.get_cell(rx, ry)
                next_cell: Optional[Cell] = self.get_cell(nx, ny)
                if self.in_bounds(nx, ny) and curent_cell and next_cell:
                    if not curent_cell.blocked and not next_cell.blocked:
                        self.carve(rx, ry, nx, ny, random_dir)

        if not animate:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(renderer.render())
