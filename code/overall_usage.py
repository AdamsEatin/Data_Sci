# -*- coding: utf-8 -*-
"""
Author: Adam Eaton - C00179859

This file generates a graph showing the overall usage of different renewable energy sources throughout the EU.
"""

import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='VMunt', api_key='w2tEETwgAuCdgRwVDqiK')



# Method to clean up a given dataset, it does this by;
# -Pulling only data to do with individual EU member states 
# -Setting the index column to the country names as opposed to numbers
# -Filling any missing values with Nan values
# -Backfilling these values 
def clean_data(dataset):
    dataset = dataset[1:29]
    dataset = dataset.set_index(["Unnamed: 0"])
    dataset = dataset.replace(':', np.nan)
    dataset = dataset.fillna(method='backfill')
    return dataset

# Method to get the sum of all data within the given dataset
def get_sum(data):
    col_len = len(list(data.columns))
    data_sum = 0 
    for index, row in data.iterrows():
        data_sum += float(row[col_len-1])
            
    return data_sum

# Method used to seperate dictionary values into seperate lists
def split_vals(data):
    x_vals = []
    y_vals = []
    for k, v in data.items():
        x_vals.append(k)
        y_vals.append(v)
    return x_vals, y_vals


# main method
def find_overall_usage():
    hydro_data = pd.read_csv('Datasets/Hydro_Consumption-By_Country.csv')
    solar_data = pd.read_csv('Datasets/Solar_Consumption-By_Country.csv')
    thermal_data = pd.read_csv('Datasets/Thermal_Consumption-By_Country.csv')
    wind_data = pd.read_csv('Datasets/Wind_Consumption-By_Country.csv')

    # Selecting the data we want to use from the datasets
    hydro_data = clean_data(hydro_data)
    solar_data = clean_data(solar_data)
    thermal_data = clean_data(thermal_data)
    wind_data = clean_data(wind_data)

    # Dictionary to store the results 
    sum_dict = {}
    sum_dict["Hydro"] = get_sum(hydro_data) 
    sum_dict["Solar"] = get_sum(solar_data)
    sum_dict["Thermal"] = get_sum(thermal_data)
    sum_dict["Wind"] = get_sum(wind_data)


    x_vals, y_vals = split_vals(sum_dict)
    trace1 = go.Bar(x = x_vals,
                    y = y_vals)
    data = [trace1]
    layout = go.Layout(title = 'Overall Renewable Energy Usage in the EU in 2016',
                       yaxis=dict(title="Thousand' Tonnes of Oil Equivelent"))
    
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='Overall-Usage-EU')