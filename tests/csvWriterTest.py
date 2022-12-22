import unittest
from csvwriter import CsvWriter


class MyTestCase(unittest.TestCase):
    def test_something(self):
        cs = CsvWriter('data', 'machine1')
        print(cs.get_path())




if __name__ == '__main__':
    unittest.main()
