import numpy as np
import xarray as xr
import matplotlib.pyplot as pp
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Read grib file
ds = xr.open_dataset("wind_temp.grib", engine="cfgrib")

# Variables
temp = ds["t2m"] - 273.15
u = ds["u10"]
v = ds["v10"]

# Keep only Sept 15–22
temp = temp.sel(time=slice("2025-09-15", "2025-09-22"))
u = u.sel(time=slice("2025-09-15", "2025-09-22"))
v = v.sel(time=slice("2025-09-15", "2025-09-22"))

# Subset domain
lat_slice = slice(43.25, 39.0)
lon_slice = slice(-90, -86)

temp = temp.sel(latitude=lat_slice, longitude=lon_slice)
u = u.sel(latitude=lat_slice, longitude=lon_slice)
v = v.sel(latitude=lat_slice, longitude=lon_slice)

# Mask temperatures below 15°C
temp = temp.where(temp >= 15)

# Figure
fig = pp.figure(figsize=(19, 7))

gs = fig.add_gridspec(
    2, 5,
    width_ratios=[1, 1, 1, 1, 0.05],
    wspace=0.05,
    hspace=0.08
)

axes = [
    fig.add_subplot(gs[0,0], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[0,1], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[0,2], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[0,3], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[1,0], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[1,1], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[1,2], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[1,3], projection=ccrs.PlateCarree()),
]

cax = fig.add_subplot(gs[:,4])

levels = np.arange(15, 30, 0.25)

for ax, t in zip(axes, temp.time):

    daily = temp.sel(time=t)
    daily_u = u.sel(time=t)
    daily_v = v.sel(time=t)

    cf = ax.contourf(
        daily.longitude,
        daily.latitude,
        daily,
        cmap="coolwarm",
        levels=levels,
        extend="both",
        transform=ccrs.PlateCarree()
    )

    skip = 2

    ax.barbs(
        daily.longitude.values[::skip],
        daily.latitude.values[::skip],
        daily_u.values[::skip, ::skip],
        daily_v.values[::skip, ::skip],
        length=5,
        linewidth=0.6,
        transform=ccrs.PlateCarree()
    )

    ax.set_extent([-90, -86, 40.75, 43.2])
    ax.add_feature(cfeature.STATES, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAKES, alpha=0.3)
    ax.coastlines(resolution="10m")

    ax.set_title(
        t.dt.strftime("%b %d").item(),
        fontsize=12
    )

cbar = fig.colorbar(cf, cax=cax)
cbar.set_label("2-m Temperature (°C)", fontsize=12)

fig.suptitle(
    "ERA5 2-m Air Temperature and 10-m Wind at 00 UTC\nSeptember 15–22, 2025",
    fontsize=18
)
pp.tight_layout(rect=[0, 0, 0.97, 0.95])
pp.savefig("era5_temp_wind.png", dpi=300, bbox_inches="tight")
pp.show()