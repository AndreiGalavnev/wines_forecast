# парсинг ссылок на все вина с vivino
# вроде работает, но ему приходится загружать страницу с over 100К позициями вин, что тяжело 
# поэтому придется разбивать задачу, фильтруя поочерёдно winetype и countries
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



# URL-адрес страницы
url = "https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1N1BLrrR1ilRLBhJ-agVAyfQ027LEoszUksQctfyiFNuU1OJktfykStuixJLMvPTi-OT80rwSAEm_GL4%3D"
input_countries_list = ['Argentina', 'Australia', 'Austria', 'Chile', 'France', 'Germany', 'Italy', 'Portugal', 'Spain', 'United States', 'Israel', 'Hungary', 'New Zealand', 'South Africa', 'Greece', 'Romania', 'Slovenia', 'Switzerland']

for chosen_country in input_countries_list:
    for wine_t in range(3):
        #driver via local machine
        driver = webdriver.Chrome()
        # открываем страницу
        driver.get(url)
        # ждем время, чтобы дать странице время на загрузку
        time.sleep(2)
        # извлекаем HTML-код страницы
        html = driver.page_source
        # создаем объект BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')


#[1] нажимаем на кнопку ship to -> DE
        button = driver.find_element(By.XPATH, "//span[text()='Ship to']") 
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)
        show_button = driver.find_element(By.XPATH,'//a[@class="shipToDropdown_itemLink__7h3Co" and text()="Germany"]')
        driver.execute_script("arguments[0].click();", show_button)
        time.sleep(5)



#[2] теперь раздвигаем ползунок цены на максимальный интервал
        # находим элемент с классом "rc-slider"
        slider = driver.find_element(By.CSS_SELECTOR,'.rc-slider')
        # находим левый и правый ползунки
        left_handle = slider.find_element(By.CSS_SELECTOR,'.rc-slider-handle-1')
        right_handle = slider.find_element(By.CSS_SELECTOR,'.rc-slider-handle-2')
        # создаем объект ActionChains
        actions = ActionChains(driver)
        # перемещаем курсор мыши к левому ползунку
        actions.move_to_element(left_handle)
        # нажимаем и удерживаем левую кнопку мыши
        actions.click_and_hold()
        # перемещаем левый ползунок влево на 40 пикселей
        actions.move_by_offset(-40, 0)
        # отпускаем левую кнопку мыши
        actions.release()
        # перемещаем курсор мыши к правому ползунку
        actions.move_to_element(right_handle)
        # нажимаем и удерживаем левую кнопку мыши
        actions.click_and_hold()
        # перемещаем правый ползунок вправо на 200 пикселей
        actions.move_by_offset(200, 0)
        # отпускаем левую кнопку мыши
        actions.release()
        # выполняем действия
        actions.perform()
        time.sleep(5)


# [3] выбираем страну 
        # ввод в строку выбора страны название, собственно, страны 
        # и далее нажатие на унопку страны чуть ниже
        
        input_elements = driver.find_elements(By.CSS_SELECTOR, 'input.filterPills__search--2JrfM')
        input_elements[2].send_keys(chosen_country)
        button = driver.find_element(By.XPATH, f"//span[text()='{chosen_country}']")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)


#[4]!актуально для Австрии, Франции, Германии, Италии, Испании, ЮАР и США
        # выбирает только красные/белые/игристые/розовые/десертные/креплёные вина  
        
        colours = ''
        if wine_t == 0:
            button = driver.find_element(By.XPATH,f"//span[text()='Red']")          #красные вина
            colours += '_red_'
            button.click()
            time.sleep(1)
        elif wine_t == 1:
            button = driver.find_element(By.XPATH,f"//span[text()='White']")        #белые вина
            colours += '_white_'
            button.click()
            time.sleep(1)
        else:
            button = driver.find_element(By.XPATH,"//span[text()='Sparkling']")    #игристые вина
            colours += '_sparkling_'
            button.click()
            time.sleep(1)
            button = driver.find_element(By.XPATH,"//span[text()='Rosé']")         #розовые вина
            colours += '_rose_'
            button.click()
            time.sleep(1)
            button = driver.find_element(By.XPATH,"//span[text()='Dessert']")       #десертные вина
            colours += '_dessert_'
            button.click()
            time.sleep(1)
            button = driver.find_element(By.XPATH,"//span[text()='Fortified']")    #крепленые вина
            colours += '_fortified_'
            button.click()
            time.sleep(1)



#[5]  дальше прокручиваем страницу до конца 
        # получаем количество найденных вин
        wine_sum_element = driver.find_element(By.CLASS_NAME, 'querySummary__querySummary--39WP2')
        text = wine_sum_element.text
        match = re.search(r'\d+', text)
        if match:
            wine_sum_number = int(match.group())
        else:
            print('Число не найдено')
        # получаем высоту страницы
        last_height = driver.execute_script("return document.body.scrollHeight")
        # устанавливаем время ожидания скрипта 
        driver.set_script_timeout(120)
        # один из методов пролистывания
        try:
            scroll_height = driver.execute_script("return document.body.scrollHeight")
            for i in range(0, scroll_height*int(wine_sum_number/100), 250):    # грузим где-то четверть самых популярных из найденных вин  
                driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(2)
        except:
            print('Scrolling has been stopped')


#[6]  теперь получаем  ссылки на страницы всех загруженных вин
        links_elements = driver.find_elements(By.CSS_SELECTOR, '.anchor_anchor__m8Qi-.wineCard__cardLink--3F_uB')
        # создаем список для хранения ссылок
        links = []
        # извлекаем ссылки из найденных элементов
        for element in links_elements:
            link = element.get_attribute('href')
            # удаляем все символы после знака "?"
            link = link.split('?')[0]
            links.append(link)
        #print(f"Number of detected wines is {len(links)} (with duplicates)")
        driver.quit()
        # убираем повторы ссылок
        links = set(links)
        links = list(links)

        # выводим число ссылок и кидаем их в .txt
        f = open(f'all_{colours}_{chosen_country}_links.txt', 'w')
        for i in links:
            f.write(f'{i}\n')
        f.close()

        #print(f"Number of detected wines is {len(links)}")

