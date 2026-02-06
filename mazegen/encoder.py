class HexEncoder:

    bit_map = {'N': 1, 'E': 2, 'S': 4, 'W': 8}
    hex_chars = "0123456789ABCDEF"

    def __init__(self, grid, width, height, entry, exit, path="") -> None:
        """Initialize with the generated maze grid."""
        self.grid = grid
        self.w = width
        self.h = height
        self.entry = entry
        self.exit = exit
        self.path = path

    def encode(self) -> str:
        hex_grid = []
        for y in range(0, self.h):
            row_str = ""
            for x in range(0, self.w):
                cell_sum = 0
                cell = self.grid[y][x]
                for direction, bit_value in self.bit_map.items():
                    if cell.walls[direction] is True:
                        cell_sum += bit_value
                row_str += self.hex_chars[cell_sum]
            hex_grid.append(row_str)
        # Join rows with newlines to match the block look in your image
        wall_block = "\n".join(hex_grid)
        output = (
            f"{wall_block}\n\n"
            f"{self.entry[0]},{self.entry[1]}\n"
            f"{self.exit[0]},{self.exit[1]}\n"
            f"{self.path}"
        )
        return output
