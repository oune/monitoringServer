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

if __name__ == '__main__':
    unittest.main()
