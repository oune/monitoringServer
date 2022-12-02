import unittest
from dataController import DataController


class MyTestCase(unittest.TestCase):
    def test_add(self):
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
        controller.add_vib(message)
        self.assertEqual(controller.machine1.vib_left, [1, 1, 1, 1, 1])
        controller.add_vib(message)
        self.assertEqual(controller.machine1.vib_left, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        controller.add_vib(message)
        self.assertEqual(controller.machine1.vib_left, [])


if __name__ == '__main__':
    unittest.main()
