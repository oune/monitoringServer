import csv
from clock import TimeController


class Saver:
    def __init__(self, directory_path: str, file_name: str):
        self.directory_path = directory_path
        self.time = TimeController()
        self.file_name = file_name

    def save(self, data):
        pass
