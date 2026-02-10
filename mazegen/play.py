from mazegen.ascii_render import AsciiRenderer
import os
import time
import random
from typing import List, Tuple, Optional, Any
from mazegen.coordinates import Coordinates


class PlayMode:

    @staticmethod
    def place_bonuses(count: int, maze: Any,
                      entry: Tuple[int, int],
                      exit: Tuple[int, int]) -> None:
        count = 5
        # Set attribute on Any to satisfy mypy
        maze.bonuses = []
        while len(maze.bonuses) < count:
            rx = random.randint(0, maze.width - 1)
            ry = random.randint(0, maze.height - 1)
            if (rx, ry) != entry and (rx, ry) != exit:
                if (rx, ry) not in maze.bonuses:
                    maze.bonuses.append((rx, ry))

    @staticmethod
    def play(maze: Any, entry: Optional[Tuple[int, int]] = None,
             exit: Optional[Tuple[int, int]] = None,
             halwasa: bool = False) -> None:
        if entry is None or exit is None:
            return

        os.system('cls' if os.name == 'nt' else 'clear')
        intor: str = "\033[1;31mHury Up Dexter Tonight is The Night !\033[0m"

        for c in intor:
            print(c, end="", flush=True)
            time.sleep(.1)

        time.sleep(1)
        renderer: AsciiRenderer = AsciiRenderer(maze, entry=entry, exit=exit)
        px, py = entry
        goal_x, goal_y = exit

        # Use class name for static call
        PlayMode.place_bonuses(5, maze, entry=(px, py), exit=(goal_x, goal_y))

        visited_path: List[Tuple[int, int]] = [(px, py)]
        steps: int = 0
        hearts: List[str] = ["\033[1;31m\u2665\033[0m",
                             "\033[1;31m\u2665\033[0m",
                             "\033[1;31m\u2665\033[0m"]

        theme: int = random.randint(0, 3)
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Hearts: ", end="")
            for heart in hearts:
                print(heart, end=" ")
            print()
            print(f"Steps: {steps} | Victim: {goal_x, goal_y}")
            print("Use 'W,A,S,D' To Move \nReach The Victim and remember:"
                  "\n\033[1;31m1 - Don't Be Catched !\033[0m\n\033[1;31m2"
                  "- Don't Leave Evidance Behind You\033[0m")
            print("to exit the play mode enter : exit \n\n")
            if halwasa:
                theme = random.randint(0, 3)

            print(renderer.render(player_pos=(px, py),
                                  visited_trail=visited_path,
                                  rotate_theme=True, theme=theme))

            if (px, py) == (goal_x, goal_y):
                print("\033[92m Youe did good, Find a place! \033[0m")
                break

            move: str = input("Move: ").lower()
            current_cell: Any = maze.get_cell(px, py)

            old_pos: Tuple[int, int] = (px, py)
            # Walls check
            if move == 'w' and current_cell and not current_cell.walls['N']:
                py -= 1
            elif move == 's' and current_cell and not current_cell.walls['S']:
                py += 1
            elif move == 'a' and current_cell and not current_cell.walls['W']:
                px -= 1
            elif move == 'd' and current_cell and not current_cell.walls['E']:
                px += 1

            # cheat codes
            elif move == 'hplus':
                print("\033[92m Cheat Code Activated: +1 Heart Added \033[0m")
                hearts.append("\033[1;31m\u2665\033[0m")
                time.sleep(0.5)
            elif move == 'tp':
                print("\033[92m Cheat Code Activated \033[0m")
                cheat_x: str = input("Enter \033[91m'X'\033[0m Value: ")
                cheat_y: str = input("Enter \033[91m'Y'\033[0m Value: ")
                try:
                    tx: int = int(cheat_x)
                    ty: int = int(cheat_y)
                    if (tx, ty) in Coordinates.forty_two_cells(maze.width,
                                                               maze.height):
                        raise ValueError("Pass...")
                    else:
                        px = tx
                        py = ty
                except Exception:
                    print("\033[91m Error: Invalid Corrdinations ! \033[0m")
                    time.sleep(3)
            # cheat codes

            elif move == 'exit':
                os.system('cls' if os.name == 'nt' else 'clear')
                PlayMode.place_bonuses(count=0, maze=maze, entry=(px, py),
                                       exit=(goal_x, goal_y))
                print(renderer.render(rotate_theme=True, theme=theme))
                break
            else:
                print("\033[91m Shhh Don't Make Noise ! \033[0m")
                print("Morgan x:", px, "Morgan y:", py)
                time.sleep(0.3)
                if hearts:
                    hearts.pop()
                if not hearts:
                    print("You've Been Caught By Mimai Metro !")
                    break
                time.sleep(0.5)

            new_pos: Tuple[int, int] = (px, py)

            if hasattr(maze, 'bonuses') and new_pos in maze.bonuses:
                hearts.append("\033[1;31m\u2665\033[0m")
                maze.bonuses.remove(new_pos)
                print("\033[92m +1 Heart Bonus! \033[0m")
                time.sleep(1)

            if new_pos != old_pos:
                steps += 1
                if new_pos not in visited_path:
                    visited_path.append(new_pos)
