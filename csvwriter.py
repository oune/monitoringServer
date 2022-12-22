import csv
import os
from clock import get_day


class CsvWriter:
    def __init__(self, directory, device_name):
        self.directory = directory
        self.device_name = device_name

    def get_path(self) -> str:
        path = os.path.join(self.directory, self.device_name, get_day() + '.csv')

        return path

    def save(self, datas):
        with open(self.get_path(), "w") as file:
            writer = csv.writer(file)
            # TODO write to csv
