import unittest
from dataController import DataController
from unittest import IsolatedAsyncioTestCase
from typing import List


class MyTestCase(IsolatedAsyncioTestCase):
    async def test_add(self):
        def callback():
            pass

        controller = DataController(callback, 10)
        message = {
            'time': '2022-01-01',
            'machine2_left': [1, 1, 1, 1, 1],
            'machine2_right': [1, 1, 1, 1, 1],
            'machine1_left': [1, 1, 1, 1, 1],
            'machine1_right': [1, 1, 1, 1, 1],
        }
        self.assertEqual(controller.machine1.vib_left, [])
        await controller.add_vib(message)
        self.assertEqual(controller.machine1.vib_left, [1, 1, 1, 1, 1])
        await controller.add_vib(message)
        self.assertEqual(controller.machine1.vib_left, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        await controller.add_vib(message)
        self.assertEqual(controller.machine1.vib_left, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    async def test_file_save(self):
        async def callback(left: List[float], right: List[float], temp: List[float], name: str):
            pass

        controller = DataController(callback, 10, 10)
        message = {
            'time': '2022-01-01',
            'machine2_left': [1, 1, 1, 1, 1],
            'machine2_right': [1, 1, 1, 1, 1],
            'machine1_left': [1, 1, 1, 1, 1],
            'machine1_right': [1, 1, 1, 1, 1],
        }
        await controller.add_vib(message)


if __name__ == '__main__':
    unittest.main()
