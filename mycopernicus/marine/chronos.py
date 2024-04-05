import datetime as dt
from numbers import Number

import numpy as np

SMOS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
SMOS_UNITS = "2000-01-01T00:00:00Z"


def float_to_timedelta(t, timeunit="days"):
    """ 
    Funcion 
    """
    auxdict = {timeunit: float(t)}
    return dt.timedelta(**auxdict)


def smos_timezero():
    """
    Funcion que devuelve en formate datetime el tiempo cero desde el cual se empiezan a contar los dias
    en los productos satelitales SMOS.
    """
    return timezero(SMOS_UNITS, SMOS_FORMAT)


def smos_to_datetime(smostime):
    """
    Funcion que transforma el tiempo de formato "numero de dias de una fecha inicial" a un formato
    datetime convencional.
    """
    time_zero = smos_timezero()
    if isinstance(smostime, Number):
        return time_zero + float_to_timedelta(smostime)
    else:
        return np.asarray([time_zero + float_to_timedelta(t) for t in smostime])


def datetime_to_smos(time):
    """
    Funcion que devuelve el numero de dias y su fraccion que pasaron desde el 2000-01-01 
    hasta la fecha indicada. Esta funcion esta pensada para los productos satelitales de SMOS. 
    """
    t0 = smos_timezero()
    ts = (time - t0).total_seconds()
    return ts/60/60/24


def timezero(unit, unit_format):
    """
    Funcion timezero template. En general los formatos de tiempo en marine copernicus sos analogs.
    Dias de distancia dada una fecha inicial. 
    unit = dia inicial en string
    unit_format = formato en el que se esta pasando el dia inicial
    """
    return dt.datetime.strptime(unit, unit_format)


def copernicus_to_datetime(time, unit=None, unit_format=None):
    """
    Funcion general que transforma el formato generico de tiempo de copernicus en datetime.
    """
    time_zero = timezero(unit, unit_format) if unit else smos_timezero()
    if isinstance(time, Number):
        return time_zero + float_to_timedelta(time)
    else:
        times = [time_zero + float_to_timedelta(t) for t in time]
        return np.asarray(times)
    

def datetime_to_copernicus(time, unit=None, unit_format=None):
    t0 = timezero(unit, unit_format) if unit else smos_timezero()
    ts = (time - t0).total_seconds()
    return ts/60/60/24



