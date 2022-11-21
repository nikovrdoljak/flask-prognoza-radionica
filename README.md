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

Ono što primjećujemo jest da teperatura nije u celzijus stupnjevima već fahrenheit, a opis vremenske situacije nije na hrvatskom već engleskom jeziku. Ovo ćemo promijeniti u sljedećem poglavlju.

```(git checkout c1)```


