import random
import time
import os
from mazegen.cell import Cell
from mazegen.coordinates import Coordinates
from mazegen.ascii_render import AsciiRenderer


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:

        self.width = width
        self.height = height
        self.grid = self.create_grid()

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

    def get_cell(self, x: int, y: int):
        """
        Retrieves the Cell object at the given (x, y) coordinates.
        """
        if not self.in_bounds(x, y):
            return None
        return self.grid[y][x]

    def carve_passage(self, x1, y1, x2, y2, direction) -> None:

        current = self.get_cell(x1, y1)
        neighbor = self.get_cell(x2, y2)

        if current and neighbor:
            current.walls[direction] = False

            opp = Coordinates.opposite[direction]
            neighbor.walls[opp] = False

    def generate(self,
                 animate=False,
                 entry=None,
                 exit=None,
                 perfect_flag=False
                 ) -> None:
        # when the 42 block should shows up
        if self.width >= 9 and self.height >= 7:
            blocked_positions = Coordinates.forty_two_cells(self.width, self.height)
            for bx, by in blocked_positions:
                blocked_cell = self.get_cell(bx, by)
                if blocked_cell:
                    blocked_cell.blocked = True

        px, py = entry if entry else (0, 0)
        stack = [(px, py)]

        cell = self.get_cell(px, py)
        if cell:
            cell.visited = True
        if exit is None:
            exit = (self.width - 1, self.height - 1)

        renderer = AsciiRenderer(self, entry=entry, exit=exit)

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
                    if neighbor and not neighbor.visited and not neighbor.blocked:
                        unvisited_neighbors.append((direction, nx, ny))

            if unvisited_neighbors:
                val = random.choice(unvisited_neighbors)
                unvisited_neighbors.remove(val)
                chosen_dir, next_x, next_y = val
                self.carve_passage(x, y, next_x, next_y, chosen_dir)

                if animate:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(renderer.render(player_pos=(next_x, next_y)))
                    time.sleep(0.01)

                neighbor_cell = self.get_cell(next_x, next_y)
                neighbor_cell.visited = True
                stack.append((next_x, next_y))
            else:
                stack.pop()

        if not perfect_flag:
            extra_walls_to_break = int((self.width * self.height) / 10)
            for _ in range(extra_walls_to_break):
                rx, ry = random.randint(0, self.width-1), random.randint(0, self.height-1)

                random_dir = random.choice(list(Coordinates.directions.keys()))
                dx, dy = Coordinates.directions[random_dir]
                nx, ny = rx + dx, ry + dy

                curent_cell = self.get_cell(rx, ry)
                next_cell = self.get_cell(nx, ny)
                if self.in_bounds(nx, ny) and not curent_cell.blocked and not next_cell.blocked:
                    self.carve_passage(rx, ry, nx, ny, random_dir)

        if not animate:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(renderer.render())

    def place_bonuses(self, count=3, entry=(0, 0), exit=(0, 0)) -> None:
        self.bonuses = []
        while len(self.bonuses) < count:
            rx, ry = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if (rx, ry) != entry and (rx, ry) != exit and (rx, ry) not in self.bonuses:
                self.bonuses.append((rx, ry))

    def show_path(self, entry, exit, path, animate=True, show=True) -> None:
        renderer = AsciiRenderer(self, entry, exit)

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


