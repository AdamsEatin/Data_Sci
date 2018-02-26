# -*- coding: utf-8 -*-
"""
Author: Adam Eaton - C00179859

This file generates a graph showing which counties have had the largest decrease in emissions since 1990
"""

import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from scipy.stats.stats import pearsonr  
plotly.tools.set_credentials_file(username='VMunt', api_key='w2tEETwgAuCdgRwVDqiK')


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


def get_diff(data, pos):
    x_vals = []
    y_vals = []
    
    for index, row in data.iterrows():
        x_vals.append(index)
        diff = float(row[pos-1]) - float(row[0])
        y_vals.append(diff)
        
    return x_vals, y_vals
    

def find_emissions_decrease():
    emissions_data = pd.read_csv('Datasets/Emissions_By_Year.csv')
    emissions_data = clean_data(emissions_data)

    col_len = len(list(emissions_data.columns))

    x_vals, y_vals = get_diff(emissions_data, col_len)
    
    
    trace1 = go.Bar(x = x_vals,
                    y = y_vals)
    data = [trace1]
    layout = go.Layout(title = 'Change in Emissions since 1990',
                       yaxis=dict(title="Thousand' Tonnes of Oil Equivelent"))
    
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='Change_In_Emissions')
