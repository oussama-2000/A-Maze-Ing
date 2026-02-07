class Coordinates:

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

    def forty_two_cells(
            maze_width: int,
            maze_height: int
                            ) -> list:
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
