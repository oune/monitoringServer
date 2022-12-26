import unittest
import csv
from csvwriter import CsvWriter
from freezegun import freeze_time


class MyTestCase(unittest.TestCase):
    def test_writer_init(self):
        cs = CsvWriter('data', 'temp', ['123', '223', '323'])
        print(cs.get_path())

    def test_write(self):
        data_list = [[0.12 + j for j in range(0, 10)] for i in range(0, 4)]
        transpose = [list(x) for x in zip(*data_list)]
        with open('test.csv', "a", newline='\n') as file:
            writer = csv.writer(file)
            writer.writerows(transpose)

    def test_writer_save(self):
        cs = CsvWriter('data', 'temp2', ['no.1', 'no.2', 'no.3', 'no.4'])
        data_list = [[0.12 + j for j in range(0, 10)] for i in range(0, 4)]
        cs.save(data_list)

    def test_save_day_pass(self):
        cs = CsvWriter('data', 'temp3', ['no.1', 'no.2', 'no.3', 'no.4'])
        data_list = [[0.12 + j for j in range(0, 10)] for i in range(0, 4)]

        with freeze_time("2012-01-14 14:59:59"):
            cs.save(data_list)

        with freeze_time("2012-01-14 15:00:00"):
            cs.save(data_list)

        with freeze_time("2012-01-14 15:00:01"):
            cs.save(data_list)

        with freeze_time("2012-01-14 16:00:00"):
            cs.save(data_list)

        with freeze_time("2012-01-14 17:00:00"):
            cs.save(data_list)

        with freeze_time("2012-01-14 18:00:00"):
            cs.save(data_list)

        with freeze_time("2012-01-14 19:00:00"):
            cs.save(data_list)



if __name__ == '__main__':
    unittest.main()
