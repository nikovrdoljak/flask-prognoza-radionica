# Flask - Vremenska prognoza
U ovoj radionici izradit ćemo Flask aplikacije za prikaz vremenske prognoze u nekom gradu. Slijedeće elemente ćemo koristiti:
* https://openweathermap.org/ za dohvat podataka o trenutnoj vremenskoj situaciji i prognoszi
* ```requests``` komponentu za pozive REST API-jima
* ```flask-wtf``` komponentu za rad s web formama
* ```bootstrap-flask``` komponentu za korištenje Bootstrap web frameworka
* ```flask-caching``` komponentu za spremanje rezultata u privremenu memoriju

## Postavimo aplikaciju
Stvorimo radnu mapu, te u njoj postavimo i aktivirajmo virtualnu okolinu:
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instalirajmo Flask:
```
pip install flask
```

Kreirajmo app.py datoteku i postavimo inicijalnu Flask aplikaciju:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Vremenska prognoza</h1>'
```

Postavimo još FLASK_DEBUG varijablu na 1, te pokrenimo aplikaciju da budemo sigurni da radi:
```
$env:FLASK_DEBUG=1
flask run
```
Provjerite u pregledniku da na adresi http://localhost:5000/ web stranica prikazuje naslov "**Vremenska prognoza**".

## Postavljanje Bootstrapa
Za rad s Bootstrap okvirom koristit ćemo flask_bootstrap komponentu. Dokumentaciju za nju možete pronaći na adresi https://bootstrap-flask.readthedocs.io/en/latest/.
Najprije ju instalirajmo:
```
pip install bootstrap-flask
```
U ```app.py``` datoteku dodajmo slijedeće import izraze te aktivirajmo Bootstrap objekt u aplikaciji:
``` python
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
app = Flask(__name__)
bootstrap = Bootstrap5(app)
```
Dodat ćemo i prvi predložak za naslovnu stranicu, koji će naslijeđivati osnovnu Bootstrap stranicu. 
Kreirajmo mapu ```templates``` te u nju dodajmo dvije datoteke:

*base.html*
```html
{% from 'bootstrap5/nav.html' import render_nav_item %}
<!doctype html>
<html lang="en">
    <head>
        {% block head %}
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        {% block styles %}
            {{ bootstrap.load_css() }}
        {% endblock %}

        <title>Vremenska prognoza</title>
        {% endblock %}
    </head>
    <body>
        <div class="container">
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <a class="navbar-brand" href="{{url_for('index')}}">Vremenska prognoza</a>
                <div class="navbar-nav mr-auto">
                    {{ render_nav_item('index', 'Vrijeme') }}
                </div>
            </nav>
        </div>
        <div class="container">
        {% block content %}{% endblock %}
        </div>
        {% block scripts %}
            {{ bootstrap.load_js() }}
        {% endblock %}
    </body>
</html>
```

*index.html*
```html
{% extends "base.html" %}
{% block content %}
<h1>Vrijeme i vremenska prognoza</h1>
<div class="card" style="width: 24rem;">
    <h4 class="card-header">
        Grad
    </h4>
    <div class="card-body">
        <h5 class="card-title">Opis vremenske situacije</h5>
        <div class="card-text">
            <p>Temperatura:  C˙</p>
     </div>
    </div>
</div>

{% endblock %}
```

Prmijenimo i vršnu rutu tako da iscrta ```index.html``` predložak.:
*app.py*
``` python
@app.route('/')
def index():
    return render_template('index.html')
```

Ako ste sve točno postavili i ponovo pokrenuli aplikaciju trebali biste dobiti slijedeći izgled stranice:
![Bootstrap stranica](/assets/c1-bootstrap.png)

Primijetite da koristimo Boostrap 5, te da smo u baznoj stranicu iskoristili macro ```render_nav_item``` za stvaranje elementa menija u zaglavlju stranice. Također ```index.html``` predložak naslijeđuje bazni ```base.html``` predložak preko definicije:

```{% extends "base.html" %}```

```(git checkout c1)```

## Dohvat podataka o vremenu s openweathermap.org
U ovom dijelu ćemo vidjeti kako se povezati na openweathermap.org stranicu, dohvatiti podatke te ih prikazati u našoj aplikaciji.

Prvi korak je da se registriramo na https://openweathermap.org/ stranici i kreiramo tzv. API_KEY koji je nužan da bismo mogli koristiti service koji su nam na raspolaganju. Vaš API trebate aktivirati u API sekciji:

![API_KEY](/assets/c2-api-key.png)

*Napomena: Nakon što kreirate ključ, potrebno je neko vrijeme da se isti aktivira prije nego ga možete koristiti (par desetak minuta).*

Nakon toga možemo koristi dohvat trenutne vremenske situacije prema uputama na stranici https://openweathermap.org/current. Tu možemo vidjeti kako naši pozivit trebaju biti strukturirani, te kakav je razultat koji nam servis vraća.

Za početak provjerimo slanje zahtjeva direktno iz preglednika. Samo zamijenite API_KEY u parametrima URL-a svojim:
```
https://api.openweathermap.org/data/2.5/weather?q=zadar&appid=<API_KEY>
```

Rezultat bi trebala biti trenutna vremenska situacija u željenom gradu:
```json
{
  "coord": {
    "lon": 15.2422,
    "lat": 44.1197
  },
  "weather": [
    {
      "id": 800,
      "main": "Clear",
      "description": "clear sky",
      "icon": "01d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 286.49,
    "feels_like": 285.19,
    "temp_min": 286.49,
    "temp_max": 286.49,
    "pressure": 1009,
    "humidity": 50
  },
  "visibility": 10000,
  "wind": {
    "speed": 2.06,
    "deg": 310
  },
  "clouds": {
    "all": 0
  },
  "dt": 1669026478,
  "sys": {
    "type": 1,
    "id": 6392,
    "country": "HR",
    "sunrise": 1669010517,
    "sunset": 1669044486
  },
  "timezone": 3600,
  "id": 3186952,
  "name": "Zadar",
  "cod": 200
}
```

Zamijenimo našu vršnu rutu slijedećim kodom:
```python
@app.route('/')
def index():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    city = 'zadar'
    parameters = {'q': city, 'appid': OPEN_WEATHER_API_KEY }
    response = requests.get(url, parameters)
    weather = response.json()
    return render_template('index.html', weather = weather)
```

U ovom primjeru tražimo vremensku siutuaciju za grad Zadar, a Json rezultat zahtjeva šaljemo kao ```weather``` objekt u predložak.

Također na vrh datoteke dodajmo kod za dohvat API_KEY-a iz tzv. environment varijable, tako da ga nećemo stavljati sami kod:
```python
import os
import requests
OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')
```

Varijablu postavimo slijedećom naredbom u terminalu:
```
$env:OPEN_WEATHER_API_KEY="VAŠ_OPENWEATHER_API_KEY"
```

Potrebna nam je i Pyhton biblioteka ```requests``` koju koristimo za REST pozive prema vanjskim servisima pa ju instalirajmo:
```
pip install requests
```
Za kraj u ```index.html``` predlošku promijenite sadržaj katice tako da prikazuje dohvaćene podatke iz ```weather``` objekta čija je struktura prikazana u primjeru iznad:

```html
<div class="card" style="width: 24rem;">
    <h4 class="card-header">
        {{weather.name}}
    </h4>
    <div class="card-body">
        <h5 class="card-title">{{weather.weather[0].description}}</h5>
        <div class="card-text">
            <p>Temperatura: {{weather.main.temp}}</p>
            <p>Vlažnost zraka: {{weather.main.humidity}}%</p>
            <p>Tlak: {{weather.main.pressure}} hpa</p>
        </div>
    </div>
</div>
```

Ponovo pokrenite aplikaciju i osvježite stranicu. Rezultat bi trebao biti:
![Zadar](/assets/c2-zadar.png)

Ono što primjećujemo jest da teperatura nije u celzijus stupnjevima već kelvinima, a opis vremenske situacije nije na hrvatskom već engleskom jeziku. Ovo ćemo promijeniti u sljedećem poglavlju.

```(git checkout c2)```

## Postavljanje mjernih jedinica i jezika preko stranice postavki
U ovom poglavlju ćemo kreirati dodatnu stranicu "Postavke", u kojoj ćemo moći upisati grad, te odabrati jezik i mjerne jedinice. Prema Open weather dokumentaciji, to možemo napraviti tako da u zahtjev pošaljemo dva dodatka parametra:
```
&units=metric&lang=hr
```
Stoga ćemo kreirati novu stranicu s formom za odabit ovih postavki, a rezultat ćemo spremiti u korisnikov ```session``` objekt, te ga poslati prilikom sljedećeg poziva.

Najprije u ```base.html``` dodajmo u navigacijski meni link na novu stranicu za postavke:
```
{{ render_nav_item('settings', 'Postavke') }}
```

Kreirajmo klasu za formu postavki novu rutu sa slijedećim kodom:
```python
class SettingsForm(FlaskForm):
    city = StringField('Grad', validators=[DataRequired()])
    lang = SelectField('Jezik', choices=[('hr', 'Hrvatski'), ('en', 'English'), ('de', 'Deutch')], validators=[DataRequired()])
    units = SelectField(choices=[('metric', 'Metric'), ('imperial', 'Imperial')], validators=[DataRequired()])
    submit = SubmitField('Spremi')

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
```

Klasa ```SettingsForm``` opisuje našu formu, te naslijeđuje ```FlaskForm``` što znači da moramo instalirati ```flask-wtf``` komponentu:
```
pip install flask-wtf
```

U ```settings``` ruti spremamo odabrane vrijednosti u ```session``` objekt, te ih i čitamo ako su postavljene.

Da bi ova konfiguracija koda radila dodajmo u import sekciji sve što treba:
```python
from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
```

Slijedeći korak je dodavanje ```settings.html``` predloška:
```html
{% from 'bootstrap5/form.html' import render_form %}
{% extends "base.html" %}
{% block content %}
<h2>Uredite postavke aplikacije</h2>
<div class="row">
    <div class="col-3">
        {{ render_form(form) }}
    </div>
</div>
{% endblock %}
```

Da bismo mogli raditi sa ```session``` objektom treba nam i ```SECRET_KEY```, pa ga dodajmo u ```app.py```:
```python
app.config['SECRET_KEY'] = 'MOJ_TAJNI_KLJUČ'
```

Za kraj još promijenimo vršnu rutu tako da prima parametre iz ```session``` objekta:
```python
@app.route('/')
def index():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    city = session.get('city') if session.get('city') else 'zadar'
    parameters = {'q': city, 'appid': OPEN_WEATHER_API_KEY, 'units':session.get('units'), 'lang':session.get('lang') }
    response = requests.get(url, parameters)
    weather = response.json()
    return render_template('index.html', weather = weather, session = session)
```

Ponovo pokrenite aplikaciju, kliknite link "Postavke", te ispunite i spremite formu:

![Settings](/assets/c3-settings.png)

Kliknite glavnu stranicu i provjerite da li su podaci prikazani u skladu s postavljenim postavkama:

![Settings](/assets/c3-split.png)

```(git checkout c3)```

## Rad s datumskim vrijednostima
U prikaz podataka dodajmo i podatak o danu i satu na koji se mjerene vrijednosti odnose. Taj podatak se nalazi u atributu ```weather.dt```, a koji u podacima ima vrijednost sličnu ```1669026478```. Radi se tzv. POSIX standardu opisa datumskih vrijednosti, a koji predstavlja broj sekundi proteklih od 1.1.1970.

Da bismo datum mogli konvertirati u naš format, iskoristit ćemo ```fromtimestamp``` metodu ```datetime``` modula. Slijedeće korake moramo napraviti:
Dodajmo u ```app.py``` import:
```python
from datetime import datetime
```
Zatim proslijedimo referencu na ```datetime``` u predložak:
```python
return render_template('index.html', weather = weather, session = session, datetime = datetime)
```

U kartici dodajmo prikaz tog podatka:
```html
<p>Datum: {{datetime.fromtimestamp(weather.dt)}}</p>
```
Ovo je i način kako u predložak možemo dodati neku funkciju. Jer u Pythonu, svaka funkcija je ujedno i objekt, te se može prosljeđivati kao argument. 

Dodajmo izlazak i zalazak sunca. Ne trebaju nam niti datum niti sekunde, samo sati i minute, pa koristimo format:
```html
<p>Izlazak sunca: {{datetime.fromtimestamp(weather.sys.sunrise).strftime('%H:%M')}}</p>
<p>Zalazak sunca: {{datetime.fromtimestamp(weather.sys.sunset).strftime('%H:%M')}}</p>
```

Ovo možemo i skratiti. Ne trebamo slati datetime u template. A dodat ćemo svoju filter funkciju:
```python
@app.template_filter('datetime')
def format_datetime(value, format='%d.%m.%Y %H:%M'):
    if format == 'time':
        format='%H:%M'
    return datetime.fromtimestamp(value).strftime(format)
```
Stoga možemo promijeniti format na:
```html
<p>Zalazak sunca: {{weather.sys.sunset | datetime('time')}}</p>
```

```(git checkout c4)```

## Sedmodnevna prognoza vremena
U ovom poglavlju ćemo doddati stranicu s prognozom vremena za sedan dana. U tu svrhu koristit ćemo API opisan na stranici https://openweathermap.org/forecast16

U bazni predložak dodajmo link:
```
{{ render_nav_item('forecast_days', '7-dnevna prognoza') }}
```

Zatim kreirajmo novu rutu:
```python
@app.route('/forecast_days')
def forecast_days():
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily'
    city = session.get('city') if session.get('city') else 'zadar'
    parameters = {'q': city, 'appid': OPEN_WEATHER_API_KEY, 'cnt': '7', 'units': session.get('units'), 'lang': session.get('lang')}
    response = requests.get(url, parameters)
    weather = response.json()
    return render_template('forecast_days.html', weather = weather)
```

Te na kraju i novi predložak :
```html
{% extends 'base.html' %}
{% block content %}
<h1>7-dnevna prognoza</h1>
<table class="table">
<tbody>
    {% for day in weather.list %}
    <tr>
        <td>{{ day.dt | datetime('%A %d.%m')}}</td>
        <td>{{ day.temp.min}} / {{ day.temp.max}}</td>
        <td>{{ day.weather[0].description }} </td>
    </tr>
    {% endfor %}
</tbody>
</table>
{% endblock %}
```

Ako sad pokrenemo aplikaciju i kliknemo na novi link dobit ćemo:
![7-days](/assets/c5-7-days.png)

Primjetimo da nam je temparatura zaokružena na dvije decimale. To želimo promijeniti u cijeli broj, pa stoga u predlošku dodajmo dvija numerička filtera:
```html
<td>{{ day.temp.min | round | int }} / {{ day.temp.max | round | int  }}</td>
```
Najprije vrijednost zaokružujemo, pa pretvaramo u cijeli broj. Sad umjesto ```8.81 / 15.05``` imamo ```9 / 15```.

Slijedeće što ćemo dodati su ikone s vizualnim prikazom vremena. Detalje pogledajte na stranici https://openweathermap.org/weather-conditions.
Dodajte slijedeći dio u predložak kako bi se u popisu prikazale i ikone:
```html
    <td><img src="http://openweathermap.org/img/wn/{{day.weather[0].icon}}.png"></td>
```

Još ćemo promijeniti nazive dana s engleskog jezika na hrvatski. To možemo učiniti na slijedeći način dodavanjem:
```python
import locale
locale.setlocale(locale.LC_ALL, 'hr')
```

Prognoza sad izgleda ovako:
![7-days](/assets/c5-7-days-2.png)

```(git checkout c5)```

## Cacheing
Pošto prilikom svakog poziva, radimo ujedno i poziv prema OpenWeather API servisima, želimo ovaj dio optimizirati, pošto se podaci o vremenu ne mijenjauu često. U tu svrhu koristimo koncept *cacheinga*, koji nam omogućava da na određeno vrijeme neke vrijednosti držimo u privremenoj mmoriji čime aplikacija dobija na performansama.

Najprije intalirajmo ```flask-caching``` komponentu:
```
pip install flask-caching
```

Dodajmo slijedeći kod:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

Između 
```python
@app.route('/')

def index():
```
dodajmo:
```python
@cache.cached(timeout=60)
```
Ovim jednostavnim rješenjem smo zapravo spremili odziv cijele vršne rute na 60 sekundi u privremenu memoriju. Ako primjerice u tu rutu dodamo ispis vremena u konzolu:
```python
print(datetime.now())
```
vidjet ćemo da se ispis vremena pojavljuje tek kad prođe 60 sekundi.

Osim što možemo *cacheirati* view na ovaj način, možemo raditi isto i s drugim uunkcijama i objektima. Detalje možete pronaći na stranici https://flask-caching.readthedocs.io/en/latest/.

## Ostale dorade na aplikaciji
Ova aplikacija ne mora biti gotova i može se proširiti na brojne načine. što možete pokušati i sami. Npr.
* Dodajte i ostale parametre poput brzine i smjera vjetra, vlažnosti, tlaka i sl. što nismo dodali u samu aplikaciju.
* Možete iskoristiti za prikaz prognoze na google maps ili open street maps
* Dodati prognozu za više gradova ili pamtiti gradove koje ste upisivali. Razmislite kako biste prikazali usporednu prognozu za više gradova.
* Dodati satnu prognozu. Vidi: https://openweathermap.org/api/hourly-forecast
* Dodajte Bootswatch temu. Vidi: https://bootstrap-flask.readthedocs.io/en/latest/advanced/#bootswatch-themes

## Upute za pokretanje aplikacije
* git clone https://github.com/nikovrdoljak/flask-prognoza-radionica
* cd flask-prognoza-radionica
* py -m venv venv
* \venv\Scripts\Activate.ps1
* pip install -r requirements.txt
* $env:OPEN_WEATHER_API_KEY="VAŠ_OPENWEATHER_API_KEY"
* $env:FLASK_DEBUG="1"
* flask run