from flask import render_template, flash, redirect, request
import ast
import json
from app import app
from app import dbFunction as f
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    '''
    #stampa = f.getIDarticolo("1AAA00100")
    #creo file di INSERIMENTO
    test2 = '{"newArticolo":{"t_art":[{"cod_art":"1ABC00100","desc_art":"cilindro","cli_art":"Asd","cod_cli_art":"123456","id_art":"10"}],"t_comp":[{"cod_comp":"1ABC00102","desc_comp":"camicia","dim_comp":"100","mat_comp":"S355","qt_comp":"1","id_comp":"10"}]}}'
    test5 = ('{"newImpegno": {"t_imp":[{"cod_imp":"123","cliente":"asd123","cod_ord_cli":"111","data_ord":"2019/12/04","id_imp":"3"}],'
            '"t_art":[{"cod_art":"1ABC00100","desc_art":"cilindro","qt_art":"2","data_cons_art":"2019/12/05","id_riga_imp":"1"}, '
            '{"cod_art":"1ABC00200","desc_art":"cilindro2","qt_art":"1","data_cons_art":"2019/12/06","id_riga_imp":"2"}], '
            '"t_comp":[{"cod_comp":"1ABC00102","desc_comp":"camicia","qt_comp":"100","data_cons_comp":"2019/12/07","id_riga_imp_comp":"1"}, '
            '{"cod_comp":"1ABC00110","desc_comp":"stelo","qt_comp":"50","data_cons_comp":"2019/12/08","id_riga_imp_comp":"2"}]}}')

    stampa = f.newImpegno(ast.literal_eval(test5))
    '''
    stampa = f.search_comp("1AAA00102")
    user = {'username': 'Mago'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
<<<<<<< HEAD
            'body': 'stampa'
        }
=======
            'body': stampa
        },
>>>>>>> ddc675772c4d78bd7794cc937db509f3f49d652a
    ]

    return render_template('index.html', user=user, posts=posts)

@app.route('/NuovoArticolo', methods=['GET', 'POST'])
def NuovoArticolo():
    if request.method == 'POST':
        print (request.form['newArticolo'])
        #print (request.form['first_call'])
        #data = request.form[0]
        #dic = ast.literal_eval(data)
        #print (dic)
        #print (request.is_json)
        #content = request.get_json()
        #print (content)
        arr = {'first_call':{'list_art':['1ASD00100','1ASD00200'],'list_comp':['1ASD00110','1ASD00103','1ASD00201']}}

        return json.dumps(arr)
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
