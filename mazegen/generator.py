import random
import time
import os
from encoders import HexEncoder
from parser import ConfigParser
from renderer import AsciiRenderer

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


class Cell:
    """Represents a single square (node) in the maze grid."""
    def __init__(self) -> None:
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        self.visited = False


class MazeGenerator:
    """Handles the creation, logic, and state of the maze grid."""
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        # Initialize the 2D array of Cell objects immediately upon creation
        self.grid = self.create_grid()

    def create_grid(self) -> list:
        """
        Builds a 2D list (matrix) populated with fresh Cell objects.
        Returns: A list of lists representing the [y][x] coordinates.
        """
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell())
            grid.append(row)
        return grid

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Security check to ensure coordinates are within the grid boundaries.
        Prevents 'Index Out of Range' errors when checking neighbors.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int):
        """
        Retrieves the Cell object at the given (x, y) coordinates.
        Returns: The Cell object if valid, or None if the coordinates are out of bounds.
        """
        if not self.in_bounds(x, y):
            return None
        return self.grid[y][x]

    def carve_passage(self, x1, y1, x2, y2, direction) -> None:
        """
        The 'Handshake' method: Removes the shared wall between two adjacent cells.
        x1, y1: Coordinates of the current cell.
        x2, y2: Coordinates of the neighbor cell.
        direction: The compass direction ('N', 'S', 'E', or 'W') from current to neighbor.
        """
        current = self.get_cell(x1, y1)
        neighbor = self.get_cell(x2, y2)

        if current and neighbor:
            current.walls[direction] = False

            opp = opposite[direction]
            neighbor.walls[opp] = False

    def generate(self, start_x=0, start_y=0, animate=False, entry=None, exit=None):

            renderer = AsciiRenderer(self, entry=entry, exit=exit)
            stack = [(start_x, start_y)]
            cell = self.get_cell(start_x, start_y)
            if cell:
                cell.visited = True
            while stack:
                if animate:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(renderer.render(player_pos=stack[-1]))
                    time.sleep(0.01)

                x, y = stack[-1]
                unvisited_neighbors = []
                for direction, (dx, dy) in directions.items():
                    nx, ny = x + dx, y + dy
                    if self.in_bounds(nx, ny):
                        neighbor = self.get_cell(nx, ny)
                        if neighbor and neighbor.visited is False:
                            unvisited_neighbors.append((direction, nx, ny))
                
                if unvisited_neighbors:
                    val = random.choice(unvisited_neighbors)
                    chosen_dir, next_x, next_y = val
                    self.carve_passage(x, y, next_x, next_y, chosen_dir)
                    neighbor_cell = self.get_cell(next_x, next_y)
                    neighbor_cell.visited = True
                    stack.append((next_x, next_y))
                else:
                    stack.pop()

    def play(self, entry=None, exit=None):

        renderer = AsciiRenderer(self, entry=entry, exit=exit)
        px, py = entry if entry else (0, 0)
        goal_x, goal_y = exit if exit else (self.width - 1, self.height - 1)

        visited_path = [(px, py)]
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("---- Maze Runner ----")
            print("Use 'W,A,S,D' To Move | Reach The End of The Maze To Win !")
            print("here\n")
            print(renderer.render(player_pos=(px, py), visited_trail=visited_path))

            if (px, py) == (goal_x, goal_y):
                print("\033[92m✨ We Have A Winner! ✨\033[0m")
                break

            move = input("Move: ").lower()
            current_cell = self.get_cell(px, py)

            # Wall checks
            if move == 'w' and not current_cell.walls['N']:
                py -= 1
            elif move == 's' and not current_cell.walls['S']:
                py += 1
            elif move == 'a' and not current_cell.walls['W']:
                px -= 1
            elif move == 'd' and not current_cell.walls['E']:
                px += 1
            else:
                print("\033[91m💥 You hit a wall!\033[0m")
                print("Player x:", px, "Player y:", py)
                time.sleep(2)
            visited_pos = (px, py)
            if (px, py) not in visited_path:
                visited_path.append(visited_pos)


parser = ConfigParser("config.txt")
config_data = parser.parse()
if config_data:

    maze = MazeGenerator(config_data['WIDTH'], config_data['HEIGHT'])
    maze.generate(animate=config_data['ANIMATE'], entry=config_data['ENTRY'], exit=config_data['EXIT'])

    encoder = HexEncoder(maze.grid, config_data['WIDTH'], config_data['HEIGHT'], config_data['ENTRY'], config_data['EXIT'], "Kantssna F BFS Dial Oussama...")
    encoder_maze = encoder.encode()
    file_name = config_data["OUTPUT_FILE"]
    try:
        with open(file_name, 'w') as file:
            file.write(encoder_maze)
        print(f"Successfully saved maze to {file_name}!")
    except Exception as e:
        print(f"Failed to save maze: {e}")

    # print("Generation Complete! Press Enter to Start Playing..")
    # input()

    # maze.play(entry=config_data['ENTRY'], exit=config_data['EXIT'])
