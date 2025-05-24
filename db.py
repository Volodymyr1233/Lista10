from peewee import SqliteDatabase

db = SqliteDatabase('rentals.sqlite3')
if not db.connect():
    raise RuntimeError('Database connection failed.')