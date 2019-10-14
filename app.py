from flask import Flask, render_template, request, url_for, redirect
import netifaces as n
import socket
import datetime
import numpy as np
import calendar
import requests

app = Flask(__name__)


@app.route('/result')
def result():
    return render_template('home.html')


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    info = requests.get('https://get.geojs.io/v1/ip/geo.json').json()
    ip = info['ip']
    # TODO parse json strings and put wanted info into container i.e. city, country, etc.
    # TODO tuple container for weather info (current temp, temp in an hour, humidity)
    time = datetime.datetime.now()
    time_now = time.strftime('%I:%M %p')
    if ip is not None:
        weather = weather_forecast(info)
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
                    day1_forecast.append(weather[i])
            elif x == 2:
                for i in range(8, 16):
                    day2_forecast.append(weather[i])
            elif x == 3:
                for i in range(16, 24):
                    day3_forecast.append(weather[i])
            elif x == 4:
                for i in range(24, 32):
                    day4_forecast.append(weather[i])
            else:
                for i in range(32, 40):
                    day5_forecast.append(weather[i])

        day1_triple = weather_block(day1_forecast)
        day1 = tuple_to_list(day1_triple)
        print(day1)

        avg_day2 = avg_temp(day2_forecast)
        avg_day3 = avg_temp(day3_forecast)
        avg_day4 = avg_temp(day4_forecast)
        avg_day5 = avg_temp(day5_forecast)

        days_list = forecast_days()

        return render_template('home.html', title='Home', ip=ip, info=info, day1=day1, avg_day2=avg_day2,
                               avg_day3=avg_day3, avg_day4=avg_day4, avg_day5=avg_day5, days_list=days_list,
                               time_now=time_now)
    else:
        return redirect(url_for('home'))


def weather_forecast(info):
    kelvin_list = []
    fa_list = []
    lat = info['latitude']
    lon = info['longitude']
    five_days = requests.get('http://api.openweathermap.org/data/2.5/forecast?lat=' + lat + '&lon=' + lon +
                             '&appid=b8fc977ef31325c1b897ea9fc8838e26').json()
    for i in range(40):
        temp_tuple = (five_days['list'][i]['main']['temp'], five_days['list'][i]['main']['temp_min'],
                      five_days['list'][i]['main']['temp_max'])
        kelvin_list.append(temp_tuple)
    for tup in kelvin_list:
        new_item = tuple(np.round(np.add(np.multiply(np.subtract(tup, 273.15), 9 / 5), 32)))
        fa_list.append(new_item)
    return fa_list


def weather_block(day1_forecast):
    hour = datetime.datetime.now().hour
    if hour == 0 or hour == 1 or hour == 2:
        return day1_forecast[0]
    elif hour == 3 or hour == 4 or hour == 5:
        return day1_forecast[1]
    elif hour == 6 or hour == 7 or hour == 8:
        return day1_forecast[2]
    elif hour == 9 or hour == 10 or hour == 11:
        return day1_forecast[3]
    elif hour == 12 or hour == 13 or hour == 14:
        return day1_forecast[4]
    elif hour == 15 or hour == 16 or hour == 17:
        return day1_forecast[5]
    elif hour == 18 or hour == 19 or hour == 20:
        return day1_forecast[6]
    else:  # 21, 22, 23
        return day1_forecast[7]


def avg_temp(forecast):  # use for days 2,3,4 and 5
    triples_list = []
    for triples in forecast:
        triples_list.append(int(triples[0]))
    length = len(triples_list)
    triples_sum = sum(triples_list)
    avg = round(triples_sum / length)
    return avg


def forecast_days():
    today = datetime.datetime.now().weekday()
    our_days = []

    for n in range(today, today + 5):
        day = n % 7
        calender_day = calendar.day_name[day]
        our_days.append(calender_day)
    return our_days


def tuple_to_list(triple):
    day1_result = []
    new_list = list(triple)
    for item in new_list:
        day1_result.append(int(item))
    return day1_result


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
