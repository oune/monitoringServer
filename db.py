import sqlite3
from datetime import datetime


class Database:
    def __init__(self, path: str):
        self.path = path

        def table_init(_):
            has_data_table = self.check_data_table()
            if not has_data_table:
                self.init_table()

        self.execute_sync(table_init)

    def execute_sync(self, func):
        conn = None
        try:
            conn = sqlite3.connect(self.path)
            res = func(conn)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            conn.close()

    async def execute(self, func):
        return self.execute_sync(func)

    def check_data_table(self):
        def query(conn):
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='data'")
            res = cursor.fetchone()[0]
            if res == 1:
                return True
            else:
                return False

        return self.execute_sync(query)

    def init_table(self):
        def query(conn):
            conn.execute("CREATE TABLE data(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP, value REAL)")

        self.execute_sync(query)

    async def get_all(self):
        def query(conn):
            cur = conn.cursor()
            cur.execute('select time, value from data order by time')
            return cur.fetchall()

        return await self.execute(query)

    async def get_by_one_day(self, date):
        def query(conn):
            cur = conn.cursor()
            cur.execute('SELECT time, value FROM data WHERE DATE(time) == ? order by time', (date,))
            return cur.fetchall()

        return await self.execute(query)

    async def get_by_duration(self, start, end):
        def query(conn):
            cur = conn.cursor()
            cur.execute('SELECT time, value FROM data WHERE DATE(time) >= ? and DATE(time) <= ? order by time',
                        (start, end))
            return cur.fetchall()

        return await self.execute(query)

    async def save(self, time, data: float):
        def query(conn):
            cur = conn.cursor()
            cur.execute('insert into data(time, value) values (?, ?)', (time, data))

        await self.execute(query)

    async def save_now(self, data):
        await self.save(datetime.now(), data)
