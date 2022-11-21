import os
import requests

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
app = Flask(__name__)
bootstrap = Bootstrap5(app)

OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')

@app.route('/')
def index():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    city = 'zadar'
    parameters = {'q': city, 'appid': OPEN_WEATHER_API_KEY }
    response = requests.get(url, parameters)
    weather = response.json()
    return render_template('index.html', weather = weather)