import unittest
from freezegun import freeze_time
from dataController import StatMachine
from unittest import IsolatedAsyncioTestCase
from db import Database

db_1_path = "../db/machine_1.db"


class MyTestCase(IsolatedAsyncioTestCase):
    async def test_callback(self):
        db1 = Database(db_1_path)
        with freeze_time("2012-01-14 14:59:59"):
            machine1_stat = StatMachine('machine1', db1)
            await machine1_stat.add_vib([1.11 for i in range(0, 30)], [1.11 for i in range(0, 30)])
            await machine1_stat.add_temp([1.11 for i in range(0, 30)])

        with freeze_time("2012-01-14 15:00:00"):
            await machine1_stat.add_vib([3.11 for i in range(0, 30)], [1.11 for i in range(0, 30)])
            await machine1_stat.add_temp([1.11 for i in range(0, 30)])

        with freeze_time("2012-01-14 15:00:01"):
            await machine1_stat.add_vib([3.11 for i in range(0, 30)], [1.11 for i in range(0, 30)])
            await machine1_stat.add_temp([1.11 for i in range(0, 30)])

        with freeze_time("2012-01-14 15:01:01"):
            await machine1_stat.add_vib([3.11 for i in range(0, 30)], [1.11 for i in range(0, 30)])
            await machine1_stat.add_temp([1.11 for i in range(0, 30)])

        with freeze_time("2012-01-14 15:10:01"):
            await machine1_stat.add_vib([3.11 for i in range(0, 30)], [1.11 for i in range(0, 30)])
            await machine1_stat.add_temp([1.11 for i in range(0, 30)])

        with freeze_time("2012-01-14 15:59:59"):
            await machine1_stat.add_vib([6.11 for i in range(0, 30)], [1.11 for i in range(0, 30)])
            await machine1_stat.add_temp([1.11 for i in range(0, 30)])

        with freeze_time("2012-01-14 16:00:00"):
            await machine1_stat.add_vib([6.11 for i in range(0, 30)], [1.11 for i in range(0, 30)])
            await machine1_stat.add_temp([1.11 for i in range(0, 30)])


if __name__ == '__main__':
    unittest.main()
