import unittest
from normalization import Normalization


class MyTestCase(unittest.TestCase):
    def test_something(self):
        norm = Normalization('../resource/normalization.data')


if __name__ == '__main__':
    unittest.main()
