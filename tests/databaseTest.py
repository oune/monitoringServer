import unittest
from unittest import IsolatedAsyncioTestCase
from db import Database


class MyTestCase(IsolatedAsyncioTestCase):
    async def test_read(self):
        db = Database("../db/machine_1.db")
        print(await db.get_all())
        print(await db.get_by_one_day('2022-12-19'))
        print(await db.get_by_duration('2022-12-13', '2022-12-20'))

    async def test_save_now(self):
        db = Database("../db/machine_1.db")
        await db.save_now(3.1111)

    async def test_save_many(self):
        db = Database("../db/machine_1.db")
        data = [
            ('2022-10-12 00:01:00.000', 2.111),
            ('2022-10-12 00:02:00.000', 3.111),
            ('2022-10-12 00:03:00.000', 4.111),
        ]
        await db.save_many(data)


if __name__ == '__main__':
    unittest.main()
