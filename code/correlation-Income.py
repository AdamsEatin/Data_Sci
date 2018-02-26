# -*- coding: utf-8 -*-
"""
Author: Adam Eaton - C00179859

This file generates a graph showing the correlation between the chosen countries usage of renewable energies and the 
mean income in the country
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



def data_prep(country, df, div):
    df_vals = pd.DataFrame(data=df.loc[country])
    df_vals = df_vals.transpose()

    vals = []
    
    if(div == True):
        for index, row in df_vals.iterrows():
            for item in row:
                vals.append(float(item)/1000)
        return vals
    
    else:
        for index, row in df_vals.iterrows():
           for item in row:
               vals.append(float(item)/1000)
        return vals

def correlation_income(country):
    renewable_data = pd.read_csv('Datasets/Renewable_Consumption-By_Country.csv')
    income_data = pd.read_csv('Datasets/Mean_Income-By_Country.csv')
    renewable_data = clean_data(renewable_data)
    income_data = clean_data(income_data)

    cols = list(income_data.columns)[:-1]
    renewable_data = renewable_data[cols]
    income_data = income_data[cols]
    
    for item in cols:
        income_data[item] = income_data[item].str.replace(",","").astype(float)

    x_vals = []
    for item in cols:
        x_vals.append(int(item))

    ren_vals = data_prep(country, renewable_data, True)
    income_data = data_prep(country , income_data, False)
    

    trace1 = go.Scatter(
            x = x_vals,
            y = income_data,
            mode='lines+markers',
            name = '{} - Mean Income in Thousand Euros'.format(country))
    
    trace2 = go.Scatter(
            x = x_vals,
            y = ren_vals,
            mode='lines+markers',
            name = '{} - TOE'.format(country))

    
    data = [trace1, trace2]
    layout = go.Layout(title = 'Renewable Energy usage vs Mean Income')
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='Renewable vs Income')
    
    ren_list = list(ren_vals)
    income_list = list(income_data)
    print(pearsonr(ren_list, income_list))