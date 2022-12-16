import unittest
from freezegun import freeze_time
from clock import TimeController


class MyTestCase(unittest.TestCase):
    def test_init(self):
        with freeze_time("2012-01-14 14:59:59"):
            tc = TimeController()
            is_day_changed = tc.is_day_change()
            is_hour_changed = tc.is_hour_change()
            self.assertEqual(False, is_day_changed)
            self.assertEqual(False, is_hour_changed)

    def test_hour_changed(self):
        with freeze_time("2012-01-14 14:59:59"):
            tc = TimeController()
            self.assertEqual(False, tc.is_hour_change())

        with freeze_time("2012-01-14 14:50:00"):
            self.assertEqual(False, tc.is_hour_change())

        with freeze_time("2012-01-14 14:50:01"):
            self.assertEqual(False, tc.is_hour_change())

        with freeze_time("2012-01-14 14:55:01"):
            self.assertEqual(False, tc.is_hour_change())

        with freeze_time("2012-01-14 14:59:01"):
            self.assertEqual(False, tc.is_hour_change())

        with freeze_time("2012-01-14 14:59:59"):
            self.assertEqual(False, tc.is_hour_change())

        with freeze_time("2012-01-14 15:00:00"):
            self.assertEqual(True, tc.is_hour_change())

        with freeze_time("2012-01-14 15:00:01"):
            self.assertEqual(False, tc.is_hour_change())

    def test_day_changed(self):
        with freeze_time("2012-01-14 14:59:59"):
            tc = TimeController()
            self.assertEqual(False, tc.is_day_change())

        with freeze_time("2012-01-14 15:00:00"):
            self.assertEqual(True, tc.is_day_change())

        with freeze_time("2012-01-14 15:00:01"):
            self.assertEqual(False, tc.is_day_change())

        with freeze_time("2012-01-14 23:59:59"):
            self.assertEqual(False, tc.is_day_change())

        with freeze_time("2012-01-15 00:00:00"):
            self.assertEqual(False, tc.is_day_change())


if __name__ == '__main__':
    unittest.main()
