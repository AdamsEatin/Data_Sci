# -*- coding: utf-8 -*-
"""
Author: Adam Eaton - C00179859

This file generates a graph showing a breakdown of the different types of renewable energies used by each member
of the EU.
"""

import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='VMunt', api_key='w2tEETwgAuCdgRwVDqiK')


def split_vals(data, opt):
    if(opt == 1):
        y_vals = []
        for k, v in data.items():
            y_vals.append(v)
        return y_vals
    else:
        x_vals = []
        y_vals = []
        for k, v in data.items():
            x_vals.append(k)
            y_vals.append(v)
        return x_vals, y_vals
   

# Function to clean up a given dataset, it does this by;
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

def each_type(data):
    val_dict = {}
    col_len = len(list(data.columns))
    for index, row in data.iterrows():
        val_dict[index] = float(row[col_len-1])
    return val_dict

def sources_per_country():
    hydro_data = pd.read_csv('Datasets/Hydro_Consumption-By_Country.csv')
    solar_data = pd.read_csv('Datasets/Solar_Consumption-By_Country.csv')
    thermal_data = pd.read_csv('Datasets/Thermal_Consumption-By_Country.csv')
    wind_data = pd.read_csv('Datasets/Wind_Consumption-By_Country.csv')

    # Selecting the data we want to use from the datasets
    hydro_data = clean_data(hydro_data)
    solar_data = clean_data(solar_data)
    thermal_data = clean_data(thermal_data)
    wind_data = clean_data(wind_data)

    hydro_dict = each_type(hydro_data)
    solar_dict = each_type(solar_data)
    thermal_dict = each_type(thermal_data)
    wind_dict = each_type(wind_data)

    x_vals, hy_y_vals = split_vals(hydro_dict, 0)
    so_y_vals = split_vals(solar_dict, 1)
    th_y_vals = split_vals(thermal_dict, 1)
    wi_y_vals = split_vals(wind_dict, 1)

    
    trace1 = go.Bar(x = x_vals,
                    y = hy_y_vals,
                    name = 'Hydro')

    trace2 = go.Bar(x = x_vals,
                    y = so_y_vals,
                    name = 'Solar')

    trace3 = go.Bar(x = x_vals,
                    y = th_y_vals,
                    name = 'Thermal')

    trace4 = go.Bar(x = x_vals,
                    y = wi_y_vals,
                    name = 'Wind')

    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(title = 'Renewable Energy Breakdown per Country in 2016',
                       yaxis=dict(title="Thousand' Tonnes of Oil Equivelent"),
                       barmode='stack')
    
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='Renewable Energy Breakdown per Country')