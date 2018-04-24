# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 09:21:07 2018

@author: glazaoska1
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    
scatter(df)

