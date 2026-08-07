import pandas as pd
import matplotlib.pyplot as plt

start = pd.Timestamp("2025-07-01 00:00")
end   = pd.Timestamp("2025-07-31 00:00")

# valpo ozone
valpo_df = pd.read_csv(
    "/Users/lynnethissen/Desktop/O3_Valpo_Data/O3_Valpo_2025_0701_0731.csv"
)

valpo_df.columns = valpo_df.columns.str.strip()

valpo_df["Date Time"] = pd.to_datetime(
    valpo_df["Date Time"],
    format="%m/%d/%y %H:%M"
)

valpo_df = valpo_df[
    (valpo_df["Date Time"] >= start) &
    (valpo_df["Date Time"] < end)
]

valpo_df["O3_ppb"] = valpo_df["O3(ppm)"] * 1000
valpo_df["Hour"] = valpo_df["Date Time"].dt.hour

ozone_diurnal = valpo_df.groupby("Hour")["O3_ppb"].mean()

# met tower
met = pd.read_csv(
    "/Users/lynnethissen/Desktop/met_tower/valpo_met_tower_2025_0701_0731.csv"
)

# Parse UTC timestamps
met["Date (YYYY-MM-DD_HH:MM:SS local)"] = pd.to_datetime(
    met["Date (YYYY-MM-DD_HH:MM:SS local)"],
    format="%Y-%m-%d_%H:%M:%S"
)
"""
# Convert to Central Time (CDT in July)
met["Tower Date (local)"] = (
    met["Server Date (UTC)"]
    .dt.tz_convert("America/Chicago")
    .dt.tz_localize(None)   # remove timezone information
)
"""
met = met[
    (met["Date (YYYY-MM-DD_HH:MM:SS local)"] >= start) &
    (met["Date (YYYY-MM-DD_HH:MM:SS local)"] < end)
]


met["Hour"] = met["Date (YYYY-MM-DD_HH:MM:SS local)"].dt.hour

swdown_diurnal = met.groupby("Hour")["SWdown (W/m2)"].mean()

# plot
fig, ax1 = plt.subplots(figsize=(9,5))

# Ozone
ax1.plot(
    ozone_diurnal.index,
    ozone_diurnal.values,
    color="tab:blue",
    marker="o",
    linewidth=2,
    label="Ozone"
)

ax1.set_xlabel("Hour of Day (Local Time)", fontsize=13)
ax1.set_ylabel("Ozone (ppb)", color="tab:blue", fontsize=13)
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax1.set_xticks(range(24))
ax1.set_xlim(0, 23)

# SWdown
ax2 = ax1.twinx()

ax2.plot(
    swdown_diurnal.index,
    swdown_diurnal.values,
    color="orange",
    marker="s",
    linewidth=2,
    label="SW Down"
)

ax2.set_ylabel(
    "SW Down (W m$^{-2}$)",
    color="orange",
    fontsize=13,
)
ax2.tick_params(axis="y", labelcolor="orange")

plt.title("Mean Diurnal Cycle: Ozone and Average Solar Radiation\nJuly 2025")

ax1.grid(alpha=0.3)
plt.tight_layout()
plt.show()
