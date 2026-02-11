from typing import List, Tuple


class Coordinates:
    """
        Represents the maze coordinates including directions,
        directions oposite and 42 bleck cells coordinate
    """
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

    @staticmethod
    def forty_two_cells(
            maze_width: int,
            maze_height: int
                            ) -> List[Tuple]:
        """
        Docstring for forty_two_cells

        :param maze_width: the maze width
        :type maze_width: int
        :param maze_height: the maze height
        :type maze_height: int
        :return: it returns a list of 42 cells coordinates
        :rtype: List[Tuple]
        """
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
