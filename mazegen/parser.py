from mazegen.coordinates import Coordinates
from typing import List, Dict, Tuple, Optional, Any


class ConfigParser:

    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.config: Dict[str, Any] = {
            "WIDTH": 0,
            "HEIGHT": 0,
            "ENTRY": (0, 0),
            "EXIT": (0, 0),
            "OUTPUT_FILE": "output_maze.txt",
            "PERFECT": False,
            "ANIMATE": False,
            "HALWASA": False
        }

    def parse(self) -> Optional[Dict[str, Any]]:
        keys_count: int = 0
        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        parts: List[str] = line.split('=', 1)
                        if len(line.split('=')) > 2:
                            raise ValueError(f"This Line '{line}' Should"
                                             "Contain Exactly The Format"
                                             "key = value")
                        key, value = parts[0], parts[1]
                    else:
                        raise ValueError("use # to make "
                                         f"comments in {self.filepath}")

                    clean_key: str = key.strip().upper()
                    if clean_key not in self.config:
                        raise ValueError(f"Unsuported key :{key}")

                    self.assign_value(clean_key, value.strip())
                    keys_count += 1

            if keys_count != len(self.config):
                raise ValueError("Make Sure Youe Entered The Require Entries")

            if self.validate():
                return self.config
            return None

        except FileNotFoundError:
            print(f"Error: The File '{self.filepath}' Was Not Found !")
        except PermissionError:
            print(f"Error: Can't Access to '{self.filepath}' "
                  "Make Sure You Have The Permission")
        except ValueError as e:
            print(f"Configuration Error: {e}")

        return None

    def assign_value(self, key: str, value: str) -> None:
        try:
            if key in ["WIDTH", "HEIGHT"]:
                self.config[key] = int(value)
            elif key in ["ENTRY", "EXIT"]:
                parts: List[int] = [int(x) for x in value.split(',')]
                if len(parts) != 2:
                    raise ValueError(f"Key {key} requires exactly"
                                     "two coordinates (x,y)")
                coords: Tuple[int, int] = (parts[0], parts[1])
                self.config[key] = coords
            elif key == "PERFECT":
                self.config[key] = value.lower() == 'true'
            elif key == "OUTPUT_FILE":
                self.config[key] = value
            elif key == "ANIMATE":
                self.config[key] = value.lower() == 'true'
            elif key == "HALWASA":
                self.config[key] = value.lower() == 'true'
        except Exception:
            raise ValueError(f"Could Not Parse '{value}' for key '{key}'")

    def validate(self) -> bool:
        w: int = int(self.config["WIDTH"])
        h: int = int(self.config["HEIGHT"])

        if w <= 0 or h <= 0:
            raise ValueError("Width And Height Must Be Positive .")
        if w < 3 or h < 3:
            raise ValueError("Give Reasonable height and width to make a maze")

        entry: Tuple[int, int] = self.config["ENTRY"]
        exit_coord: Tuple[int, int] = self.config["EXIT"]

        if entry == exit_coord:
            raise ValueError("Entry and Exit must be different")

        if w >= 9 and h >= 7:
            if entry in Coordinates.forty_two_cells(w, h):
                raise ValueError("Entry Coordinates Should not"
                                 "located in the 42 block")

            if exit_coord in Coordinates.forty_two_cells(w, h):
                raise ValueError("Exit Coordinates Should not"
                                 "located in the 42 block")

        entry_x: int
        entry_y: int
        exit_x: int
        exit_y: int

        try:
            entry_x, entry_y = entry
            exit_x, exit_y = exit_coord
        except (ValueError, TypeError):
            raise ValueError("Entry and Exit Coordinates"
                             "Should be Exactly two dimentions")

        if (entry_x < 0) or (entry_x >= w) or (entry_y < 0) or (entry_y >= h):
            raise ValueError(f"Entry {entry_x},{entry_y}"
                             f"is outside The {w}x{h} grid !")

        if (exit_x < 0) or (exit_x >= w) or (exit_y < 0) or (exit_y >= h):
            raise ValueError(f"Exit {exit_x},{exit_y}"
                             f"is outside The {w}x{h} grid !")

        return True
