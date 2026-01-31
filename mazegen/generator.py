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

    def create_grid(self) -> list:
        """
        Builds a 2D list (matrix) populated with fresh Cell objects.
        Returns: A list of lists representing the [y][x] coordinates.
        """
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell()) # Create a unique Cell instance for every coordinate
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


# maze = MazeGenerator(4, 3)

# x1, y1 = 0, 0
# x2, y2 = 1, 0
# direction = 'E'

# cell_a = maze.get_cell(x1, y1)
# cell_b = maze.get_cell(x2, y2)
# grid = maze.grid
# print("--- BEFORE CARVING ---")
# print(f"Cell A (0,0) East Wall: {cell_a.walls['E']}")
# print(f"Cell B (1,0) West Wall: {cell_b.walls['W']}")

# # 4. Perform the carve
# maze.carve_passage(x1, y1, x2, y2, direction)

# # 5. Check walls AFTER carving
# print("\n--- AFTER CARVING ---")
# print(f"Cell A (0,0) East Wall: {cell_a.walls['E']} (Should be False)")
# print(f"Cell B (1,0) West Wall: {cell_b.walls['W']} (Should be False)")

# # 6. Verify other walls are still intact (Safety Check)
# print(f"Cell A (0,0) North Wall: {cell_a.walls['N']} (Should still be True)")
