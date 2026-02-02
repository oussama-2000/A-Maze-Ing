class ConfigParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.config = {
            "WIDTH": 0,
            "HEIGHT": 0,
            "ENTRY": (0, 0),
            "EXIT": (0, 0),
            "OUTPUT_FILE": "maze.txt",
            "PERFECT": True
        }
    
    def parse(self):
        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        self.assign_value(key.strip().upper(), value.strip())
            self.validate()
            return self.config
        except FileNotFoundError:
            print(f"Error: The File '{self.filepath}' Was Not Found !")
            raise
        except ValueError as e:
            print(f"Configuration Error: {e}")
            raise
    
    def assign_value(self, key, value):
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
        except Exception:
            raise ValueError(f"Could Not Parse '{value} for key '{key}")
        
    def validate(self):
        w, h = self.config["WIDTH"], self.config["HEIGHT"]

        if w <= 0 or h <= 0:
            raise ValueError("Width And Height Must Be Positive .")
        for label, (x, y) in [("ENTRY", self.config["ENTRY"]), ("EXIT", self.config["EXIT"])]:
            if (x < 0) or (x >= w) or (y < 0) or (y >= h):
                raise ValueError(f"{label} {x},{y} is outside The {w}x{h} grid !")