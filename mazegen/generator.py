import random
import time
import os
from cell import Cell
from coordinates import Coordinates
from parser import ConfigParser
from ascii_render import AsciiRenderer
from encoder import HexEncoder
from sys import argv
from play import PlayMode
from solver import Solver



class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:

        self.width = width
        self.height = height
        self.grid = self.create_grid()

    def create_grid(self) -> list:
        """creates the maze grid (x, y)"""
        grid = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(Cell())
            grid.append(row)
        return grid

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Security check to ensure coordinates are within the grid.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int):
        """
        Retrieves the Cell object at the given (x, y) coordinates.
        """
        if not self.in_bounds(x, y):
            return None
        return self.grid[y][x]

    def carve_passage(self, x1, y1, x2, y2, direction) -> None:

        current = self.get_cell(x1, y1)
        neighbor = self.get_cell(x2, y2)

        if current and neighbor:
            current.walls[direction] = False

            opp = Coordinates.opposite[direction]
            neighbor.walls[opp] = False

    def generate(self,
                 start_x=0,
                 start_y=0,
                 animate=False,
                 entry=None,
                 exit=None,
                 perfect_flag=False
                 ) -> None:

        blocked_positions = Coordinates.forty_two_cells(self.width, self.height)

        for x, y in blocked_positions:
            if self.in_bounds(x, y):
                self.get_cell(x, y).blocked = True

        px, py = entry if entry else (start_x, start_y)
        stack = [(px, py)]

        cell = self.get_cell(px, py)
        if cell:
            cell.visited = True
        if exit is None:
            exit = (self.width - 1, self.height - 1)
        renderer = AsciiRenderer(self, entry=entry, exit=exit)

        while stack:
            if animate:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(renderer.render(player_pos=stack[-1]))
                time.sleep(0.1)

            x, y = stack[-1]
            unvisited_neighbors = []

            for direction, (dx, dy) in Coordinates.directions.items():
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny):
                    neighbor = self.get_cell(nx, ny)
                    if neighbor and not neighbor.visited and not neighbor.blocked:
                        unvisited_neighbors.append((direction, nx, ny))

            if unvisited_neighbors:
                # if cell and neighbor and not cell.blocked and not neighbor.blocked:
                val = random.choice(unvisited_neighbors)
                unvisited_neighbors.remove(val)
                chosen_dir, next_x, next_y = val
                self.carve_passage(x, y, next_x, next_y, chosen_dir)

                if animate:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(renderer.render(player_pos=(next_x, next_y)))
                    time.sleep(0.02)

                neighbor_cell = self.get_cell(next_x, next_y)
                neighbor_cell.visited = True
                stack.append((next_x, next_y))
            else:
                stack.pop()

        if not perfect_flag:
            extra_walls_to_break = int((self.width * self.height) / 10)
            for _ in range(extra_walls_to_break):
                rx, ry = random.randint(0, self.width-1), random.randint(0, self.height-1)
                random_dir = random.choice(list(Coordinates.directions.keys()))
                dx, dy = Coordinates.directions[random_dir]
                nx, ny = rx + dx, ry + dy

                if self.in_bounds(nx, ny):
                    self.carve_passage(rx, ry, nx, ny, random_dir)

        if not animate:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(renderer.render())

    def place_bonuses(self, count=3, entry=(0, 0), exit=(0, 0)) -> None:
        self.bonuses = []
        while len(self.bonuses) < count:
            rx, ry = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if (rx, ry) != entry and (rx, ry) != exit and (rx, ry) not in self.bonuses:
                self.bonuses.append((rx, ry))

    def show_path(self, entry, exit, path, animate=True, show=True) -> None:
        renderer = AsciiRenderer(self, entry, exit)

        if animate:
            visible_path = set()

            for cell in path:
                visible_path.add(cell)
                os.system('cls' if os.name == 'nt' else 'clear')
                print(renderer.render(path=visible_path, show=show))
                time.sleep(0.05)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(renderer.render(path=set(path), show=show))


configration = ConfigParser(argv[1])
data = configration.parse()

if data:
    width = data['WIDTH']
    height = data['HEIGHT']
    entry = data['ENTRY']
    exit = data['EXIT']
    perfect = data['PERFECT']
    animate = data['ANIMATE']
    output_file = data['OUTPUT_FILE']
    halwasa_mode = data['HALWASA']

    maze = MazeGenerator(width, height)
    maze.generate(animate=animate, entry=entry, exit=exit, perfect_flag=perfect)

    theme = 0
    show = True

    while True:

        directions_path = Solver.solve_bfs(maze=maze, entry=entry, exit=exit)
        out_path = ""
        for i in directions_path:
            out_path += i

        encoder = HexEncoder(maze.grid, width=width, height=height, entry=entry, exit=exit, path=out_path)
        output = encoder.encode()

        with open(output_file, "w") as file:
            file.write(output)

        directions_path = Solver.solve_bfs(maze=maze, entry=entry, exit=exit)
        coordinates_path = Solver.path_to_cells(maze=maze, entry=entry, path=directions_path)

        print("="*10, "A-Maze-Ing", "="*10)
        options = {
            1: 're-generate a new maze',
            2: 'show/hide path from entry to exit',
            3: 'rotate maze colors',
            4: 'player mode',
            5: 'quit',
        }

        for key, option in options.items():
            print(f'{key}. {option}')
        try:
            choice = int(input("Choice: "))
        except ValueError:
            print("invalid option")
        if choice not in options.keys():
            print("invalid option")
        elif choice == 1:
            show = True
            os.system('cls' if os.name == 'nt' else 'clear')
            maze = MazeGenerator(width, height)
            maze.generate(animate=animate, entry=entry, exit=exit, perfect_flag=perfect)
        elif choice == 2:

            if show:
                maze.show_path(entry=entry, exit=exit, path=coordinates_path, animate=animate)
                show = False
            elif not show:
                maze.show_path(entry=entry, exit=exit, path=coordinates_path, animate=animate, show=show)
                show = True
        elif choice == 3:

            os.system('cls' if os.name == 'nt' else 'clear')
            renderer = AsciiRenderer(maze=maze, entry=entry, exit=exit)
            print(renderer.render(rotate_theme=True, theme=theme))
            theme += 1
            if theme > 3:
                theme = 0

        elif choice == 4:

            PlayMode.play(maze=maze, entry=entry, exit=exit, halwasa=halwasa_mode)
        elif choice == 5:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Exiting The Maze Game !")
            break
