import os
import requests

from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.config['SECRET_KEY'] = 'MOJ_TAJNI_KLJUČ'
OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')

class SettingsForm(FlaskForm):
    city = StringField('Grad', validators=[DataRequired()])
    lang = SelectField('Jezik', choices=[('hr', 'Hrvatski'), ('en', 'English'), ('de', 'Deutch')], validators=[DataRequired()])
    units = SelectField(choices=[('metric', 'Metric'), ('imperial', 'Imperial')], validators=[DataRequired()])
    submit = SubmitField('Spremi')


@app.route('/')
def index():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    city = session.get('city') if session.get('city') else 'zadar'
    parameters = {'q': city, 'appid': OPEN_WEATHER_API_KEY, 'units':session.get('units'), 'lang':session.get('lang') }
    response = requests.get(url, parameters)
    weather = response.json()
    return render_template('index.html', weather = weather, session = session)


@app.route('/settings/', methods=['GET','POST'])
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        session['city'] = form.city.data
        session['lang'] = form.lang.data
        session['units'] = form.units.data
        return redirect(url_for('settings'))

    form.city.data = session.get('city')
    form.lang.data = session.get('lang')
    form.units.data = session.get('units')
    return render_template('settings.html', form = form)    