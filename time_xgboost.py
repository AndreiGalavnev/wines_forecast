# XGBOOST
import pandas as pd
from xgboost import XGBRegressor
import lightgbm as lgb
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error,mean_squared_error
import matplotlib.pyplot as plt



def xgb(df, period):
    # resample
    df = df.resample('2W').mean().reset_index()
    
    # Создаю диапазон дат для прогноза
    start_date = pd.to_datetime('2023-07-01')
    end_date = start_date + pd.DateOffset(months=period)
    forecast_range = pd.date_range(start=start_date, end=end_date, freq='2W')

    #  пустой датафрейм с прогнозируемыми датами
    forecast_df = pd.DataFrame(index=forecast_range)
    forecast_df.index.name = 'Дата'
    forecast_df = forecast_df.reset_index()
    df = pd.concat([df, forecast_df], axis=0)
    df = df.reset_index(drop=True)
    # добавим признаков
    df["day_of_year"] = df["Дата"].dt.dayofyear
    df["month"] = df["Дата"].dt.month
    df["quarter"] = df["Дата"].dt.quarter
    df["year"] = df["Дата"].dt.year
    # train-test
    train = df[:int(0.7*(len(df)))]
    test = df[int(0.7*(len(df))):]
    # дропаем Дата столбец
    train_dates = train["Дата"]
    train = train.drop(columns=["Дата"])
    test_dates = test["Дата"]
    test = test.drop(columns=["Дата"])
    X_train = train[["day_of_year", "month", "quarter", "year"]]
    y_train = train["Количество"]
    X_test = test[["day_of_year", "month", "quarter", "year"]]
    y_test = test["Количество"]

    # MODEL
    params ={'colsample_bytree': 0.8, 'learning_rate': 0.15, 'max_depth': 12, 'n_estimators': 1000} 
    model = XGBRegressor(**params)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    ser_predict = pd.Series(prediction)
    df__train = pd.DataFrame({"date": train_dates, "actual": y_train})
    df__test = pd.DataFrame({"date": test_dates, "actual": y_test})
    df__pred = pd.DataFrame({"date": test_dates, "prediction": prediction})
    
    # Добавление текста c метриками
    mse = mean_squared_error(y_test[:-(int(len(forecast_range)))], prediction[:-(int(len(forecast_range)))])
    mae = mean_absolute_error(y_test[:-(int(len(forecast_range)))], prediction[:-(int(len(forecast_range)))])
    mape = mean_absolute_percentage_error(y_test[:-(int(len(forecast_range)))], prediction[:-(int(len(forecast_range)))])    
    metric_text=f"MSE: {mse}\nMAE: {mae}\nMAPE: {mape}"
    # visualization
    figure, ax = plt.subplots(figsize=(15, 8))
    plt.title(f"XGBOOST forecast for {period} months")
    df__train.plot(ax=ax, label="Train data", x="date", y="actual", color='black')
    df__test.plot(ax=ax, label="Test data", x="date", y="actual", color='red')
    df__pred.plot(ax=ax, label="Forecast", x="date", y="prediction", color="purple")
    plt.legend()
    # добавим сетку
    plt.grid()
    plt.ylabel('Reviews (mean)')
    plt.xlabel('Date')
    plt.text(0.2, 0.82, f"{metric_text}", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=12, color='blue')
    return plt.gcf()