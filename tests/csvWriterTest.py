import unittest
import csv
from csvwriter import CsvWriter


class MyTestCase(unittest.TestCase):
    def test_something(self):
        cs = CsvWriter('data', 'machine1')
        print(cs.get_path())

    def test_write(self):
        data_list = [[0.12 + j for j in range(0, 10)] for i in range(0, 4)]
        transpose = [list(x) for x in zip(*data_list)]
        with open('test.csv', "a", newline='\n') as file:
            writer = csv.writer(file)
            writer.writerows(transpose)




if __name__ == '__main__':
    unittest.main()
