from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Mago'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', user=user, posts=posts)

@app.route('/NuovoArticolo')
def NuovoArticolo():
    return render_template('NuovoArticolo.html', title='CREAZIONE ARTICOLO - CILINDRO')

@app.route('/NuovoComponente')
def NuovoComponente():
    return render_template('NuovoComponente.html', title='CREAZIONE COMPONENTE SINGOLO PER PRODUZIONE')

@app.route('/NuovoImpegno')
def NuovoImpegno():
    return render_template('NuovoImpegno.html', title='CREAZIONE IMPEGNO')

@app.route('/About')
def About():
    return render_template('About.html')
