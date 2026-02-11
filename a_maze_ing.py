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
            raise ValueError("Error: No More Arguments More Than Program "
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
            halwasa_mode = data['HALWASA']

            maze = MazeGenerator(width, height)
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

                with open(output_file, "w") as file:
                    file.write(output)

                coordinates_path = Solver.path_to_cells(
                                            entry=entry,
                                            path=directions_path
                                            )

                print(" █████╗       ███╗   ███╗ █████╗"
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
                      "╚══════╝╚══════╝      ╚═╝╚═╝  ╚══╝ ╚═════╝ ")
                print("\n")
                options = {
                    1: 're-generate a new maze           ',
                    2: 'show/hide path from entry to exit',
                    3: 'rotate maze colors               ',
                    4: 'player mode                      ',
                    5: 'quit                             '
                }

                for key, option in options.items():
                    print(f"|                    {key}. {option}"
                          "                    |")
                print("|                                        "
                      "                                    |")
                print("-"*78)

                try:
                    choice = int(input("Choice: "))

                    if choice not in options.keys():
                        raise ValueError
                except ValueError:
                    raise ValueError("Error: You Entered Invalid Option")
                if choice == 1:
                    show = True
                    os.system('cls' if os.name == 'nt' else 'clear')
                    maze = MazeGenerator(width, height)
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

                    os.system('cls' if os.name == 'nt' else 'clear')
                    renderer = AsciiRenderer(maze=maze, entry=entry, exit=exit)
                    print(renderer.render(rotate_theme=True, theme=theme))
                    theme += 1
                    if theme > 3:
                        theme = 0

                elif choice == 4:

                    PlayMode.play(
                        maze=maze,
                        entry=entry,
                        exit=exit,
                        halwasa=halwasa_mode
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
