import os

from peewee import SqliteDatabase

import models
from models import *
import db



class CommandLineInterfaceApp:

    def __init__(self):
        self._commands = {
            'list':(self._get_stations,'list stations'),
            'select':(self._select,'select station'),
            'mean_start':(lambda : self._id_wrap(self._get_mean_startstation_time),'mean start station'),
            'mean_end':(lambda : self._id_wrap(self._get_mean_endstation_time),'mean end station'),
            'unique_end':(lambda : self._id_wrap(self._get_unique_bikes_number),'unique bikes on station'),
            'min':(lambda : self._id_wrap(self._min_rentaltime_date),'min renting time'),
            'max':(lambda : self._id_wrap(self._max_rentaltime_date),'max renting time'),
            'info':(self._info,'information'),
        }
        self.selected_id = None

    def _info(self):
        r = 'commands\n'
        for k,(_,d) in self._commands.items():
            r+= f' {k} : {d}\n'
        r+= f'Selected station id: {self.selected_id}\n' if self.selected_id is not None else ''
        return r
    _rental_time_diff_query = fn.strftime('%s',Rental.end_time) - fn.strftime('%s',Rental.start_time)
    def _try(self,f,*args):
        if db.db is None or db.db.is_closed():
            return 'database is closed or not conected'
        else:
            return  f(*args)
    def _id_wrap(self,f):
        if self.selected_id is None:
            return 'Nie wybrano stacji'
        else:
            temp = f(self.selected_id)
            return temp if temp is not None else 'brak rekordow'
    def _select(self,id):
        if Station.select().where(Station.station_id==id).exists():
            self.selected_id = id
            return f'wybrano stacje {id}'
        else:
            return f'Brak takiej stacji {id}'
    def _get_stations(self)->str:
        result = ''
        for station in Station.select().order_by((Station.station_id).asc()):
            result += f'{station.station_id}\t{station.station_name}\n'
        return result
    def _get_mean_startstation_time(self, id):
        mean = (((
            Rental.select(fn.avg(self._rental_time_diff_query))))
                .where(Rental.rental_station==id)

        )
        return mean.scalar()
    def _get_mean_endstation_time(self, id):
        mean = (((
            Rental.select(fn.avg(self._rental_time_diff_query))))
                .where(Rental.return_station == id)
                )
        return mean.scalar()
    def _get_unique_bikes_number(self,id):
        number = (
            Rental.select(fn.COUNT(fn.DISTINCT(Rental.bike_number))).where((Rental.return_station==id) | (Rental.return_station==id))
        )
        return number.scalar()
    def _max_rentaltime_date(self, id):
        temp = Rental.select(Rental).where(Rental.rental_station==id).order_by((self._rental_time_diff_query).desc())
        return temp.first()
    def _min_rentaltime_date(self, id):
        temp = Rental.select(Rental).where(Rental.rental_station==id).order_by((self._rental_time_diff_query).asc())
        return temp.first()

    def start(self):

        line = ''
        while True:
            line = input('write:')
            if line == 'exit':
                break
            line = line.split(' ',maxsplit=1)
            key = line[0]
            arg = line[1] if len(line) > 1 else None
            if key in self._commands:
             try:
                if arg is not None:
                        print(self._commands[key][0](arg))
                else:
                        print(self._commands[key][0]())
             except TypeError:
                    print(f'wrong command')
            else:
                print('unknown command')




if __name__ == "__main__":

    c = CommandLineInterfaceApp()
    c.start()

