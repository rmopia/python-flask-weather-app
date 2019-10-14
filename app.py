from flask import Flask, render_template, request, url_for, redirect
import netifaces as n
import socket
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
    if ip is not None:
        lat = info['latitude']
        lon = info['longitude']
        weather = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon +
                               '&appid=b8fc977ef31325c1b897ea9fc8838e26').json()
        return render_template('home.html', title='Home', ip=ip, info=info, weather=weather)
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.run(debug=True)


