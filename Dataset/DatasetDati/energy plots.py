# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 17:22:30 2023

@author: rohit.trivedi
"""

#%% Section-1: Plotting the figures from energy data.
# =============================================================================
# STEP-1: Rename columns according to filename and extract specific column.
# Then, Plot aggregated annual energy consumption profiles
# =============================================================================
import pandas as pd
import os

# Create an empty dataframe to store the extracted columns
new_df = pd.DataFrame()

# Loop through all the csv files in the directory
for file_name in os.listdir('D:/Nature sample/Nature/processed_data/energy/'):
    if file_name.endswith('.csv'):
        # Load the csv file into a dataframe
        df = pd.read_csv('D:/Nature sample/Nature/processed_data/energy/' + file_name)
        
        # Rename the columns using the file name
        new_column_names = {}
        for column_name in df.columns:
            new_column_names[column_name] = f"{file_name[:-4]}_{column_name}"
        df = df.rename(columns=new_column_names)
        
        # Extract the desired column and add it to the new dataframe
        column_name_to_extract = f"{file_name[:-4]}_ Consumption(Wh)"
        new_df[column_name_to_extract] = df[column_name_to_extract]

# Print the new dataframe
print(new_df)

new_df.set_axis(['H10', 'H11', 'H12', 'H13', 'H14', 'H15',
                  'H16', 'H17', 'H18', 'H19', 'H1', 'H20',
                  'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
                  'H8', 'H9'], axis=1, 
                        inplace=True)


# Reorder the columns from 'H1' to 'H20'
column_order = ['H{}'.format(i) for i in range(1, 21)]
new_df = new_df.reindex(columns=column_order)

# Print the reordered dataframe
print(new_df)

new_df_sum = new_df.sum(axis=0).round(decimals = 2)/1000
df = new_df_sum.to_frame()
print(df)
new_sum=df
new_sum.columns = ['values']
new_sum
print(df)
new_df_sumT=new_sum.transpose()
new_df_sumT
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
# sns.barplot(data=new_df_sumT)
def show_values(axs, orient="v", space=.01):
    def _single(ax):
        if orient == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height() + (p.get_height()*0.01)
                value = '{:.1f}'.format(p.get_height())
                ax.text(_x, _y, value, ha="center") 
        elif orient == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width()/2 + float(space)
                _y = p.get_y() + p.get_height() - (p.get_height()*0.5)
                value = '{:.1f}'.format(p.get_width())
                ax.text(_x, _y, value, ha="center")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _single(ax)
    else:
        _single(axs)

plt.figure(figsize=(16,6), dpi=600) #set dpi=2000 for better resolution
p=sns.barplot(data=new_df_sumT,
                orient='v', palette="YlGnBu")
# YlGnBu # pastel # GnBu_d
show_values(p, "v", space=0)
plt.xticks(fontsize=12, rotation=0)
plt.yticks(fontsize=12, rotation=0)
p.set_xlabel("House ID", fontsize=16)
p.set_ylabel("Annual energy consumption (kWh/annum)", fontsize=16)
plt.savefig('D:/Nature sample/Nature/figures/Annual energy consumption.png')


# =============================================================================
# STEP-2: Radar plot using plotly
# Plotly figure will be saved in specified folder and be automatically shown 
# in your default web browser. Size of desktop screen and web browser window 
# might change the appearance of the plot since plotly graphs adjusts by screen 
# and browser window size.  
# =============================================================================
import pandas as pd
import os

# Create an empty dataframe to store the extracted columns
new_df_P = pd.DataFrame()
new_df_C = pd.DataFrame()
new_df_TG = pd.DataFrame()
new_df_FG = pd.DataFrame()
# Loop through all the csv files in the directory
for file_name in os.listdir('D:/Nature sample/Nature/processed_data/energy/'):
    if file_name.endswith('.csv'):
        # Load the csv file into a dataframe
        df = pd.read_csv('D:/Nature sample/Nature/processed_data/energy/' + file_name)
        
        # Rename the columns using the file name
        new_column_names = {}
        for column_name in df.columns:
            new_column_names[column_name] = f"{file_name[:-4]}_{column_name}"
        df = df.rename(columns=new_column_names)
        
        # Extract the desired column and add it to the new dataframe
        column_name_to_extract1 = f"{file_name[:-4]}_ Production(Wh)"
        new_df_P[column_name_to_extract1] = df[column_name_to_extract1]
        
        column_name_to_extract2 = f"{file_name[:-4]}_ Consumption(Wh)"
        new_df_C[column_name_to_extract2] = df[column_name_to_extract2]
        
        column_name_to_extract3 = f"{file_name[:-4]}_ Feed-in(Wh)"
        new_df_TG[column_name_to_extract3] = df[column_name_to_extract3]
        
        column_name_to_extract4 = f"{file_name[:-4]}_ From grid(Wh)"
        new_df_FG[column_name_to_extract4] = df[column_name_to_extract4]

# Print the new dataframe
print(new_df_P)
# new_df_P.to_csv('new_df_Px.csv')
print(new_df_C)
# new_df_C.to_csv('new_df_Cx.csv')
print(new_df_TG)
print(new_df_FG)
# Set the axis in each dataframe
new_df_P.set_axis(['H10', 'H11', 'H12', 'H13', 'H14', 'H15',
                  'H16', 'H17', 'H18', 'H19', 'H1', 'H20',
                  'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
                  'H8', 'H9'], axis=1, inplace=True)
new_df_C.set_axis(['H10', 'H11', 'H12', 'H13', 'H14', 'H15',
                  'H16', 'H17', 'H18', 'H19', 'H1', 'H20',
                  'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
                  'H8', 'H9'], axis=1, inplace=True)
new_df_TG.set_axis(['H10', 'H11', 'H12', 'H13', 'H14', 'H15',
                  'H16', 'H17', 'H18', 'H19', 'H1', 'H20',
                  'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
                  'H8', 'H9'], axis=1, inplace=True)
new_df_FG.set_axis(['H10', 'H11', 'H12', 'H13', 'H14', 'H15',
                  'H16', 'H17', 'H18', 'H19', 'H1', 'H20',
                  'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
                  'H8', 'H9'], axis=1,  inplace=True)

# Sum all the values in the column
new_df_P_sum= new_df_P.sum(axis=0).round(decimals = 2)/1000
new_df_C_sum= new_df_C.sum(axis=0).round(decimals = 2)/1000
new_df_TG_sum= new_df_TG.sum(axis=0).round(decimals = 2)/1000
new_df_FG_sum= new_df_FG.sum(axis=0).round(decimals = 2)/1000
# Transpose all the dataframes
new_df_P_sumT=new_df_P_sum.transpose()
new_df_C_sumT=new_df_C_sum.transpose()
new_df_TG_sumT=new_df_TG_sum.transpose()
new_df_FG_sumT=new_df_FG_sum.transpose()
new_df_P_sumT

# Set index to transposed dataframes according to house ID and reset 
new_df_P_sumT.index= ['H10', 'H11', 'H12', 'H13', 'H14', 'H15',
                  'H16', 'H17', 'H18', 'H19', 'H1', 'H20',
                  'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
                  'H8', 'H9']
new_df_P_sumT.index.name='House ID'
new_df_P_sumT=new_df_P_sumT.reset_index('House ID')
new_df_P_sumT.columns = ['ID', 'values']

new_df_C_sumT.index= ['H10', 'H11', 'H12', 'H13', 'H14', 'H15',
                  'H16', 'H17', 'H18', 'H19', 'H1', 'H20',
                  'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
                  'H8', 'H9']
new_df_C_sumT.index.name='House ID'
new_df_C_sumT=new_df_C_sumT.reset_index('House ID')
new_df_C_sumT.columns = ['ID', 'values']

new_df_FG_sumT.index= ['H10', 'H11', 'H12', 'H13', 'H14', 'H15',
                  'H16', 'H17', 'H18', 'H19', 'H1', 'H20',
                  'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
                  'H8', 'H9']
new_df_FG_sumT.index.name='House ID'
new_df_FG_sumT=new_df_FG_sumT.reset_index('House ID')
new_df_FG_sumT.columns = ['ID', 'values']

new_df_TG_sumT.index= ['H10', 'H11', 'H12', 'H13', 'H14', 'H15',
                  'H16', 'H17', 'H18', 'H19', 'H1', 'H20',
                  'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
                  'H8', 'H9']
new_df_TG_sumT.index.name='House ID'
new_df_TG_sumT=new_df_TG_sumT.reset_index('House ID')
new_df_TG_sumT.columns = ['ID', 'values']
# Making copy of dataframes and extracting non zero values
new_df_P_sumT_drop=new_df_P_sumT
new_df_C_sumT_drop=new_df_C_sumT
new_df_FG_sumT_drop=new_df_FG_sumT
new_df_TG_sumT_drop=new_df_TG_sumT

new_df_P_sumT_drop= new_df_P_sumT_drop[new_df_P_sumT_drop['values'] != 0]
new_df_P_sumT_drop
new_df_C_sumT_drop= new_df_C_sumT_drop[new_df_C_sumT_drop['values'] != 0]
new_df_C_sumT_drop.drop([2,4,5,6,8,9,11,16,18,19], axis=0, inplace=True)
new_df_C_sumT_drop
new_df_FG_sumT_drop= new_df_FG_sumT_drop[new_df_FG_sumT_drop['values'] != 0]
new_df_FG_sumT_drop
new_df_FG_sumT_drop.drop([2,4,5,6,8,9,11], axis=0, inplace=True)
new_df_FG_sumT_drop.drop([16], axis=0, inplace=True)
new_df_FG_sumT_drop.drop([18,19], axis=0, inplace=True)
new_df_FG_sumT_drop
new_df_TG_sumT_drop= new_df_TG_sumT_drop[new_df_TG_sumT_drop['values'] != 0]
new_df_TG_sumT_drop
# 
# Importing plotly library
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
import plotly.io as io
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.io as pio
io.renderers.default='browser'
io.renderers.default='svg'
import plotly.express as px
fig = make_subplots(rows=2, cols=2, vertical_spacing=0.15, 
                    horizontal_spacing=0.12,
                    specs=[[{"type":"polar"}, {"type":"polar"}], 
                                            [{"type":"polar"}, {"type":"polar"}]],
                    subplot_titles=('<b>Production(kWh)</b>', 
                                    '<b>Consumption(kWh)</b>', 
                                    '<b>Energy-feed to utility grid (kWh)</b>',
                                    '<b>Energy from utility grid (kWh)</b>',))
fig.add_trace(go.Scatterpolar(
          r=new_df_P_sumT_drop["values"],
          theta=new_df_P_sumT_drop["ID"],
          fill='toself',
          # name='Production(Wh)',
          marker=dict(size=5, color = "gray"),
          fillcolor='skyblue',
          showlegend=False), row=1, col=1)

fig.add_trace(go.Scatterpolar(
          r=new_df_C_sumT_drop["values"],
          theta=new_df_C_sumT_drop["ID"],
          fill='toself',
          # name='Consumption (Wh)',
          marker=dict(size=5, color = "lightcoral"),
          fillcolor='lightslategray',
          showlegend=False), row=1, col=2)

fig.add_trace(go.Scatterpolar(
          r=new_df_TG_sumT_drop["values"],
          theta=new_df_TG_sumT_drop["ID"],
          fill='toself',
          # name='Energy-feed to utility grid (Wh)',
          marker=dict(size=5, color = "orangered"),
          fillcolor='peru',
          showlegend=False), row=2, col=1)

fig.add_trace(go.Scatterpolar(
          r=new_df_FG_sumT_drop["values"],
          theta=new_df_FG_sumT_drop["ID"],
          fill='toself',
          # name='Energy from utility grid (Wh)',
          marker=dict(size=5, color="mediumpurple"),
          fillcolor='steelblue',
          showlegend=False), row=2, col=2)

fig.update_layout(title_text='<b>Annual energy profiles</b>', title_x=0.5) # height=600, width=1400,
fig.update_polars(radialaxis_ticklabelstep=2)
fig.update_annotations(yshift=20)
pio.write_html(fig, file='figure.html', auto_open=True)  
fig.show()
#from kaleido.scopes.plotly import PlotlyScope
#pio.kaleido.scope.default_format = "svg"
# save plot in PNG format in specific directory
path = 'D:/Nature sample/Nature/figures/Annual energy profiles.png'
pio.write_image(fig, path, format='png')


# =============================================================================
## STEP-3: Power profiles per day for house H4 (ID-90962---"H4") 
# =============================================================================
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set the directory where the CSV files are located
directory = 'D:/Nature sample/Nature/processed_data/energy/'

# Set the name of the CSV file you want to load
filename = 'H4_Wh.csv'

# Construct the full path to the CSV file
filepath = os.path.join(directory, filename)

# Load the CSV file into a Pandas DataFrame
df_H4 = pd.read_csv(filepath)

# Convert the 'date_column' to datetime format
df_H4['date'] = pd.to_datetime(df_H4['date'])

# Calculate time difference between consecutive data points in hours
time_diff = df_H4['date'].diff().dt.total_seconds() / 3600

# Convert all Wh values to W except for the last column
columns_to_convert = df_H4.columns[1:-1]  # Exclude the first and last columns
df_H4[columns_to_convert] /= time_diff.values[:, None]  # Divide all selected columns by time_diff to convert to W


# Filter the DataFrame to include only the data for one week in December
december_data = df_H4[(df_H4['date'].dt.month == 12) & (df_H4['date'].dt.week == 50)]
december_data
fig, axes = plt.subplots(nrows=7, ncols=1, figsize=(16,10), sharex=True, dpi=1000)

december_data.plot(x='date', y=' Production(Wh)', ax=axes[0], kind='area', color='mediumseagreen')
december_data.plot(x='date', y=' Consumption(Wh)', ax=axes[1], kind='area', color='purple')
december_data.plot(x='date', y=' From grid(Wh)', ax=axes[2], kind='area', color='gray')
december_data.plot(x='date', y=' Feed-in(Wh)', ax=axes[3], kind='area', color='plum')
december_data.plot(x='date', y=' Charge(Wh)', ax=axes[4], kind='area', color='green')
december_data.plot(x='date', y=' Discharge(Wh)', ax=axes[5], kind='area',  color='orange')
december_data.plot(x='date', y=' State of Charge(%)', ax=axes[6], kind='area', color='magenta')

# Set legend labels
legend_labels = ['Production (W)', 'Consumption (W)', 'From grid (W)', 
                 'Feed-in (W)', 'Charge (W)', 'Discharge (W)',
                 'State of Charge (%)']
for i, ax in enumerate(axes):
    ax.legend([legend_labels[i]], loc="upper left", prop={'size': 16}, frameon=False)


# Set tick label font size for both axes
for ax in axes:
    ax.tick_params(axis='both', which='major', labelsize=16)

# Remove x-axis label
plt.xlabel('Date (07/12/2020 to 13/12/2020)', fontsize=18)
    
plt.ylabel('Power Profiles for house ID "H4"', horizontalalignment='center',
           y=4.5, fontsize=18, labelpad=30)

# Set legend font size
for ax in axes:
    plt.setp(ax.get_legend().get_texts(), fontsize='16')

plt.show()

fig.savefig('D:/Nature sample/Nature/figures/Power profiles per day for house H4.png')


# =============================================================================
## STEP-4: Power Vs Energy (Production and consumption) validation 
# =============================================================================
import os
import pandas as pd 
# Set the directory where the CSV files are located
directory_energy = 'C:/Users/rohit.trivedi/natdata/nat-data/original data/energy/'
# Set the name of the CSV file you want to load
filename_energy = '90962_2020_Wh.csv'
# Construct the full path to the CSV file
filepath = os.path.join(directory_energy, filename_energy)
# Load the CSV file into a Pandas DataFrame
df_H4_Wh = pd.read_csv(filepath)
# Print the first five rows of the DataFrame to confirm that it loaded correctly
print(df_H4_Wh)

directory_power = 'C:/Users/rohit.trivedi/natdata/nat-data/original data/power/'
filename_power= '90962_2020_W.csv'
# Construct the full path to the CSV file
filepath = os.path.join(directory_power, filename_power)
# Load the CSV file into a Pandas DataFrame
df_H4_W = pd.read_csv(filepath)
# Print the first five rows of the DataFrame to confirm that it loaded correctly
print(df_H4_W.head())

# Use DataFrame.tail() method to drop first row
# df_H4_W = df_H4_W.tail(-1)
# print(df_H4_W)

df_H4_Wh['date'] = pd.to_datetime(df_H4_Wh['date'])
df_H4_Wh_resampled = df_H4_Wh.resample('min', on='date').min()
df_H4_Wh_interpolate = df_H4_Wh_resampled.interpolate('linear')

df_H4_W['date'] = pd.to_datetime(df_H4_W['date'])
df_H4_W_resampled = df_H4_W.resample('min', on='date').min()
df_H4_W_interpolate = df_H4_W_resampled.interpolate('linear')

dfWh_resampled2=df_H4_Wh_resampled
# find NaN values
nan_mask = dfWh_resampled2.isna()
# identify values immediately after NaN values
next_values_mask = nan_mask.shift(1, fill_value=False)
# exclude the next values of NaNs
dfWh_resampled3 = dfWh_resampled2[~next_values_mask]
print(dfWh_resampled3)
# # checking the added timestapms with NaN values 
# dfW_resampled4=dfW_resampled3[(dfW_resampled3.index >= '2020-01-01 02:27') & (dfW_resampled3.index <= '2020-01-01 02:30')]
# print(dfW_resampled4)
# fill missing values with previous value
dfWh_resampled5 = dfWh_resampled3.fillna(method='ffill')
# # checking the added timestapms with NaN values 
# dfW_resampled6=dfW_resampled5[(dfW_resampled5.index >= '2020-01-01 02:27') & (dfW_resampled5.index <= '2020-01-01 02:30')]
# print(dfW_resampled6)

dfW_resampled2=df_H4_W_resampled
# find NaN values
nan_mask = dfW_resampled2.isna()
# identify values immediately after NaN values
next_values_mask = nan_mask.shift(1, fill_value=False)
# exclude the next values of NaNs
dfW_resampled3 = dfW_resampled2[~next_values_mask]
print(dfW_resampled3)
# # checking the added timestapms with NaN values 
# dfW_resampled4=dfW_resampled3[(dfW_resampled3.index >= '2020-01-01 02:27') & (dfW_resampled3.index <= '2020-01-01 02:30')]
# print(dfW_resampled4)
# fill missing values with previous value
dfW_resampled5 = dfW_resampled3.fillna(method='ffill')
# # checking the added timestapms with NaN values 
# dfW_resampled6=dfW_resampled5[(dfW_resampled5.index >= '2020-01-01 02:27') & (dfW_resampled5.index <= '2020-01-01 02:30')]
# print(dfW_resampled6)

# create an Empty DataFrame object for resampled data NaN values
df_WhW_interpolate = pd.DataFrame()
#  Concate all columns in one new dataframe
df_WhW_interpolate = pd.concat([dfW_resampled5, dfWh_resampled5], axis=1)
df_WhW_interpolate

df_WhW_interpolate_new = df_WhW_interpolate.tail(-1)
print(df_WhW_interpolate_new)

df_WhW_new=df_WhW_interpolate_new
# multiply columns 3 and 4 by 60 and round off to 1 decimal place
df_WhW_new[[' Consumption(Wh)', ' Production(Wh)']] = df_WhW_new[[' Consumption(Wh)', ' Production(Wh)']].apply(lambda x: x * 60).round(1)
df_WhW_new

# NEW ONE
x1=df_WhW_new[' Production(W)']
y1=df_WhW_new[' Production(Wh)']
xlim1 = x1.min(), x1.max()
ylim1 = y1.min(), y1.max()

fig, (ax0, ax1) = plt.subplots(ncols=2, sharey=False, figsize=(16, 8), dpi=300) # Use dpi=2000 for high resolution plot

hb=ax0.hexbin(x1, y1, gridsize=50, bins='log', cmap='inferno')
ax0.set(xlim=xlim1, ylim=ylim1)
# ax0.set_title("Hexagon binning", fontweight="bold", size=18)
cb = fig.colorbar(hb, ax=ax0)
ax0.tick_params(axis='both', which='major', labelsize=14)
ax0.tick_params(axis='both', which='minor', labelsize=14)
ax0.set_ylabel('Measured Energy (Production (Wh)/h in W)', fontsize = 16.0) # Y label
ax0.set_xlabel('Measured Power (Production (W) in W)', fontsize = 16) # X label

x2=df_WhW_new[' Consumption(W)']
y2=df_WhW_new[' Consumption(Wh)']
xlim2 = x2.min(), x2.max()
ylim2 = y2.min(), y2.max()

hb=ax1.hexbin(x2, y2, gridsize=50, bins='log', cmap='inferno')
ax1.set(xlim=xlim2, ylim=ylim2)
# ax1.set_title("With a log color scale", fontweight="bold", size=18)
cb = fig.colorbar(hb, ax=ax1, label='Counts at log10(N)')

ax1.tick_params(axis='both', which='major', labelsize=14)
ax1.tick_params(axis='both', which='minor', labelsize=14)
ax1.set_ylabel('Measured Energy (Consumption (Wh)/h in W)', fontsize = 16.0) # Y label
ax1.set_xlabel('Measured Power (Consumption (W) in W)', fontsize = 16) # X label
fig.savefig('C:/Users/rohit.trivedi/natdata/nat-data/figures/power energy validation for house H4.png')
plt.show()
#%% Section-2: Plotting the figures from weather and energy consumption data.
# =============================================================================
# STEP-1: extract the temperature (dry bulb) from weather data.
# Then, Plot aggregated annual energy consumption profiles
# =============================================================================

import pandas as pd
# Specify the folder path where the weather.csv file is located
# It is located in both the folders (original data and processed data)
folder_path = "D:/Nature sample/Nature/processed_data"  # Replace with the actual folder path
# Read the CSV file
combined_df = pd.read_csv(f"{folder_path}/weather.csv")
# Calculate daily average of 'drybulb' column
daily_average_drybulb = combined_df.groupby(combined_df['date'].dt.date)['drybulb'].mean()
# Create a new DataFrame with the daily average of 'drybulb'
daily_average_df = pd.DataFrame({'Date': daily_average_drybulb.index, 'Drybulb': daily_average_drybulb.values})
print(daily_average_df)

# Make a new dataframes with temperature and consumption profiles of all houses
# Create an empty dataframe to store the extracted columns
new_df = pd.DataFrame()

# Loop through all the csv files in the directory
for file_name in os.listdir('D:/Nature sample/Nature/copy_resample_experiment/energy/'):
    if file_name.endswith('.csv'):
        # Load the csv file into a dataframe
        df = pd.read_csv('D:/Nature sample/Nature/copy_resample_experiment/energy/' + file_name)
        
        # Rename the columns using the file name
        new_column_names = {}
        for column_name in df.columns:
            new_column_names[column_name] = f"{file_name[:-4]}_{column_name}"
        df = df.rename(columns=new_column_names)
        
        # Extract the desired column and add it to the new dataframe
        column_name_to_extract = f"{file_name[:-4]}_ Consumption(Wh)"
        new_df[column_name_to_extract] = df[column_name_to_extract]

# Print the new dataframe
print(new_df)

new_df.set_axis(['H10', 'H11', 'H12', 'H13', 'H14', 'H15',
                  'H16', 'H17', 'H18', 'H19', 'H1', 'H20',
                  'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
                  'H8', 'H9'], axis=1, 
                        inplace=True)


# Reorder the columns from 'H1' to 'H20'
column_order = ['H{}'.format(i) for i in range(1, 21)]
new_df = new_df.reindex(columns=column_order)
# new_df=df
# Print the reordered dataframe
print(new_df)
df=new_df
import pandas as pd
import matplotlib.pyplot as plt
df

# Assuming you have a DataFrame named 'df' with 20 columns

# Create a new column containing the sum of each row
df['Sum'] = df.sum(axis=1)

# Display the updated DataFrame
print(df)

# Making a new dataframe with date column ranging from Jan to Dec with consumption 
# and temperature columns
# Create a date range from '2020-01-01 00:00:00' to '2020-12-31 23:59:00'
date_range = pd.date_range(start='2020-01-01 00:00:00', end='2020-12-31 23:59:00', freq='1min')
# Create a DataFrame with the date range
date_df = pd.DataFrame({'Date': date_range})
date_df

# Merge 'Date' column from 'date_df' to 'df'
df1 = pd.merge(df['Sum'], date_df[['Date']], left_index=True, right_index=True)
# Display the updated DataFrame
print(df1)
# Convert 'Date' column to datetime format
df1['Date'] = pd.to_datetime(df1['Date'])
# Calculate daily average of 'H1' column
daily_average_h1 = df1['Sum'].groupby(df1['Date'].dt.date).mean()
print(daily_average_h1)
# Calculate daily average of 'drybulb' column
daily_average_drybulb = combined_df['drybulb'].groupby(combined_df['date'].dt.date).mean()
# Create DataFrame with daily averages of 'H1' and 'drybulb'
daily_average_df = pd.DataFrame({'Date': daily_average_h1.index, 'Consumption': daily_average_h1.values, 'Drybulb': daily_average_drybulb.values})

# Final plotting of consumption and temperature values with dates on x-axis
import matplotlib.pyplot as plt
# Create a figure and axis object
fig, ax1 = plt.subplots(figsize=(12, 8),dpi=600)
# Plot 'H1' as an area curve
ax1.fill_between(daily_average_df['Date'], daily_average_df['Consumption'], color='blue', alpha=0.4, label='Consumption')
ax1.set_xlabel('Date', fontsize=18)  # Increase font size
ax1.tick_params(axis='x', labelsize=18)  # Increase x-axis tick label size
ax1.set_ylabel('Consumption (kWh/day)', fontsize=18)  # Increase font size
ax1.tick_params(axis='y', labelsize=16)  # Increase tick label size
# Create a secondary y-axis for 'drybulb'
ax2 = ax1.twinx()
# Plot 'drybulb' on the secondary y-axis as a line curve
ax2.plot(daily_average_df['Date'], daily_average_df['Drybulb'], color='tab:red', label='Ambient Temperature')
ax2.set_ylabel('Temperature in °C', fontsize=18)  # Increase font size
ax2.tick_params(axis='y', labelsize=16)  # Increase tick label size
# Set y-axis limit for 'drybulb' starting from zero
ax2.set_ylim(bottom=0)
# Add legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=16)  # Increase legend font size
# Title
plt.title('Daily Energy Consumption and Ambient temperature', fontsize=20)  # Increase title font size
# Grid
plt.grid(True)
plt.savefig('D:/Nature sample/Nature/figures/Consumption vs Temperature.png')
# Show plot
plt.show()