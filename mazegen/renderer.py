class AsciiRenderer:
    V_WALL = "\u2503" 
    H_WALL = "\u2501" 

    TL, TR = "\u256D", "\u256e" 
    BL, BR = "\u2570", "\u256f" 

    J_TOP, J_BOT = "\u2501", "\u2501"
    J_LEFT, J_RIGHT = "\u2503", "\u2503"
    J_INNER = "\u2b57"

    def __init__(self, maze, entry=None, exit=None):
        self.maze = maze
        self.entry = entry
        self.exit = exit

    def render(self, player_pos=None, visited_trail=None):
        width = self.maze.width
        height = self.maze.height
        h_seg = self.H_WALL * 3
        
        # 1. TOP BORDER: Connects smoothly to vertical walls
        output = self.TL + (h_seg + self.J_TOP) * (width - 1) + h_seg + self.TR + "\n"
        
        for y in range(height):
            row_str = self.V_WALL
            for x in range(width):
                if (x, y) == player_pos:
                    body = " \033[96m\U0001fbb2\033[0m "
                elif (x, y) == self.entry:
                    body = " \U0001f3da "
                elif (x, y) == self.exit:
                    body = " \033[91m\U0001fbc9\033[0m "
                elif hasattr(self.maze, 'bonuses') and (x, y) in self.maze.bonuses:
                    body = " \033[91m\U0001fbc4\033[0m "
                elif visited_trail and (x, y) in visited_trail:
                    body = " \033[96m\u25aa\033[0m "
                else:
                    body = "   "
                
                # East Wall: Use border junction ┫ at the far right
                wall_char = self.V_WALL if self.maze.get_cell(x, y).walls["E"] or x == width - 1 else " "
                row_str += body + wall_char
            output += row_str + "\n"

            # 3. THE INTERNAL SEPARATORS
            if y < height - 1:
                row_str = self.J_LEFT
                for x in range(width):

                    wall = h_seg if self.maze.get_cell(x, y).walls["S"] else "   "

                    joint = self.J_RIGHT if x == width - 1 else self.J_INNER
                    row_str += wall + joint
                output += row_str + "\n"

        output += self.BL + (h_seg + self.J_BOT) * (width - 1) + h_seg + self.BR + "\n"           
        return output
