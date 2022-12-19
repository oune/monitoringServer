import csv
from clock import TimeController


class Saver:
    def __init__(self, directory_path: str, file_name: str):
        self.directory_path = directory_path
        self.file_name = file_name
        self.time = TimeController()

    def save(self, data):
        pass
