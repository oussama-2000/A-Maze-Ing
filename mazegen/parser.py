from typing import Dict, Optional
from mazegen.coordinates import Coordinates


class ConfigParser:
    """
    Docstring for ConfigParser
    Class that responsible for config file parsing
    """

    def __init__(self, filepath: str) -> None:

        self.filepath = filepath
        self.config: Dict = {
            "WIDTH": 0,
            "HEIGHT": 0,
            "ENTRY": (0, 0),
            "EXIT": (0, 0),
            "OUTPUT_FILE": "output_maze.txt",
            "PERFECT": False,
            "ANIMATE": False,
            "SEED": None,
            "HALLUCINATION": False
        }

    def parse(self) -> Optional[Dict]:
        """
        Docstring for parse
        the parsing method ,parses the config file entries
        :return: it returns a dict of config data
        :rtype: Dict | None
        """

        require_keys = ["width", "height", "entry",
                        "exit", "output_file", "perfect"]
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
                            raise ValueError(f"This Line '{line}' Should "
                                             "Contain Exactly The "
                                             "Format key = value")
                    if '=' not in line:
                        raise ValueError("use # to make comments "
                                         f"in {self.filepath}")
                    if key.strip().upper() not in self.config.keys():
                        raise ValueError(f"Unsuported key :{key}")
                    self.assign_value(key.strip().upper(), value.strip())
                    if key.lower() in require_keys:
                        keys_count += 1

            if keys_count != len(require_keys):
                raise ValueError("Make Sure Youe Entered The Require Entries")

            if self.validate():
                return self.config

        except FileNotFoundError:
            print(f"Error: The File '{self.filepath}' Was Not Found !")
        except PermissionError:
            print(f"Error: Can't Access to '{self.filepath}' Make"
                  " Sure You Have The Permission")
        except ValueError as e:
            print(f"Configuration Error: {e}")
        return None

    def assign_value(self, key: str, value: str) -> None:
        """
        Docstring for assign_value
        helper method to set set values
        :param key: entry key
        :type key: str
        :param value: entry value
        :type value: str
        """
        try:

            if key in ["WIDTH", "HEIGHT"]:
                self.config[key] = int(value)
            elif key in ["ENTRY", "EXIT"]:
                coords = tuple(map(int, value.split(',')))
                self.config[key] = coords
            elif key == "PERFECT":
                if value.lower() == 'true':
                    self.config[key] = True
                elif value.lower() == 'false':
                    self.config[key] = False
                else:
                    self.config[key] = None
            elif key == "OUTPUT_FILE":
                self.config[key] = value
            elif key == "ANIMATE":
                if value.lower() == 'true':
                    self.config[key] = True
                elif value.lower() == 'false':
                    self.config[key] = False
                else:
                    self.config[key] = None
            elif key == "SEED":
                self.config["SEED"] = int(value)
            elif key == "HALLUCINATION":
                if value.lower() == 'true':
                    self.config[key] = True
                elif value.lower() == 'false':
                    self.config[key] = False
                else:
                    self.config[key] = None
        except Exception:
            raise ValueError(f"Could Not Parse '{value} for key '{key}")

    def validate(self) -> bool:
        """
        Docstring for validate
        helper method to validate entries
        :return: valid or not
        :rtype: bool
        """
        w = self.config["WIDTH"]
        h = self.config["HEIGHT"]

        if w < 9 or h < 7:
            raise ValueError("Give Reasonable height and width to make a maze "
                             "with the 42 block")

        if self.config["ENTRY"] == self.config["EXIT"]:
            raise ValueError("Entry and Exit must be different")

        try:
            entry_x, entry_y = self.config["ENTRY"]
            exit_x, exit_y = self.config["EXIT"]
        except ValueError:
            raise ValueError("Entry and Exit Coordinates Should be Exactly"
                             " two dimentions")

        if w >= 9 and h >= 7:
            if self.config["ENTRY"] in Coordinates.forty_two_cells(w, h):
                raise ValueError("Entry Coordinates Should not located in"
                                 " the 42 block")

            if self.config["EXIT"] in Coordinates.forty_two_cells(w, h):
                raise ValueError("Exit Coordinates Should not located in"
                                 " the 42 block")

        if (entry_x < 0) or (entry_x >= w) or (entry_y < 0) or (entry_y >= h):
            raise ValueError(f"Entry {entry_x},{entry_y} "
                             f"is outside The {w}x{h} grid !")

        if (exit_x < 0) or (exit_x >= w) or (exit_y < 0) or (exit_y >= h):
            raise ValueError(f"Exit {exit_x},{exit_y}"
                             f" is outside The {w}x{h} grid !")

        if self.config["PERFECT"] is None:
            raise ValueError("PERFECT value must be in boolean "
                             "(True or False) !")
        if self.config["ANIMATE"] is None:
            raise ValueError("ANIMATE value must be in boolean "
                             "(True or False) !")
        if self.config["HALLUCINATION"] is None:
            raise ValueError("hallucination mode value must be in boolean "
                             "(True or False) !")

        if self.config["OUTPUT_FILE"] is None or\
                len(self.config["OUTPUT_FILE"]) < 1:
            raise ValueError("You must provide a output file")

        if self.config["OUTPUT_FILE"] == '.' or\
                self.config["OUTPUT_FILE"] == '..' or\
                self.config["OUTPUT_FILE"] == './' or\
                self.config["OUTPUT_FILE"] == '../' or\
                self.config["OUTPUT_FILE"] == '/':
            raise ValueError("You Entered a Directory instead of file !")

        return True
