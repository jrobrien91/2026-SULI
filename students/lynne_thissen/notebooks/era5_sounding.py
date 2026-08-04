#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
era5 reanalysis sounding create
@author: lynnethissen
"""
import numpy as np
import xarray as xr
import matplotlib.pyplot as pp
import matplotlib as mpl
import metpy.calc as mpcalc
from metpy.units import units
from metpy.plots import SkewT
from metpy.plots import Hodograph
import cdsapi

# settings!
lat = 42.4838
lon = -87.0640       
location = 'Valparaiso, IN'
date = "2025-09-19"
time = "06:00"       # UTC
outfile = "era5_sounding.nc"

"""
# download era 5 --> comment out once you've loaded in the data and created the nc file
pad = 0.5

client = cdsapi.Client()

year, month, day = date.split("-")

client.retrieve(
    "reanalysis-era5-pressure-levels",
    {
        "product_type": "reanalysis",
        "variable": [
            "temperature",
            "relative_humidity",
            "u_component_of_wind",
            "v_component_of_wind",
            "geopotential",
        ],
        "pressure_level": [
            "1000","975","950","925","900","875","850","825",
            "800","775","750","700","650","600","550","500",
            "450","400","350","300","250","225","200","175",
            "150","125","100","70","50","30","20","10"
        ],
        "year": year,
        "month": month,
        "day": day,
        "time": time,
        "area": [lat + pad, lon - pad, lat - pad, lon + pad],
        "data_format": "netcdf",
    },
    outfile,
)
"""
# land
outfile = "era5_sounding.nc"
ds = xr.open_dataset(outfile)

lat_name = "latitude" if "latitude" in ds.coords else "lat"
lon_name = "longitude" if "longitude" in ds.coords else "lon"

profile = ds.sel(
    {lat_name: lat, lon_name: lon},
    method="nearest"
)

if "valid_time" in profile.dims:
    profile = profile.isel(valid_time=0)
elif "time" in profile.dims:
    profile = profile.isel(time=0)

p = profile.pressure_level.values.astype(float) * units.hPa
T = (profile.t.values - 273.15) * units.degC
RH = np.clip(profile.r.values, 0, 100) * units.percent
Td = mpcalc.dewpoint_from_relative_humidity(T, RH)

u = profile.u.values * units("m/s")
v = profile.v.values * units("m/s")

# Put surface first
order = np.argsort(p.magnitude)[::-1]

p = p[order]
T = T[order]
Td = Td[order]
u = u[order]
v = v[order]

# skew-t!
fig = pp.figure(figsize=(8,10))
skew = SkewT(fig, rotation=45)

skew.plot(p, T, "r", linewidth=2, label="Temperature")
skew.plot(p, Td, "g", linewidth=2, label="Dewpoint")
skew.plot_barbs(p, u, v)

skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-40, 40)

skew.plot_dry_adiabats(alpha=0.4)
skew.plot_moist_adiabats(alpha=0.4)
skew.plot_mixing_lines(alpha=0.4)

# Parcel path
try:
    parcel = mpcalc.parcel_profile(p, T[0], Td[0]).to("degC")
    skew.plot(p, parcel, "k--", linewidth=2)

    lcl_p, lcl_t = mpcalc.lcl(p[0], T[0], Td[0])
    skew.plot(lcl_p, lcl_t, "ko")

    skew.shade_cape(p, T, parcel)
    skew.shade_cin(p, T, parcel, Td)
except Exception as e:
    print(e)
    
#hodograph
ax_hodo = fig.add_axes((0.73, 0.60, 0.25, 0.25))
h = Hodograph(ax_hodo, component_range=40.)

h.add_grid(increment=10)

h.plot_colormapped(u, v, p)
ax_hodo.set_title(f'Hodograph at {time}', fontsize=11)


pp.title(f"ERA5 Sounding\n{date} {time} UTC\n{location}")
pp.legend()
pp.tight_layout(rect=[0, 0, 0.75, 1])
pp.savefig(f'/Users/lynnethissen/Desktop/skew_t/skewt_{date}_{time}_{location}.png')
pp.show() 
