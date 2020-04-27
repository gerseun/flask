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

#first = '{"firstCall":{"list_imp":["123","321","145","167"],"list_art":["1ABC00100","1ABC00200","1BCA00100","1BCA00200"],"list_comp":["1ABC00102","1ABC00110","1ABC00201","1BCA00120","1BCA00230"]}}'

@app.route('/')
@app.route('/index')

def index():
    test4 = {"newComponente":{"t_comp":[{"cod_comp":"1ABC00110","desc_comp":"stelo 1","dim_comp":"50","mat_comp":"C45", "id_comp":"36"}, {"cod_comp":"1ABC00112","desc_comp":"stelo sec","dim_comp":"50","mat_comp":"C45", "id_comp":"37"}]}}
    test2 = {"newArticolo":{"t_art":[{"cod_art":"1ABC00100","desc_art":"cilindro","cli_art":"Asd","cod_cli_art":"123456","id_art":"1"}],"t_comp":[{"cod_comp":"1ABC00102","desc_comp":"camicia","dim_comp":"100","mat_comp":"S355","qt_comp":"3","id_comp":"1"},{"cod_comp":"1ABC00110","desc_comp":"stelo","dim_comp":"50","mat_comp":"C45","qt_comp":"4","id_comp":"2"}]}}

    test5 = {"newImpegno":{"t_imp":[{"cod_imp":"123","cliente":"asd","cod_ord_cli":"111","data_ord":"2019-12-04","id_imp":"1"}], "t_art":[{"cod_art":"1ABC00100","desc_art":"cilindro","qt_art":"3","data_cons_art":"2019-12-05","id_riga_imp":"1"}], "t_comp":[{"cod_comp":"1ABC00102","desc_comp":"camicia","qt_comp":"100","data_cons_comp":"2019-12-07","id_riga_imp_comp":"1"}, {"cod_comp":"1ABC00110","desc_comp":"stelo","qt_comp":"50","data_cons_comp":"2019-12-08","id_riga_imp_comp":"2"}]}}

    pagina = "home"
    stampa = f.search_imp("home","2/20")
    #stampa = 'asd'

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
        #print('Dati filtrati newArticolo:')
        #print(formatted_data['newArticolo']['t_art'][0]['cod_art'])
        risposta = 'Risposta default'
        if 'newArticolo' in formatted_data:
            risposta = f.newArticolo(formatted_data)
            #risposta = 'ok'
        if 'firstCall' in formatted_data:
            risposta = json.dumps(f.first_call())
            #risposta = first
        if 'newArticolo_search_comp' in formatted_data:
            print(formatted_data['newArticolo_search_comp'])
            risposta1 = f.search_comp(formatted_data['newArticolo_search_comp'])
            risposta = json.dumps(risposta1)
            print(risposta)
            #risposta = ""
        if 'newArticolo_search_art' in formatted_data:
            risposta = ""
        return risposta  #risponde al client
    else:
        return render_template('NuovoArticolo.html', title='CREAZIONE ARTICOLO - CILINDRO')

@app.route('/NuovoComponente', methods=['GET', 'POST'])
def NuovoComponente():
    if request.method == 'POST':    #Aspetta una richiesta POST dal client
        content = request.get_data()    #Riceve una stringa
        formatted_data = json.loads(content)    #Trasforma la stringa in dizionario pythons
        print('Dati ricevuti:')
        pprint.pprint(formatted_data)
        print('Dati filtrati newComponente:')
        print(formatted_data['newComponente']['t_comp'][0]['cod_comp'])
        risposta = f.newComponente(formatted_data)
        #risposta = 'ok'
        return risposta  #risponde al client
    else:
        return render_template('NuovoComponente.html', title='CREAZIONE COMPONENTE SINGOLO PER PRODUZIONE')

@app.route('/NuovoImpegno', methods=['GET', 'POST'])
def NuovoImpegno():
    return render_template('NuovoImpegno.html', title='CREAZIONE IMPEGNO')

@app.route('/About')
def About():
    if request.method == 'POST':    #Aspetta una richiesta POST dal client
        content = request.get_data()    #Riceve una stringa
        formatted_data = json.loads(content)    #Trasforma la stringa in dizionario pythons
        print('Dati ricevuti:')
        pprint.pprint(formatted_data)
        #print('Dati filtrati newComponente:')
        #print(formatted_data['newComponente']['t_comp'][0]['cod_comp'])
        #risposta = f.newComponente(formatted_data)
        risposta = 'ok'
        return risposta  #risponde al client
    else:
        return render_template('NuovoImpegno.html', title='CREAZIONE COMPONENTE SINGOLO PER PRODUZIONE')

@app.route('/ListaTaglio')
def ListaTaglio():
    if request.method == 'POST':    #Aspetta una richiesta POST dal client
        content = request.get_data()    #Riceve una stringa
        formatted_data = json.loads(content)    #Trasforma la stringa in dizionario pythons
        print('Dati ricevuti:')
        pprint.pprint(formatted_data)
        risposta = 'ok'
        return risposta  #risponde al client
    else:
        return render_template('ListaTaglio.html', title='CREAZIONE COMPONENTE SINGOLO PER PRODUZIONE')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':    #Aspetta una richiesta POST dal client
        content = request.get_data()    #Riceve una stringa
        formatted_data = json.loads(content)    #Trasforma la stringa in dizionario pythons
        print('Dati ricevuti:')
        pprint.pprint(formatted_data)
        if formatted_data['azione'] == 'first_call':
            risposta = json.dumps(f.first_call(formatted_data['pagina']))
        if (formatted_data['azione'] == 'search_art') and (formatted_data['pagina'] == 'newArticolo'):
            risposta = json.dumps(f.search_art(formatted_data['pagina'], formatted_data['messaggio']))
        if (formatted_data['azione'] == 'search_comp') and (formatted_data['pagina'] == 'newArticolo'):
            risposta = json.dumps(f.search_comp(formatted_data['pagina'], formatted_data['messaggio']))

        if (formatted_data['azione'] == 'search_comp') and (formatted_data['pagina'] == 'newComponente'):
            risposta = json.dumps(f.search_comp(formatted_data['pagina'], formatted_data['messaggio']))

        if (formatted_data['azione'] == 'search_imp') and (formatted_data['pagina'] == 'newImpegno'):
            risposta = json.dumps(f.search_imp(formatted_data['pagina'], formatted_data['messaggio']))
        if (formatted_data['azione'] == 'search_art') and (formatted_data['pagina'] == 'newImpegno'):
            risposta = json.dumps(f.search_art(formatted_data['pagina'], formatted_data['messaggio']))
        if (formatted_data['azione'] == 'search_comp') and (formatted_data['pagina'] == 'newImpegno'):
            risposta = json.dumps(f.search_comp(formatted_data['pagina'], formatted_data['messaggio']))

        if (formatted_data['azione'] == 'ins_nuovo') and (formatted_data['pagina'] == 'newArticolo'):
            risposta = f.newArticolo(formatted_data['messaggio'])
        if (formatted_data['azione'] == 'ins_nuovo') and (formatted_data['pagina'] == 'newComponente'):
            risposta = f.newComponente(formatted_data['messaggio'])
        if (formatted_data['azione'] == 'ins_nuovo') and (formatted_data['pagina'] == 'newImpegno'):
            risposta = f.newImpegno(formatted_data['messaggio'])

        if (formatted_data['azione'] == 'search_imp') and (formatted_data['pagina'] == 'listaTaglio'):
            risposta = json.dumps(f.search_imp(formatted_data['pagina'], formatted_data['messaggio']))

        if (formatted_data['azione'] == 'search_imp_lt') and (formatted_data['pagina'] == 'listaTaglio'):
            risposta = json.dumps(f.search_imp(formatted_data['pagina'], formatted_data['messaggio']))
        if (formatted_data['azione'] == 'search_art') and (formatted_data['pagina'] == 'listaTaglio'):
            risposta = json.dumps(f.search_art(formatted_data['pagina'], formatted_data['messaggio']))
        if (formatted_data['azione'] == 'search_comp') and (formatted_data['pagina'] == 'listaTaglio'):
            risposta = json.dumps(f.search_comp(formatted_data['pagina'], formatted_data['messaggio']))

        #risposta = 'ok'
        return risposta
