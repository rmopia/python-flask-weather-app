import requests
import datetime
import numpy as np
import calendar
import os
import json

info = requests.get('https://get.geojs.io/v1/ip/geo.json').json()
city = info['city']
ip = info['ip']
time_zone = info['timezone']
lat = info['latitude']
longitude = info['longitude']

print(ip)
print(time_zone)
print(city + ', ' + info['region'] + ', ' + info['country'])

# api_key = 'b8fc977ef31325c1b897ea9fc8838e26'
weather = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + longitude +
                       '&appid=b8fc977ef31325c1b897ea9fc8838e26').json()

# print(weather)
# print(weather['main'])

# 5 day weather

fiveday = requests.get('http://api.openweathermap.org/data/2.5/forecast?lat=' + lat + '&lon=' + longitude +
                       '&appid=b8fc977ef31325c1b897ea9fc8838e26').json()

kelvin_list = []
fa_list = []
#print(fiveday)
# for item in fiveday['list']:
#    kelvin_list.append(item)
# print(fiveday['list'][2])
# print(fiveday['list'][39]['main']['temp'])

for i in range(40):
    temp_tuple = (fiveday['list'][i]['main']['temp'], fiveday['list'][i]['main']['temp_min'], fiveday['list'][i]['main']['temp_max'])
    kelvin_list.append(temp_tuple)

print(kelvin_list)

for tup in kelvin_list:
    new_item = tuple(np.round(np.add(np.multiply(np.subtract(tup, 273.15), 9/5), 32)))
    #new_item = round((float(tup) - 273.15) * (9 / 5) + 32)
    fa_list.append(new_item)


print("fa list: " + str(fa_list))

day1_forecast = []
day2_forecast = []
day3_forecast = []
day4_forecast = []
day5_forecast = []

for x in range(1, 6):
    # print(x)
    if x == 1:
        for i in range(0, 8):
            # print(i)
            day1_forecast.append(fa_list[i])
    elif x == 2:
        for i in range(8, 16):
            day2_forecast.append(fa_list[i])
    elif x == 3:
        for i in range(16, 24):
            day3_forecast.append(fa_list[i])
    elif x == 4:
        for i in range(24, 32):
            day4_forecast.append(fa_list[i])
    else:
        for i in range(32, 40):
            day5_forecast.append(fa_list[i])

print(day1_forecast)
print(day2_forecast)
print(day3_forecast)
print(day4_forecast)
print(day5_forecast)

cur_time = datetime.datetime.now()  # determines what 3-hour block of weather info will show for at least today
print(cur_time)
cur_hour = cur_time.hour


def determine_weather(hour, forecast):
    if hour == 24 or hour == 0 or hour == 1 or hour == 2:
        print(forecast[0])
    if hour == 3 or hour == 4 or hour == 5:
        print(forecast[1])
    if hour == 6 or hour == 7 or hour == 8:
        print(forecast[2])
    if hour == 9 or hour == 10 or hour == 11:
        print(forecast[3])
    if hour == 12 or hour == 13 or hour == 14:
        print(forecast[4])
    if hour == 15 or hour == 16 or hour == 17:
        print(forecast[5][0])
    if hour == 18 or hour == 19 or hour == 20:
        print(forecast[6][0])
    if hour == 21 or hour == 22 or hour == 23:
        print(forecast[7])


def avg_temp(forecast):  # use for days 2,3,4 and 5
    triples_list = []
    for triples in forecast:
        triples_list.append(int(triples[0]))
    length = len(triples_list)
    triples_sum = sum(triples_list)
    avg = round(triples_sum/length)
    return avg


def forecast_days():
    today = datetime.datetime.now().weekday()
    our_days = []

    for n in range(today, today + 5):
        day = n % 7
        calender_day = calendar.day_name[day]
        our_days.append(calender_day)

    print(our_days)


determine_weather(cur_hour, day1_forecast)
navg = avg_temp(day2_forecast)
# print(navg)
forecast_days()

time = datetime.datetime.now().time()
print(time)
