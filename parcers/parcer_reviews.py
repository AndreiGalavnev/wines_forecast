# парсит с одной страницы вина: страна производства, регион (важно для игристых), винодельня, тип вина, сорт винограда, даты отзывов, страны отзывов, средний рейтинг вина

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import boto3
import os
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.edge.service import Service
from datetime import datetime

k = 0
edgedriver_path = 'C:/Users/user/projects/wine/msedgedriver.exe'

with open('C:/Users/user/projects/wine/links/all_wines_links_auto.txt', 'r', encoding='utf-8') as f:
    urls = f.readlines() 
    for url in urls:
        # создаем объект webdriver
        try:
            edge_service = Service(edgedriver_path)
            driver = webdriver.Edge(service=edge_service)
        except:
            edge_service = Service(edgedriver_path)
            driver = webdriver.Edge(service=edge_service)
        # открываем страницу
        driver.get(url)
        # ждем, чтобы дать странице время на загрузку
        time.sleep(7)
        # извлекаем HTML-код страницы
        html = driver.page_source
        # создаем объект BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        # ставим время ожидания загрузки страницы на поменьше
        driver.set_page_load_timeout(60)




        grape = ''
        wines = []
        winery = ''
        region = ''
        country = ''
        wine_type = ''
        sum_reviews = 0
        av_rating = 0
        review_dates = []
        review_country = []
        rating_stars = 0
        # находим все элементы с описанием вина
        grape_elements = driver.find_elements(By.XPATH,'//a[@class="anchor_anchor__m8Qi- breadCrumbs__link--1TY6b"]')
        # выдаёт по очереди страну, регион, винодельню, тип вина, сорт винограда
        country = grape_elements[0].text
        region = grape_elements[1].text
        winery = grape_elements[2].text
        wine_type = grape_elements[3].text
        grape = grape_elements[4].text
        # иногда виноград не указан, поэтому пропускаем его
        if not grape:
            continue
        
        # выдаёт  средний рейтинг
        av_rating_elements = soup.find('div', class_='vivinoRating_averageValue__uDdPM')
        av_rating = str(av_rating_elements.text)
        # листаем страницу
        actions = ActionChains(driver)
        for i in range(22):
            actions.scroll_by_amount(delta_x=0, delta_y=400)
            actions.perform()
            time.sleep(1)

        # находим кнопку Show more reviews и жмем
        time.sleep(3)
        show_button = driver.find_element(By.XPATH,"//span[text()='Show more reviews']")
        show_button.click()
        time.sleep(5)

        # считаем количество отзывов (не на всех страницах есть общее кол-во отзывов, поэтому приходится брать по отдельности кол-во отзывов от 1 до 5)
        # а ещё иногда (рандомно) он находит кроме цифр пустые строки или вообще начинает по второму кругу забирать кол-ва, но это исправлено
        num_reviews_elements = driver.find_elements(By.CLASS_NAME,'RatingsFilter__counter--1wmJd') 
        for num_reviews_element in num_reviews_elements:
            if num_reviews_element.text != '' and rating_stars < 5:
                rating_stars += 1
                sum_reviews += int(num_reviews_element.text)
        
        # выбираем элемент с отзывами
        modal_body = driver.find_element(By.CLASS_NAME,'allReviews__reviews--EpUem')
        

        # прокручиваем всплывающее окно 
        if sum_reviews < 200:
            driver.quit()
            continue
        # на локальной машине не хватает мощности поэтому...
        if sum_reviews > 75000:
            driver.set_page_load_timeout(27)
        # помещаем курсор примерно на список отзывов и пролистываем примерно на 7% от всех отзывов (на локальной машине не хватает мощности)
        for i in range(0, int(sum_reviews/20/12-1)):      
            try:
                actions = ActionChains(driver)
                actions.scroll(x=500,y=500, delta_x=0,delta_y=100000) 
                i += 1
                actions.perform()
                time.sleep(1)
            except:
                pass


        # извлекаем HTML-код всплывающего окна
        modal_html = modal_body.get_attribute('innerHTML')
        # создаем объект BeautifulSoup для анализа HTML-кода всплывающего окна
        soup = BeautifulSoup(modal_html, 'html.parser')
        # находим все элементы (даты отзывов) 
        date_review_elements = soup.find_all('a', class_='anchor_anchor__m8Qi- reviewAnchor__anchor--2NKFw reviewДата__reviewДата--49vpM undefined')
        #  даты всех отзывов ->  список
        for date_review_element in date_review_elements:
            review_dates.append(date_review_element.text)

        #БЕЗ СТРАН ЮЗЕРОВ ДАЛЬШЕ МОЖНО КОД НЕ ВЫПОЛНЯТЬ
        # получаем ссылки всех людей из отзывов (для  дальнейшего получения из стран)
        # находим все элементы с классом "communityReview__textInfo--7SzS6"
        #review_links_elements = driver.find_elements(By.CSS_SELECTOR,'.communityReview__textInfo--7SzS6')
        #print(review_dates)
        # создаем пустой список для хранения ссылок
        #links = []


        # перебираем все найденные элементы
        #for review_links_element in review_links_elements:
            # находим первую ссылку в элементе
            #link_element = review_links_element.find_element(By.TAG_NAME,'a')
            
            # получаем значение атрибута "href" ссылки
            #link = link_element.get_attribute('href')
            
            # добавляем ссылку в список
            #links.append(link)

        driver.quit()
        #перебираем ссылки на страницы всех оставивших отзывы и достаём их страны 
        # (ВИДИМО НЕТ , ПОТОМУ ЧТО САЙТ БЛОЧИТ, ЕСЛИ ПРОИЗВОДИШЬ БОЛЬШЕ 300 ЗАПРОСОВ ЗА КОРОТКОЕ ВРЕМЯ)
        #for l in links[:-3]:   #последние три ссылки не берем, т.к. это первые три отзыва с основной страницы
            #он прогоняет по отзывам из всплывающего окна, а потом цепляет три отзыва за ним
        #    driver.get(l)
        #    time.sleep(1)
        #    try:
        #        country = driver.find_element(By.XPATH,'//div[@class="user-header__status text-mini text-muted"]')
        #        review_country.append(country.text)
        #    except:
        #        print('User is 404')
        
        
        
        
        # to the DynamoDB
        access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region = os.environ.get('AWS_REGION')
        dynamodb = boto3.resource('dynamodb', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=aws_region)
        # Получаем доступ к таблице 
        table = dynamodb.Table('wine_dates_reviews1')
        # Генерация уникального идентификатора вина
        wine_id = f"{country}_{region}_{winery}_{wine_type}_{grape}"

        # Сохранение данных в таблицу
        item = {
            'wine_id': wine_id,
            'country': country,
            'region': region,
            'winery': winery,
            'wine_type': wine_type,
            'grape_variety': grape,
            'review_dates': review_dates,
            'average_rating': av_rating
        }
        table.put_item(Item=item)

        k += 1
        # logging
        with open('all_wines_in_db_log.txt', 'a', encoding='utf-8') as file:
            file.write(f"Date&time of execution - {datetime.now()}\n")
            file.write(f"URL # {k}.\n")
            file.write(f"Country - {country}.\n")
            file.write(f"Region - {region}.\n")
            file.write(f"Winery - {winery}.\n")
            file.write(f"Wine type - {wine_type}.\n")
            file.write(f"Grape variety - {grape}.\n")
            file.write(f"Sum of reviews - {sum_reviews}.\n")
            file.write(f"Sum of parsed reviews - {len(review_dates)}.\n")
            file.write('-' * 35)
            file.write('\n')









