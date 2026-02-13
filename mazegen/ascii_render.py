from mazegen.coordinates import Coordinates
from typing import Tuple, List, Any, Optional, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from mazegen.generator import MazeGenerator
    # to avoid circular import; TYPE_CHECKING false at runtime


class AsciiRenderer:
    """
        This class responsible for the maze visualisation
        Including themes shapes ...
        you can use it by accessing the render method:
        rendering = AsciiRenderer.render(parameters)
    """
    def __init__(self,
                 maze: "MazeGenerator",
                 entry: Tuple[int, int],
                 exit: Tuple[int, int]
                 ) -> None:

        self.maze = maze
        self.entry = entry
        self.exit = exit

    def render(self,
               player_pos: Optional[Tuple[int, int]] = None,
               visited_trail: Optional[List[Tuple[int, int]]] = None,
               path: Optional[Set[Any]] = None,
               theme: Optional[int] = None,
               rotate_theme: bool = False,
               show: bool = True
               ) -> str:
        """
        Docstring for render

        :param player_pos: player position
        :type player_pos: Optional[Tuple[int, int]]
        :param visited_trail: cells that visited by player
        :type visited_trail: Optional[List[Tuple[int, int]]]
        :param path: the solution path
        :type path: Optional[Set[Any]]
        :param theme: the maze theme
        :type theme: Optional[int]
        :param rotate_theme: flage of rotating the maze themes
        :type rotate_theme: bool
        :param show: flage of showing the solution path / or hide it
        :type show: bool
        :return: it returns the maze ascii representation
        :rtype: str
        """
        colors = [31,  # 0 red
                  32,  # 1 green
                  33,  # 2 yellow
                  34,  # 3 blue
                  35,  # 4 magenta
                  36,  # 5 cyan
                  39,  # 6 default
                  93   # 7 bright yellow
                  ]

        origin_theme = {
            'walls': colors[3],
            'inner': colors[1],
            'player': colors[7],
            'entry': colors[6],
            'target': colors[3],
            'path': colors[2],
            'bonuses': colors[5],
            'visited_cells': colors[2],
            'cells_42': colors[4],
        }

        theme_1 = {
            'walls': colors[0],
            'inner': colors[3],
            'player': colors[4],
            'entry': colors[3],
            'target': colors[6],
            'path': colors[3],
            'bonuses': colors[5],
            'visited_cells': colors[0],
            'cells_42': colors[7],
        }
        theme_2 = {
            'walls': colors[5],
            'inner': colors[2],
            'player': colors[7],
            'entry': colors[5],
            'target': colors[6],
            'path': colors[4],
            'bonuses': colors[3],
            'visited_cells': colors[1],
            'cells_42': colors[5],
        }
        theme_3 = {
            'walls': colors[0],
            'inner': colors[3],
            'player': colors[7],
            'entry': colors[6],
            'target': colors[5],
            'path': colors[4],
            'bonuses': colors[2],
            'visited_cells': colors[1],
            'cells_42': colors[6],
        }
        theme_4 = {
            'walls': colors[4],
            'inner': colors[2],
            'player': colors[2],
            'entry': colors[7],
            'target': colors[4],
            'path': colors[3],
            'bonuses': colors[5],
            'visited_cells': colors[7],
            'cells_42': colors[5],
        }

        themes = theme_1, theme_2, theme_3, theme_4

        if rotate_theme and theme is not None:
            origin_theme = themes[theme]

        V_WALL = f"\033[{origin_theme['walls']}m\u2503\033[0m"
        H_WALL = f"\033[{origin_theme['walls']}m\u2501\033[0m"

        TL = f"\033[{origin_theme['walls']}m\u256D\033[0m"
        TR = f"\033[{origin_theme['walls']}m\u256e\033[0m"

        BL = f"\033[{origin_theme['walls']}m\u2570\033[0m"
        BR = f"\033[{origin_theme['walls']}m\u256f\033[0m"

        J_TOP = f"\033[{origin_theme['walls']}m\u2501\033[0m"
        J_BOT = f"\033[{origin_theme['walls']}m\u2501\033[0m"

        J_LEFT = f"\033[{origin_theme['walls']}m\u2503\033[0m"
        J_RIGHT = f"\033[{origin_theme['walls']}m\u2503\033[0m"

        J_INNER = f"\033[{origin_theme['inner']}m\u2b57\033[0m"

        width = self.maze.width
        height = self.maze.height
        h_seg = H_WALL * 3

        # 1. top border
        output = TL + (h_seg + J_TOP) * (width - 1) + h_seg + TR + "\n"

        for y in range(height):
            row_str = V_WALL
            for x in range(width):
                if (x, y) == player_pos:
                    body = " "\
                        f"\033[1;{origin_theme['player']}m\U0001fbb2\033[0m"\
                        " "
                elif (x, y) == self.entry:
                    body = " "\
                        f"\033[1;{origin_theme['entry']}m\U0001f3da\033[0m"\
                        " "
                elif (x, y) == self.exit:
                    body = f"\033[1;\
                        {origin_theme['target']}m\U0001f46d\033[0m "
                elif self.maze.bonuses and \
                        (x, y) in self.maze.bonuses:
                    body = " "\
                        f"\033[0;{origin_theme['bonuses']}m\U0001fbc4\033[0m"\
                        " "
                elif visited_trail and (x, y) in visited_trail:
                    body = " "\
                        f"\033[{origin_theme['visited_cells']}m\u25aa\033[0m"\
                        " "
                elif path and (x, y) in path:
                    if show:
                        body = f" \033[{origin_theme['path']}m\u25aa\033[0m "
                    else:
                        body = "   "
                else:
                    body = "   "
                if (x, y) in Coordinates.forty_two_cells(width, height) and \
                        width >= 9 and height >= 7:
                    body = f" \033[0;{origin_theme['cells_42']}m\u2588\033[0m "

                cell = self.maze.get_cell(x, y)
                # East Wall:
                wall_char = V_WALL if (cell and cell.walls["E"]) or \
                    x == width - 1 else " "
                row_str += body + wall_char
            output += row_str + "\n"

            # 3. THE INTERNAL SEPARATORS
            if y < height - 1:
                row_str = J_LEFT
                for x in range(width):

                    cell = self.maze.get_cell(x, y)

                    wall = h_seg if (cell and cell.walls["S"]) \
                        else "   "

                    joint = J_RIGHT if x == width - 1 else J_INNER
                    row_str += wall + joint
                output += row_str + "\n"

        output += BL + (h_seg + J_BOT) * (width - 1) + h_seg + BR + "\n"
        return output
