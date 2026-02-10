from mazegen.coordinates import Coordinates


class ConfigParser:

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.config = {
            "WIDTH": 0,
            "HEIGHT": 0,
            "ENTRY": (0, 0),
            "EXIT": (0, 0),
            "OUTPUT_FILE": "output_maze.txt",
            "PERFECT": False,
            "ANIMATE": False,
            "HALWASA": False
        }

    def parse(self) -> dict:
        keys_count = 0
        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        if len(line.split('=')) > 2:
                            raise ValueError(f"This Line '{line}' Should Contain Exactly The Format key = value")
                    if '=' not in line:
                        raise ValueError(f"use # to make comments in {self.filepath}")
                    if key.strip() not in self.config.keys():
                        raise ValueError(f"Unsuported key :{key}")
                    self.assign_value(key.strip().upper(), value.strip())
                    keys_count += 1

            if keys_count != len(self.config.keys()):
                raise ValueError("Make Sure Youe Entered The Require Entries")

            if self.validate():
                return self.config
            else:
                return
        except FileNotFoundError:
            print(f"Error: The File '{self.filepath}' Was Not Found !")
        except PermissionError:
            print(f"Error: Can't Access to '{self.filepath}' Make Sure You Have The Permission")
        except ValueError as e:
            print(f"Configuration Error: {e}")

    def assign_value(self, key, value) -> None:
        try:

            if key in ["WIDTH", "HEIGHT"]:
                self.config[key] = int(value)
            elif key in ["ENTRY", "EXIT"]:
                coords = tuple(map(int, value.split(',')))
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
            raise ValueError(f"Could Not Parse '{value} for key '{key}")

    def validate(self) -> bool:
        w, h = self.config["WIDTH"], self.config["HEIGHT"]

        if w <= 0 or h <= 0:
            raise ValueError("Width And Height Must Be Positive .")
        if w < 3 or h < 3:
            raise ValueError("Give Reasonable height and width to make a maze")

        if self.config["ENTRY"] == self.config["EXIT"]:
            raise ValueError("Entry and Exit must be different")

        if w >= 9 and h >= 7:
            if self.config["ENTRY"] in Coordinates.forty_two_cells(self.config["WIDTH"], self.config["HEIGHT"]):
                raise ValueError("Entry Coordinates Should not located in the 42 block")

            if self.config["EXIT"] in Coordinates.forty_two_cells(self.config["WIDTH"], self.config["HEIGHT"]):
                raise ValueError("Exit Coordinates Should not located in the 42 block")
        try:
            entry_x, entry_y = self.config["ENTRY"]
            exit_x, exit_y = self.config["EXIT"]
        except ValueError:
            raise ValueError("Entry and Exit Coordinates Should be Exactly two dimentions")

        if (entry_x < 0) or (entry_x >= w) or (entry_y < 0) or (entry_y >= h):
            raise ValueError(f"Entry {entry_x},{entry_y} is outside The {w}x{h} grid !")

        if (exit_x < 0) or (exit_x >= w) or (exit_y < 0) or (exit_y >= h):
            raise ValueError(f"Exit {exit_x},{exit_y} is outside The {w}x{h} grid !")

        return True
