# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 09:21:07 2018

@author: glazaoska1
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pycountry as pyc
import matplotlib
from matplotlib import cm
import plotly.plotly as py
import plotly.offline as offline
import plotly.graph_objs as go

#Initiate offline notebook for plotly
offline.init_notebook_mode(connected=True)

#Open data files
reviews1 = ".\data\winemag-data_first150k.csv"

#Read data into the DataFrame
df = pd.read_csv(reviews1, index_col=0)

#Create a scatter graph from the DataFrama
def scatter(df):
    
    fig = plt.figure()
    #Scatter the score against price. Low alpha for visualising points density
    plt.scatter(df['price'], df['points'], s=25, alpha=0.008, c='purple', marker='h')
    
    ax = plt.gca()
    
    #Log scale for price
    ax.set_xscale('log')
    
    #Styling
    fig.suptitle('Wine rating vs price', fontsize=12)
    ax.set_xlabel('Price [$]')
    ax.set_ylabel('Rating [out of 100]')
    
    #Save to PNG
    plt.savefig('.\charts\scatter.png', format='png', dpi=200)

#Get country ISO-3 code from a name
def ccode(cname):
    
    #Check if the name exists in the pycountry list
    try:
        return pyc.countries.get(name=cname).alpha_3
    
    except KeyError:
        
        #Check if the short name works (e.g. US)
        try:    
            return pyc.countries.get(alpha_2=cname).alpha_3
        
        except KeyError:
            return None
    
    #Special case for UK 
    if(cname=='UK'):
        return 'GBR'

#Formats a cmap into an RGB map ---(source: plotly API)---
def cmap_RGB(col_map, inverse):
    
    cmap = matplotlib.cm.get_cmap(col_map)
    col_map_rgb = []
    norm = matplotlib.colors.Normalize(vmin=0, vmax=255)
    
    for i in range(0, 255):
        k = matplotlib.colors.colorConverter.to_rgb(cmap(norm(i)))
        col_map_rgb.append(k)
    
    def matplotlib_plotly(c_map, pl_entries):
        h = 1.0/(pl_entries-1)
        pl_colorscale = []
        
        for k in range(pl_entries):
            
            if(inverse):
                idx = ((pl_entries-1)-k)*h #inverse the colour order
            else:
                idx = k*h #regular order
            
            
            c = list(map(np.uint8, np.array(c_map(idx)[:3])*255))
            pl_colorscale.append([k*h, 'rgb'+str((c[0], c[1], c[2]))])
            
        return pl_colorscale
    
    return matplotlib_plotly(cmap, 255)

#Create a choropleth chart ---(source: plotly API)---
def choropleth(df):
    
    #Count the number of reviews for each country
    world_occurences = df['country_code'].value_counts()
    world_occurences = world_occurences.dropna()
    #Add to a new DataFrame
    df_world = pd.DataFrame({'occurences': world_occurences})
    
    #Average score for each country
    df_world['avg_points'] = df.groupby('country_code')['points'].mean()
    #Average price for each country ($ ?)
    df_world['avg_price'] = df.groupby('country_code')['price'].mean()
    
    #Create dictionary for mapping country names to country codes from the initial DataFrame
    cmap = df[['country_code', 'country']].copy().dropna().drop_duplicates().set_index('country_code').to_dict()['country']
    df_world['country_code'] = df_world.index
    #Map country names to codes
    df_world['country'] = df_world['country_code'].map(cmap)
    
    #Data and styling for plotting
    data = [dict(
            type = 'choropleth',
            locations =  df_world['country_code'], #dimension, displayed
            z = df_world['avg_points'], #measure, displayed
            text = df_world['country'], #displayed country names
            #colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],[0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
            colorscale = cmap_RGB('BuPu', True),
            autocolorscale = False,
            reversescale = True, #legend goes from high to low
            marker = dict(
                    line = dict(
                            color = 'rgb(180,180,180)',
                            width = 0.5
                            )),
            colorbar = dict(
                    title = 'Average rating'),)]
            
    #Chart layout properties
    layout = dict(
            title = 'Average wine rating per country',
            geo = dict(
                    showframe = False,
                    showcoastlines = False, #country coastlines
                    showcountries = True, #country borders
                    projection = dict(
                            type = 'Mercator')))
    
    #Combine chart properties
    fig = dict(
            data = data,
            layout = layout)
    
    #Save an offline copy of the chart
    offline.plot(fig, filename='wine-scores-map.html')
    
#Apply the country coding function
df['country_code'] = df['country'].apply(ccode)