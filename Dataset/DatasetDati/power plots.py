# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:08:49 2023

@author: rohit.trivedi
"""

# %% Section-1: Plotting the figures from power data.

# =============================================================================
# Start running the code from this section
# Step-1: Extracting date and status columns from processed csv files
# =============================================================================
import os
import pandas as pd

# Specify the directory containing the CSV files
directory = 'D:/Nature sample/Nature/processed_data/power/'

# Create an empty list to hold the extracted DataFrames
dfs = []

# Loop through all CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Read in the CSV file
        df = pd.read_csv(os.path.join(directory, filename))
        
        # Extract the column with the same name as the filename
        column_name = filename[:-4]  # Remove the '.csv' extension
        extracted_column = df[column_name]
        
        # Extract the date column
        date_column = df['date']
        
        # Create a new DataFrame with the extracted columns
        new_df = pd.DataFrame({'date': date_column, column_name: extracted_column})
        
        # Add the new DataFrame to the list
        dfs.append(new_df)
        
# Concatenate all DataFrames in the list into a single DataFrame
result = pd.concat(dfs, axis=1)
print(result)

# =============================================================================
# # Step-2: Drop duplicates in new dataframe (result) and plot the missing data plot
# =============================================================================
#Drop the duplicate columns
new = result.loc[:, ~result.columns.duplicated()]
# Display the resulting DataFrame
print(new)
# Define a new list of column names
new_columns = ['date', 'H10', 'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18',
                'H19', 'H1', 'H20', 'H2', 'H3', 'H4','H5', 'H6', 'H7', 'H8', 'H9'               
                ]

# Rename the columns
new.columns = new_columns
# Display the resulting DataFrame
print(new)
# Extract the numeric part of the column names and convert to integers
numeric_cols = [int(col[1:]) for col in new.columns if col.startswith('H')]
# Sort the numeric column names
sorted_cols = sorted(numeric_cols)
# Create a list of sorted column names with the 'H' prefix
new_columns = [f'H{col}' for col in sorted_cols]
# Reorder the DataFrame columns
df_new = new[new_columns]
# Display the resulting DataFrame
print(df_new)
# Extract the column you want to add from df1
new_column = new['date']
# Concatenate the new column to the left of df2 using 'concat' function
df_new_date = pd.concat([new_column, df_new], axis=1)
df_new_date


import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns
import pandas as pd

# dfd_all=df_new.reset_index()
dfd_all=df_new_date
dfd_all
dfd_all_try=dfd_all
# convert the date column to datetime format
dfd_all_try['date'] = pd.to_datetime(dfd_all_try['date'], format='%Y-%m-%d %H:%M:%S')
# create a new column with the desired format
dfd_all_try['month_year'] = dfd_all_try['date'].dt.strftime('%b-%Y')
# dfd_all_try.reset_index()
dfd_all_try=dfd_all_try.drop(['date'], axis=1)
dfd_all_try
dfd_all_try.set_index('month_year', inplace=True)
plt.figure(figsize=(18,10), dpi=600) #set dpi=2000 for better resolution
ax=sns.heatmap(dfd_all_try.fillna(0).transpose(),
            cmap="YlGnBu",
            cbar_kws={'label': 'Available Data'})
xticks = dfd_all.index[0::100000]
ax.xaxis.tick_top()
ax.tick_params(axis='x', rotation=90)
# ax.set(yticklabels=[])
ax.set(xlabel=None)
ax.patch.set_edgecolor('0.15')
ax.patch.set_linewidth(2)
plt.yticks(fontsize=12, rotation=0)
plt.savefig('D:/Nature sample/Nature/figures/missing data.png')
plt.savefig("missing data.png", dpi=300, bbox_inches='tight')

#=============================================================================
# Step-3: Percentage available data subplots 
#=============================================================================
dfd_all=df_new_date
dfd_all
# dfd_all=dfd_all.reset_index()
dfd_all=dfd_all.drop(['month_year'], axis=1)
dft=dfd_all
print(dft)
dft=dft.drop(['date'], axis=1)
prcnt_avail=dft.apply(pd.value_counts).fillna(0)*100 / len(dfd_all)
prcnt_avail

prcnt_availT=prcnt_avail.transpose()
prcnt_availT
prcnt_availT=prcnt_availT.reset_index()
prcnt_availT=prcnt_availT.set_axis(['ID', 'available'], axis=1)
prcnt_availT['available']=prcnt_availT['available'].round(decimals = 2)
 
x=prcnt_availT['available']
y=prcnt_availT['ID']

def show_values(axs, orient="v", space=.01):
    def _single(ax):
        if orient == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height() + (p.get_height()*0.01)
                value = '{:.2f}%'.format(p.get_height())
                ax.text(_x, _y, value, ha="center") 
        elif orient == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width()/2 + float(space)
                _y = p.get_y() + p.get_height() - (p.get_height()*0.5)
                value = '{:.2f}%'.format(p.get_width())
                ax.text(_x, _y, value, ha="center")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _single(ax)
    else:
        _single(axs)

plt.figure(figsize=(2,10), dpi = 1000)
# p=sns.barplot(x=prcnt_availT['available'], y=prcnt_availT['ID'],
#                orient='h', palette="GnBu_d")
p=sns.barplot(x=prcnt_availT['available'], y=prcnt_availT['ID'],
                orient='h')
show_values(p, "h", space=0)
p.set(xticklabels=[])
p.set(xlabel=None)
p.set(yticklabels=[])
p.set(ylabel=None)
p.tick_params(right = True)
p.tick_params(left = False)
p.tick_params(bottom = False)
p.axes.set(title='Available data')
plt.savefig('D:/Nature sample/Nature/figures/available data.png')
plt.savefig("available data.png", dpi=600, bbox_inches='tight')
# %%

