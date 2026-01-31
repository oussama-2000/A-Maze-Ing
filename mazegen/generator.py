class Cell:
    """Represents one maze cell"""
    def __init__(self) -> None:
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        self.visited = False


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = self.create_grid()

    def create_grid(self) -> list:
        """Create a 2D grid of Cell objects"""
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell())
            grid.append(row)
        return grid

    def in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are inside the maze"""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int):
        """Safely get a cell"""
        if not self.in_bounds(x, y):
            return None
        return self.grid[y][x]

