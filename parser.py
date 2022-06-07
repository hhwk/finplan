from itertools import count
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
prognos()