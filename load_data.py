import pandas as pd
from db import db
from models import Station, Rental
import sys
from peewee import OperationalError


def main():
    if len(sys.argv) < 3:
        raise ValueError("Please specify filename and database")
    try:
        df = pd.read_csv(f"csv/{sys.argv[1]}")
    except FileNotFoundError:
        raise FileNotFoundError("Please specify csv filename EXISTS!")
    except PermissionError:
        raise PermissionError("You don't have permissions")
    except pd.errors.EmptyDataError:
        raise ValueError("Your data is empty")

    db.init(f"{sys.argv[2]}.sqlite3")
    try:
        db.connect()
    except OperationalError:
        raise FileNotFoundError("Can't connect to your database")

    records = df.to_dict(orient="records")

    records_to_write_database = []

    for record in records:
        rental_station, _ = Station.get_or_create(station_name=record["Stacja wynajmu"])
        return_station, _ = Station.get_or_create(station_name=record["Stacja zwrotu"])

        records_to_write_database.append(Rental(
            uid_number=record['UID wynajmu'],
            bike_number=record['Numer roweru'],
            start_time=record['Data wynajmu'],
            end_time=record['Data zwrotu'],
            rental_station=rental_station,
            return_station=return_station
        ))

    with db.atomic():
        Rental.bulk_create(records_to_write_database, batch_size=100)

    db.close()

if __name__ == "__main__":
    main()


