from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
from pmdarima.arima import auto_arima
import matplotlib.pyplot as plt

def model_arima(df: pd.DataFrame, period: int):
    train = df.resample('M').mean()[:int(0.85*(len(df.resample('M').mean())))]
    test = df.resample('M').mean()[int(0.85*(len(df.resample('M').mean()))):]
    
    # автоматическая arima (сама выбирает параметры)
    model = auto_arima(train,  trace=True, error_action='ignore', suppress_warnings=True,seasonal=True,m=12)
    result = model.fit(train)
    predictions = model.predict(n_periods=(10+period))


    # обычная модель arima
    #start = len(train)
    #end = len(train)+ len(test) + period - 1
    #model = ARIMA(train, order = (1,1,0), seasonal_order = (2, 0, 0, 12))
    #result = model.fit()
    #predictions = result.predict(start, end)
    

    # метрики
    mse = mean_squared_error(test, predictions[:int(len(test))])
    mae = mean_absolute_error(test, predictions[:int(len(test))])
    mape = mean_absolute_percentage_error(test, predictions[:int(len(test))])
    # visualization
    plt.figure(figsize=(15, 8))
    plt.plot(train, color="black", label="Train data")
    plt.plot(test, color="red", label="Test data")
    plt.plot(predictions, color="purple", label="Forecast")
    # заголовок и подписи к осям
    plt.title(f"ARIMA forecast for {period} months")
    plt.ylabel('Reviews (mean)')
    plt.xlabel('Date')
    plt.legend()
    # добавим сетку
    plt.grid()
    xticks = pd.date_range(start=train.index[0], end=predictions.index[-1], freq='2M')
    plt.xticks(xticks, rotation=45, ha='right')
    # Добавление текста c метриками
    arima_order = model.get_params()['order']
    arima_s_order = model.get_params()['seasonal_order']
    metric_text=f"MSE: {mse}\nMAE: {mae}\nMAPE: {mape}\np,d,q: {arima_order}\nP,D,Q,s: {arima_s_order}"
    text_x = train.index[0]  
    text_y = train.mean()  
    plt.annotate(metric_text, (text_x, text_y*1.3), xytext=(5, -10), textcoords='offset points', fontsize=11, color='blue')
    return plt.gcf()


