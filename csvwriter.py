import csv
import os
from typing import List

from clock import get_day


async def save_data(path, datas):
    with open(path, "a", newline='\n') as file:
        writer = csv.writer(file)
        writer.writerows(datas)


class CsvWriter:
    def __init__(self, directory, device_name, header: List[str]):
        self.directory = directory
        self.device_name = device_name
        self.header = header

    async def get_path(self) -> str:
        return os.path.join(self.directory, self.device_name + '_' + get_day() + '.csv')

    async def file_init(self, path: str):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        if not os.path.isfile(path):
            with open(path, "w", newline='\n') as file:
                writer = csv.writer(file)
                writer.writerow(self.header)

    async def save(self, datas):
        path = await self.get_path()
        await self.file_init(path)

        transpose = [list(x) for x in zip(*datas)]
        await save_data(path, transpose)
