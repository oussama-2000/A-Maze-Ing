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
