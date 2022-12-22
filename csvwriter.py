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
        path = self.get_path()

        # TODO if path 가 존재하지 않는다면 파일을 만들고 헤더를 추가

        transpose = [list(x) for x in zip(*datas)]
        with open(path, "a", newline='\n') as file:
            writer = csv.writer(file)
            writer.writerows(transpose)
