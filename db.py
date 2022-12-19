import sqlite3


# sql lite 사용

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
        def try_check_data_table(conn):
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='data'")
            res = cursor.fetchone()[0]
            if res == 1:
                return True
            else:
                return False

        return self.execute(try_check_data_table)

    def init_table(self):
        def try_init_table(conn):
            conn.execute("CREATE TABLE data(id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT, value REAL)")

        self.execute(try_init_table)

    def save(self, data: float):
        def try_save(conn):
            cur = conn.cursor()
            cur.execute('insert into data(time, value) values (?, ?)', ('2022-12-01 00:00:00.000', data))

        self.execute(try_save)


db = Database("db/machine_1.db")
