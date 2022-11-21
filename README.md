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