from flask import render_template, flash, redirect, request, jsonify
import ast
from app import app
#from app import dbFunction as f
from app.forms import LoginForm
import ast

@app.route('/')
@app.route('/index')
def index():
    #stampa = f.getIDarticolo("1AAA00100")
    #creo file di INSERIMENTO
    #test2 = '{"newArticolo":{"t_art":[{"cod_art":"1ABC00100","desc_art":"cilindro","cli_art":"Asd","cod_cli_art":"123456","id_art":"1"}],"t_comp":[{"cod_comp":"1ABC00102","desc_comp":"camicia","dim_comp":"100","mat_comp":"S355","qt_comp":"1","id_comp":"1"}]}}'
    #f.newArticolo(ast.literal_eval(test2))

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
    print('func')
    if request.method == 'POST':
        data = request.form['new']
        dic = ast.literal_eval(data)
        print (dic['asd'])
        #print (request.is_json)
        #content = request.get_json()
        #print (content)
        return ('ok')
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
