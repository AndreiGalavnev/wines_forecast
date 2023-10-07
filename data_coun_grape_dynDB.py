import boto3
import os
from boto3.dynamodb.conditions import Key
import pandas as pd


def country_variety_DB(coun_name: str, grape_name: str, access_key, secret_key):

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    table = dynamodb.Table('wine_dates_reviews1')
    # запрос с вторичным индексом
    # в country указываешь страну, а в grape_variety - сорт винограда
    resp = table.query(
        IndexName="country-grape_variety-index",
        KeyConditionExpression=Key('country').eq(f"{coun_name}") & Key('grape_variety').eq(f"{grape_name}"))

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