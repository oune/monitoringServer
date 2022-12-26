import csv
import os
from clock import get_day


class CsvWriter:
    def __init__(self, directory, device_name, header):
        self.directory = directory
        self.device_name = device_name
        self.header = header

    def get_path(self) -> str:
        path = os.path.join(self.directory, self.device_name, get_day() + '.csv')

        return path

    def save(self, datas):
        path = self.get_path()

        if not os.path.isfile(path):
            with open(path, "a", newline='\n') as file:
                writer = csv.writer(file)
                writer.writerow(self.header)

        transpose = [list(x) for x in zip(*datas)]
        with open(path, "a", newline='\n') as file:
            writer = csv.writer(file)
            writer.writerows(transpose)
