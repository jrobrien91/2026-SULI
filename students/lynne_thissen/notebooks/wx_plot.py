import pandas as pd
import numpy as np
import matplotlib.pyplot as pp

# Read CSV
csv = '/Users/lynnethissen/Desktop/mettower_20250901_20250930.csv'
df = pd.read_csv(csv)

# Check column names
print(df.columns)

df['Tower Date (local)'] = pd.to_datetime(df['Tower Date (local)'],
    format='%Y-%m-%d_%H:%M:%S')


#mask it up girl
df.loc[(df['Temp (C)'] < -20) | (df['Temp (C)'] > 45), 'Temp (C)'] = np.nan
df.loc[(df['Pres (mb)'] < 900) | (df['Pres (mb)'] > 1100), 'Pres (mb)'] = np.nan
df.loc[(df['Wspd (m/s)'] < 0) | (df['Wspd (m/s)'] > 40), 'Wspd (m/s)'] = np.nan
df.loc[(df['RH (%)'] < 0) | (df['RH (%)'] > 100), 'RH (%)'] = np.nan


# Create figure
fig, axs = pp.subplots(3, 2, figsize=(15, 12), sharex=True)

# 1. Temperature
axs[0,0].plot(df['Tower Date (local)'], df['Temp (C)'])
axs[0,0].set_title('Temperature')
axs[0,0].set_ylabel('°C')

# 2. Relative Humidity
axs[0,1].plot(df['Tower Date (local)'], df['RH (%)'])
axs[0,1].set_title('Relative Humidity')
axs[0,1].set_ylabel('%')

# 3. Pressure
axs[1,0].plot(df['Tower Date (local)'], df['Pres (mb)'])
axs[1,0].set_title('Pressure')
axs[1,0].set_ylabel('mb')

# 4. Wind Speed
axs[1,1].plot(df['Tower Date (local)'], df['Wspd (m/s)'])
axs[1,1].set_title('Wind Speed')
axs[1,1].set_ylabel('m/s')

# 5. Rainfall
axs[2,0].plot(df['Tower Date (local)'], df['Daily Total Rain (mm)'])
axs[2,0].set_title('Daily Rainfall')
axs[2,0].set_ylabel('mm')

# Empty panel for summary statistics
axs[2,1].axis('off')

max_temp = df['Temp (C)'].max()
min_temp = df['Temp (C)'].min()

axs[2,1].text(
    0.05, 0.9,
    f'Max Temp: {max_temp:.1f} °C\n'
    f'Min Temp: {min_temp:.1f} °C',
    fontsize=12,
    verticalalignment='top'
)

# Date formatting
for ax in axs.flat:
    ax.grid(True, alpha=0.3)

fig.suptitle('September 2025 Meteorological Tower Observations', fontsize=16)

pp.tight_layout()
pp.savefig('valpo_met_september25.png')
pp.show()