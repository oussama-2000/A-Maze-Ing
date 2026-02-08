from mazegen.ascii_render import AsciiRenderer
import os
import time
import random

class PlayMode:

    def play(maze, entry=None, exit=None, halwasa=False) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        intor = "\033[1;31mHury Up Dexter Tonight is The Night !\033[0m"

        for c in intor:
            print(c, end="", flush=True)
            time.sleep(.1)

        time.sleep(1)
        renderer = AsciiRenderer(maze, entry=entry, exit=exit)
        px, py = entry if entry else (0, 0)
        goal_x, goal_y = exit if exit else (maze.width - 1, maze.height - 1)

        maze.place_bonuses(count=5, entry=(px, py), exit=(goal_x, goal_y))

        visited_path = [(px, py)]
        steps = 0
        hearts = ["\033[1;31m\u2665\033[0m", "\033[1;31m\u2665\033[0m", "\033[1;31m\u2665\033[0m"]

        theme = random.randint(0, 3)
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Hearts: ", end="")
            for heart in hearts:
                print(heart, end=" ")
            print()
            print(f"Steps: {steps} | Victim: {goal_x, goal_y}")
            print("Use 'W,A,S,D' To Move \nReach The Victim and remember:\n\033[1;31m1 - Don't Be Catched !\033[0m\n\033[1;31m2 - Don't Leave Evidance Behind You\033[0m")
            print("to exit the play mode enter : exit \n\n")
            if halwasa:
                theme = random.randint(0, 3)
            print(renderer.render(player_pos=(px, py), visited_trail=visited_path, rotate_theme=True, theme=theme))

            if (px, py) == (goal_x, goal_y):
                print("\033[92m Youe did good Find a place! \033[0m")
                break

            move = input("Move: ").lower()
            current_cell = maze.get_cell(px, py)

            old_pos = (px, py)
            # Walls check
            if move == 'w' and not current_cell.walls['N']:
                py -= 1
            elif move == 's' and not current_cell.walls['S']:
                py += 1
            elif move == 'a' and not current_cell.walls['W']:
                px -= 1
            elif move == 'd' and not current_cell.walls['E']:
                px += 1
            elif move == 'exit':
                os.system('cls' if os.name == 'nt' else 'clear')
                maze.place_bonuses(count=0, entry=(px, py), exit=(goal_x, goal_y))  # to remove bounses
                print(renderer.render(rotate_theme=True, theme=theme))
                break
            else:
                print("\033[91m Shhh Don't Make Noise ! \033[0m")
                print("Morgan x:", px, "Morgan y:", py)
                time.sleep(0.3)
                hearts.pop()
                if not hearts:
                    print("You've Been Caught By Mimai Metro !")
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