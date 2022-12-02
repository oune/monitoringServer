import unittest
from dataController import Machine


class MyTestCase(unittest.TestCase):
    def test_something(self):
        def do_pass():
            pass

        machine = Machine(do_pass, 3)
        machine.add_vib_left([1, 2, 3])
        self.assertEqual(machine.vib_left, [1, 2, 3])
        machine.add_vib_right([1, 2, 3])
        self.assertEqual(machine.vib_right, [1, 2, 3])
        machine.add_temp([1, 2, 3])
        self.assertEqual(machine.temp, [])


if __name__ == '__main__':
    unittest.main()
