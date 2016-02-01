import sqlite3


class Cursor(object):
    def __init__(self, sql_cursor):
        self.sql_cursor = sql_cursor

    def select(self, *args):
        return self.sql_cursor.execute(*args)


class Database(object):
    def __init__(self):
        self.db = sqlite3.connect('./data/database.sqlite')

    def query(self):
        return Cursor(self.db.cursor())


db = None


def get_db(self):
    global db

    if not db:
        db = Database()

    return db
