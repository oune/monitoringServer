import unittest
from db import Database


class MyTestCase(unittest.TestCase):
    def test_something(self):
        d = Database()
        d.show()


if __name__ == '__main__':
    unittest.main()
