from flask import render_template, flash, redirect, request
import ast
try:
    import simplejson as json
except ImportError:
    import json
from app import app
from app import dbFunction as f #f verrà usata per richiamare le funzioni in dbFunction
from app.forms import LoginForm
import pprint


@app.route('/')
@app.route('/index')

def index():
    test4 = {"newComponente":{"t_comp":[{"cod_comp":"1ABC00110","desc_comp":"stelo 1","dim_comp":"50","mat_comp":"C45", "id_comp":"36"}, {"cod_comp":"1ABC00112","desc_comp":"stelo sec","dim_comp":"50","mat_comp":"C45", "id_comp":"37"}]}}
    test2 = {"newArticolo":{"t_art":[{"cod_art":"1ABC00100","desc_art":"cilindro","cli_art":"Asd","cod_cli_art":"123456","id_art":"1"}],"t_comp":[{"cod_comp":"1ABC00102","desc_comp":"camicia","dim_comp":"100","mat_comp":"S355","qt_comp":"3","id_comp":"1"},{"cod_comp":"1ABC00110","desc_comp":"stelo","dim_comp":"50","mat_comp":"C45","qt_comp":"4","id_comp":"2"}]}}

    test5 = {"newImpegno":{"t_imp":[{"cod_imp":"123","cliente":"asd","cod_ord_cli":"111","data_ord":"2019-12-04","id_imp":"1"}], "t_art":[{"cod_art":"1ABC00100","desc_art":"cilindro","qt_art":"3","data_cons_art":"2019-12-05","id_riga_imp":"1"}], "t_comp":[{"cod_comp":"1ABC00102","desc_comp":"camicia","qt_comp":"100","data_cons_comp":"2019-12-07","id_riga_imp_comp":"1"}, {"cod_comp":"1ABC00110","desc_comp":"stelo","qt_comp":"50","data_cons_comp":"2019-12-08","id_riga_imp_comp":"2"}]}}

    stampa = f.first_call()

    user = {'username': 'Mago'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': stampa
        }
    ]

    return render_template('index.html', user=user, posts=posts)

@app.route('/NuovoArticolo', methods=['GET', 'POST'])
def NuovoArticolo():
    if request.method == 'POST':    #Aspetta una richiesta POST dal client
        content = request.get_data()    #Riceve una stringa
        formatted_data = json.loads(content)    #Trasforma la stringa in dizionario pythons
        print('Dati ricevuti:')
        pprint.pprint(formatted_data)
        print('Dati filtrati:')
        print(formatted_data['newArticolo']['t_art'][0]['cod_art'])
        risposta = f.newArticolo(formatted_data)
        #arr = {'first_call':{'list_art':['1ASD00100','1ASD00200'],'list_comp':['1ASD00110','1ASD00103','1ASD00201']}}
        #return json.dumps(content)
        return risposta  #risponde al client
    else:
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
