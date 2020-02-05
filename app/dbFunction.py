import mysql.connector
import datetime

'''
FUNZIONI RICHIAMATE DA PAGINE ESTERNE
'''
#FUNZIONE CHE SCARICA I DATI SALVATI
def first_call():
    #array impegni
    impegni = getCodImpegni()
    #array componenti
    componenti = getCodComponenti()
    #array articoli
    articoli = getCodArticoli()
    #concatenazione array
    arrCodici = {"list_imp": impegni, "list_art": articoli, "list_comp": componenti}
    arrRisultato = {"first_call": arrCodici}
    return arrRisultato

#inserimento nuovo componente
def newComponente(assieme):
    #INSERISCO I COMPONENTI SINGOLI
    componenti = assieme
    #idComp = setCompSingolo(componenti)
    #return assieme

#inserimento nuovo articolo
def newArticolo(assieme):
    #CREAZIONE NUOVO ARTICOLO - CILINDRO
    #echo "<br>REPORT NEW ARTICOLO:<br>";
    articolo = assieme["newArticolo"]["t_art"]
    componenti = assieme["newArticolo"]["t_comp"]
    #setto l' articolo
    idArt = setArticolo(articolo[0])

    #salvo i componenti e li vado a collegare all' articolo
    #setComponenteInArticolo(codArticolo, componenti)
    return idArt

#inserimento nuovo impegno
def newImpegno(assieme):
    #separo le componenti principali
    impegno = assieme["newImpegno"]["t_imp"]
    articoli = assieme["newImpegno"]["t_art"]
    componenti = assieme["newImpegno"]["t_comp"]
    #1-> CREO LA RIGA IMPEGNO
    id_imp = setImpegno(impegno[0])
    #2-> CICLO GLI ARTICOLI-COMPONENTI DA INSERIRE NELL' IMPEGNO
    #if($id_imp):
     # #se l' impegno è stato inserito correttamente
      ##vado ad inserire le righe articolo
      #$varDB->setArticoloInImpegno($articoli, $id_imp);
      ##vado ad inserire le righe componente
      #$varDB->setComponenteInImpegno($componenti, $id_imp);
    return id_imp

#ricerca componente gia inserito
def search_comp(ricercaComp):
    #RICERCO IL CODICE COMPONENTE ED INVIO I DATI
    componente = getComponente(ricercaComp)
    #creo array di risposta
    comp = {"t_comp": componente}
    risposta = {"search_comp": comp}
    #consegno il pacco
    return risposta

#ricerca articolo gia inserito con i relativi componenti
def search_art(ricercaArt):
    #RICERCO IL CODICE ARTICOLO ED I DATI
    articolo = getArticolo(ricercaArt)
    #ricerco i comp contenuti nell' articolo
    componenti = getCompInArticolo(articolo["id_art"])
    #creo array di risposta
    artComp = {"t_art": articolo, "t_comp": componenti}
    risposta = {"search_art": artComp}
    #consegno il pacco
    return risposta

'''
FUNZIONI CHE RIUTILIZZO IN QUESTA PAGINA
'''
#funzione per la connessione al database
def connessione():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="db_progresso"
    )
    return mydb;

#RICERCA COMPONENTE INSERITO
def getComponente(ricComponente):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #istruzione query string -> seleziono il componente ricercato
    mioDB.execute("SELECT * FROM componente WHERE cod_comp='" + ricComponente + "'")
    row = mioDB.fetchone()
    if row:
        #salvo i dati componente
        arrayComp = {"id_comp": row["id_comp"], "cod_comp": row["cod_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"]}
    else:
        arrayComp = {"id_comp": "", "cod_comp": "","desc_comp": "","dim_comp": "","mat_comp": ""}
    mydb.close()
    return arrayComp

#RICERCA ARTICOLO INSERITO
def getArticolo(ricArticolo):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #istruzione query string -> seleziono articolo ricercato
    mioDB.execute("SELECT * FROM articolo WHERE cod_art='" + ricArticolo + "'")
    row = mioDB.fetchone()
    if row:
        #salvo i dati articolo
        arrayArt = {"id_art": row["id_art"], "cod_art": row["cod_art"],"desc_art": row["desc_art"],"cli_art": row["cli_art"],"cod_cli_art": row["cod_cli_art"]}
    else:
        arrayArt = {"id_art": "", "cod_art": "","desc_art": "","cli_art": "","cod_cli_art": ""}
    mydb.close()
    return arrayArt

#RICERCA I COMPONENTI INSERITI IN UN DATO ID_ARTICOLO
def getCompInArticolo(ric_id_articolo):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #seleziono gli id_componenti dell' articolo ricercato
    mioDB.execute("SELECT * FROM articolo_componenti INNER JOIN componente ON componente.ID_comp=articolo_componenti.ID_comp  WHERE articolo_componenti.id_art = '" + str(ric_id_articolo) + "'")
    risultato = mioDB.fetchall()
    #variabili array COMPONENTI
    arr_Componenti = []
    #ciclo tutti i componenti
    flag = False
    for row in risultato:
        flag = True
        arr_Componenti.append({"id_comp": row["id_comp"], "cod_comp": row["cod_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"],"qt_comp": row["qt_comp"]})
    #se non aveva componenti passo stringa vuota
    if flag == False:
        arr_Componenti.append({"id_comp": "", "cod_comp": "","desc_comp": "","dim_comp": "","mat_comp": "","qt_comp": ""})
    #chiusura
    mydb.close()
    return arr_Componenti

#RICEVO TUTTI I CODICI IMPEGNO
def getCodImpegni():
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #istruzione query string -> seleziono tutti gli impegni inseriti
    mioDB.execute("SELECT cod_imp FROM impegno")
    result = mioDB.fetchall()
    #ricevo tutte le righe
    flag = False
    arr_Impegno = []
    for x in result:
        #salvo l' array codici impegni
        arr_Impegno.append(x["cod_imp"])
        flag = True
    #se non sono presenti righe, passo casella VUOTA
    if flag == False:
        arr_Impegno.append("")
    #chiudo la connessione al DB e passo i dati
    mydb.close()
    return arr_Impegno

#RICEVO TUTTI I CODICI COMPONENTI
def getCodComponenti():
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #istruzione query string -> seleziono tutti i componenti inseriti
    mioDB.execute("SELECT cod_comp FROM componente")
    result = mioDB.fetchall()
    #ricevo tutte le righe
    flag = False
    arr_Componente = []
    for x in result:
        #salvo l' array codici componente
        arr_Componente.append(x["cod_comp"])
        flag = True
    #se non sono presenti righe, passo casella VUOTA
    if flag == False:
        arr_Componente.append("")
    #chiudo la connessione al DB e passo i dati
    mydb.close()
    return arr_Componente

#RICEVO TUTTI I CODICI ARTICOLI
def getCodArticoli():
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #istruzione query string -> seleziono tutti gli articoli inseriti
    mioDB.execute("SELECT cod_art FROM articolo")
    result = mioDB.fetchall()
    #ricevo tutte le righe
    flag = False
    arr_Articolo = []
    for x in result:
        #salvo l' array codici articoli
        arr_Articolo.append(x["cod_art"])
        flag = True
    #se non sono presenti righe, passo casella VUOTA
    if flag == False:
        arr_Articolo.append("")
    #chiudo la connessione al DB e passo i dati
    mydb.close()
    return arr_Articolo

#ricerco ID ARTICOLO
def getIDarticolo(art):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #istruzione query string
    mioDB.execute("SELECT id_art FROM articolo WHERE cod_art='" + art + "';")
    result = mioDB.fetchall()
    #controllo se articolo già salvato
    for x in result:
      #articolo gia inserito -> salvo i dati articolo
      idart = x["id_art"]
      mydb.close()
      return idart
    #non esiste
    mydb.close()
    return ""

#ricerco ID COMPONENTE
def getIDcomponente(comp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #istruzione query string
    mioDB.execute("SELECT id_comp FROM componente WHERE cod_comp='" + comp + "';")
    result = mioDB.fetchall()
    #controllo se componente già salvato
    '''
    MODIFICARE CON FETCHONE
    '''
    for x in result:
      #componente gia inserito -> salvo i dati componente
      idcomp = x["id_comp"]
      mydb.close()
      return idcomp
    #non esiste
    mydb.close()
    return ""

#SALVO I COMPONENTI SINGOLI AL DI FUORI DELL' ASSIEME
def setCompSingolo(codComponenti):
    #ricevo un array di componenti, devo ciclarli ed inserirli uno alla volta
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #variabili per la formattazione delle DATE da salvare
    now = datetime.datetime.now()
    dataOra = now.strftime("%Y/%m/%d") #("Y-m-d") data odierna
    #ciclo tutti i componenti
    for componente in codComponenti:
        #ciclo tutti i componenti
        codComp = componente["cod_comp"]
        desc = componente["desc_comp"]
        dim = componente["dim_comp"]
        mat = componente["mat_comp"]
        #query per inserire il componente nella tabella componenti
        sql = "INSERT INTO componente (cod_comp, desc_comp, dim_comp, mat_comp, pos_comp, data_comp) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE desc_comp = %s, dim_comp = %s, mat_comp = %s, pos_comp = %s"
        val = (codComp, desc, dim, mat, "0", dataOra, desc, dim, mat, "0")
        mioDB.execute(sql, val)
        mydb.commit()
        #prendo l' indice di componente
        idComp = mioDB.lastrowid
        print("1 comp inserted, ID:", idComp)
    #disconnessione
    mydb.close()
    return idComp

#SETTO UN NUOVO ARTICOLO
def setArticolo(articolo):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #variabili per la formattazione delle DATE da salvare
    now = datetime.datetime.now()
    dataOra = now.strftime("%Y/%m/%d") #("Y-m-d") data odierna
    #variabili del cilindro per settarlo
    codArt = articolo["cod_art"]
    desc = articolo["desc_art"]
    cli = articolo["cli_art"]
    codCli = articolo["cod_cli_art"]
    #inserisco la riga articolo oppure aggiorno
    sql = "INSERT INTO articolo (cod_art, desc_art, cli_art, cod_cli_art, kit_art, data_art) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE desc_art = %s, cli_art = %s, cod_cli_art = %s, kit_art = %s"
    val = (codArt, desc, cli, codCli, "0", dataOra, desc, cli, codCli, "0")
    mioDB.execute(sql, val)
    id_art = mioDB.lastrowid
    mydb.commit()
    mydb.close()
    #restituisco l' ID dell'articolo appena salvato
    return id_art

#INSERISCO I COMPONENTI NELLA TABELLA DELL' ARTICOLO
def setComponenteInArticolo(codArt, codComponenti):
    flag_anag_comp = 0       #"" -> nuovo comp
                             #num -> anagrafica già inserita
    #variabili per la formattazione delle DATE da salvare
    now = datetime.datetime.now()
    dataOra = now.strftime("%Y/%m/%d") #("Y-m-d") data odierna
    #prendo l' indice di articolo
    idArt = getIDarticolo(codArt)
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #ciclo tutti i componenti
    cont = 0
    for componente in codComponenti:
        #echo "<br>".$cont."<br>";
        #salvo variabili del componente
        codComp = componente["cod_comp"]
        desc = componente["desc_comp"]
        dim = componente["dim_comp"]
        mat = componente["mat_comp"]
        qt = componente["qt_comp"]
        #controllo se l' anagrafica componente esiste già
        flag_anag_comp = getIDcomponente(codComp)
        if flag_anag_comp == "":
            #salvo il codice componente nell' anagrafica componente
            #inserisco la nuova riga componente
            sql = "INSERT INTO componente (cod_comp, desc_comp, dim_comp, mat_comp, pos_comp, data_comp) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (codComp, desc, dim, mat, "0", dataOra)
            mioDB.execute(sql, val)
            mydb.commit()
            #prendo l' indice di componente
            idComp = mioDB.lastrowid
            print("1 comp inserted, ID:", idComp)
        else:
            idComp = flag_anag_comp
        #salvo la riga nella tabella articolo_componenti
        sql = "INSERT INTO articolo_componenti (id_art, id_comp, qt_comp) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE qt_comp = %s"
        val = (idArt, idComp, qt, qt)
        print(sql, val)
        mioDB.execute(sql, val)
        idArtIns = mioDB.lastrowid
        print("1 art inserted, ID:", idArtIns)
        #incremento il contatore
        cont = cont + 1
        #disconnessione
        mydb.close()

#CREO LA RIGA IMPEGNO - DA COLLAUDARE!!!!!!
def setImpegno(assImp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #variabili per la formattazione delle DATE da salvare
    now = datetime.datetime.now()
    dataOra = now.strftime("%Y/%m/%d") #("Y-m-d") data odierna
    #inserisco la riga nuovo impegno
    #query per inserire il componente nella tabella componenti
    sql = "INSERT INTO impegno (cod_imp, cliente, cod_ord_cli, data_ord, data_comp) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE cliente = %s, cod_ord_cli = %s, data_ord = %s"
    val = (assImp["cod_imp"], assImp["cliente"], assImp["cod_ord_cli"], assImp["data_ord"], dataOra, assImp["cliente"], assImp["cod_ord_cli"], assImp["data_ord"])
    #provo ad eseguire l' inserimento
    mioDB.execute(sql, val)
    if mioDB.lastrowid > 0:
        #nuovo inserimento
        #prendo l' indice di componente
        idImp = mioDB.lastrowid
    else:
        #impegno gia inserito
        sql = "SELECT id_imp FROM impegno WHERE cod_imp='" + assImp["cod_imp"] + "';"
        mioDB.execute(sql)
        result = mioDB.fetchall()
        #MODIFICARE CON LA FUNZION FETCHONE
        for x in result:
          #articolo gia inserito -> salvo i dati articolo
          idImp = x["id_imp"]
    mydb.commit()
    #disconnessione
    mydb.close()
    return idImp
