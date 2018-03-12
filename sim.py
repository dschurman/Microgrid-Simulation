import os
import inspect
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# dependencies: pvlib (pip install pvlib)
import pvlib
from pvlib import pvsystem
from pvlib.location import Location

# example from http://nbviewer.jupyter.org/github/pvlib/pvlib-python/blob/master/docs/tutorials/pvsystem.ipynb
tus = Location(32.2, -111, 'US/Arizona', 700, 'Tucson')

times_loc = pd.date_range(start=datetime.datetime(2014,4,1), end=datetime.datetime(2014,4,2), freq='30s', tz=tus.tz)
solpos = pvlib.solarposition.get_solarposition(times_loc, tus.latitude, tus.longitude)
dni_extra = pvlib.irradiance.extraradiation(times_loc)
airmass = pvlib.atmosphere.relativeairmass(solpos['apparent_zenith'])
pressure = pvlib.atmosphere.alt2pres(tus.altitude)
am_abs = pvlib.atmosphere.absoluteairmass(airmass, pressure)
cs = tus.get_clearsky(times_loc)

surface_tilt = tus.latitude
surface_azimuth = 180  # pointing south

aoi = pvlib.irradiance.aoi(surface_tilt, surface_azimuth,
                           solpos['apparent_zenith'], solpos['azimuth'])
total_irrad = pvlib.irradiance.total_irrad(surface_tilt,
                                           surface_azimuth,
                                           solpos['apparent_zenith'],
                                           solpos['azimuth'],
                                           cs['dni'], cs['ghi'], cs['dhi'],
                                           dni_extra=dni_extra,
                                           model='haydavies')

# dictionary of a bunch of existing solar panels and their specifications
sandia_modules = pvsystem.retrieve_sam(name='SandiaMod')
# get specific panle info
sandia_module = sandia_modules.Canadian_Solar_CS5P_220M___2009_
module = sandia_module

# a sunny, calm, and hot day in the desert
temps = pvsystem.sapm_celltemp(total_irrad['poa_global'], 0, 30)

effective_irradiance = pvlib.pvsystem.sapm_effective_irradiance(
    total_irrad['poa_direct'], total_irrad['poa_diffuse'],
    am_abs, aoi, module)
effective_irradiance.plot()
plt.show()
'''
GRAPH KEY: 
i_sc : Short-circuit current (A)
i_mp : Current at the maximum-power point (A)
v_oc : Open-circuit voltage (V)
v_mp : Voltage at maximum-power point (V)
p_mp : Power at maximum-power point (W)
i_x : Current at module V = 0.5Voc, defines 4th point on I-V curve for modeling curve shape
i_xx : Current at module V = 0.5(Voc+Vmp), defines 5th point on I-V curve for modeling curve shape
'''
sapm_1 = pvlib.pvsystem.sapm(effective_irradiance, temps['temp_cell'], module)
sapm_1.plot()
plt.show()