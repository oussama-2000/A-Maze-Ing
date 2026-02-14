import random
import time
import os
from mazegen.cell import Cell
from mazegen.coordinates import Coordinates
from mazegen.ascii_render import AsciiRenderer
from typing import List, Optional, Tuple


class MazeGenerator:
    """
        Instantiation :
            instance_name = MazeGenerator(width, height)
            for example:
                maze = MazeGenerator(15, 17)
        Access :
            To access a maze solution you can do:
                grid = maze.grid()

    """
    def __init__(self, width: int, height: int,
                 seed: Optional[int] = None) -> None:

        self.width = width
        self.height = height
        self.grid: List[List[Cell]] = self.create_grid()
        self.bonuses: List = []
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randint(0, 10**6)

    def create_grid(self) -> list:
        """creates the maze grid (x, y)"""
        grid = []
        for _ in range(self.height):
            row = []
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

    def carve(self, x1: int, y1: int,
              x2: int, y2: int, direction: str
              ) -> None:
        """
        carve current cell wall and the neighbor cell oposit wall
        """
        current = self.get_cell(x1, y1)
        neighbor = self.get_cell(x2, y2)

        if current and neighbor:
            current.walls[direction] = False

            opp = Coordinates.opposite[direction]
            neighbor.walls[opp] = False

    def generate_DFS(self,
                     entry: Tuple[int, int],
                     exit: Tuple[int, int],
                     animate: bool = False,
                     perfect_flag: bool = False
                     ) -> None:
        """
        DFS generation algorithm to carve the maze
        """
        random.seed(str(self.seed))
        # when the 42 block should shows up
        if self.width >= 9 and self.height >= 7:
            blocked_positions = \
                Coordinates.forty_two_cells(self.width, self.height)
            for bx, by in blocked_positions:
                blocked_cell = self.get_cell(bx, by)
                if blocked_cell:
                    blocked_cell.blocked = True

        px, py = entry
        stack = [(px, py)]

        cell = self.get_cell(px, py)
        if cell:
            cell.visited = True

        renderer = AsciiRenderer(self, entry=entry, exit=exit)

        # For The First Animation
        if Cell.flag:
            Cell.flag = False
            os.system('cls' if os.name == 'nt' else 'clear')
            intor = "\033[1;36m!!! A-MAZE-ING !!!\nDirected By Amkhou And" \
                " Taoussi !\033[0m"

            for c in intor:
                print(c, end="", flush=True)
                time.sleep(.1)
            time.sleep(0.5)

        while stack:
            if animate:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(renderer.render(player_pos=stack[-1]))
                time.sleep(0.01)

            x, y = stack[-1]
            unvisited_neighbors = []

            for direction, (dx, dy) in Coordinates.directions.items():
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny):
                    neighbor = self.get_cell(nx, ny)
                    if neighbor and not neighbor.visited and\
                            not neighbor.blocked:
                        unvisited_neighbors.append((direction, nx, ny))

            if unvisited_neighbors:
                val = random.choice(unvisited_neighbors)
                chosen_dir, next_x, next_y = val
                self.carve(x, y, next_x, next_y, chosen_dir)

                if animate:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(renderer.render(player_pos=(next_x, next_y)))
                    time.sleep(0.01)

                neighbor_cell = self.get_cell(next_x, next_y)
                if neighbor_cell:
                    neighbor_cell.visited = True
                stack.append((next_x, next_y))
            else:
                stack.pop()

        if not perfect_flag:
            extra_walls_to_break = int((self.width * self.height) / 10)
            for _ in range(extra_walls_to_break):
                rx, ry = random.randint(0, self.width-1), \
                    random.randint(0, self.height-1)
                random_dir = random.choice(list(Coordinates.directions.keys()))
                dx, dy = Coordinates.directions[random_dir]
                nx, ny = rx + dx, ry + dy
                # to make sure if it's owned by 42 block
                curent_cell = self.get_cell(rx, ry)
                next_cell = self.get_cell(nx, ny)
                if curent_cell and next_cell:
                    if self.in_bounds(nx, ny) and not curent_cell.blocked and\
                            not next_cell.blocked:
                        self.carve(rx, ry, nx, ny, random_dir)

        if not animate:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(renderer.render())
