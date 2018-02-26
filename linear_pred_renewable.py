# -*- coding: utf-8 -*-
"""
Author: Adam Eaton - C00179859

This file generates a prediction for future Renewable Energy Usage using Linear Regression 
"""

import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from sklearn import linear_model
from sklearn.model_selection import train_test_split

plotly.tools.set_credentials_file(username='VMunt', api_key='w2tEETwgAuCdgRwVDqiK')

def clean_data(dataset):
    dataset = dataset[1:29]
    dataset = dataset.set_index(["Unnamed: 0"])
    dataset = dataset.replace(':', np.nan)
    dataset = dataset.fillna(method='backfill')
    return dataset

 
def generate_prediction(country):
    rnd_data = pd.read_csv('Datasets/R&D-By_Country.csv')
    rnd_data = clean_data(rnd_data)
    renewable_data = pd.read_csv('Datasets/Renewable_Consumption-By_Country.csv')
    renewable_data = clean_data(renewable_data)

    rnd_cols = list(rnd_data.columns)[2:]
    renewable_cols = list(renewable_data.columns)
    rnd_data = rnd_data[rnd_cols]
    renewable_data = renewable_data[renewable_cols]

    rnd_list = rnd_data.loc[country].values
    rnd_list = rnd_list.reshape(-1, 1)
    rene_list = renewable_data.loc[country].values
    rene_list = rene_list.astype(np.float)
    rene_list = rene_list.reshape(-1, 1)


    X_train, X_test, y_train, y_test = train_test_split(rnd_list, rene_list, test_size=0.40)

    model = linear_model.LinearRegression()
    model.fit(X_train, y_train)
    
    prediction = model.predict(X_test)


    trace1 = go.Scatter(
                x = X_test,
                y = y_test,
                mode='markers',
                name = '{} - Test Values'.format(country))
        
    trace2 = go.Scatter(
                x = X_test,
                y = prediction,
                mode='lines',
                name = '{} - Predictions'.format(country))

    
    data = [trace1, trace2]
    layout = go.Layout(title = 'Predicted future Renewable Energy Usage',
                       xaxis=dict(title="Renewable Energy Consumption"), 
                       yaxis=dict(title="Research & Development share of GDP"))
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='Predicted future Renewable Energy Usage')


generate_prediction("Germany")