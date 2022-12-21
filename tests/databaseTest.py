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
        await db.save_now(3.1111, 2.111, 3.1111)

    async def test_save_many(self):
        db = Database("../db/machine_1.db")
        data = [
            ('2022-10-12 00:01:00.000', 2.111, 1111, 1111.2222),
            ('2022-10-12 00:02:00.000', 3.111, 3.22222, 3.444),
            ('2022-10-12 00:03:00.000', 4.111, 4.26512, 4.22112),
        ]
        await db.save_many(data)


if __name__ == '__main__':
    unittest.main()
