import sqlite3
from datetime import datetime


class Database:
    def __init__(self, path: str):
        self.path = path

        def table_init(_):
            has_data_table = self.check_data_table()
            if not has_data_table:
                self.init_table()

        self.execute(table_init)

    def execute(self, func):
        try:
            conn = sqlite3.connect(self.path)
            res = func(conn)
            conn.commit()
            return res
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()

    def check_data_table(self):
        def query(conn):
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='data'")
            res = cursor.fetchone()[0]
            if res == 1:
                return True
            else:
                return False

        return self.execute(query)

    def init_table(self):
        def query(conn):
            conn.execute("CREATE TABLE data(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP, value REAL)")

        self.execute(query)

    def get_all(self):
        def query(conn):
            cur = conn.cursor()
            cur.execute('select * from data')
            print(cur.fetchall())

        self.execute(query)

    def get_by_one_day(self, date):
        def query(conn):
            cur = conn.cursor()
            cur.execute('SELECT * FROM data WHERE DATE(time) == ?', (date, ))
            print(cur.fetchall())

        self.execute(query)

    def save(self, time, data: float):
        def query(conn):
            cur = conn.cursor()
            cur.execute('insert into data(time, value) values (?, ?)', (time, data))

        self.execute(query)


db = Database("db/machine_1.db")
# db.save(datetime.now(), 3.22)
db.get_all()
print()
db.get_by_one_day('2022-12-19')
