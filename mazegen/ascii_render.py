from mazegen.coordinates import Coordinates
from typing import Tuple, Optional, List
from mazegen.generator import MazeGenerator


class AsciiRenderer:

    def __init__(self, maze: MazeGenerator,
                 entry: Optional[Tuple[int, int]] = None,
                 exit: Optional[Tuple[int, int]] = None) -> None:
        self.maze: MazeGenerator = maze
        self.entry: Optional[Tuple[int, int]] = entry
        self.exit: Optional[Tuple[int, int]] = exit

    def render(self,
               player_pos: Optional[Tuple[int, int]] = None,
               visited_trail: Optional[List[Tuple[int, int]]] = None,
               path: Optional[List[Tuple[int, int]]] = None,
               rotate_theme: bool = False,
               theme: Optional[int] = None,
               show: bool = True
               ) -> str:

        colors = [31, 32, 33, 34, 35, 36, 39, 93]

        origin_theme = {
            'walls': colors[0],
            'inner': colors[1],
            'player': colors[7],
            'entry': colors[6],
            'target': colors[3],
            'path': colors[2],
            'bonuses': colors[5],
            'visited_cells': colors[2],
            'cells_42': colors[6],
        }

        theme_1 = {
            'walls': colors[1],
            'inner': colors[2],
            'player': colors[4],
            'entry': colors[7],
            'target': colors[6],
            'path': colors[3],
            'bonuses': colors[5],
            'visited_cells': colors[0],
            'cells_42': colors[7],
        }
        theme_2 = {
            'walls': colors[2],
            'inner': colors[0],
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
            'walls': colors[1],
            'inner': colors[2],
            'player': colors[2],
            'entry': colors[7],
            'target': colors[4],
            'path': colors[3],
            'bonuses': colors[5],
            'visited_cells': colors[7],
            'cells_42': colors[7],
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
                    body = " \033[1;"
                    f"{origin_theme['player']}m\U0001fbb2\033[0m "
                elif (x, y) == self.entry:
                    body = " \033[1;"
                    f"{origin_theme['entry']}m\U0001f3da\033[0m "
                elif (x, y) == self.exit:
                    body = "\033[1;"
                    f"{origin_theme['target']}m\U0001f46d\033[0m "
                elif hasattr(self.maze, 'bonuses'):
                    val = (x, y) in self.maze.bonuses
                    if val:
                        body = " \033[0;"
                        f"{origin_theme['bonuses']}m\U0001fbc4\033[0m "
                elif visited_trail and (x, y) in visited_trail:
                    body = f" \033[{origin_theme['visited_cells']}"
                    "m\u25aa\033[0m "
                elif path and (x, y) in path:
                    if show:
                        body = f" \033[{origin_theme['path']}m\u25aa\033[0m "
                    else:
                        body = "   "
                else:
                    body = "   "
                if (x, y) in Coordinates.forty_two_cells(width, height):
                    if width >= 9 and height >= 7:
                        body = f" \033[0;{origin_theme['cells_42']}"
                        "m\u2588\033[0m "

                # East Wall:
                wall_char: str = " "
                if x == width - 1:
                    wall_char = V_WALL
                else:
                    cell = self.maze.get_cell(x, y)
                    if cell and cell.walls["E"]:
                        wall_char = V_WALL
                row_str += body + wall_char
            output += row_str + "\n"

            # 3. THE INTERNAL SEPARATORS
            if y < height - 1:
                row_str = J_LEFT
                for x in range(width):

                    wall: str = "   "

                    cell = self.maze.get_cell(x, y)
                    if cell:
                        if cell.walls["S"]:
                            wall = h_seg

                    joint = J_RIGHT if x == width - 1 else J_INNER
                    row_str += wall + joint
                output += row_str + "\n"

        output += BL + (h_seg + J_BOT) * (width - 1) + h_seg + BR + "\n"
        return output
