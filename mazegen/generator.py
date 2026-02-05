import random
import time
import os
from cell import Cell
from coordinates import directions
from coordinates import opposite
from collections import deque
from parser import ConfigParser
from ascii_render import AsciiRenderer
from encoder import HexEncoder


class MazeGenerator:
    def __init__(self, width: int,
                 height: int,) -> None:
        self.width = width
        self.height = height
        self.grid = self.create_grid()

    def create_grid(self) -> list:
        """creates the maze grid (x, y)"""
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
        """
        x1, y1: Coordinates of the current cell.
        x2, y2: Coordinates of the neighbor cell.
        """
        current = self.get_cell(x1, y1)
        neighbor = self.get_cell(x2, y2)

        # Only proceed if both coordinates actually point to valid cells
        if current and neighbor:
            # Knock down the wall on the current cell's side
            current.walls[direction] = False

            # Identify the matching wall on the neighbor's side using the 'opposite' helper
            opp = opposite[direction]
            neighbor.walls[opp] = False

    def generate(self, start_x=0, start_y=0, animate=False, entry=None, exit=None, rotate_theme=False, perfect_flag=False):
        if entry is None:
            stack = [(start_x, start_y)]
            cell = self.get_cell(start_x, start_y)
            if cell:
                cell.visited = True
        else:
            stack = [entry]
        if exit is None:
            exit = (self.width - 1, self.height - 1)
        renderer = AsciiRenderer(self, entry=entry, exit=exit)

        # if animate:
        #     print(renderer.render())
        #     time.sleep(2)
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
                random_dir = random.choice(list(directions.keys()))
                dx, dy = directions[random_dir]
                nx, ny = rx + dx, ry + dy
                
                if self.in_bounds(nx, ny):
                    self.carve_passage(rx, ry, nx, ny, random_dir)

        if not animate:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(renderer.render())

    def place_bonuses(self, count=3, entry=(0, 0), exit=(0, 0)):
        self.bonuses = []
        while len(self.bonuses) < count:
            rx, ry = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if (rx, ry) != entry and (rx, ry) != exit and (rx, ry) not in self.bonuses:
                self.bonuses.append((rx, ry))

    def play(self, entry=None, exit=None):

        renderer = AsciiRenderer(self, entry=entry, exit=exit)
        px, py = entry if entry else (0, 0)
        goal_x, goal_y = exit if exit else (self.width - 1, self.height - 1)

        self.place_bonuses(count=5, entry=(px, py), exit=(goal_x, goal_y))

        visited_path = [(px, py)]
        steps = 0
        hearts = ["\u2665", "\u2665", "\u2665"]
        theme = random.randint(0, 3)
        
        while True:
            val = "\U0001fb78\U0001fb78\U0001fb78\U0001fb78"
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{val} Maze Runner {val}")
            print("Hearts:", hearts)
            print(f"Steps: {steps} | Goal: {goal_x, goal_y}")
            print("Use 'W,A,S,D' To Move | Reach The End of The Maze To Win !")
            print("for exit the play mode enter : exit")
            # theme = random.randint(0, 3)  # For Halwassa Game !
            print(renderer.render(player_pos=(px, py), visited_trail=visited_path, rotate_theme=True, theme=theme))

            if (px, py) == (goal_x, goal_y):
                print("\033[92m We Have A Winner! \033[0m")
                break

            move = input("Move: ").lower()
            current_cell = self.get_cell(px, py)

            old_pos = (px, py)
            # Wall checks
            if move == 'w' and not current_cell.walls['N']:
                py -= 1
            elif move == 's' and not current_cell.walls['S']:
                py += 1
            elif move == 'a' and not current_cell.walls['W']:
                px -= 1
            elif move == 'd' and not current_cell.walls['E']:
                px += 1
            elif move == "hplus":
                print("\033[35m Cheat Code Activated +1 Heart \033[0m")
                time.sleep(0.5)
                hearts += ["\u2665"]
            elif move == 'exit':
                break
            else:
                print("\033[91m You hit a wall!\033[0m")
                print("Player x:", px, "Player y:", py)
                hearts.pop()
                if not hearts:
                    print("You Lose All Your Hearts")
                    break
                time.sleep(0.3)
            new_pos = (px, py)
            if new_pos in self.bonuses:
                hearts.append("\u2665")
                self.bonuses.remove(new_pos)
                print("\033[92m +1 Heart Bonus! \033[0m")
                time.sleep(1)
            if new_pos != old_pos:
                steps += 1
                if new_pos not in visited_path:
                    visited_path.append(new_pos)

    def solve_bfs(self, entry, exit):
        start = entry
        goal = exit

        queue = deque([start])
        visited = set([start])
        parent = {}
        # {'reached cell(x, y)' : ('from which cell(x, y), 'wich direction') }

        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                break

            cell = self.get_cell(x, y)

            # iterating directions to expand neighbors
            for direction, (dx, dy) in directions.items():

                if cell.walls[direction]:
                    continue  # wall is closed

                # compute neighbor coordinates
                nx, ny = x + dx, y + dy

                if not self.in_bounds(nx, ny):
                    continue

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y, direction)
                    queue.append((nx, ny))
                    # add it to queue for next exploration

        return self.generate_path(parent, entry, exit)

    def generate_path(self, parent, entry, exit):
        path = []
        current = exit

        while current != entry:
            x, y, direction = parent[current]
            path.append(direction)
            current = (x, y)

        path.reverse()
        return path

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


    def path_to_cells(self, entry, path):
        x, y = entry
        cell_pos = [(x, y)]

        for direction in path:
            dx, dy = directions[direction]
            x += dx
            y += dy
            cell_pos.append((x, y))
        return cell_pos



configration = ConfigParser("../config/config.txt")
data = configration.parse()

if data:
    width = data['WIDTH']
    height = data['HEIGHT']
    entry = data['ENTRY']
    exit = data['EXIT']
    perfect = data['PERFECT']
    animate = data['ANIMATE']
    output_file = data['OUTPUT_FILE']

    maze = MazeGenerator(width, height)
    maze.generate(animate=animate, entry=entry, exit=exit, perfect_flag=perfect)

    theme = 0
    show = True
    flag = True
    while True:

        directions_path = maze.solve_bfs(entry, exit)
        out_path = ""
        for i in directions_path:
            out_path += i
        
        encoder = HexEncoder(maze.grid, width=width, height=height, entry=entry, exit=exit, path=out_path)
        output = encoder.encode()

        with open(output_file, "w") as file:
                    file.write(output)

        directions_path = maze.solve_bfs(entry, exit)
        coordinates_path = maze.path_to_cells(entry, directions_path)

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
            if not flag:
                show = True
            os.system('cls' if os.name == 'nt' else 'clear')
            maze = MazeGenerator(width, height)
            maze.generate(animate=animate, entry=entry, exit=exit, perfect_flag=perfect)
        elif choice == 2:

            if show:
                maze.show_path(entry=entry, exit=exit, path=coordinates_path, animate=animate)
                show = False
                flag = False
            elif not show:
                maze.show_path(entry=entry, exit=exit, path=coordinates_path, animate=animate, show=show)
                show = True
        elif choice == 3:

            if not flag:
                show = True
            os.system('cls' if os.name == 'nt' else 'clear')
            renderer = AsciiRenderer(maze=maze, entry=entry, exit=exit)
            print(renderer.render(rotate_theme=True, theme=theme))
            theme += 1
            if theme > 3:
                theme = 0

        elif choice == 4:
            if not flag:
                show = True
            maze.play(entry=entry, exit=exit)
        elif choice == 5:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Exiting The Maze Game !")
            break
