from peewee import *
from db import db


class BaseModel(Model):
    class Meta:
        database = db


class Station(BaseModel):
    station_id = PrimaryKeyField(column_name="station_id")
    station_name = CharField(column_name="Nazwa stacji", max_length=255, null=False)


class Rental(BaseModel):
    rental_id = PrimaryKeyField(column_name="rental_id")
    uid_number = IntegerField(column_name="UID wynajmu", null=False)
    bike_number = IntegerField(column_name="Numer roweru", null=False)
    start_time = DateTimeField(column_name="Data wynajmu", null=False)
    end_time = DateTimeField(column_name="Data zwrotu", null=False)
    rental_station = ForeignKeyField(Station, column_name="Stacja wynajmu", null=False, backref="rentals_start")
    return_station = ForeignKeyField(Station, column_name="Stacja zwrotu", null=False, backref="rentals_return")
