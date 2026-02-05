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
