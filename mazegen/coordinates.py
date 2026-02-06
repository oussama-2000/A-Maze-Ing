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

    def check_forty_two_place(
            curent_place: tuple,
            maze_width: int,
            maze_height: int
                            ) -> tuple:

        if curent_place == ((maze_width // 2) + 2, (maze_height // 2) - 2) or \
                            curent_place == ((maze_width // 2) + 1,
                                             (maze_height // 2) - 2) or \
                            curent_place == ((maze_width // 2) + 3,
                                             (maze_height // 2) - 2) or \
                            curent_place == ((maze_width // 2) + 3,
                                             (maze_height // 2) - 1) or \
                            curent_place == ((maze_width // 2) + 3,
                                             (maze_height // 2)) or \
                            curent_place == ((maze_width // 2) + 2,
                                             (maze_height // 2)) or \
                            curent_place == ((maze_width // 2) + 1,
                                             (maze_height // 2)) or \
                            curent_place == ((maze_width // 2) + 1,
                                             (maze_height // 2) + 1) or \
                            curent_place == ((maze_width // 2) + 1,
                                             (maze_height // 2) + 2) or \
                            curent_place == ((maze_width // 2) + 2,
                                             (maze_height // 2) + 2) or \
                            curent_place == ((maze_width // 2) + 3,
                                             (maze_height // 2) + 2) or \
                                \
                            curent_place == ((maze_width // 2) - 3,
                                             (maze_height // 2) - 2) or \
                            curent_place == ((maze_width // 2) - 3,
                                             (maze_height // 2) - 1) or \
                            curent_place == ((maze_width // 2) - 3,
                                             (maze_height // 2)) or \
                            curent_place == ((maze_width // 2) - 3,
                                             (maze_height // 2) + 1) or \
                            curent_place == ((maze_width // 2) - 2,
                                             (maze_height // 2) + 1) or \
                            curent_place == ((maze_width // 2) - 1,
                                             (maze_height // 2)) or \
                            curent_place == ((maze_width // 2) - 1,
                                             (maze_height // 2) + 1) or \
                            curent_place == ((maze_width // 2) - 1,
                                             (maze_height // 2) + 2):
            return True
        return False

    def forty_two_cells(width: int, height: int) -> set[tuple[int, int]]:
        cx, cy = width // 2, height // 2

        offsets = [
            (1, -2), (2, -2), (3, -2),
            (3, -1), (3,  0),
            (2,  0), (1,  0),
            (1,  1), (1,  2),
            (2,  2), (3,  2),

            (-3, -2), (-3, -1), (-3, 0), (-3, 1),
            (-2,  1),
            (-1,  0), (-1, 1), (-1, 2),
        ]

        return {(cx + dx, cy + dy) for dx, dy in offsets}

