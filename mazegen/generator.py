import random


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
        # Dictionary tracking if a wall exists in each direction
        # True means the wall is solid; False means it has been carved (pathway)
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        # Used by the generation algorithm to ensure we don't visit the same room twice
        self.visited = False


class MazeGenerator:
    """Handles the creation, logic, and state of the maze grid."""
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        # Initialize the 2D array of Cell objects immediately upon creation
        self.grid = self.create_grid()

    # def visited_check(self):
    #     visited = []
    #     for y in range(self.height):
    #         row = []
    #         for x in range(self.width):
    #             row.append(False)
    #         visited.append(row)
    #     return visited

    def create_grid(self) -> list:
        """
        Builds a 2D list (matrix) populated with fresh Cell objects.
        Returns: A list of lists representing the [y][x] coordinates.
        """
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell())  # Create a unique Cell instance for every coordinate
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

    def display(self) -> None:
        """Prints the maze to the console using ASCII characters."""
        # Print the very top boundary of the entire maze
        output = "\u250f" + "\u2501\u2501\u2501+" * self.width + "\n"
        for y in range(self.height):
            # 1. First line per row: Vertical walls and paths
            row_str = "\u2503"
            for x in range(self.width):
                cell = self.get_cell(x, y)
                # If the 'E' (East) wall is True, it's a solid wall '|'
                # If it's False, it's an open passage ' '
                wall = "\u2503" if cell.walls["E"] else " "
                row_str += "   " + wall
            output += row_str + "\n"

            # 2. Second line per row: Horizontal walls and corners
            row_str = "+"
            for x in range(self.width):
                cell = self.get_cell(x, y)
                # If the 'S' (South) wall is True, it's a solid wall '---'
                # If it's False, it's an open passage '   '
                wall = "\u2501\u2501\u2501" if cell.walls["S"] else "   "
                row_str += wall + "+"
            output += row_str + "\n"

        print(output)


maze = MazeGenerator(20, 20)
maze.generate()
maze.display()