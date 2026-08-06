#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot EPA Ozone Data for Valparaiso
lthissen, kbarber
"""

import json
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import time

# --- EPA Ozone Data Request, Valpo ---
url = (
    "https://aqs.epa.gov/data/api/sampleData/bySite?"
    'email=katelyn.barber@valpo.edu&key=mauvewolf78&param=44201'
    '&bdate=20260501'
    '&edate=20260531'
    '&state=18'
    '&county=127'
    '&site=0026'
)

print("Fetching EPA ozone data...")

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    raise SystemExit(f"Error fetching EPA data: {e}")

if "Data" not in data or len(data["Data"]) == 0:
    print("No data available for this month at this site.")
    exit()

ozone, date_time = [], []
for entry in data["Data"]:
    try:
        val = float(entry["sample_measurement"])
        date_d = entry["date_local"]
        time_s = entry["time_local"]
        dt_object = datetime.strptime(f"{date_d} {time_s}", "%Y-%m-%d %H:%M")
        ozone.append(val)
        date_time.append(dt_object)
    except Exception as e:
        print(f"Skipping entry due to error: {e}")

ozone = np.array(ozone)
date_time = np.array(date_time)

# --- Get sunrise/sunset from NOAA API ---
lat, lon = 41.4731, -87.0611
sunrise_times, sunset_times = [], []

print("Fetching sunrise/sunset times...")
for single_date in np.unique([dt.date() for dt in date_time]):
    date_str = single_date.strftime("%Y-%m-%d")
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date_str}&formatted=0"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        sdata = r.json()["results"]
        sunrise = datetime.fromisoformat(sdata["sunrise"])
        sunset = datetime.fromisoformat(sdata["sunset"])
        sunrise_times.append(sunrise)
        sunset_times.append(sunset)
        time.sleep(0.3)  # polite delay
    except Exception as e:
        print(f"Warning: Skipping {date_str} ({e})")

# --- Plot ---
fig, ax1 = plt.subplots(figsize=(16, 6))

# Plot ozone
ax1.plot(date_time, ozone, marker="o", linestyle="-", color="blue", markersize=3, label="Ozone (ppm)")

# Set bottom y-position for markers (5% above min ozone)
y_bottom = min(ozone) + 0.05 * (max(ozone) - min(ozone))

# Plot sunrise and sunset markers
ax1.scatter(sunrise_times, [y_bottom]*len(sunrise_times), color="red", marker="^", label="Sunrise", zorder=5)
ax1.scatter(sunset_times, [y_bottom]*len(sunset_times), color="green", marker="v", label="Sunset", zorder=5)

# Formatting x-axis
day_locator = mdates.DayLocator(interval=1)
day_formatter = mdates.DateFormatter("%d")
ax1.xaxis.set_major_locator(day_locator)
ax1.xaxis.set_major_formatter(day_formatter)

fig.autofmt_xdate()
ax1.grid(which="both", linestyle="--", alpha=0.6)
ax1.set_xlabel("Day of September 2025", fontweight="bold")
ax1.set_ylabel("Ozone (ppm)", fontweight="bold")
ax1.set_ylim(0,.09)
ax1.set_title("Valparaiso EPA Ozone Data\nwith Sunrise/Sunset Marker\nMay 2026", fontweight="bold")
ax1.legend()

plt.savefig("epa_ozone_May26.png", bbox_inches="tight", dpi=600)
plt.show()