import random
import time
import os

directions = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0),
}
opposite = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E',
}


class Cell:
    """Represents a single square (node) in the maze grid."""
    def __init__(self) -> None:
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        self.visited = False


class MazeGenerator:
    """Handles the creation, logic, and state of the maze grid."""
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        # Initialize the 2D array of Cell objects immediately upon creation
        self.grid = self.create_grid()

    def create_grid(self) -> list:
        """
        Builds a 2D list (matrix) populated with fresh Cell objects.
        Returns: A list of lists representing the [y][x] coordinates.
        """
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell())
            grid.append(row)
        return grid

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Security check to ensure coordinates are within the grid boundaries.
        Prevents 'Index Out of Range' errors when checking neighbors.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int):
        """
        Retrieves the Cell object at the given (x, y) coordinates.
        Returns: The Cell object if valid, or None if the coordinates are out of bounds.
        """
        if not self.in_bounds(x, y):
            return None
        return self.grid[y][x]

    def carve_passage(self, x1, y1, x2, y2, direction) -> None:
        """
        The 'Handshake' method: Removes the shared wall between two adjacent cells.
        x1, y1: Coordinates of the current cell.
        x2, y2: Coordinates of the neighbor cell.
        direction: The compass direction ('N', 'S', 'E', or 'W') from current to neighbor.
        """
        current = self.get_cell(x1, y1)
        neighbor = self.get_cell(x2, y2)

        if current and neighbor:
            current.walls[direction] = False

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
                time.sleep(0.01)

                x, y = stack[-1]
                unvisited_neighbors = []
                for direction, (dx, dy) in directions.items():
                    nx, ny = x + dx, y + dy
                    if self.in_bounds(nx, ny):
                        neighbor = self.get_cell(nx, ny)
                        if neighbor and neighbor.visited is False:
                            unvisited_neighbors.append((direction, nx, ny))
                
                if unvisited_neighbors:
                    val = random.choice(unvisited_neighbors)
                    chosen_dir, next_x, next_y = val
                    self.carve_passage(x, y, next_x, next_y, chosen_dir)
                    neighbor_cell = self.get_cell(next_x, next_y)
                    neighbor_cell.visited = True
                    stack.append((next_x, next_y))
                else:
                    stack.pop()

    def display(self, current_pos=None) -> None:
        """Prints the maze to the console using ASCII characters."""

        output = "\u250f" + "\u2501\u2501\u2501+" * self.width + "\n"
        for y in range(self.height):
            row_str = "\u2503"
            for x in range(self.width):
                cell = self.get_cell(x, y)
                if current_pos and (x, y) == current_pos:
                    body = "███"
                else:
                    body = "   "
                wall = "\u2503" if cell.walls["E"] else " "
                row_str += body + wall
            output += row_str + "\n"

            row_str = "+"
            for x in range(self.width):
                cell = self.get_cell(x, y)
                wall = "\u2501\u2501\u2501" if cell.walls["S"] else "   "
                row_str += wall + "+"
            output += row_str + "\n"
        print(output)

    def play(self):
        px, py = 0, 0  # Starting position
        goal_x, goal_y = self.width - 1, self.height - 1  # Goal To Reach

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
                print("You Hit A Wall !!!")
                print("Player x:", px, "Player y:", py)
                time.sleep(2)


maze = MazeGenerator(10, 10)
maze.generate()
# maze.display()
print("Generation Complete! Starting game...")
time.sleep(2)

maze.play()
