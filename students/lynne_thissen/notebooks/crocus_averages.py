#imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as pp
import netCDF4 as nc
import glob
import re

# files
aqt_files = sorted(glob.glob('atmos-aqt-a1/*.nc'))
wxt_files = sorted(glob.glob('atmos-wxt-a1/*.nc'))

def get_date(fname):
    match = re.search(r'\d{8}', fname)
    return match.group(0) if match else None

aqt_dict = {get_date(f): f for f in aqt_files}
wxt_dict = {get_date(f): f for f in wxt_files}

#date filter
common_dates = sorted(set(aqt_dict.keys()) & set(wxt_dict.keys()))

start_date = "20250318"
end_date   = "20250819"

campaign_dates = [d for d in common_dates if start_date <= d <= end_date]

print(f"Matched campaign days: {len(campaign_dates)}")

# storage
aqt_time_all = []
wxt_time_all = []

o3, no2, pm25 = [], [], []
humidity, temperature, pressure = [], [], []

# load
for d in campaign_dates:

    fn1 = nc.Dataset(aqt_dict[d])
    fn2 = nc.Dataset(wxt_dict[d])

    # AQT
    t1 = fn1.variables["time"][:]
    base_date = pd.to_datetime(d, format="%Y%m%d")
    dates1 = base_date + pd.to_timedelta(t1, unit="ns")

    # WXT
    t2 = fn2.variables["time"][:]
    dates2 = base_date + pd.to_timedelta(t2, unit="s")

    # store times
    aqt_time_all.extend(dates1)
    wxt_time_all.extend(dates2)

    # var
    o3_vals = np.ma.filled(
        fn1.variables["o3"][:] * 1000,
        np.nan
    )

    no2_vals = np.array(
        fn1.variables["no2"][:] * 1000,
        dtype=float
    )

    pm25_vals = np.array(
        fn1.variables["pm2.5"][:],
        dtype=float
    )

    humidity_vals = np.array(
        fn2.variables["humidity"][:],
        dtype=float
    )

    temperature_vals = np.array(
        fn2.variables["temperature"][:],
        dtype=float
    )

    pressure_vals = np.array(
        fn2.variables["pressure"][:],
        dtype=float
    )

    # store variables
    o3.extend(o3_vals)
    no2.extend(no2_vals)
    pm25.extend(pm25_vals)

    humidity.extend(humidity_vals)
    temperature.extend(temperature_vals)
    pressure.extend(pressure_vals)

    fn1.close()
    fn2.close()

aqt_df = pd.DataFrame(
    {
        "o3": o3,
        "no2": no2,
        "pm25": pm25
    },
    index=pd.to_datetime(aqt_time_all)
).sort_index()

wxt_df = pd.DataFrame(
    {
        "humidity": humidity,
        "temperature": temperature,
        "pressure": pressure
    },
    index=pd.to_datetime(wxt_time_all)
).sort_index()

"""
#printing to check every single diagnosis there could ever be
print(aqt_df.loc["2025-07-15":"2025-07-15 00:20"])
print(aqt_df["o3"].last_valid_index())
print(aqt_df["no2"].last_valid_index())
print(aqt_df["pm25"].last_valid_index())
"""
late_file = aqt_dict["20250608"]


ds = nc.Dataset(late_file)

print(ds.variables["o3"][:20])
print(ds.variables["no2"][:20])
print(ds.variables["pm2.5"][:20])

ds.close()

ds = nc.Dataset(late_file)

print(np.ma.count(ds.variables["o3"][:]))
print(ds.variables["o3"][:].shape)

print(np.ma.count(ds.variables["no2"][:]))
print(np.ma.count(ds.variables["pm2.5"][:]))

ds.close()

for d in campaign_dates[-20:]:
    ds = nc.Dataset(aqt_dict[d])

    o3 = ds.variables["o3"][:]

    print(
        d,
        np.ma.count(o3),
        o3.shape[0]
    )

    ds.close()
#end print statements (please delete)


# cleaning time
aqt_df["o3"] = aqt_df["o3"].where(aqt_df["o3"] > 0.1, np.nan)
aqt_df["o3"] = aqt_df["o3"].where(aqt_df["o3"] < 85, np.nan)
aqt_df["no2"] = aqt_df["no2"].where(aqt_df["no2"] > 0, np.nan)
aqt_df["no2"] = aqt_df["no2"].where(aqt_df["no2"] < 85, np.nan)
aqt_df["pm25"] = aqt_df["pm25"].where(aqt_df["pm25"] < 55, np.nan)

aqt_df = aqt_df.apply(pd.to_numeric, errors="coerce")
wxt_df = wxt_df.apply(pd.to_numeric, errors="coerce")

aqt_hourly = aqt_df.resample("1h").mean()
wxt_hourly = wxt_df.resample("1h").mean()

hourly = pd.concat(
    [aqt_hourly, wxt_hourly],
    axis=1
)

print(hourly.head())
print(hourly.columns)

o3_8hr = hourly["o3"].rolling(8, min_periods=1).mean()
no2_8hr = hourly["no2"].rolling(8, min_periods=1).mean()
pm25_8hr = hourly["pm25"].rolling(8, min_periods=1).mean()

humidity_8hr = hourly["humidity"].rolling(8, min_periods=1).mean()
temperature_8hr = hourly["temperature"].rolling(8, min_periods=1).mean()
pressure_8hr = hourly["pressure"].rolling(8, min_periods=1).mean()

met_daily = hourly.resample("1D").mean()

# pm2.5 filtered
pm25_24hr = hourly["pm25"].rolling(24, min_periods=1).mean()

pm25_count = hourly["pm25"].resample("1D").count()
pm25_24hr = pm25_24hr.resample("1D").mean()
pm25_24hr = pm25_24hr.where(pm25_count >= 8)
# plot
fig, axs = pp.subplots(
    3, 2,
    figsize=(14,14),
    sharex=True
)

fig.suptitle(
    "CROCUS ATMOS \nStandard Averaged Products\n3/18/2025-8/19/2025",
    fontweight='bold',
    fontsize=20
)

# O3
axs[0,0].plot(o3_8hr.index, o3_8hr, color='green', label="8-hr mean")
axs[0,0].set_ylabel("O₃", fontweight='bold', fontsize=12)
axs[0,0].set_ylim(0, 80)

# NO2
axs[0,1].plot(aqt_hourly.index, aqt_hourly["no2"], color='orange', label="Hourly")
axs[0,1].plot(no2_8hr.index, no2_8hr, color='red', linestyle='--', label="8-hr")
axs[0,1].set_ylabel("NO₂", fontweight='bold', fontsize=12)
axs[0,1].set_ylim(0, 80)
axs[0,1].legend()

# PM2.5
axs[1,0].plot(pm25_24hr.index, pm25_24hr, color='blue', label="24-hr")
axs[1,0].plot(pm25_8hr.index, pm25_8hr, color='navy', linestyle='--', label="8-hr")
axs[1,0].set_ylabel("PM2.5", fontweight='bold', fontsize=12)
axs[1,0].set_ylim(0, 60)
axs[1,0].legend()

# Humidity
axs[1,1].plot(met_daily.index, met_daily["humidity"], color='purple', label="Daily")
axs[1,1].plot(humidity_8hr.index, humidity_8hr, color='violet', linestyle='--', label="8-hr")
axs[1,1].set_ylabel("Humidity", fontweight='bold', fontsize=12)
axs[1,1].set_ylim(0, 100)
axs[1,1].legend()

# Temperature
axs[2,0].plot(met_daily.index, met_daily["temperature"], color='red', label="Daily")
axs[2,0].plot(temperature_8hr.index, temperature_8hr, color='darkred', linestyle='--', label="8-hr")
axs[2,0].set_ylabel("Temperature", fontweight='bold', fontsize=12)
axs[2,0].set_ylim(0, 40)
axs[2,0].legend()

# Pressure
axs[2,1].plot(met_daily.index, met_daily["pressure"], color='black', label="Daily")
axs[2,1].plot(pressure_8hr.index, pressure_8hr, color='gray', linestyle='--', label="8-hr")
axs[2,1].set_ylabel("Pressure", fontweight='bold', fontsize=12)
axs[2,1].set_ylim(950, 1050)
axs[2,1].legend()

# formatting
for ax in axs.flat:
    ax.set_xlabel("Time")
    ax.tick_params(axis='x', labelrotation=45)

pp.tight_layout()
pp.savefig("atmos_fixed_averages.png", dpi=300)
pp.show()



