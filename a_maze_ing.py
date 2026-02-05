from mazegen.generator import MazeGenerator
from mazegen.parser import ConfigParser


configration = ConfigParser("./config/config.txt")
data = configration.parse()
if data:
    width = data['WIDTH']
    height = data['HEIGHT']
    entry = data['ENTRY']
    exit = data['EXIT']
    perfect = data['PERFECT']
    animate = data['ANIMATE']

    maze = MazeGenerator(width, height)
    maze.generate(animate=animate, entry=entry, exit=exit)

    # maze.play(entry=entry, exit=exit)
    solution = maze.solve_bfs(entry, exit)

    path = maze.path_to_cells(entry, solution)
    if perfect:
        maze.show_path(entry=entry, exit=exit, path=path)
    print(path)