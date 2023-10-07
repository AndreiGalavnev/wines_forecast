import boto3
import os
from boto3.dynamodb.conditions import Key
import pandas as pd

# для игристых, крепленых и десертных
def region_type_DB(reg_name: str, type_name: str, access_key, secret_key):

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    table = dynamodb.Table('wine_dates_reviews1')
    # запрос с вторичным индексоm
    resp = table.query(
        IndexName="region-wine_type-index",
        KeyConditionExpression=Key('region').eq(f"{reg_name}") & Key('wine_type').eq(f"{type_name}"))

    # Обработка результатов запроса и перевод данных в список
    items = resp['Items']
    if len(items) == 0:
        return None
    review_dates_list = []
    for item in items:
        review_dates = item.get('review_dates', [])
        for date in review_dates:
            review_dates_list.append(date)
    len_revs = str(len(review_dates_list))
    # обработка (в timestamp ->  в датафрейм для timeseries) 
    timestamps = pd.to_datetime(review_dates_list, format='%b %d, %Y')
    df = pd.DataFrame({'Дата': timestamps})
    df.set_index('Дата', inplace=True)
    # Создание DataFrame с помощью resample для получения количества появлений даты
    df_resampled = df.resample('D').size().reset_index(name='Количество')
    # Заполнение пропущенных дат нулями
    df_resampled = df_resampled.fillna(0)
    df_resampled = df_resampled.set_index('Дата') 
    return df_resampled, len_revs