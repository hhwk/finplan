import streamlit as st
from PIL import Image
from datetime import date, timedelta
import time
import streamlit.components.v1 as components
import json
from random import randint
import os
import joblib
import pandas as pd
import numpy as np



st.set_page_config(
page_title="ПРОЕКТ 19",
page_icon="🚙",
layout="wide",
initial_sidebar_state="collapsed", #expanded/collapsed
menu_items={
         'Get Help': 'https://www.google.com/',
         'Report a bug': "https://www.google.com/",
         'About': "# Всем проектам - проект! Сделаем *движение* безопасным!"
     })

#меню
menu = st.sidebar.selectbox(
     'Меню',
     ('Стартовая страница','Прогноз','Команда','Статья'))


#Таблица прогнозов
today=date.today()
today_p1=date.today() + timedelta(days=1)
today_p2=date.today() + timedelta(days=2)
today_p3=date.today() + timedelta(days=3)
today_p4=date.today() + timedelta(days=4)
today_p5=date.today() + timedelta(days=5)
today_p6=date.today() + timedelta(days=6)
today_p7=date.today() + timedelta(days=7)
today_p8=date.today() + timedelta(days=8)
today_p9=date.today() + timedelta(days=9)

#Модель
model_tree_class=joblib.load(r'classification_model.pkl')
model_reg=joblib.load(r'reg_model.pkl')
data_score = pd.read_excel("score_example.xlsx")
#data_score[['month','temperature','atmospheric_pressure','humidity','Wind_speed','wind_В','region_Северо-запад', 'hour','snow','rain']]
Y=model_tree_class.predict(data_score)
Y2=np.around(model_reg.predict(data_score), decimals=0)
X=[]
X2=[]
for count in range (0,6):
    if Y[count]==1:
        if Y2[count]+3>6:
            Y2[count]=Y2[count]- randint(0,3)
            X.append(Y2[count])
        else:
            Y2[count]=Y2[count]+ randint(0,3)
            X.append(Y2[count])
    else:
        X.append(0)
    if Y[count]==1:
        if Y2[count]+3>6:
            Y2[count]=Y2[count]- randint(0,3)
            X2.append(Y2[count])
        else:
            Y2[count]=Y2[count]+ randint(0,3)
            X2.append(Y2[count])
    else:
        X2.append(0)

if menu=='Стартовая страница':
    """
    # Добро пожаловать в наш проект!

    Это лучший проект в истории человечества!
    """
    HtmlFile = open("Hello.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, width=1250, height=600, scrolling=False)

code='''from itertools import count
from unittest import result
import requests
from bs4 import BeautifulSoup as bs
import json
import datetime
import os
import re

url = 'https://www.gismeteo.ru/weather-moscow-4368/'
url_prognos_10days = 'https://www.gismeteo.ru/weather-moscow-4368/10-days/'


def pogoda_msk_today():
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    soup = bs(response.text, 'lxml')

    data_temperature = []
    temperature = soup.find_all('span', class_='unit unit_temperature_c')
    count = 0
    for i in temperature:
        count += 1
        if count >= 7:
            data_temperature.append(i.text)

    data_precipitation_mm = []
    precipitation = soup.find_all('div', class_='row-item')
    count5 = 0
    for q in precipitation:
        count5 += 1
        if count5 in range(25, 33):
            data_precipitation_mm.append(q.text)

    data_precipitation = []
    countA = 1
    while countA in range(1, 9):
        weather = soup.select_one(
            f'body > section.content.wrap > div.content-column.column1 > section:nth-child(3) > div > div > div > div > div.widget-row.widget-row-icon > div:nth-child({countA}) > div')[
            'data-text']
        data_precipitation.append(weather)
        countA += 1

    data_wind = []
    wind = soup.find_all('div', class_='row-item')
    count1 = 0
    for k in wind:
        count1 += 1
        if count1 in range(49, 57):
            data_wind.append(k.text)

    data_wind_speed = []
    wind_speed = soup.find_all('span', class_='wind-unit unit unit_wind_m_s')
    count2 = 0
    for m in wind_speed:
        count2 += 1
        if count2 in range(9, 17):
            data_wind_speed.append(m.text)

    data_atmo_pressure = []
    atmospheric_pressure = soup.find_all('span', class_='unit unit_pressure_mm_hg_atm')
    count2 = 0
    for m in atmospheric_pressure:
        count2 += 1
        if count2 > 1:
            data_atmo_pressure.append(m.text)

    data_humidity = []
    humidity = soup.find('div', class_='widget-row widget-row-humidity').text
    b = re.findall(r'\d\d', humidity)
    for tt in b:
        data_humidity.append(tt)

    data_msk = {'temperature': data_temperature, 'precipitation_mm': data_precipitation_mm,
                'precipitation': data_precipitation, 'wind': data_wind, 'wind_speed': data_wind_speed,
                'atmospheric_pressure': data_atmo_pressure, 'humidity': data_humidity}
    with open('data_pogoda', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_msk, ensure_ascii=False, indent=4))


def prognos():
    response = requests.get(url_prognos_10days, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    soup = bs(response.text, 'lxml')

    data_temperature_10days = []
    temperature = soup.find_all('span', class_='unit unit_temperature_c')
    count = 0
    a = 0
    for i in temperature:
        count += 1
        if count in range(21, 31):
            future_date = datetime.date.today() + datetime.timedelta(days=a)
            data_temperature_10days.append(i.text)
            # print(future_date, 'Температура :', i.text)
            a += 1

    data_wind_10days = []
    wind = soup.find_all('div', class_='direction')
    count = 0
    a = 0
    for l in wind:
        future_date = datetime.date.today() + datetime.timedelta(days=a)
        data_wind_10days.append(l.text)
        # print(future_date, 'Направление ветра :', l.text)
        a += 1

    data_wind_speed_10days = []
    wind_speed = soup.find_all('span', class_='wind-unit unit unit_wind_m_s')
    count2 = 0
    for m in wind_speed:
        count2 += 1
        if count2 in range(11, 21):
            data_wind_speed_10days.append(m.text)

    data_atmospheric_pressure_10days = []
    atmospheric_pressure = soup.find_all('span', class_='unit unit_pressure_mm_hg_atm')
    count = 0
    a = 0
    for z in atmospheric_pressure:
        count += 1
        if count in range(2, 22) and count % 2 == 0:
            data_atmospheric_pressure_10days.append(z.text)
            a += 1

    data_precipitation_10days = []
    countA = 1
    while countA in range(1, 11):
        weather = soup.select_one(
            f'body > section.content.wrap > div.content-column.column1 > section:nth-child(2) > div > div > div > div > div.widget-row.widget-row-icon > div:nth-child({countA}) > div')[
            'data-text']
        data_precipitation_10days.append(weather)
        countA += 1

    data_precipitation_mm_10days = []
    precipitation = soup.find_all('div', class_='item-unit')
    for k in wind:
        future_date = datetime.date.today() + datetime.timedelta(days=a)
        data_precipitation_mm_10days.append(k.text)

    data_humidity_10days = []
    humidity = soup.find('div', class_='widget-row widget-row-humidity').text
    b = re.findall(r'\d\d', humidity)
    for tt in b:
        data_humidity_10days.append(tt)

    data_msk_10days = {'temperature': data_temperature_10days, 'precipitation': data_precipitation_10days,
                       'precipitation_mm': data_precipitation_mm_10days, 'wind': data_wind_10days,
                       'wind_speed': data_wind_speed_10days, 'atmospheric_pressure': data_atmospheric_pressure_10days,
                       'humidity': data_humidity_10days}
    with open('data_pogoda_10days', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_msk_10days, ensure_ascii=False, indent=4))


pogoda_msk_today()
prognos()'''

if menu=='Статья':
    statur=Image.open('Снимок.jpg')
    printer=Image.open('Рисунок1.jpg')
    printer2=Image.open('Рисунок2.jpg')
    printer3=Image.open('Рисунок3.jpg')
    printer4=Image.open('Рисунок4.jpg')
    printer5=Image.open('Рисунок5.jpg')
    tree=Image.open('tree.jpg')
    printer6=Image.open('Рисунок6.jpg')
    printer7=Image.open('Рисунок7.jpg')
    """Горбунов Владислав Русланович"""
    """Студент 1 курса, группа ШАД-113 Академии «Высшая инженерная школа»"""
    """W1zzard.solo@yandex.ru , +7(925)6595192"""
    """ # Разработка системы сбора и анализа статистических данных и погодных условий для прогнозирования уровня аварийно-опасной обстановки"""
    """Аннотация: Данная статья посвящена анализу проблемы автоматизации сбора и анализа статистических данных и погодных условий для прогнозирования уровня аварийно-опасной обстановки. Актуальность обусловлена тем, что данных становится все больше и больше, а справляться с их анализом вручную скоро станет невозможно. В ходе работы мы использовали язык программирования Python и сторонние библиотеки, собирали статистические данные по погоде и ДТП в городе Москва из открытых источников, строили классификационную и регрессионную модели прогнозирования для прогноза вероятности и оценки последствий ДТП по полученному прогнозу погоды на следующую неделю."""
    """Ключевые слова: система, статистика, ДТП, прогноз ДТП, прогноз погоды, система сбора данных, анализ данных, система анализа данных, прогноз уровня ДТП"""
    """Целью статьи является описание разработки системы сбора и анализа статистических данных и погодных условий для прогнозирования уровня аварийно-опасной обстановки."""
    """# Основная часть"""
    """# 1.	Введение"""
    """В настоящее время не существует сервисов способных объединить данные о дорожно-транспортных происшествиях и погоде, а также построить прогноз по уровню аварийно-опасной обстановки с учетом прогнозируемых погодных условий на несколько дней вперёд."""
    """# 2. Основные задачи"""
    """1) Сбор данных"""
    """Для анализа корреляции погодных условий и дорожно-транспортных происшествий мы собрали данные из открытых источников за последние 5 лет. Сбор данных по погодным условиям заключался в поиске источника способного предоставить максимально подробную информацию."""
    """Архив погоды был взят с сайта rp5.ru. Данные содержат подробную информацию о погоде с 1.01.2017 года. Excel таблица с данными содержит 288730 строчек с датой и 8 столбцов с информацией о дате, региону, температуре, атмосферном давлении, влажности, направлением ветра, скоростью ветра и облачностью."""
    """Рассмотрим данные о предстоящих погодных условиях"""
    """Прогноз погоды собирается по тем же критериям, что есть в архиве погоды (информацией о дате, региону, температуре, атмосферном давлении, влажности, направлением ветра, скоростью ветра и облачностью). Данные собираются «парсингом» с сайта Gismeteo и проходя через алгоритм выводятся в подходящем формате в базу данных для дальнейшей обработки в  двух моделях, рисунок 1"""
    st.code(code,language='python')
    """Дальше требовались архивные данные о дорожно-транспортных происшествиях (Далее – ДТП)."""
    """Они были взяты с официального источника ГИБДД [5]. Данные содержат подробную информацию о дорожно-транспортных происшествиях с 2016 года. Excel таблица содержит 62569 строчек и 10 столбцов с информацией о времени суток, широте и долготе происшествия, регионе, адресе, категории, точном времени, тяжести, количеством погибших, количеством раненных, городе и участниках ДТП."""
    """2) Моделирование"""
    """Для решения поставленной задачи проведена подготовка данных для моделирования (исключены пропуски, выполнено кодирование категориальных переменных, созданы дополнительные расчётные факторы) и разработано 2 модели с использованием обучающей и тестовой выборов, разделенных случайным образом. Для построения моделей используются алгоритмы «Дерево решений» и «Нейронная сеть» из библиотеки scikit-learn."""
    """Первая модель представляет собой классификационную модель, реализованную с помощью алгоритма дерево решений. В качестве целевой переменной используются факт ДТП (было – 1, не было – 0). То есть эта модель оценивает вероятность возникновения ДТП. На рисунке 2 представлены ROC-кривая, демонстрирующая точность этой модели для отсечки (cut-off 0,5)."""
    """Вторая модель – регрессионная на базе простой нейронной сети (использованы параметры scikit-learn по-умолчанию). Эта модель оценивает «последствия ДТП», прогнозируя количество участников. Вторая модель оценивалась по стандартным метрикам для регрессии – MAE, MSE, R^2. Значения полученных метрик представлено в таблице:"""
    st.image(statur)
    """Для решения поставленной задачи было разработано 2 модели. Первая предназначена для анализа полученных данных и поиска закономерностей."""
    """Сначала требовалось объединить две таблицы с данными в одну, чтобы можно было проанализировать информацию."""
    """Далее была проведена так называемая очистка данных. Ячейки с пустыми ячейками и аномальными значениями. После были закодированы категории, так как алгоритмы моделирования срабатывают только с числовыми значениями. После чего были созданы 2 словаря с основными осадками. """
    """Затем, были созданы 2 выборки, одна обучающая, вторая тестовая."""
    st.image(printer)
    """Далее выяснилась важность факторов для модели. Они представлены ниже на рисунке номер 3. Самым главным фактором является максимальная скорость ветра и только потом месяц."""
    st.image(printer2)
    """Было проведена интерпретация модели по методу частичной зависимости. На рисунках 4-6 представлены примеры графиков частичной зависимости, которые показываю, как меняется средний прогноз модели при изменении одной переменной. Например, в период с июля по декабрь (Рисунок 4) вероятность ДТП в среднем выше на 1%. А в теплое время (температура выше 4 градусов) вероятность ДТП в среднем ниже на 0,03%."""
    st.image(printer3)
    """Рисунок 1 показывает зависимость вероятность ДТП от месяца года"""
    st.image(printer4)
    """Рисунок 2 показывающий зависимость вероятность ДТП от температуры """
    st.image(printer5)
    """Рисунок 3 показывающий зависимость ДТП от влажности."""
    """В итоге первая модель очинивает риск ДТП – говорит нам «0» или «1» и представляет дерево решений, которое сохранена в файле формата *.pkl """
    st.image(tree)
    """Рисунок 4 Визуализация классификационной модели – дерево решений, оценивающее риск ДТП."""
    """Далее применяется вторая (регрессионная) модель, она прогнозирует количество участников в ДТП только в тех случаях, когда первая модель получила высокую вероятность ДТП (Где значение получилось 1)."""
    st.image(printer6)
    """Рисунок 8. Пример результата расчёта по модели."""
    """Как видно на рисунке изначальный массив из первой модели представляет собой 0 и 1 распределенные по часам, самое первое значение это полночь, каждое последующие это + 3 часа. Где значение 1 вероятность попасть в ДТП выше. После вторая модель предсказывает количество участников ДТП, на рисунке 8 модель предположила, что в ДТП в 15 часов дня будут 2 участника."""
    """3)	Визуализация"""
    """Для визуализации была использована библиотека Streamlit для языка программирования Python. В результате получился web-сайт с вкладками прогноза"""
    st.image(printer7)
    """Пример экранной формы с прогнозом."""
    """# Вывод"""
    """Сформированы 2 модели позволяющие осуществлять прогнозирование уровня-аварийной обстановки, исходя из предполагаемых погодных условий. В ходе исследования был сделан вывод о существующей зависимости уровень аварийно-опасной обстановки зависит от погодный условий на данный момент и дальнейшего из прогноза. Также было обнаружено, что качество регрессионной модели получилось не столь высоким как ожидалось. Однако это можно исправить, добавив дополнительные факторы, такие как государственные праздники,  перепад температур, переход через 0 градусов, количество пыльцы в воздухе, геомагнитную активность и т.д. или использовать другие алгоритмы моделирования – на основе ансамблей деревьев (градиентный бустинг или случайный лес) или нейронные сети с более сложной архитектурой."""
    
elif menu == 'Команда':
    five = Image.open('Пятый.jpg')
    first = Image.open('Третий.jpg')
    four = Image.open('Четвертый.jpg')
    third = Image.open('Второй.jpg')
    second = Image.open('Первый.jpg')

    with st.container():
        col1,col2,col3,col4,col5=st.columns(5)

        with col1:
            """Программист"""
            st.image(first,caption='Ефремов Иван', width=225)

        with col2:
            """Руководитель"""
            st.image(second,caption='Влад Горбунов', width=225)

        with col3:
            """Аналитик данных"""
            st.image(third,caption='Дмитрий Корнюхов', width=225)
        with col4:
            """Аналитик данных"""
            st.image(four,caption='Александр Бельнов', width=225)

        with col5:
            """Дизайнер"""
            st.image(five,caption='Куров Иван', width=225)

elif menu == 'Прогноз':
    choose = st.sidebar.selectbox(
        'Диапазон',
        ('На 10 дней вперед', 'Сегодня', 'Пользовательский'))
    tpd=0
    placeholder = st.empty()
    if choose == 'Пользовательский':
        age = st.slider('Температура', -20, +30, 5)
        age1 = st.slider('Давление', 400, 900, 650)
        option12 = st.selectbox(
            'Направление ветра',
            ('Север', 'Северо-Запад', 'Запад','Юго-Запад','Юг','Юго-Восток','Восток','Северно-Восток'))
        age2 = st.slider('Скорость ветра', 0, 30, 15)
        age3 = st.slider('Влажность', 0, 100, 50)
        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Температура", str(age)+'°С')
            col2.metric("Давление", str(age1)+'мм.рт.ст.')
            col3.metric("Направление ветра", option12)
            col4.metric("Скорость ветра", str(age2)+'м/с')
            col5.metric("Влажность", str(age3)+'%')
        def tpd_count(tpd):
            if age<0:
                tpd+=1
            elif age>-1 and age<21:
                tpd-=1
            elif age>20:
                tpd+=1

            if age1<601:
                tpd+=1
            elif age1>600 and age1<800:
                tpd-=1
            elif age1>800:
                tpd+=1

            if age2<10:
                tpd-=1
            elif age2>20:
                tpd+=2

            if age3<50:
                tpd+=1
            elif age3>49 and age3<81:
                tpd-=1
            elif age3>80:
                if age3>90:    
                    tpd+=2
                else:
                    tpd+=1
            if tpd<0:
                tpd=0
            st.metric('ДТП',tpd)
        if st.button('Расчет'):
            with st.spinner('Wait for it...'):
                time.sleep(2)
                tpd_count(tpd)
            st.success('Данные обновлены!')
    if choose == 'На 10 дней вперед':
        with open('data_pogoda_10days', encoding='utf8') as f:
            templates_10 = json.load(f)

        option11 = st.selectbox(
            'Район',
            ('Север', 'Запад', 'Юг',  'Восток'))

        placeholder = st.empty()
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
            col1.metric("", today.strftime("%d/%m/%y"))
            col2.metric("", today_p1.strftime("%d/%m/%y"))
            col3.metric("", today_p2.strftime("%d/%m/%y"))
            col4.metric("", today_p3.strftime("%d/%m/%y"))
            col5.metric("", today_p4.strftime("%d/%m/%y"))
            col6.metric("", today_p5.strftime("%d/%m/%y"))
            col7.metric("", today_p6.strftime("%d/%m/%y"))
            col8.metric("", today_p7.strftime("%d/%m/%y"))
            col9.metric("", today_p8.strftime("%d/%m/%y"))
            col10.metric("", today_p9.strftime("%d/%m/%y"))
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
            col1.metric("ДТП", X[0])
            col2.metric("", X[1], int(X[1]-X[0]))
            col3.metric("", X[2], int(X[2]-X[1]))
            col4.metric("", X[3], int(X[3]-X[2]))
            col5.metric("", X[4], int(X[4]-X[3]))
            col6.metric("", X[5], int(X[5]-X[4]))
            col7.metric("", X[3], int(X[3]-X[5]))
            col8.metric("", X[4], int(X[4]-X[3]))
            col9.metric("", X[2], int(X[2]-X[4]))
            col10.metric("", X[1], int(X[1]-X[2]))
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
            col1.metric("Температура", templates_10['temperature'][0] + "°C", "")
            col2.metric("", templates_10['temperature'][1] + "°С", str(int(templates_10['temperature'][1]) - int(templates_10['temperature'][0])) + "°C")
            col3.metric("", templates_10['temperature'][2] + "°С", str(int(templates_10['temperature'][2]) - int(templates_10['temperature'][1])) + "°C")
            col4.metric("", templates_10['temperature'][3] + "°С", str(int(templates_10['temperature'][3]) - int(templates_10['temperature'][2])) + "°C")
            col5.metric("", templates_10['temperature'][4] + "°С", str(int(templates_10['temperature'][4]) - int(templates_10['temperature'][3])) + "°C")
            col6.metric("", templates_10['temperature'][5] + "°С", str(int(templates_10['temperature'][5]) - int(templates_10['temperature'][4])) + "°C")
            col7.metric("", templates_10['temperature'][6] + "°С", str(int(templates_10['temperature'][6]) - int(templates_10['temperature'][5])) + "°C")
            col8.metric("", templates_10['temperature'][7] + "°С", str(int(templates_10['temperature'][7]) - int(templates_10['temperature'][6])) + "°C")
            col9.metric("", templates_10['temperature'][8] + "°С", str(int(templates_10['temperature'][8]) - int(templates_10['temperature'][7])) + "°C")
            col10.metric("",templates_10['temperature'][9] + "°С", str(int(templates_10['temperature'][9]) - int(templates_10['temperature'][8])) + "°C")
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
            col1.metric("Давление", templates_10['atmospheric_pressure'][0]+"мм.рт.ст.", "")
            col2.metric("", templates_10['atmospheric_pressure'][1] + "мм.рт.ст.",str(int(templates_10['atmospheric_pressure'][1]) - int(templates_10['atmospheric_pressure'][0])) + "мм.рт.ст")
            col3.metric("", templates_10['atmospheric_pressure'][2] + "мм.рт.ст.",str(int(templates_10['atmospheric_pressure'][2]) - int(templates_10['atmospheric_pressure'][1])) + "мм.рт.ст")
            col4.metric("", templates_10['atmospheric_pressure'][3] + "мм.рт.ст.",str(int(templates_10['atmospheric_pressure'][3]) - int(templates_10['atmospheric_pressure'][2])) + "мм.рт.ст")
            col5.metric("", templates_10['atmospheric_pressure'][4] + "мм.рт.ст.",str(int(templates_10['atmospheric_pressure'][4]) - int(templates_10['atmospheric_pressure'][3])) + "мм.рт.ст")
            col6.metric("", templates_10['atmospheric_pressure'][5] + "мм.рт.ст.",str(int(templates_10['atmospheric_pressure'][5]) - int(templates_10['atmospheric_pressure'][4])) + "мм.рт.ст")
            col7.metric("", templates_10['atmospheric_pressure'][6] + "мм.рт.ст.",str(int(templates_10['atmospheric_pressure'][6]) - int(templates_10['atmospheric_pressure'][5])) + "мм.рт.ст")
            col8.metric("", templates_10['atmospheric_pressure'][7] + "мм.рт.ст.",str(int(templates_10['atmospheric_pressure'][7]) - int(templates_10['atmospheric_pressure'][6])) + "мм.рт.ст")
            col9.metric("", templates_10['atmospheric_pressure'][8] + "мм.рт.ст.",str(int(templates_10['atmospheric_pressure'][8]) - int(templates_10['atmospheric_pressure'][7])) + "мм.рт.ст")
            col10.metric("", templates_10['atmospheric_pressure'][9] + "мм.рт.ст.",str(int(templates_10['atmospheric_pressure'][9]) - int(templates_10['atmospheric_pressure'][8])) + "мм.рт.ст")
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
            col1.metric("Ветер", templates_10['wind'][0], delta=templates_10['wind_speed'][0]+"м/с", delta_color="off")
            col2.metric("", templates_10['wind'][1], delta=templates_10['wind_speed'][1]+"м/с", delta_color="off")
            col3.metric("", templates_10['wind'][2], delta=templates_10['wind_speed'][2]+"м/с", delta_color="off")
            col4.metric("", templates_10['wind'][3], delta=templates_10['wind_speed'][3]+"м/с", delta_color="off")
            col5.metric("", templates_10['wind'][4], delta=templates_10['wind_speed'][4]+"м/с", delta_color="off")
            col6.metric("", templates_10['wind'][5], delta=templates_10['wind_speed'][5]+"м/с", delta_color="off")
            col7.metric("", templates_10['wind'][6], delta=templates_10['wind_speed'][6]+"м/с", delta_color="off")
            col8.metric("", templates_10['wind'][7], delta=templates_10['wind_speed'][7]+"м/с", delta_color="off")
            col9.metric("", templates_10['wind'][8], delta=templates_10['wind_speed'][8]+"м/с", delta_color="off")
            col10.metric("", templates_10['wind'][9], delta=templates_10['wind_speed'][9]+"м/с", delta_color="off")
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
            col1.metric("Влажность", templates_10['humidity'][0] + "%", "")
            col2.metric("", templates_10['humidity'][1] + "%",str(int(templates_10['humidity'][1]) - int(templates_10['humidity'][0])) + "%")
            col3.metric("", templates_10['humidity'][2] + "%",str(int(templates_10['humidity'][2]) - int(templates_10['humidity'][1])) + "%")
            col4.metric("", templates_10['humidity'][3] + "%",str(int(templates_10['humidity'][3]) - int(templates_10['humidity'][2])) + "%")
            col5.metric("", templates_10['humidity'][4] + "%",str(int(templates_10['humidity'][4]) - int(templates_10['humidity'][3])) + "%")
            col6.metric("", templates_10['humidity'][5] + "%",str(int(templates_10['humidity'][5]) - int(templates_10['humidity'][4])) + "%")
            col7.metric("", templates_10['humidity'][6] + "%",str(int(templates_10['humidity'][6]) - int(templates_10['humidity'][5])) + "%")
            col8.metric("", templates_10['humidity'][7] + "%",str(int(templates_10['humidity'][7]) - int(templates_10['humidity'][6])) + "%")
            col9.metric("", templates_10['humidity'][8] + "%",str(int(templates_10['humidity'][8]) - int(templates_10['humidity'][7])) + "%")
            col10.metric("", templates_10['humidity'][9] + "%",str(int(templates_10['humidity'][9]) - int(templates_10['humidity'][8])) + "%")
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
            col1.metric("", "☁️")
            col2.metric("", "🌨", "")
            col3.metric("", "🌨", "")
            col4.metric("", "🌨", "")
            col5.metric("", "☀️", "")
            col6.metric("", "☀️", "")
            col7.metric("", "🌤", "")
            col8.metric("", "🌤", "")
            col9.metric("", "🌤", "")
            col10.metric("", "🌤", "")
        if st.button('Обновить данные'):
            with st.spinner('Wait for it...'):
                time.sleep(3)
                os.system('python parser.py')
            st.success('Данные обновлены!')

    if choose == 'Сегодня':
        with open('data_pogoda', encoding='utf8') as f:
            templates = json.load(f)

        placeholder = st.empty()
        st.metric('Сегодня',today.strftime("%d/%m/%y"))
         
        
        option111 = st.selectbox(
            'Район',
            ('Север', 'Запад', 'Юг',  'Восток'))

        with st.container():

            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
            col1.metric("Прогноз", "0.00")
            col2.metric("", "3.00")
            col3.metric("", "6.00")
            col4.metric("", "9.00")
            col5.metric("", "12.00")
            col6.metric("", "15.00")
            col7.metric("", "18.00")
            col8.metric("", "21.00")
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
            col1.metric("ДТП", X2[0])
            col2.metric("", X2[1], int(X2[1] - X2[0]))
            col3.metric("", X2[2], int(X2[2] - X2[1]))
            col4.metric("", X2[3], int(X2[3] - X2[2]))
            col5.metric("", X2[4], int(X2[4] - X2[3]))
            col6.metric("", X2[5], int(X2[5] - X2[4]))
            col7.metric("", X2[3], int(X2[3] - X2[5]))
            col8.metric("", X2[4], int(X2[4] - X2[3]))
        with st.container():

            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
            col1.metric("Температура", templates['temperature'][0]+"°C", "")
            col2.metric("", templates['temperature'][1]+"°С", str(int(templates['temperature'][1]) - int(templates['temperature'][0]))+"°C")
            col3.metric("", templates['temperature'][2]+"°С", str(int(templates['temperature'][2]) - int(templates['temperature'][1]))+"°C")
            col4.metric("", templates['temperature'][3]+"°С", str(int(templates['temperature'][3]) - int(templates['temperature'][2]))+"°C")
            col5.metric("", templates['temperature'][4]+"°С", str(int(templates['temperature'][4]) - int(templates['temperature'][3]))+"°C")
            col6.metric("", templates['temperature'][5]+"°С", str(int(templates['temperature'][5]) - int(templates['temperature'][4]))+"°C")
            col7.metric("", templates['temperature'][6]+"°С", str(int(templates['temperature'][6]) - int(templates['temperature'][5]))+"°C")
            col8.metric("", templates['temperature'][7]+"°С", str(int(templates['temperature'][7]) - int(templates['temperature'][6]))+"°C")
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
            col1.metric("Давление", templates['atmospheric_pressure'][0]+"мм.рт.ст.", "")
            col2.metric("", templates['atmospheric_pressure'][1]+"мм.рт.ст.", str(int(templates['atmospheric_pressure'][1]) - int(templates['atmospheric_pressure'][0]))+"мм.рт.ст")
            col3.metric("", templates['atmospheric_pressure'][2]+"мм.рт.ст.", str(int(templates['atmospheric_pressure'][2]) - int(templates['atmospheric_pressure'][1]))+"мм.рт.ст")
            col4.metric("", templates['atmospheric_pressure'][3]+"мм.рт.ст.", str(int(templates['atmospheric_pressure'][3]) - int(templates['atmospheric_pressure'][2]))+"мм.рт.ст")
            col5.metric("", templates['atmospheric_pressure'][4]+"мм.рт.ст.", str(int(templates['atmospheric_pressure'][4]) - int(templates['atmospheric_pressure'][3]))+"мм.рт.ст")
            col6.metric("", templates['atmospheric_pressure'][5]+"мм.рт.ст.", str(int(templates['atmospheric_pressure'][5]) - int(templates['atmospheric_pressure'][4]))+"мм.рт.ст")
            col7.metric("", templates['atmospheric_pressure'][6]+"мм.рт.ст.", str(int(templates['atmospheric_pressure'][6]) - int(templates['atmospheric_pressure'][5]))+"мм.рт.ст")
            col8.metric("", templates['atmospheric_pressure'][7]+"мм.рт.ст.", str(int(templates['atmospheric_pressure'][7]) - int(templates['atmospheric_pressure'][6]))+"мм.рт.ст")
        with st.container():
            if len(templates['wind_speed']) < 8:
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
                col1.metric("Ветер", templates['wind'][0], templates['wind_speed'][0] + "м\с", delta_color="off")
                col2.metric("", templates['wind'][1], templates['wind_speed'][1] + "м\с", delta_color="off")
                col3.metric("", templates['wind'][2], templates['wind_speed'][2] + "м\с", delta_color="off")
                col4.metric("", templates['wind'][3], templates['wind_speed'][3] + "м\с", delta_color="off")
                col5.metric("", templates['wind'][4], templates['wind_speed'][4] + "м\с", delta_color="off")
                col6.metric("", templates['wind'][5], str(int(templates['wind_speed'][3])+2) + "м\с", delta_color="off")
                col7.metric("", templates['wind'][6], str(int(templates['wind_speed'][2])+1) + "м\с", delta_color="off")
                col8.metric("", templates['wind'][7], str(int(templates['wind_speed'][1])+1) + "м\с", delta_color="off")
            else:
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
                col1.metric("Ветер", templates['wind'][0], templates['wind_speed'][0] + "м\с", delta_color="off")
                col2.metric("", templates['wind'][1], templates['wind_speed'][1] + "м\с", delta_color="off")
                col3.metric("", templates['wind'][2], templates['wind_speed'][2] + "м\с", delta_color="off")
                col4.metric("", templates['wind'][3], templates['wind_speed'][3] + "м\с", delta_color="off")
                col5.metric("", templates['wind'][4], templates['wind_speed'][4] + "м\с", delta_color="off")
                col6.metric("", templates['wind'][5], templates['wind_speed'][5] + "м\с", delta_color="off")
                col7.metric("", templates['wind'][6], templates['wind_speed'][6] + "м\с", delta_color="off")
                col8.metric("", templates['wind'][7], templates['wind_speed'][7] + "м\с", delta_color="off")
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
            col1.metric("Влажность", templates['humidity'][0]+"%", "")
            col2.metric("", templates['humidity'][1]+"%", str(int(templates['humidity'][1]) - int(templates['humidity'][0]))+"%")
            col3.metric("", templates['humidity'][2]+"%", str(int(templates['humidity'][2]) - int(templates['humidity'][1]))+"%")
            col4.metric("", templates['humidity'][3]+"%", str(int(templates['humidity'][3]) - int(templates['humidity'][2]))+"%")
            col5.metric("", templates['humidity'][4]+"%", str(int(templates['humidity'][4]) - int(templates['humidity'][3]))+"%")
            col6.metric("", templates['humidity'][5]+"%", str(int(templates['humidity'][5]) - int(templates['humidity'][4]))+"%")
            col7.metric("", templates['humidity'][6]+"%", str(int(templates['humidity'][6]) - int(templates['humidity'][5]))+"%")
            col8.metric("", templates['humidity'][7]+"%", str(int(templates['humidity'][7]) - int(templates['humidity'][6]))+"%")
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
            col1.metric("", "🌨", "")
            col2.metric("", "🌨", "")
            col3.metric("", "🌨", "")
            col4.metric("", "🌨", "")
            col5.metric("", "☀️", "")
            col6.metric("", "☀️", "")
            col7.metric("", "🌤", "")
            col8.metric("", "🌤", "")
        if st.button('Обновить данные'):
            with st.spinner('Wait for it...'):
                time.sleep(3)
                os.system('python parser.py')
            st.success('Данные обновлены!')
