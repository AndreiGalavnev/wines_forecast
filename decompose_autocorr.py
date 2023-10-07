from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

def df_decompose(df):
    # Decompose plot
    plt.figure(figsize = (11,10))
    decompose = seasonal_decompose(df.resample('M').mean())
    decompose.plot()
    return plt.gcf()

def autocorr(df):
    # Autocorrelation and partial autocorrelation plot
    plt.figure(figsize=[15, 3])
    ax = plt.subplot(121)
    plot_acf(df.resample('M').mean(), lags=36, ax=ax)
    ax = plt.subplot(122)
    plot_pacf(df.resample('M').mean(), lags=36, ax=ax)
    plt.tight_layout()
    return plt.gcf()

def adf_test(df):
    # Dickey-Fuller test
    adf, pval, usedlag, nobs, crit_vals, icbest =  adfuller(df['Количество'])
    return adf, pval, usedlag, nobs, crit_vals, icbest