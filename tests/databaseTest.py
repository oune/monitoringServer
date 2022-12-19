import unittest
from db import Database


class MyTestCase(unittest.TestCase):
    def test_something(self):
        db = Database("../db/machine_1.db")
        print(db.get_all())
        print(db.get_by_one_day('2022-12-19'))
        print(db.get_by_duration('2022-12-13', '2022-12-20'))


if __name__ == '__main__':
    unittest.main()
