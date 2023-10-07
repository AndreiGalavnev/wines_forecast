import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


def preprocess(df): 
    # подрезаем данные слева и справа по датам
    mask = df.index >= pd.to_datetime('2023-06-01')
    df = df.loc[~mask]
    mask = df.index < pd.to_datetime('2016-12-01')
    df = df.loc[~mask]
    # проверка на стационарность
    adf_test = adfuller(df['Количество'])
    
    if adf_test[1] > 0.05:
        mask = df.index < pd.to_datetime('2017-05-01')
        df = df.loc[~mask]
    
    adf_test = adfuller(df['Количество'])
    if adf_test[1] > 0.05:
        mask = df.index < pd.to_datetime('2017-12-01')
        df = df.loc[~mask]
    return df