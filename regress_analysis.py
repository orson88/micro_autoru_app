import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

def bhp_growth(bhp):
    df = pd.read_csv('auto_data.csv')
    df = df[
        (df['horsepower'] > bhp*0.8) & (df['horsepower'] < bhp*1.2)
    ]
    m = LinearRegression()
    m.fit(df['horsepower'].values.reshape(-1,1), df['price'].values)
    plt.figure(figsize=(8,15))
    plt.plot(df.sort_values(by = 'price')['horsepower'],
             df.sort_values(by='price')['price'])
    plt.show()
    return round(m.coef_[0]*10)



