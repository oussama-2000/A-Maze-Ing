from mazegen.ascii_render import AsciiRenderer
from mazegen.coordinates import Coordinates
from typing import Tuple, TYPE_CHECKING
import os
import time
import random
if TYPE_CHECKING:
    from mazegen.generator import MazeGenerator


class PlayMode:
    """
    represent the bluprint of maze play mode
    """
    @staticmethod
    def place_bonuses(count: int,
                      maze: "MazeGenerator",
                      entry: Tuple[int, int],
                      exit: Tuple[int, int]
                      ) -> None:
        """
        Docstring for place_bonuses
        this method responsible for bonuses box placement
        :param count: how many box
        :type count: int
        :param maze: the maze object
        :type maze: "MazeGenerator"
        :param entry: the maze entry
        :type entry: Tuple[int, int]
        :param exit: the maze exit
        :type exit: Tuple[int, int]
        """

        while len(maze.bonuses) < count:
            rx, ry = random.randint(0, maze.width - 1), \
                random.randint(0, maze.height - 1)

            if (rx, ry) != entry and (rx, ry) != exit and\
                    (rx, ry) not in maze.bonuses:
                maze.bonuses.append((rx, ry))

    @staticmethod
    def play(maze: "MazeGenerator",
             entry: Tuple[int, int],
             exit: Tuple[int, int],
             hallucination: bool = False
             ) -> None:
        """
        Docstring for play
        the play method represent the play mode dashbord
        where the player can:
            move with keys:
                up: w
                down: s
                right: d
                left: a
            use cheet codes
            enter: 'exit' to exit
        :param maze: the maze object
        :type maze: "MazeGenerator"
        :param entry: the maze entry
        :type entry: Tuple[int, int]
        :param exit: the maze exit
        :type exit: Tuple[int, int]
        :param halwasa: flage for halwasa mode
            halwasa mode makes the maze themes changing
            when moving like a bar light
        :type halwasa: bool
        """

        os.system('cls' if os.name == 'nt' else 'clear')
        intor = "\033[1;31mHury Up Dexter Tonight is The Night !\033[0m"

        for c in intor:
            print(c, end="", flush=True)
            time.sleep(.1)

        time.sleep(1)
        renderer = AsciiRenderer(maze, entry=entry, exit=exit)
        px, py = entry
        goal_x, goal_y = exit

        PlayMode.place_bonuses(5, maze, entry=(px, py), exit=(goal_x, goal_y))

        visited_path = [(px, py)]
        steps = 0
        hearts = [
            "\033[1;31m\u2665\033[0m",
            "\033[1;31m\u2665\033[0m",
            "\033[1;31m\u2665\033[0m"
            ]

        theme = random.randint(0, 3)
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Hearts: ", end="")
            for heart in hearts:
                print(heart, end=" ")
            print()
            print(f"Steps: {steps} | Victim: {goal_x, goal_y}")
            print("Use 'W,A,S,D' To Move \n"
                  "Reach The Victim and remember:"
                  "\n\033[1;31m1 - Don't Be Catched !\033[0m\n"
                  "\033[1;31m2 - Don't Leave Evidance Behind You\033[0m")
            print("to exit the play mode enter : exit \n\n")

            if hallucination:
                theme = random.randint(0, 3)

            print(renderer.render(
                                  player_pos=(px, py),
                                  visited_trail=visited_path,
                                  rotate_theme=True, theme=theme)
                  )

            if (px, py) == (goal_x, goal_y):
                print("\033[92m Well Done Morgan, You"
                      " Find The Suspect \033[0m")
                time.sleep(1.8)
                os.system('cls' if os.name == 'nt' else 'clear')
                maze.bonuses = []  # to remove bounuses
                print(renderer.render(rotate_theme=True, theme=theme))
                break

            move = input("Move: ").lower()
            current_cell = maze.get_cell(px, py)

            old_pos = (px, py)
            if current_cell:
                # Walls check
                if move == 'w' and not current_cell.walls['N']:
                    py -= 1
                elif move == 's' and not current_cell.walls['S']:
                    py += 1
                elif move == 'a' and not current_cell.walls['W']:
                    px -= 1
                elif move == 'd' and not current_cell.walls['E']:
                    px += 1

                # cheat codes
                elif move == 'hplus':
                    print("\033[92m Cheat Code Activated:"
                          " +1 Heart Added \033[0m")
                    hearts.append("\033[1;31m\u2665\033[0m")
                    time.sleep(0.5)
                elif move == 'tp':
                    print("\033[92m Cheat Code Activated \033[0m")
                    cheat_x = input("Enter \033[91m'X'\033[0m Value: ")
                    cheat_y = input("Enter \033[91m'Y'\033[0m Value: ")
                    try:
                        tx = int(cheat_x)
                        ty = int(cheat_y)
                        if (tx, ty) in Coordinates.forty_two_cells(
                                                        maze.width,
                                                        maze.height
                                                        ):
                            raise ValueError
                        if not maze.in_bounds(tx, ty):
                            raise ValueError
                        else:
                            px = tx
                            py = ty
                    except Exception:
                        print("\033[91m Error: Invalid "
                              "Corrdinations ! \033[0m")
                        time.sleep(3)
                # =======

                elif move == 'exit':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    maze.bonuses = []  # to remove bounuses
                    print(renderer.render(rotate_theme=True, theme=theme))
                    break
                else:
                    print("\033[91m Shhh Don't Make Noise ! \033[0m")
                    print("Morgan x:", px, "Morgan y:", py)
                    time.sleep(0.3)
                    hearts.pop()
                    if not hearts:
                        print("\033[91m You've Been Caught By Mimai Metro !"
                              "\033[0m")
                        time.sleep(1.8)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        maze.bonuses = []  # to remove bounuses
                        print(renderer.render(rotate_theme=True, theme=theme))
                        break
                    time.sleep(0.5)
                new_pos = (px, py)
                if new_pos in maze.bonuses:
                    hearts.append("\033[1;31m\u2665\033[0m")
                    maze.bonuses.remove(new_pos)
                    print("\033[92m +1 Heart Bonus! \033[0m")
                    time.sleep(1)
                if new_pos != old_pos:
                    steps += 1
                    if new_pos not in visited_path:
                        visited_path.append(new_pos)
