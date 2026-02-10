from maze.coordinates import Coordinates


class AsciiRenderer:

    def __init__(self, maze, entry=None, exit=None):
        self.maze = maze
        self.entry = entry
        self.exit = exit

    def render(self,
               player_pos=None,
               visited_trail=None,
               path=None,
               rotate_theme=False,
               theme=None,
               show=True
               ) -> None:

        colors = [31, 32, 33, 34, 35, 36, 39, 93]
        # colors = [91, 92, 94, 95, 96, 97, 93, 33]

        origin_theme = {
            'walls': colors[0],
            'inner': colors[1],
            'player': colors[7],
            'entry': colors[6],
            'target': colors[3],
            'path': colors[4],
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

        TL, TR = f"\033[{origin_theme['walls']}m\u256D\033[0m", f"\033[{origin_theme['walls']}m\u256e\033[0m" 
        BL, BR = f"\033[{origin_theme['walls']}m\u2570\033[0m", f"\033[{origin_theme['walls']}m\u256f\033[0m" 

        J_TOP, J_BOT = f"\033[{origin_theme['walls']}m\u2501\033[0m", f"\033[{origin_theme['walls']}m\u2501\033[0m"
        J_LEFT, J_RIGHT = f"\033[{origin_theme['walls']}m\u2503\033[0m", f"\033[{origin_theme['walls']}m\u2503\033[0m"
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
                    body = f" \033[1;{origin_theme['player']}m\U0001fbb2\033[0m "
                elif (x, y) == self.entry:
                    body = f" \033[1;{origin_theme['entry']}m\U0001f3da\033[0m "
                elif (x, y) == self.exit:
                    body = f"\033[1;{origin_theme['target']}m\U0001f46d\033[0m "
                elif hasattr(self.maze, 'bonuses') and (x, y) in self.maze.bonuses:
                    body = f" \033[0;{origin_theme['bonuses']}m\U0001fbc4\033[0m "
                elif visited_trail and (x, y) in visited_trail:
                    body = f" \033[{origin_theme['visited_cells']}m\u25aa\033[0m "
                elif path and (x, y) in path:
                    if show:
                        body = f" \033[{origin_theme['path']}m\u25aa\033[0m "
                    else:
                        body = "   "
                else:
                    body = "   "
                if (x, y) in Coordinates.forty_two_cells(width, height) and width >= 9 and height >= 7:
                    body = f" \033[0;{origin_theme['cells_42']}m\u2588\033[0m "

                # East Wall:
                wall_char = V_WALL if self.maze.get_cell(x, y).walls["E"] or x == width - 1 else " "
                row_str += body + wall_char
            output += row_str + "\n"

            # 3. THE INTERNAL SEPARATORS
            if y < height - 1:
                row_str = J_LEFT
                for x in range(width):

                    wall = h_seg if self.maze.get_cell(x, y).walls["S"] else "   "

                    joint = J_RIGHT if x == width - 1 else J_INNER
                    row_str += wall + joint
                output += row_str + "\n"

        output += BL + (h_seg + J_BOT) * (width - 1) + h_seg + BR + "\n"
        return output
