# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 09:21:07 2018

@author: glazaoska1
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pycountry as pyc
import plotly.plotly as py

reviews1 = ".\data\winemag-data_first150k.csv"

df = pd.read_csv(reviews1, index_col=0)

def scatter(df):
    
    fig = plt.figure()
    plt.scatter(df['price'], df['points'], s=25, alpha=0.008, c='purple', marker='h')
    ax = plt.gca()
    ax.set_xscale('log')
    fig.suptitle('Wine rating vs price', fontsize=12)
    ax.set_xlabel('Price [$]')
    ax.set_ylabel('Rating [out of 100]')
    plt.savefig('.\charts\scatter.png', format='png', dpi=200)


def ccode(cname):
    
    try:
        return pyc.countries.get(name=cname).alpha_3
    
    except KeyError:
        
        try:    
            return pyc.countries.get(alpha_2=cname).alpha_3
        
        except KeyError:
            return None
    
    if(cname=='UK'):
        return 'GBR'


def choropleth(df):
    
    world_occurences = df['country_code'].value_counts()
    world_occurences = world_occurences.dropna()
    df_world = pd.DataFrame({'occurences': world_occurences})
    
    df_world['avg_points'] = df.groupby('country_code')['points'].mean()
    df_world['avg_price'] = df.groupby('country_code')['price'].mean()
    
    df_world['country'] = df['country'].unique()
    
    return df_world.head()
    
    
    data = [dict(
            type = 'choropleth',
            locations =  df_world['country_code'],
            z = df_world['avg_points'],
            text = df_world['country'],
            colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
            autocolorscale = False,
            reversescale = True,
            marker = dict(
                    line = dict(
                            color = 'rgb(180,180,180)',
                            width = 0.5
                            )),
            colorbar = dict(
                    autotick = False,
                    title = 'Average rating'),)]
            
    layout = dict(
            title = 'Average wine rating per country',
            geo = dict(
                    showframe = False,
                    showcoastlines = False,
                    projection = dict(
                            type = 'Mercator')))
    
    fig = dict(
            data = data,
            layout = layout)
    
    py.iplot(fig, validate = False, filename='wine_ratings')
    

df['country_code'] = df['country'].apply(ccode)