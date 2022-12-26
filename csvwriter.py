import csv
import os
from clock import get_day


class CsvWriter:
    def __init__(self, directory, device_name, header):
        self.directory = directory
        self.device_name = device_name
        self.header = header
        path = self.get_path()
        self.file_init(path)

    def get_path(self) -> str:
        path = os.path.join(self.directory, self.device_name + '_' + get_day() + '.csv')

        return path

    def file_init(self, path: str):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        if not os.path.isfile(path):
            with open(path, "w", newline='\n') as file:
                writer = csv.writer(file)
                writer.writerow(self.header)

    def save(self, datas):
        path = self.get_path()

        transpose = [list(x) for x in zip(*datas)]
        with open(path, "a", newline='\n') as file:
            writer = csv.writer(file)
            writer.writerows(transpose)
