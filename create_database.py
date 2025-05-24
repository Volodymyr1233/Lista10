import sys
from models import Station, Rental
from db import db
from peewee import OperationalError




if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise FileNotFoundError("You don't specify file name")

    database_name = f"{sys.argv[1]}.sqlite3"

    db.init(database_name)
    try:
        db.connect()
    except OperationalError:
        raise FileNotFoundError("Can't connect to your database")

    db.create_tables([Station, Rental])

    db.close()