#import
import numpy as np
import matplotlib.pyplot as pp
import netCDF4 as nc
import json
from datetime import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.lines import Line2D
from cartopy.feature import NaturalEarthFeature


#coords for site plotting on map
sites = {
    "Valparaiso University": (41.4639, -87.0439),  # CSV site
    "Valparaiso": (41.473093, -87.0611),
    "CHI_TAFT": (41.8781, -87.6298), #6545 W. Hurlbut St, Norwood Park
    "SWFP": (41.7574, -87.5418), #Eugene Sawyer Water Purification Plant
    "Gary-IITRI": (41.6066, -87.3049),
    "Michigan City-4th St": (41.7074, -86.8820),
    "La Porte\nE. Lincolnway": (41.6106, -86.7225),
    "Ogden Dunes": (41.6478, -87.1914),
    "ALSIP": (41.6689, -87.7387),
    "LEMONT": (41.6680, -87.9867),
    "LISLE": (41.8011, -88.0748),
    "ELGIN_DMV": (42.0354, -88.2825),
    "Hammond-141st St": (41.5834, -87.5000),
    "CHI_COM": (41.7194, -87.7478),
    "Evanston, IL": (42.0618, -87.6736)
}
crocus = {
    "NEIU": (41.9805, -87.7166),
    "CCIS": (41.8229, -87.6098),
    "ATMOS": (41.7016, -87.9951),
    "UIC": (41.8693, -87.6457),
    "CSU": (41.7200, -87.6128),
    "NU": (42.0514, -87.6777),
    "HUM": (41.9055, -87.7034),
    "DOWN": (41.7953, -88.0063),
    "VLPK": (41.7817, -87.6108),
    "SHEDD": (41.8676, -87.6130),
    "BIG": (41.7770, -87.6098)
    }

#Figure
fig = pp.figure(figsize=(14, 14))

#Map 
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.stock_img()  # adds a simple terrain/background image
roads = NaturalEarthFeature(
    category='cultural',
    name='roads',
    scale='10m',
    facecolor='none'
)
ax.add_feature(roads,
               edgecolor='gray',
               linewidth=0.5)
ax.set_extent([-88.5, -86.4, 41.3, 42.6], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.LAKES, alpha=0.2) #alpha makes land/lake border easier to see

"""

# add label for CROCUS sites' definitions
text = fig.text(0.50, 0.02,
                'NEIU: Northeastern Illinois University' \n
                'CCIS: NEIU Carruthers Center for Inner City Studies Rooftop '\n 
                'ATMOS: Argonne Testbed for Multiscale Observational Science '\n
                'UIC: University of Illinois Chicago' \n
                'CSU Prairie: Chicago State University Prairie Site' \n
                'CSU Roof: Chicago State Univerisity Rooftop Site' \n
                'BIG: West Woodlawn "Blacks in Green"' \n
                'NU: Northwestern University Scott Hall Rooftop' \n
                'HUM: Humboldt Park' \n
                'DOWN: Downers Grove Municipal Rooftop' \n
                'SHEDD: Shedd Aquarium Rooftop (Museum Campus)' \n
                'IBP: Indian boundary Prairies', 
                horizontalalignment='center', wrap=True)
"""

# Plot sites
for name, (lat, lon) in sites.items():
    ax.plot(lon, lat, "ro", markersize=6, transform=ccrs.PlateCarree())
    if name == "Valparaiso University":
        ax.plot(lon, lat, "bo", markersize=6,  transform=ccrs.PlateCarree())
        ax.text(lon + 0.02, lat - 0.03, name, fontsize=14, fontweight='bold', transform=ccrs.PlateCarree())
    elif name == "Valparaiso": 
        ax.text(lon, lat, name, fontsize=14, fontweight='bold', transform=ccrs.PlateCarree())
    elif name == "CHI_TAFT":
        ax.text(lon - 0.18, lat + 0, name, fontsize=14, transform=ccrs.PlateCarree())
    elif name == "CHI_COM":
        ax.text(lon - 0.1, lat + 0.03, name, fontsize=14, transform=ccrs.PlateCarree())
    elif name == "LISLE":
        ax.text(lon - 0.12, lat + 0.01, name, fontsize=14, transform=ccrs.PlateCarree())
    elif name == "Hammond-141st St":
        ax.text(lon - 0.3, lat + 0.01, name, fontsize=14, transform=ccrs.PlateCarree())
    elif name == "Ogden Dunes":
        ax.text(lon - 0.226, lat + 0.01, name, fontsize=14, transform=ccrs.PlateCarree())
    else:
        ax.text(lon + 0.02, lat + 0.005, name, fontsize=14, transform=ccrs.PlateCarree())


for name, (lat, lon) in crocus.items():
    ax.plot(lon, lat, "b+", markersize=6, transform=ccrs.PlateCarree())
    if name == "UIC":
        ax.text(lon - 0.04, lat - 0.03, name, fontsize=14, fontweight='bold', transform=ccrs.PlateCarree())
    elif name == "VLPK":
        ax.text(lon - 0.08, lat - 0.01, name, fontsize=14, transform=ccrs.PlateCarree())
    elif name == "BIG":
        ax.text(lon + 0.015, lat + 0, name, fontsize=14, fontweight='bold', transform=ccrs.PlateCarree())
    elif name == "NU":
        ax.text(lon - 0.057, lat - 0.01, name, fontsize=14, transform=ccrs.PlateCarree())
    elif name == "NEIU":
        ax.text(lon, lat, name, fontsize=14, fontweight='bold', transform=ccrs.PlateCarree())
    elif name == "BIG":
        ax.text(lon, lat, name, fontsize=14, fontweight='bold', transform=ccrs.PlateCarree())
    else:
        ax.text(lon + 0.015, lat + 0.01, name, fontsize=14, transform=ccrs.PlateCarree())

#legend
    legend_elements = [
    Line2D([0], [0], marker='+', color='b',
           linestyle='None', markersize=12,
           label='CROCUS Sites'),
    Line2D([0], [0], marker='o', color='w',
           markerfacecolor='r', markersize=10,
           label='EPA Monitoring Sites'),
    Line2D([0], [0], marker='o', color='w',
           markerfacecolor='b', markersize=10,
           label='Valparaiso University'),
    Line2D([], [], linestyle='None',
           label='Bold labels = sites used in study')
]

ax.legend(handles=legend_elements, loc='lower left', fontsize=20)

ax.set_title("Map of CROCUS Sites and Other Ozone Monitoring Sites in NW Indiana/NE Illinois", fontweight='bold', fontsize=20)
    
# Save Figure
pp.tight_layout()
pp.savefig("Thissen_map.png", dpi=300)
pp.show()
