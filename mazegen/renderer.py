class AsciiRenderer:
    V_WALL = "\u2503"  # ┃
    H_WALL = "\u2501"  # ━
    CORNER = "\u254b"  # ╋ (Universal joint)

    def __init__(self, maze, entry=None, exit=None):
        self.maze = maze
        self.entry = entry
        self.exit = exit

    def render(self, player_pos=None, path=None, visited_trail=None):
        """
        player_pos: (x, y) tuple for animation
        path: A list of (x, y) tuples if you want to draw the solution
        """
        width = self.maze.width
        height = self.maze.height
        
        output = "+" + (self.H_WALL * 3 + "+") * width + "\n"
        
        for y in range(height):
            row_str = self.V_WALL
            for x in range(width):
                cell = self.maze.get_cell(x, y)
                
                if (x, y) == player_pos:
                    body = " \033[94mO\033[0m " # Green Player
                elif (x, y) == self.entry:
                    body = " \033[92mS\033[0m "              # Start
                elif (x, y) == self.exit:
                    body = " \033[91mF\033[0m "              # Finish
                elif visited_trail and (x, y) in visited_trail:
                    body = " \033[96m\u25aa\033[0m "  # Color For Visited_Path
                elif path and (x, y) in path:
                    body = " \033[93m\u00b7\033[0m " # Yellow dot for path
                else:
                    body = "   "
                
                wall = self.V_WALL if cell.walls["E"] else " "
                row_str += body + wall
            output += row_str + "\n"

            row_str = "+"
            for x in range(width):
                cell = self.maze.get_cell(x, y)
                wall = (self.H_WALL * 3) if cell.walls["S"] else "   "
                row_str += wall + "+"
            output += row_str + "\n"
            
        return output