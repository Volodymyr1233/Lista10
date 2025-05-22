import sys
from models import Station, Rental
from db import db




if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise FileExistsError("You don't specify file name")

    database_name = f"{sys.argv[1]}.sqlite3"

    db.init(database_name)
    db.connect()

    db.create_tables([Station, Rental])

    db.close()