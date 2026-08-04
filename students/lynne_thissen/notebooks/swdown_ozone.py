import numpy
import pandas as pd
import matplotlib.pyplot as pp
import matplotlib.dates as mdates
import json
import requests
import numpy as np 
from datetime import datetime, timedelta
import os 
#ozone
o3 = pd.read_csv("O3_Valpo_2025_0914_0921.csv")

o3["Date Time"] = pd.to_datetime(
    o3["Date Time"],
    format="%m/%d/%y %H:%M"
)
# met tower
met = pd.read_csv("/home/lthissen/summer_research/synoptic_plots_september/mettower_20250901_20250926.csv")

met["Tower Date (local)"] = pd.to_datetime(
    met["Tower Date (local)"],
    format="%Y-%m-%d_%H:%M:%S"
)

# date
start = pd.Timestamp("2025-09-14 00:00")
end   = pd.Timestamp("2025-09-21 00:00")

o3 = o3[
    (o3["Date Time"] >= start) &
    (o3["Date Time"] < end)
]
o3["O3(ppb)"] = o3[" O3(ppm)"] * 1000
met = met[
    (met["Tower Date (local)"] >= start) &
    (met["Tower Date (local)"] < end)
]

#epa
url = (
    "https://aqs.epa.gov/data/api/sampleData/bySite?"
    'email=katelyn.barber@valpo.edu&key=mauvewolf78&param=44201'
    '&bdate=20250914'
    '&edate=20250921'
    '&state=18'
    '&county=127'
    '&site=0026'
)

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
ozone = ozone * 1000 #convert ppm to ppb


max_idx = np.argmax(ozone)
print(f"Highest ozone concentration: {ozone[max_idx]:.1f} ppb")
# plot
fig, ax1 = pp.subplots(figsize=(16,6))

# VU ozone
ax1.plot(
    o3["Date Time"],
    o3["O3(ppb)"],
    color="tab:blue",
    lw=2,
    label="VU Ozone"
)

# EPA ozone
ax1.plot(
    date_time,
    ozone,
    color="fuchsia",
    lw=2,
    marker="o",
    markersize=3,
    label="EPA Ozone"
)

ax1.set_ylabel("Ozone (ppb)", fontsize=14, weight="bold")
ax1.set_ylim(0, 80)

# Solar radiation
ax2 = ax1.twinx()

ax2.plot(
    met["Tower Date (local)"],
    met["SWdown (W/m2)"],
    color="orange",
    lw=2.5,
    label="SW Down"
)

ax2.set_ylabel("SW Down (W m$^{-2}$)", fontsize=14, weight="bold", color="orange")
ax2.tick_params(axis="y", colors="orange")

# Formatting
ax1.set_xlim(start, end)
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=6))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))

ax1.set_xlabel("Time (Local)", fontsize=14, weight="bold")
ax1.grid(alpha=0.4)

pp.title(
    "Valparaiso University Ozone, EPA, and Incoming Solar Radiation\n14–21 September 2025",
    fontsize=18,
    weight="bold",
)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

pp.tight_layout()
pp.savefig("valpo_ozone_swdown_epa_0914_0921.png", dpi=600)
pp.show()

print