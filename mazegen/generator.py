import random
import time
import os
import cell
from coordinates import directions
from coordinates import opposite
from collections import deque


class MazeGenerator:
    def __init__(self, width: int,
                 height: int,
                 entry: tuple,
                 exit: tuple) -> None:
        self.width = width
        self.height = height
        self.entry = entry if entry else (0, 0)
        self.exit = exit if exit else (width - 1, height - 1)
        self.grid = self.create_grid()

    def create_grid(self) -> list:
        """creates the maze grid (x, y)"""
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(cell.Cell())
            grid.append(row)
        return grid

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Security check to ensure coordinates are within the grid boundaries.
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
        """
        x1, y1: Coordinates of the current cell.
        x2, y2: Coordinates of the neighbor cell.
        """
        current = self.get_cell(x1, y1)
        neighbor = self.get_cell(x2, y2)

        # Only proceed if both coordinates actually point to valid cells
        if current and neighbor:
            # Knock down the wall on the current cell's side
            current.walls[direction] = False

            # Identify the matching wall on the neighbor's side using the 'opposite' helper
            opp = opposite[direction]
            neighbor.walls[opp] = False

    def generate(self, start_x=0, start_y=0):
        stack = [(start_x, start_y)]
        cell = self.get_cell(start_x, start_y)
        if cell:
            cell.visited = True

        while stack:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display(current_pos=stack[-1])
            time.sleep(0.05)
            x, y = stack[-1]
            unvisited_neighbors = []
            for direction, (dx, dy) in directions.items():
                nx = x + dx
                ny = y + dy
                if self.in_bounds(nx, ny):
                    neighbor = self.get_cell(nx, ny)
                    if neighbor.visited is False:
                        unvisited_neighbors.append((direction, nx, ny))
            if unvisited_neighbors:
                val = random.choice(unvisited_neighbors)
                choosen_dir, next_x, next_y = val
                self.carve_passage(x, y, next_x, next_y, choosen_dir)
                neighbor_cell = self.get_cell(next_x, next_y)
                neighbor_cell.visited = True
                stack.append((next_x, next_y))
            else:
                stack.pop()

    def display(self, current_pos=None) -> None:
        output = "\u250f" + "\u2501\u2501\u2501+" * self.width + "\n"

        for y in range(self.height):
            # 1. Vertical walls + cell content
            row_str = "\u2503"
            for x in range(self.width):
                cell = self.get_cell(x, y)

                if current_pos and (x, y) == current_pos:
                    body = " * "
                elif (x, y) == self.entry:
                    body = " E "
                elif (x, y) == self.exit:
                    body = " X "
                else:
                    body = "   "

                wall = "\u2503" if cell.walls["E"] else " "
                row_str += body + wall

            output += row_str + "\n"

            # 2. Horizontal walls
            row_str = "+"
            for x in range(self.width):
                cell = self.get_cell(x, y)
                wall = "\u2501\u2501\u2501" if cell.walls["S"] else "   "
                row_str += wall + "+"
            output += row_str + "\n"

        print(output)

    def play(self):
        px, py = 0, 0  # Starting position
        goal_x, goal_y = self.width - 1, self.height - 1

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Use 'W,A,S,D' To Move | Reach The End of The Maze To Win !")
            self.display(current_pos=(px, py))

            if (px, py) == (goal_x, goal_y):
                print("We Have A Winner !")
                break

            move = input("Move: ").lower()
            current_cell = self.get_cell(px, py)

            # Wall checks
            if move == 'w' and not current_cell.walls['N']:
                py -= 1
            elif move == 's' and not current_cell.walls['S']:
                py += 1
            elif move == 'a' and not current_cell.walls['W']:
                px -= 1
            elif move == 'd' and not current_cell.walls['E']:
                px += 1
            else:
                print("We Caught A Looser !")
                print("Player x:", px, "Player y:", py)
                return

    def solve_bfs(self):
        start = self.entry
        goal = self.exit

        queue = deque([start])
        visited = set([start])
        parent = {}
        # {'reached cell(x, y)' : ('from which cell(x, y), 'wich direction') }

        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                break

            cell = self.get_cell(x, y)

            # iterating directions to expand neighbors
            for direction, (dx, dy) in directions.items():

                if cell.walls[direction]:
                    continue  # wall is closed

                # compute neighbor coordinates
                nx, ny = x + dx, y + dy

                if not self.in_bounds(nx, ny):
                    continue

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y, direction)
                    queue.append((nx, ny))
                    # add it to queue for next exploration

        return self.generate_path(parent)

    def generate_path(self, parent):
        print(parent)
        path = []
        current = self.exit

        while current != self.entry:
            x, y, direction = parent[current]
            path.append(direction)
            current = (x, y)

        path.reverse()
        return path


maze = MazeGenerator(6, 4, (0, 0), (5, 3))
maze.generate()


solution = maze.solve_bfs()
print(solution)
