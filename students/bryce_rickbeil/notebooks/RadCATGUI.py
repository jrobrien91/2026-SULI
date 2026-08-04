# This is a new version of RadCAT but instead uses a GUI to allow for 
# user interaction in selecting files to be processed using RadCAT 
# software. This will be awful code and will probably break...
# Good. Luck.

import tkinter as tk 
from tkinter import filedialog
from tkinter import ttk
import xarray as xr
import os
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyart
import numpy as np
import threading
#from csu_radartools import csu_fhc

# Initialization of the RadCAT display GUI
root = tk.Tk()
root.title("RadCAT Display GUI")
root.geometry("1000x600")
root.configure(bg='white')

# Global variables to track file paths safely
radar_dir = ""
micro_file = []

def select_directory_radar():
    global radar_dir
    selected = filedialog.askdirectory(title='Select a folder')
    if selected:
        radar_dir = selected + '/'
        radar_path_label.config(text=radar_dir)

radar_file_button = tk.Button(root, text='Browse Folder', command=select_directory_radar, bg="pink")
radar_file_button.place(x=10, y=0)
radar_label = tk.Label(root, text='Radar directory selected', font=('Arial', 10), bg='white')
radar_label.place(x=100, y=0)
radar_path_label = tk.Label(root, text='No file selected', bg='white', borderwidth=1, relief='solid')
radar_path_label.place(x=275, y=0)

def select_directory_hvps():
    global micro_file
    micro_file = filedialog.askopenfilenames(title='Select microphysics file(s)')
    if micro_file:
        micro_path_label.config(text=micro_file)

micro_file_button = tk.Button(root, text='Browse Folder', command=select_directory_hvps, bg='pink')
micro_file_button.place(x=10, y=30)
micro_label = tk.Label(root, text='Microphysics file selected', font=('Arial', 10), bg='white')
micro_label.place(x=100, y=30)
micro_path_label = tk.Label(root, text='No file selected', bg='white', borderwidth=1, relief='solid')
micro_path_label.place(x=275, y=30)

# Thread wrapper function to keep UI responsive
def start_processing():
    if not micro_file or not radar_dir:
        radar_path_label.config(text="ERROR: Select both paths first!", fg="red")
        return
    
    # Disable button so user doesn't click twice
    process_button.config(state="disabled", text="Processing...")
    
    # Run the heavy mathematical loops inside a separate background worker thread
    threading.Thread(target=process_data_func, args=(micro_file, radar_dir), daemon=True).start()


def process_data_func(aircraft_file, radar_data_directory):
    # Initialize the progress bar safely using context rules
    progress_bar['value'] = 0
    
    with os.scandir(radar_data_directory) as entries:
        radar_files = list(entries)

    if not radar_files:
        print("No radar files found.")
        root.after(0, lambda: process_button.config(state="normal", text="Process Data"))
        return

    # Gather times securely from string indexing
    radar_file_times = []
    for x in range(len(radar_files)):
        name = radar_files[x].name
        # Assumes format matches your layout specs
        hours = int(name[30:32])
        minutes = int(name[32:34])
        seconds = int(name[34:36])
        radar_file_times.append((hours * 3600) + (minutes * 60) + seconds)

    # Use the context manager `with` to load and completely unlock the file resource
    with xr.open_dataset(aircraft_file[0], engine='netcdf4') as cloud_micro:
        times = cloud_micro.Time.data  
        lats = cloud_micro.POS_Lat.data
        lons = cloud_micro.POS_Lon.data
        alts = cloud_micro.POS_Alt.data
        
        # Make a detached clean memory deep-copy of the dataset to save safely later
        output_ds = cloud_micro.copy(deep=True)

    sweep_options = ['below', 'in', 'above']
    reflec_data_array = xr.DataArray(
        data=np.nan, 
        dims=["Time", "sweep"],
        coords={"Time": times, "sweep": sweep_options})

    total_files = len(radar_file_times) - 1

    # Looping through files safely
    for number_files in range(total_files):
        data1 = pyart.io.read(radar_data_directory + radar_files[number_files].name)
        data2 = pyart.io.read(radar_data_directory + radar_files[number_files + 1].name)

        file_start_time = radar_file_times[number_files] + data1.extract_sweeps([data1.nsweeps - 1]).time['data'].max()
        file_end_time = radar_file_times[number_files + 1] + data2.extract_sweeps([data2.nsweeps - 1]).time['data'].max()

        for time_idx in range(len(times)):
            current_time = times[time_idx]

            if file_start_time <= current_time < file_end_time:
                # Find valid sweeps
                vert_radar_profile = pyart.util.columnsect.get_field_location(data2, lats[time_idx], lons[time_idx])
                sweep = np.argmin(abs(vert_radar_profile.corrected_reflectivity_horizontal.height.data - alts[time_idx]))

                sweep_time = data2.extract_sweeps([sweep]).time['data'].max()
                if (sweep_time + radar_file_times[number_files + 1]) <= current_time:
                    if sweep == 0 or sweep == data2.nsweeps - 1:
                        reflec_data_below = np.nan 
                        reflec_data_ontop = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep]
                        reflec_data_above = np.nan
                    else:
                        reflec_data_below = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep - 1]
                        reflec_data_ontop = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep]
                        reflec_data_above = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep + 1]
                else:
                    vert_radar_profile = pyart.util.columnsect.get_field_location(data1, lats[time_idx], lons[time_idx])
                    sweep = np.argmin(abs(vert_radar_profile.corrected_reflectivity_horizontal.height.data - alts[time_idx]))
                    
                    if sweep == 0 or sweep == data1.nsweeps - 1:
                        reflec_data_below = np.nan 
                        reflec_data_ontop = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep]
                        reflec_data_above = np.nan
                    else:
                        reflec_data_below = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep - 1]
                        reflec_data_ontop = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep]
                        reflec_data_above = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep + 1]    

                reflec_data = [reflec_data_below, reflec_data_ontop, reflec_data_above]
                reflec_data_array.loc[{'Time': current_time}] = reflec_data

        # Safely update GUI tracking elements from the worker thread using root.after
        progress_val = int(((number_files + 1) / total_files) * 100)
        root.after(0, lambda v=progress_val: progress_bar.config(value=v))

    # Append our newly computed calculations array straight into the independent dataset
    output_ds['corrected_reflectivity'] = reflec_data_array

    # Save output file cleanly away from the locked input path
    output_filename = os.path.dirname(aircraft_file[0]) + '/' + aircraft_file[0].split('/')[-1][0:-3] + '.radadd.nc'
    
    # Save step execution
    output_ds.to_netcdf(output_filename, format="NETCDF4")

    # Reset UI Elements when finished
    root.after(0, lambda: process_button.config(state="normal", text="Process Data"))
    root.after(0, lambda: process_button.config(text=f"Saved: {os.path.basename(output_filename)}", fg="black"))


# UI Setup for Execution trigger 
progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate', maximum=100)
progress_bar.place(x=10, y=90)

process_button = tk.Button(root, text='Process Data', command=start_processing, bg='lightgreen', font=('Arial', 11, 'bold'))
process_button.place(x=10, y=130)

root.mainloop()