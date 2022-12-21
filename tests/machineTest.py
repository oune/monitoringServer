import unittest
from dataController import ModelMachine


class MyTestCase(unittest.TestCase):
    def test_batch_size_3(self):
        def do_pass():
            pass

        machine = ModelMachine(do_pass, 3)
        machine.add_vib_left([1, 2, 3])
        self.assertEqual(machine.vib_left, [1, 2, 3])
        machine.add_vib_right([1, 2, 3])
        self.assertEqual(machine.vib_right, [1, 2, 3])
        machine.add_temp([1, 2, 3])
        self.assertEqual(machine.temp, [])
        self.assertEqual(machine.vib_left, [])
        self.assertEqual(machine.vib_right, [])

    def test_batch_size_10(self):
        def do_pass():
            pass

        machine = ModelMachine(do_pass, 10)
        machine.add_vib_left([1, 2, 3])
        self.assertEqual(machine.vib_left, [1, 2, 3])
        machine.add_vib_right([1, 2, 3])
        self.assertEqual(machine.vib_right, [1, 2, 3])
        machine.add_temp([1, 2, 3])

        self.assertEqual(machine.temp, [1, 2, 3])
        self.assertEqual(machine.vib_left, [1, 2, 3])
        self.assertEqual(machine.vib_right, [1, 2, 3])

        machine.add_vib_left([1, 2, 3])
        machine.add_vib_right([1, 2, 3])
        machine.add_temp([1, 2, 3])
        machine.add_vib_left([1, 2, 3])
        machine.add_vib_right([1, 2, 3])
        machine.add_temp([1, 2, 3])
        machine.add_vib_left([1, 9, 11])
        machine.add_vib_right([1, 9, 11])
        machine.add_temp([1, 9, 11])

        self.assertEqual(machine.temp, [9, 11])
        self.assertEqual(machine.vib_left, [9, 11])
        self.assertEqual(machine.vib_right, [9, 11])


if __name__ == '__main__':
    unittest.main()
