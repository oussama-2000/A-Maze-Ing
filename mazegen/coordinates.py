from typing import Tuple, Dict, List


class Coordinates:

    directions: Dict[str, Tuple[int, int]] = {
        'N': (0, -1),
        'S': (0, 1),
        'E': (1, 0),
        'W': (-1, 0),
    }
    opposite: Dict[str, str] = {
        'N': 'S',
        'S': 'N',
        'E': 'W',
        'W': 'E',
    }

    def forty_two_cells(
            maze_width: int,
            maze_height: int
                            ) -> List[Tuple[int, int]]:
        cells = [
            ((maze_width // 2) + 2, (maze_height // 2) - 2),
            ((maze_width // 2) + 1, (maze_height // 2) - 2),
            ((maze_width // 2) + 3, (maze_height // 2) - 2),
            ((maze_width // 2) + 3, (maze_height // 2) - 1),
            ((maze_width // 2) + 3, (maze_height // 2)),
            ((maze_width // 2) + 2, (maze_height // 2)),
            ((maze_width // 2) + 1, (maze_height // 2)),
            ((maze_width // 2) + 1, (maze_height // 2) + 1),
            ((maze_width // 2) + 1, (maze_height // 2) + 2),
            ((maze_width // 2) + 2, (maze_height // 2) + 2),
            ((maze_width // 2) + 3, (maze_height // 2) + 2),
            \
            ((maze_width // 2) - 3, (maze_height // 2) - 2),
            ((maze_width // 2) - 3, (maze_height // 2) - 1),
            ((maze_width // 2) - 3, (maze_height // 2)),
            ((maze_width // 2) - 3, (maze_height // 2) + 1),
            ((maze_width // 2) - 2, (maze_height // 2) + 1),
            ((maze_width // 2) - 1, (maze_height // 2)),
            ((maze_width // 2) - 1, (maze_height // 2) + 1),
            ((maze_width // 2) - 1, (maze_height // 2) + 2)
        ]
        return cells
