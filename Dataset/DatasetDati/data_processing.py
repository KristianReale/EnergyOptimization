# -*- coding: utf-8 -*-
"""
Created on Mon May 20 17:14:27 2024

@author: trivedi_r
"""

#%% Section-1: POWER CSV FILES
# Data processing. Filename arrangements and resampling in 1 minute resolution
           
# =============================================================================
# #  STEP-XX (No need to do it again. Already done. Skip to Next step)
# Change filenames to a series of 1 to 20 in 'power' folder (DONE)
# =============================================================================
# import os
# folder_path = "D:/Nature sample/Nature/processed_data/power/"  # Replace with the path to your folder

# # Dictionary containing old and new filenames
# filename_dict = {
#     "90956_2020_W.csv": "H1_W.csv",
#     "90959_2020_W.csv": "H2_W.csv",
#     "90960_2020_W.csv": "H3_W.csv",
    
#     "90962_2020_W.csv": "H4_W.csv",
#     "90963_2020_W.csv": "H5_W.csv",
#     "91811_2020_W.csv": "H6_W.csv",
    
#     "91812_2020_W.csv": "H7_W.csv",
#     "91813_2020_W.csv": "H8_W.csv",
#     "91814_2020_W.csv": "H9_W.csv",
    
#     "91819_2020_W.csv": "H10_W.csv",
#     "91820_2020_W.csv": "H11_W.csv",
#     "91823_2020_W.csv": "H12_W.csv",
    
#     "91824_2020_W.csv": "H13_W.csv",
#     "91934_2020_W.csv": "H14_W.csv",
#     "91935_2020_W.csv": "H15_W.csv",
    
#     "91946_2020_W.csv": "H16_W.csv",
#     "91947_2020_W.csv": "H17_W.csv",
#     "91950_2020_W.csv": "H18_W.csv",
    
#     "91951_2020_W.csv": "H19_W.csv",
#     "91953_2020_W.csv": "H20_W.csv",
# }

# for filename in os.listdir(folder_path):
#     if filename.endswith(".csv"):
#         old_path = folder_path + filename
#         new_path = folder_path + filename_dict[filename]  # Get new filename from dictionary
#         os.rename(old_path, new_path)

       
# =============================================================================
# # STEP-XX (No need to do it again. Already done. Skip to Next step) 
# Set column name as filename and set values as 1 (status) for all files in folder(DONE)
# =============================================================================
# import pandas as pd
# import os

# # Path to the directory containing the CSV files
# csv_dir = 'D:/Nature sample/Nature/processed_data/power/'

# # Loop through each CSV file in the directory
# for csv_file in os.listdir(csv_dir):
#     # Check that the file is a CSV file
#     if csv_file.endswith('.csv'):
#         # Load the CSV file into a Pandas DataFrame
#         df = pd.read_csv(os.path.join(csv_dir, csv_file))
        
#         # Get the name of the column to update (same as the filename)
#         column_name = os.path.splitext(csv_file)[0]
        
#         # Update the column with 1s
#         df[column_name] = 1
        
#         # Save the updated DataFrame back to the CSV file
#         df.to_csv(os.path.join(csv_dir, csv_file), index=False)




# =============================================================================
# # STEP-XX (No need to do it again. Already done. Skip to Next step)
# # resample the data to 1 minute resolution (DONE)
# =============================================================================
# import os
# import pandas as pd

# # Specify the directory containing the CSV files
# directory = 'D:/Nature sample/Nature/processed_data/power/'

# # Loop through all CSV files in the directory
# for filename in os.listdir(directory):
#     if filename.endswith('.csv'):
#         # Read in the CSV file
#         df = pd.read_csv(os.path.join(directory, filename))
        
#         # Convert the date column to a datetime object
#         df['date'] = pd.to_datetime(df['date'])
        
#         # Set the date column as the index
#         df.set_index('date', inplace=True)
        
#         # Resample the data to 1 minute resolution
#         df_resampled = df.resample('min').min()
        
#         # Save the resampled CSV file
#         df_resampled.to_csv(os.path.join(directory, filename), index=True)

#%% Section-2: ENERGY CSV FILES
# Data processing. Filename arrangements and resampling in 1 minute resolution

# =============================================================================
# STEP-XX (No need to do it again. Already done. Skip to Next step)
# Change filename of all files in a directory 'energy' folder (DONE)
# =============================================================================
# Change filenames to a series of 1 to 20 in 'energy' folder
# import os

# folder_path = "D:/Nature sample/Nature/processed_data/energy/"  # Replace with the path to your folder

# # Dictionary containing old and new filenames
# filename_dict = {
#     "90956_2020_Wh.csv": "H1_Wh.csv",
#     "90959_2020_Wh.csv": "H2_Wh.csv",
#     "90960_2020_Wh.csv": "H3_Wh.csv",
    
#     "90962_2020_Wh.csv": "H4_Wh.csv",
#     "90963_2020_Wh.csv": "H5_Wh.csv",
#     "91811_2020_Wh.csv": "H6_Wh.csv",
    
#     "91812_2020_Wh.csv": "H7_Wh.csv",
#     "91813_2020_Wh.csv": "H8_Wh.csv",
#     "91814_2020_Wh.csv": "H9_Wh.csv",
    
#     "91819_2020_Wh.csv": "H10_Wh.csv",
#     "91820_2020_Wh.csv": "H11_Wh.csv",
#     "91823_2020_Wh.csv": "H12_Wh.csv",
    
#     "91824_2020_Wh.csv": "H13_Wh.csv",
#     "91934_2020_Wh.csv": "H14_Wh.csv",
#     "91935_2020_Wh.csv": "H15_Wh.csv",
    
#     "91946_2020_Wh.csv": "H16_Wh.csv",
#     "91947_2020_Wh.csv": "H17_Wh.csv",
#     "91950_2020_Wh.csv": "H18_Wh.csv",
    
#     "91951_2020_Wh.csv": "H19_Wh.csv",
#     "91953_2020_Wh.csv": "H20_Wh.csv",
#     }

# for filename in os.listdir(folder_path):
#     if filename.endswith(".csv"):
#         old_path = folder_path + filename
#         new_path = folder_path + filename_dict[filename]  # Get new filename from dictionary
#         os.rename(old_path, new_path)
 
# =============================================================================
## STEP-XX (No need to do it again. Already done. Skip to Next step)
## resample and linearly interpolate the data to 1 minute resolution (DONE)
# =============================================================================
# import os
# import pandas as pd

# # Specify the directory containing the CSV files
# directory = 'D:/Nature sample/Nature/processed_data/energy/'

# # Loop through all CSV files in the directory
# for filename in os.listdir(directory):
#     if filename.endswith('.csv'):
#         # Read in the CSV file
#         df = pd.read_csv(os.path.join(directory, filename))
        
#         # Convert the date column to a datetime object
#         df['date'] = pd.to_datetime(df['date'])
        
#         # Set the date column as the index
#         df.set_index('date', inplace=True)
        
#         # Resample the data to 1 minute resolution
#         df_resampled = df.resample('min').min()
#         df_interpolate = df_resampled.interpolate('linear')

        
#         # Save the resampled CSV file
#         df_interpolate.to_csv(os.path.join(directory, filename), index=True)
# =============================================================================
#%% Section-3: data processing for weather data. Weather data was downloaded from 
# nearest weather station to the project site from met eireann website historical data section.
# Below code turns monthly weather data (12 months) into one csv file for whole year.
# =============================================================================
## STEP-XX (No need to do it again. Already done)
# =============================================================================
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# # Specify the directory containing the CSV files
# directory = 'D:/Nature sample/Nature/original data/weather/'


# import os

# # Create an empty list to store DataFrames
# dfs = []

# # Loop through each CSV file in the folder
# for filename in os.listdir(directory):
#     if filename.endswith('.csv'):
#         # Read the CSV file into a DataFrame
#         filepath = os.path.join(directory, filename)
#         df = pd.read_csv(filepath)
        
#         # Append the DataFrame to the list
#         dfs.append(df)

# # Concatenate all DataFrames in the list
# combined_df = pd.concat(dfs, ignore_index=True)

# # Convert the 'date' column to datetime format
# combined_df['date'] = pd.to_datetime(combined_df['date'])

# # Sort the DataFrame by the 'date' column
# combined_df.sort_values(by='date', inplace=True)

# # Print the combined DataFrame
# print(combined_df)

# combined_df.to_csv('weather.csv')