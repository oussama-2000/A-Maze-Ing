from mazegen.solver import Solver
from mazegen.generator import MazeGenerator
from mazegen.encoder import HexEncoder
from mazegen.ascii_render import AsciiRenderer
from mazegen.parser import ConfigParser
from mazegen.play import PlayMode
from sys import argv
import os

if __name__ == "__main__":

    try:
        if len(argv) < 2:
            raise ValueError("Error: You Sould Provide The Config File")
        if len(argv) > 2:
            raise ValueError("Error: No More Arguments More Than Program name"
                             "and Config file")
        config_file = argv[1]
        configration = ConfigParser(config_file)
        data = configration.parse()

        if data:
            width = data['WIDTH']
            height = data['HEIGHT']
            entry = data['ENTRY']
            exit = data['EXIT']
            perfect = data['PERFECT']
            animate = data['ANIMATE']
            output_file = data['OUTPUT_FILE']
            seed = data['SEED']
            hallucination_mode = data['HALLUCINATION']

            maze = MazeGenerator(width, height, seed)
            maze.generate_DFS(
                animate=animate,
                entry=entry,
                exit=exit,
                perfect_flag=perfect
                )

            theme = 0
            show = True

            while True:

                directions_path = Solver.solve_bfs(
                                            maze=maze,
                                            entry=entry,
                                            exit=exit
                                            )
                out_path = ""
                for i in directions_path:
                    out_path += i

                encoder = HexEncoder(
                            maze.grid,
                            width=width,
                            height=height,
                            entry=entry,
                            exit=exit,
                            path=out_path
                            )
                output = encoder.encode()

                try:
                    with open(output_file, "w") as file:
                        file.write(output)
                except PermissionError:
                    os.system(f"rm -rf {output_file}")
                    with open(output_file, "w") as file:
                        file.write(output)
                coordinates_path = Solver.path_to_cells(
                                            entry=entry,
                                            path=directions_path
                                            )

                # Color codes
                GREEN = "\033[32m"
                MAGENTA = "\033[35m"
                CYAN = "\033[36m"
                BOLD = "\033[1m"
                RESET = "\033[0m"

                print(f"{BOLD}{MAGENTA}Maze Seed : "
                      f"{maze.seed}{RESET} \n")

                print(f"{CYAN} █████╗       ███╗   ███╗ █████╗"
                      " ███████╗███████╗      ██╗███╗  ██╗ ██████╗ ")
                print("██╔══██╗      ████╗ ████║██╔══██╗"
                      "╚════██║██╔════╝      ██║████╗ ██║██╔════╝ ")
                print("███████║█████╗██╔████╔██║███████║"
                      "  ███╔═╝█████╗  █████╗██║██╔██╗██║██║  ██╗ ")
                print("██╔══██║╚════╝██║╚██╔╝██║██╔══██║"
                      "██╔══╝  ██╔══╝  ╚════╝██║██║╚████║██║  ╚██╗")
                print("██║  ██║      ██║ ╚═╝ ██║██║  ██║"
                      "███████╗███████╗      ██║██║ ╚███║╚██████╔╝")
                print("╚═╝  ╚═╝      ╚═╝     ╚═╝╚═╝  ╚═╝"
                      f"╚══════╝╚══════╝      ╚═╝╚═╝  ╚══╝ ╚═════╝ {RESET}")
                print("\n")
                options = {
                    1: 're-generate a new maze           ',
                    2: 'show/hide path from entry to exit',
                    3: 'rotate maze colors               ',
                    4: 'player mode                      ',
                    5: 'quit                             '
                }

                for key, option in options.items():
                    print(f"{BOLD}{GREEN}|                    {key}. {option}"
                          f"                    {BOLD}{GREEN}|")
                print(f"{BOLD}{GREEN}|                                        "
                      f"                                    |{RESET}")
                print(f"{BOLD}{GREEN}{'-' * 78}{RESET}")

                try:
                    choice = int(input(f"{BOLD}Choice: {RESET}"))

                    if choice not in options.keys():
                        raise ValueError
                except ValueError:
                    raise ValueError("Error: You Entered Invalid Option")
                if choice == 1:
                    show = True
                    os.system('cls' if os.name == 'nt' else 'clear')
                    maze = MazeGenerator(width, height, seed)
                    maze.generate_DFS(
                            animate=animate,
                            entry=entry,
                            exit=exit,
                            perfect_flag=perfect
                            )
                elif choice == 2:
                    if show:
                        Solver.show_path(maze,
                                         entry=entry,
                                         exit=exit,
                                         path=coordinates_path,
                                         animate=animate
                                         )
                        show = False
                    elif not show:
                        Solver.show_path(
                                maze,
                                entry=entry,
                                exit=exit,
                                path=coordinates_path,
                                animate=animate,
                                show=show
                                )
                        show = True
                elif choice == 3:
                    show = True
                    os.system('cls' if os.name == 'nt' else 'clear')
                    renderer = AsciiRenderer(maze=maze, entry=entry, exit=exit)
                    print(renderer.render(rotate_theme=True, theme=theme))
                    theme += 1
                    if theme > 3:
                        theme = 0

                elif choice == 4:
                    show = True
                    PlayMode.play(
                        maze=maze,
                        entry=entry,
                        exit=exit,
                        hallucination=hallucination_mode
                        )

                elif choice == 5:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Exiting The Maze Game !")
                    break
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Exiting The Maze Game !")
