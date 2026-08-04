# This is RadCAT. 

# Further BS coding, Yippee!
import pyart
import xarray as xr
import os
import io
import numpy as np
from csu_radartools import csu_fhc
import sys

def classify_summer(radar, rtemp, sweep):

    #=================================================
    # Hydrometeor phase calculation code using 
    # CSU radar tools python library to find which 
    # hydrometeor phase the aircraft is suppose to be 
    # in.
    #=================================================

    dbz = radar.variables['corrected_reflectivity_horizontal'].data[sweep]
    zdr = radar.variables['diff_reflectivity'].data[sweep]
    kdp = radar.variables['diff_phase'].data[sweep]
    rhv = radar.variables['copol_coeff'].data[sweep]
    score = csu_fhc.csu_fhc_summer(dz=dbz, zdr=zdr, rho=rhv, kdp=kdp, use_temp=True, band='C', T=rtemp)
    return score


def radar_aircraft_data_sync(aircraft_file, radar_data_directory):
    #===============================================================
    # This block of code looks at both radar times and aircraft times
    # and generates a surrounding environment radar scan based on
    # the location and timing of the aircraft during observations.
    # This will also return the phase classification given radar data
    # at the aircrafts location. 
    #
    # Inputs: 1. Aircraft Microphysics File
    #         2. Directory of CSAPR radar files close to flight time
    #
    # Ouputs: NetCDF microphysics file with reflectivity and phase
    #         classification included 
    #===============================================================

    # Initial read in of all possible radar times that could be plotted 
    with os.scandir(radar_data_directory) as entries:
        radar_files = list(entries)

    # List creation of all possible radar files 
    radar_file_times = []
    for x in range(len(radar_files)):
        radar_file_times.append((int(radar_files[x].name[30:36][0:2]) * 3600) + (int(radar_files[x].name[30:36][2:4]) * 60) + (int(radar_files[x].name[30:36][4:6])))

    # Open cloud microphysics file to eventually append it.
    cloud_micro = xr.open_dataset(aircraft_file)

    # Generate empty data array for radar sweeps to be populated in
    times = cloud_micro.Time.data  
    sweep_options = ['below', 'in', 'above']
    reflec_data_array = xr.DataArray(
        data = np.nan, 
        dims=["Time", "sweep"],
        coords={"Time": times, "sweep": sweep_options})

    phase_data_array = xr.DataArray(
        data = np.nan, 
        dims=["Time"],
        coords={"Time": times})

    # Looping through radar files to populate the radar sweep array with data 
    for number_files in range(len(radar_file_times) - 1):
        
        # Read in of both data files that will be later compared against aircraft times
        data1 = pyart.io.read(radar_data_directory + radar_files[number_files].name)
        data2 = pyart.io.read(radar_data_directory + radar_files[number_files + 1].name)

        # Code to find the start and end range of times that aircraft data can be compared against 
        file_start_time = radar_file_times[number_files] + data1.extract_sweeps([data1.nsweeps - 1]).time['data'].max()
        file_end_time = radar_file_times[number_files + 1] + data2.extract_sweeps([data2.nsweeps - 1]).time['data'].max()

        # Looping through every tenth aircraft time
        for time in range(len(cloud_micro.Time.data)):

            # If statement to find which aircraft times are within the radar time range 
            if cloud_micro.Time.data[time] >= file_start_time and cloud_micro.Time.data[time] < file_end_time:

                # Find the sweep that is appropriate to the aircrafts position 
                vert_radar_profile = pyart.util.columnsect.get_field_location(data2, cloud_micro.POS_Lat.data[time], cloud_micro.POS_Lon.data[time])
                sweep = np.argmin(abs(vert_radar_profile.corrected_reflectivity_horizontal.height.data - (cloud_micro.POS_Alt.data[time])))

                # Find if the sweep is within a valid time range or not
                sweep_time = data2.extract_sweeps([sweep]).time['data'].max()
                if (sweep_time + radar_file_times[number_files + 1]) <= cloud_micro.Time.data[time]:
                    
                    # Find if the sweep is at the lowest or highest position
                    if sweep == 0 or sweep == data2.nsweeps - 1:
                        reflec_data_below = np.nan 
                        reflec_data_ontop = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep]
                        reflec_data_above = np.nan

                    # Otherwise return regular above, on, and below sweeps
                    else:
                        reflec_data_below = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep - 1]
                        reflec_data_ontop = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep]
                        reflec_data_above = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep+1]
                
                # Otherwise if the sweep is not within a valid time use the data1 file for sweep return
                else:
                    vert_radar_profile = pyart.util.columnsect.get_field_location(data1, cloud_micro.POS_Lat.data[time], cloud_micro.POS_Lon.data[time])
                    sweep = np.argmin(abs(vert_radar_profile.corrected_reflectivity_horizontal.height.data - (cloud_micro.POS_Alt.data[time])))
                    
                    # Find if the sweep is at the lowest or highest position
                    if sweep == 0 or sweep == data1.nsweeps - 1:
                        reflec_data_below = np.nan 
                        reflec_data_ontop = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep]
                        reflec_data_above = np.nan

                    # Otherwise return regular above, on, and below sweeps
                    else:
                        reflec_data_below = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep - 1]
                        reflec_data_ontop = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep]
                        reflec_data_above = vert_radar_profile.corrected_reflectivity_horizontal.data[sweep+1]    

                # Code to calculate hydrometeor phase given vertical column 
                hydro_class = classify_summer(vert_radar_profile, float(cloud_micro.Air_Temp.sel(Time = cloud_micro.Time.data[time])), sweep)
                
                reflec_data = [reflec_data_below, reflec_data_ontop, reflec_data_above]
                reflec_data_array.loc[{'Time' : reflec_data_array.Time.data[time]}] = reflec_data
                phase_data_array.loc[{'Time' : phase_data_array.Time.data[time]}] = hydro_class

        print(f'{number_files + 1} of {len(radar_file_times) - 1} radar files complete')

    # Combining of datasets into one 
    reflec_data_array = reflec_data_array.to_dataset(name = 'Radar_Reflectivity')
    phase_data_array = phase_data_array.to_dataset(name = 'Phase_Classification')
    Data = xr.combine_by_coords([cloud_micro, reflec_data_array, phase_data_array])

    # Fixes encoding error after concat
    for var in Data.data_vars:
        Data[var].encoding = {}
    Data['Time'].encoding.clear()


    # Save data to netcdf file within flight data directory 
    Data.to_netcdf(aircraft_file[0:17] + '.radadd.nc')
    print(f'Data processing complete, outputed data file {aircraft_file[0:17]}.radadd.nc')

def main():
    if len(sys.argv) < 3:
        print('Missing arguments \n python3 RadCAT.py aircraft_microphysics_file.nc radar_data_directory/')
        sys.exit(1)

    else:
        aircraft_file = sys.argv[1]
        radar_data_directory = sys.argv[2]

        radar_aircraft_data_sync(aircraft_file, radar_data_directory)

if __name__ == '__main__':
    main()