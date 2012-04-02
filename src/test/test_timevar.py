import unittest
import os
import netCDF4
from datetime import timedelta, datetime, tzinfo
from src.cdm.timevar import Timevar
import numpy as np
from dateutil.parser import parse
import pytz

class TimevarTest(unittest.TestCase):
    def test_timevar_length(self):

        datafile = os.path.normpath(os.path.join(__file__,"../../resources/models/pws/pws_L2_2012040100.nc"))
        # Manually extract
        ds = netCDF4.Dataset(datafile)
        data = ds.variables['time'][:]
        # Timevar extract
        tvar = Timevar(datafile)
        assert data.shape == tvar.shape

        datafile = os.path.normpath(os.path.join(os.path.dirname(__file__),"./resources/files/ocean_avg_synoptic_seg22.nc"))
        # Manually extract
        ds = netCDF4.Dataset(datafile)
        data = ds.variables['ocean_time'][:]
        # Timevar extract
        tvar = Timevar(datafile, name='ocean_time')
        assert data.shape == tvar.shape

    def test_timevar_values(self):

        datafile = os.path.normpath(os.path.join(os.path.dirname(__file__),"./resources/files/ocean_avg_synoptic_seg22.nc"))

        # Manually extract
        # ocean_time:units = "seconds since 1990-01-01 00:00:00" ;
        # ocean_time:calendar = "gregorian" ;
        dt = datetime(1990,1,1,tzinfo=pytz.utc)
        ds = netCDF4.Dataset(datafile)
        data = ds.variables['ocean_time'][:]
        # Convert to days
        factor = 60 * 60 * 24
        data = data / factor

        # Timevar extract
        tvar = Timevar(datafile, name='ocean_time')

        assert np.allclose(data,tvar.days)


        # Now compare datetimes
        data = data.tolist()
        jds = []
        for x in data:
            jds.append(dt + timedelta(days=x))

        assert jds == tvar.dates