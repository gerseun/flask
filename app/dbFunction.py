import mysql.connector
import datetime

'''
FUNZIONI RICHIAMATE DA PAGINE ESTERNE
'''
#FUNZIONE CHE SCARICA I DATI SALVATI
def first_call(namePage):
    #array impegni
    impegni = getCodImpegni()
    #array componenti
    componenti = getCodComponenti()
    #array articoli
    articoli = getCodArticoli()
    #concatenazione array
    arrCodici = {"list_imp": impegni, "list_art": articoli, "list_comp": componenti}
    arrRisultato = {"pagina": namePage,"azione": "first_call" , "messaggio": arrCodici}
    return arrRisultato

#inserimento nuovo componente
def newComponente(assieme):
    #INSERISCO I COMPONENTI SINGOLI / IL COMPONENTE SINGOLO
    componenti = assieme["t_comp"]
    idComp = setComponenti(componenti)
    return idComp

#inserimento nuovo articolo
def newArticolo(assieme):
    #CREAZIONE NUOVO ARTICOLO - CILINDRO
    #echo "<br>REPORT NEW ARTICOLO:<br>";
    articolo = assieme["t_art"][0]
    componenti = assieme["t_comp"]
    #setto l' articolo
    idArt = setArticolo(articolo)
    #setto i componenti
    idComp = setComponenti(componenti)
    #salvo i componenti e li vado a collegare all' articolo
    setComponenteInArticolo(idArt, idComp, componenti)
    #risposta
    risposta = str(idArt) + " - " + str(idComp)
    return risposta

#inserimento nuovo impegno
def newImpegno(assieme):
    #separo le componenti principali
    impegno = assieme["t_imp"][0]
    articoli = assieme["t_art"]
    #componenti = assieme["newImpegno"]["t_comp"]
    #1-> CREO LA RIGA IMPEGNO
    id_imp = setImpegno(impegno)
    #2-> CICLO GLI ARTICOLI-COMPONENTI DA INSERIRE NELL' IMPEGNO
    id_riga_imp = setArticoloInImpegno(articoli, id_imp)
    #vado ad inserire le righe componente
    #$varDB->setComponenteInImpegno($componenti, $id_imp);
    return id_riga_imp

#ricerca componente gia inserito
def search_comp(namePage, ricercaComp):
    #RICERCO IL CODICE COMPONENTE ED INVIO I DATI
    componente = getComponente(ricercaComp)
    #creo array di risposta
    comp = {"t_comp": [componente]}
    risposta = {"pagina": namePage,"azione": "search_comp" , "messaggio": comp}
    #consegno il pacco
    return risposta

#ricerca articolo gia inserito con i relativi componenti
def search_art(namePage, ricercaArt):
    #RICERCO IL CODICE ARTICOLO ED I DATI
    articolo = getArticolo(ricercaArt)
    #ricerco i comp contenuti nell' articolo
    componenti = getCompInArticolo(articolo["id_art"])
    #creo array di risposta
    artComp = {"t_art": [articolo], "t_comp": componenti}
    risposta = {"pagina": namePage,"azione": "search_art" , "messaggio": artComp}
    #consegno il pacco
    return risposta

#ricerca impegno gia inserito con i relativi articolo e/o componenti
def search_imp(namePage, ricercaImp):
    #RICERCO IL CODICE IMPEGNO ED I DATI
    impegno = getImpegno(ricercaImp)
    #ricerco i comp contenuti nell' impegno
    componenti = getCompInImpegno(impegno["id_imp"])
    #ricerco gli articoli contenuti nell' impegno
    articoli = getArtInImpegno(impegno["id_imp"])
    #creo array di risposta
    impArtComp = {"t_imp": [impegno], "t_art": articoli, "t_comp": componenti}
    risposta = {"pagina": namePage,"azione": "search_imp" , "messaggio": impArtComp}
    #consegno il pacco
    return risposta



'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
FUNZIONI CHE RIUTILIZZO IN QUESTA PAGINA
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
#funzione per la connessione al database
def connessione():
    mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="LsRISZ5PFW",
    passwd="K6Qv7xehdj",
    database="LsRISZ5PFW"
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

#RICERCA IMPEGNO INSERITO
def getImpegno(ricImpegno):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #istruzione query string -> seleziono impegno ricercato
    mioDB.execute("SELECT * FROM impegno WHERE cod_imp='" + ricImpegno + "'")
    row = mioDB.fetchone()
    if row:
        #salvo i dati articolo
        arrayImp = {"id_imp": row["id_imp"], "cod_imp": row["cod_imp"],"cliente": row["cliente"],"cod_ord_cli": row["cod_ord_cli"],"data_ord": row["data_ord"]}
    else:
        arrayImp = {"id_imp": "", "cod_imp": "","cliente": "","cod_ord_cli": "","data_ord": ""}
    mydb.close()
    return arrayImp

#RICERCA I COMPONENTI INSERITI IN UN DATO ID_ARTICOLO
def getCompInArticolo(ric_id_articolo):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #seleziono gli id_componenti dell' articolo ricercato
    mioDB.execute("SELECT * FROM articolo_componenti INNER JOIN componente ON componente.ID_comp=articolo_componenti.ID_comp  WHERE articolo_componenti.id_art = '" + str(ric_id_articolo) + "'")
    risultato = mioDB.fetchall()
    print(risultato)
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

#RICERCA I COMPONENTI INSERITI IN UN DATO ID_ARTICOLO
def getCompInImpegno(ric_id_impegno):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #seleziono gli id_componenti dell' impegno ricercato
    mioDB.execute("SELECT * FROM riga_imp_comp INNER JOIN componente ON riga_imp_comp.ID_comp=componente.ID_comp  WHERE riga_imp_comp.ID_imp = '" + str(ric_id_impegno) + "'")
    risultato = mioDB.fetchall()
    #variabili array COMPONENTI
    arr_Componenti = []
    #ciclo tutti i componenti
    flag = False
    for row in risultato:
        flag = True
        arr_Componenti.append({"id_riga_imp_comp": row["id_riga_imp_comp"], "cod_comp": row["cod_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"qt_comp": row["qt_comp"],"data_cons_comp": row["data_cons_comp"]})
    #se non aveva componenti passo stringa vuota
    if flag == False:
        arr_Componenti.append({"id_riga_imp_comp": "", "cod_comp": "","desc_comp": "","dim_comp": "","qt_comp": "","data_cons_comp": ""})
    #chiusura
    mydb.close()
    return arr_Componenti

#RICERCA I COMPONENTI INSERITI IN UN DATO ID_ARTICOLO
def getArtInImpegno(ric_id_impegno):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #seleziono gli id_riga_imp dell' impegno ricercato
    mioDB.execute("SELECT * FROM riga_imp INNER JOIN articolo ON riga_imp.ID_art=articolo.ID_art  WHERE riga_imp.ID_imp = '" + str(ric_id_impegno) + "' ORDER BY riga_imp.ID_riga_imp ASC")
    risultato = mioDB.fetchall()
    #variabili array COMPONENTI
    arr_Articoli = []
    #ciclo tutti i componenti
    flag = False
    for row in risultato:
        flag = True
        arr_Articoli.append({"id_riga_imp": row["id_riga_imp"], "cod_art": row["cod_art"],"id_art": row["id_art"],"desc_art": row["desc_art"],"qt_art": row["qt_art"],"data_cons_art": row["data_cons_art"]})
    #se non aveva componenti passo stringa vuota
    if flag == False:
        arr_Articoli.append({"id_riga_imp": "", "cod_art": "","id_art": "","desc_art": "","qt_art": "","data_cons_art": ""})
    #chiusura
    mydb.close()
    return arr_Articoli

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
def setComponenti(codComponenti):
    #ricevo un array di componenti, devo ciclarli ed inserirli uno alla volta
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #variabili per la formattazione delle DATE da salvare
    now = datetime.datetime.now()
    dataOra = now.strftime("%Y/%m/%d") #("Y-m-d") data odierna
    #id componenti inseriti
    idComp = []
    contComp = 0
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
        if mioDB.lastrowid == 0:
            #vecchio componente, prendo l' ID
            idComp.append(componente["id_comp"])
        else:
            idComp.append(mioDB.lastrowid)
        contComp = contComp + 1
    #disconnessione
    '''
    - se la funzione viene chiamata per inserire un solo componente, ritorna l' ID del componente inserito in un array 'singolo'
    - se viene utilizzata per inserire più componenti, ritorna un array con gli ID in ordine di inserimento
    - se non modifica nulla ritorna '0'
    '''
    mydb.close()
    return "Righe inserite: " + str(contComp)

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
    if id_art == 0:
        #se l' articolo era vecchio, ho già l'ID ART
        id_art = articolo["id_art"]
    #aggiorno e chiudo il DB
    mydb.commit()
    mydb.close()
    #restituisco l' ID dell'articolo appena salvato
    return id_art

#INSERISCO I COMPONENTI NELLA TABELLA DELL' ARTICOLO
def setComponenteInArticolo(idA, idC, comp):
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #ciclo tutte le righe componente
    cont = 0
    #FUNZIONA MA NON OTTIMALE
    for item in comp:
        #salvo la riga nella tabella articolo_componenti
        sql = "INSERT INTO articolo_componenti (id_art, id_comp, qt_comp) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE qt_comp = %s"
        val = (idA, idC[cont], comp[cont]["qt_comp"], comp[cont]["qt_comp"])
        mioDB.execute(sql, val)
        #incremento il contatore
        cont = cont + 1
    '''
    #OTTIMALE MA NON FUNZIONA
    #salvo la riga nella tabella articolo_componenti
    val = []
    sql = "INSERT INTO articolo_componenti (id_art, id_comp, qt_comp) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE qt_comp = %s"
    for item in comp:
        #riga da inserire
        val.append((idA, idC[cont], comp[cont]["qt_comp"], comp[cont]["qt_comp"]))
        #incremento il contatore
        cont = cont + 1
    print("val")
    print(sql,val)
    print("val")
    mioDB.executemany(sql, val)
    '''
    #aggiorno e chiudo il DB
    mydb.commit()
    mydb.close()

#CREO LA RIGA IMPEGNO
def setImpegno(assImp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #variabili per la formattazione delle DATE da salvare
    now = datetime.datetime.now()
    dataOra = now.strftime("%Y/%m/%d") #("Y-m-d") data odierna
    #variabili dell' impegno
    cod_imp = assImp["cod_imp"]
    cliente = assImp["cliente"]
    cod_ord_cli = assImp["cod_ord_cli"]
    data_ord = assImp["data_ord"]
    #inserisco la riga nuovo impegno
    #query per inserire il componente nella tabella componenti
    sql = "INSERT INTO impegno (cod_imp, cliente, cod_ord_cli, data_ord, data_comp) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE cliente = %s, cod_ord_cli = %s, data_ord = %s"
    val = (cod_imp, cliente, cod_ord_cli, data_ord, dataOra, cliente, cod_ord_cli, data_ord)
    #provo ad eseguire l' inserimento
    mioDB.execute(sql, val)
    idImp = mioDB.lastrowid
    if mioDB.lastrowid > 0:
        #nuovo inserimento o modificato
        #prendo l' indice di componente
        idImp = mioDB.lastrowid
    else:
        #impegno gia inserito
         idImp = assImp["id_imp"]
    mydb.commit()
    #disconnessione
    mydb.close()
    return idImp

def setArticoloInImpegno(artAssieme, idImp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #id righe inserite
    id_righe = []
    #ciclo gli articoli da inserire nell' impegno
    cont = 0
    for item in artAssieme:
        #cerco id_articolo
        idArt = getIDarticolo(item["cod_art"])
        #query string per settare la riga nel DB
        '''
        - Devo controllare se la riga è già stata inserita. 1-> se è già inserita aggiorno solamente le quantità
                                                            2-> se item["id_riga_imp"] è vuota creo la nuova riga
                                                            3-> se viene cancellata non corrisponde l' item["id_riga_imp"]
        '''
        #1
        if item["id_riga_imp"].isnumeric():
            #aggiorno
            sql = "UPDATE riga_imp SET qt_art = %s, data_cons_art = %s WHERE id_riga_imp = %s"
            val = (item["qt_art"], item["data_cons_art"],  item["id_riga_imp"])

        #2
        else:
            #inserisco
            sql = "INSERT INTO riga_imp (id_imp, id_art, qt_art, data_cons_art) VALUES (%s, %s, %s, %s)"
            val = (idImp, idArt, item["qt_art"], item["data_cons_art"])
        #eseguo
        mioDB.execute(sql, val)
        #prendo l' indice della riga
        if mioDB.lastrowid == 0:
            #vecchia riga NON MODIFICATA, prendo l' ID
            id_righe.append(item["id_riga_imp"])
        else:
            #nuova riga o riga modificata
            id_righe.append(mioDB.lastrowid)
        #incremento il contatore
        cont = cont + 1
    #aggiorno e chiudo il DB
    mydb.commit()
    mydb.close()
    return id_righe
