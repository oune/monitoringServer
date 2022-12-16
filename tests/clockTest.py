import unittest
from freezegun import freeze_time


class MyTestCase(unittest.TestCase):
    def test_something(self):
        with freeze_time("2012-01-14 14:59:59"):
            self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
