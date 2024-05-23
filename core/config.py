import json

class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_config()

    def load_config(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Configuration file not found: {self.file_path}")
        except json.JSONDecodeError:
            raise Exception(f"Error decoding JSON from the configuration file: {self.file_path}")

    def get_bot_config(self, key):
        return self.data
