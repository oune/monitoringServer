import csv
from clock import Time


class Saver:
    def __init__(self, directory_path: str, file_name: str):
        self.directory_path = directory_path
        self.time = Time()
        self.file_name = file_name

    def save(self, data):
        pass
