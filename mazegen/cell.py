from typing import Dict


class Cell:
    """represents a single square in the maze grid."""
    def __init__(self) -> None:
        self.walls: Dict[str, bool] = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        self.visited: bool = False
        self.blocked: bool = False  # owned by 42
