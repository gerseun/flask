import mysql.connector
import datetime

'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
FUNZIONI PER PRODUZIONE - UFFICIO TECNICO
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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
    return "Inserito"

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
    componenti = assieme["t_comp"]
    #1-> CREO LA RIGA IMPEGNO
    id_imp = setImpegno(impegno)
    #2-> CICLO GLI ARTICOLI-COMPONENTI DA INSERIRE NELL' IMPEGNO
    id_riga_imp = setArticoloInImpegno(articoli, id_imp)
    #vado ad inserire le righe componente
    id_riga_imp_comp = setComponenteInImpegno(componenti, id_imp)
    return "INSERITO CORRETTAMENTE"

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
    #ricerco gli articoli contenuti nell' impegno - con i loro sottocomponenti
    articoli = getArtInImpegno(impegno["id_imp"])
    #creo array di risposta
    impArtComp = {"t_imp": [impegno], "t_art": articoli, "t_comp": componenti}
    risposta = {"pagina": namePage,"azione": "search_imp" , "messaggio": impArtComp}
    #consegno il pacco
    return risposta

def search_Produzione_Articolo(namePage, id_riga_imp):
    #prendo i componenti in produzione dell' articolo
    compInArticolo = getCompInArtImpegno(id_riga_imp)
    risposta = {"pagina": namePage,"azione": "search_Produzione_Articolo" , "messaggio": compInArticolo}
    return risposta

def setAzioneArticolo(namePage, articolo):
    #ciclo i componenti da salvare
    componenti = articolo["t_comp"]
    for x in componenti:
        #salvo nel DB Backup
        saveBackupDett(x)
        #salvo la nuova Azione
        #apro la connessione al database
        mydb = connessione()
        mioDB = mydb.cursor(dictionary=True)
        sql = "UPDATE riga_dett SET qt_comp = %s, id_produzione = %s WHERE id_riga_dett = %s"
        val = (x["qt_comp"], x["id_produzione"], x["id_riga_dett"])
        mioDB.execute(sql, val)
    #fine
    risposta = {"pagina": namePage,"azione": "aggiorna_comp" , "messaggio": "AGGIORNATO CON SUCCESSO"}
    return risposta

def setAzioneCompSingolo(namePage, componenti):
    #ciclo i componenti da salvare
    comp = componenti["t_comp"]
    for x in comp:
        #salvo nel DB Backup
        saveBackupCompSingolo(x)
        #salvo la nuova Azione
        #apro la connessione al database
        mydb = connessione()
        mioDB = mydb.cursor(dictionary=True)
        sql = "UPDATE riga_imp_comp SET  qt_comp = %s, id_produzione = %s WHERE id_riga_imp_comp = %s"
        val = (x["qt_comp"], x["id_produzione"], x["id_riga_imp_comp"])
        mioDB.execute(sql, val)
    #fine
    risposta = {"pagina": namePage,"azione": "aggiorna_comp" , "messaggio": "AGGIORNATO CON SUCCESSO"}
    return risposta

def deleteComp(IDcomp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #elimino componente dal DB
    sql = "DELETE FROM component WHERE id_comp = %s"
    val = (IDcomp)
    mioDB.execute(sql, val)
    return "DELETE COMPLETE"

def deleteCompInArticolo(IDartcomp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #elimino componente nell' articolo, ma non il componente da DB
    sql = "DELETE FROM articolo_componenti WHERE id_artcomp = %s"
    val = (IDartcomp)
    mioDB.execute(sql, val)
    return "DELETE COMPLETE"

def deleteArtInImpegno(IDrigaArt):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #elimino articolo dall' impegno
    sql = "DELETE FROM riga_imp WHERE id_riga_imp = %s"
    val = (IDrigaArt)
    mioDB.execute(sql, val)
    #elimino componenti dell' articolo dall' impegno
    sql = "DELETE FROM riga_dett WHERE id_riga_imp = %s"
    val = (IDrigaArt)
    mioDB.execute(sql, val)
    return "DELETE COMPLETE"

def deleteCompArtInImpegno(IDrigaCompArt):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #elimino componente singolo dall' impegno
    sql = "DELETE FROM riga_dett WHERE id_riga_dett = %s"
    val = (IDrigaCompArt)
    mioDB.execute(sql, val)
    return "DELETE COMPLETE"

def deleteCompSingInImpegno(IDrigaComp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #elimino componente singolo dall' impegno
    sql = "DELETE FROM riga_imp_comp WHERE id_riga_imp_comp = %s"
    val = (IDrigaComp)
    mioDB.execute(sql, val)
    return "DELETE COMPLETE"

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
        arrayComp = {"id_comp": row["id_comp"], "cod_comp": row["cod_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"],"grezzo": row["grezzo"]}
    #else:
        #arrayComp = {"id_comp": "", "cod_comp": "","desc_comp": "","dim_comp": "","mat_comp": ""}
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
    #else:
        #arrayArt = {"id_art": "", "cod_art": "","desc_art": "","cli_art": "","cod_cli_art": ""}
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
        #elaboro la data
        data = row["data_ord"].strftime("%d/%m/%Y")
        arrayImp = {"id_imp": row["id_imp"], "cod_imp": row["cod_imp"],"cliente": row["cliente"],"cod_ord_cli": row["cod_ord_cli"],"data_ord": data}
    #else:
        #arrayImp = {"id_imp": "", "cod_imp": "","cliente": "","cod_ord_cli": "","data_ord": ""}
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
        arr_Componenti.append({"id_artcomp": row["id_artcomp"], "id_comp": row["id_comp"], "cod_comp": row["cod_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"],"qt_comp": row["qt_comp"],"grezzo": row["grezzo"]})
    #se non aveva componenti passo stringa vuota
    #if flag == False:
        #arr_Componenti.append({"id_comp": "", "cod_comp": "","desc_comp": "","dim_comp": "","mat_comp": "","qt_comp": ""})
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
        data = row["data_cons_comp"].strftime("%d/%m/%Y")
        if row["scadenza"]:
            scad = row["scadenza"].strftime("%d/%m/%Y")
        else:
            scad = None
        arr_Componenti.append({"id_riga_imp_comp": row["id_riga_imp_comp"], "id_comp": row["id_comp"], "cod_comp": row["cod_comp"],"desc_comp": row["desc_comp"], "dim_comp": row["dim_comp"], "mat_comp": row["mat_comp"],"qt_comp": row["qt_comp"],"data_cons_comp": data, "id_produzione": row["id_produzione"], "cod_ordine": row["cod_ordine"], "scadenza": scad, "grezzo": row["grezzo"]})
    #se non aveva componenti passo stringa vuota
    #if flag == False:
        #arr_Componenti.append({"id_riga_comp": "", "cod_comp": "","desc_comp": "","dim_comp": "","qt_comp": "","data_cons_comp": ""})
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
    #variabili array ARTICOLI
    arr_Articoli = []
    #ciclo tutti i componenti
    flag = False
    for row in risultato:
        flag = True
        data = row["data_cons_art"].strftime("%d/%m/%Y")

        #cerco i suoi componenti
        arrComp = getCompInArtImpegno(row["id_riga_imp"])
        #arrComp = {"t_comp": componenti}
        #creo array
        arr_Articoli.append({"id_riga_imp": row["id_riga_imp"], "cod_art": row["cod_art"],"id_art": row["id_art"],"desc_art": row["desc_art"],"qt_art": row["qt_art"],"data_cons_art": data, "t_comp": arrComp})
    #se non aveva componenti passo stringa vuota
    #if flag == False:
        #arr_Articoli.append({"id_riga_art": "", "cod_art": "","id_art": "","desc_art": "","qt_art": "","data_cons_art": ""})
    #chiusura
    mydb.close()
    return arr_Articoli

def getCompInArtImpegno(ric_id_art_imp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #prendo i componenti e la loro descrizione
    mioDB.execute("SELECT * FROM riga_dett INNER JOIN componente ON riga_dett.ID_comp=componente.ID_comp  WHERE riga_dett.ID_riga_imp = '" + str(ric_id_art_imp) + "' ORDER BY riga_dett.ID_riga_dett ASC")
    risultato = mioDB.fetchall()
    #variabili array COMPONENTI IN ARTICOLO
    arr_CompInArtImp = []
    #ciclo tutti i componenti
    flag = False
    for row in risultato:
        flag = True
        if row["scadenza"]:
            scad = row["scadenza"].strftime("%d/%m/%Y")
        else:
            scad = None
        arr_CompInArtImp.append({"id_riga_dett": row["id_riga_dett"], "cod_comp": row["cod_comp"],"id_comp": row["id_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"],"qt_comp": row["qt_comp"],"id_produzione": row["id_produzione"],"pos_comp_imp": row["pos_comp_imp"], "cod_ordine": row["cod_ordine"], "scadenza": scad, "grezzo": row["grezzo"] })
    #chiusura
    mydb.close()
    return arr_CompInArtImp

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
        grez = componente["grezzo"]
        desc = componente["desc_comp"]
        dim = componente["dim_comp"]
        mat = componente["mat_comp"]
        #query per inserire il componente nella tabella componenti
        sql = "INSERT INTO componente (cod_comp, grezzo, desc_comp, dim_comp, mat_comp, pos_comp, data_comp) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE desc_comp = %s, dim_comp = %s, mat_comp = %s, pos_comp = %s, grezzo = %s"
        val = (codComp, grez, desc, dim, mat, "0", dataOra, desc, dim, mat, "0", grez)
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
    data_ord = datetime.datetime.strptime(assImp["data_ord"], '%d/%m/%Y').date()
    #inserisco la riga nuovo impegno
    #query per inserire il componente nella tabella componenti
    sql = "INSERT INTO impegno (cod_imp, cliente, cod_ord_cli, data_ord, data_comp) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE cliente = %s, cod_ord_cli = %s, data_ord = %s"
    val = (cod_imp, cliente, cod_ord_cli, data_ord, dataOra, cliente, cod_ord_cli, data_ord)
    #provo ad eseguire l' inserimento
    mioDB.execute(sql, val)
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

#CREO LE RIGHE ARTICOLO IN IMPEGNO
def setArticoloInImpegno(artAssieme, idImp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #id righe inserite
    id_riga = 0
    #ciclo gli articoli da inserire nell' impegno
    cont = 0
    for item in artAssieme:
        #idArt non può essere null, filtro su inserimento dati
        #1 -> ID_RIGA_ART NULL, NUOVO INSERIMENTO
        if item["id_riga_imp"] == "":
            #query string per settare la riga nel DB
            data_cons = datetime.datetime.strptime(item["data_cons_art"], '%d/%m/%Y').date()
            sql = "INSERT INTO riga_imp (id_imp, id_art, qt_art, data_cons_art) VALUES (%s, %s, %s, %s)"
            val = (idImp, item["id_art"], item["qt_art"], data_cons)
            mioDB.execute(sql, val)
            #nuova riga
            id_riga = mioDB.lastrowid
        #2 -> ID_RIGA_ART NUMERICO, MODIFICO LE QUANTITA
        else:
            #query string per settare la riga nel DB
            data_cons = datetime.datetime.strptime(item["data_cons_art"], '%d/%m/%Y').date()
            sql = "UPDATE riga_imp SET qt_art = %s, data_cons_art = %s WHERE id_riga_imp = %s"
            val = (item["qt_art"], data_cons, item["id_riga_imp"])
            mioDB.execute(sql, val)
            #nuova riga
            id_riga = item["id_riga_imp"]
        #incremento il contatore
        cont = cont + 1
        #SETTO LA PRODUZIONE DELL' ARTICOLO INSERITO
        setProduzioneArt(id_riga, item["id_art"], item["qt_art"])
    #aggiorno e chiudo il DB
    mydb.commit()
    mydb.close()
    return cont

#CREO LA PRODUZIONE DEGLI ARTICOLI IN IMPEGNO
def setProduzioneArt(idRiga, idArt, qtArt):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #ricevo dalla tabella articolo_componenti le righe da mettere in produzione
    arrayComp = getCompInArticolo(idArt)
    #ciclo le righe componente e vado a settar la produzione
    for comp in arrayComp:
        qtImp = int(comp["qt_comp"]) * int(qtArt)
        sql = "INSERT INTO riga_dett (id_riga_imp, id_comp, qt_comp, id_produzione) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE qt_comp=%s"
        val = (idRiga, comp["id_comp"], qtImp, "0", qtImp)
        mioDB.execute(sql, val)
    #aggiorno e chiudo il DB
    mydb.commit()
    mydb.close()

#CREO LE RIGHE COMPONENTE IN IMPEGNO
def setComponenteInImpegno(compAssieme, idImp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #id righe inserite
    id_riga = 0
    #ciclo gli articoli da inserire nell' impegno
    cont = 0
    for item in compAssieme:
        #1 -> ID_RIGA_COMP NULL, NUOVO INSERIMENTO
        if item["id_riga_imp_comp"] == "":
            #idArt non può essere null, filtro su inserimento dati
            #query string per settare la riga nel DB
            data_cons = datetime.datetime.strptime(item["data_cons_comp"], '%d/%m/%Y').date()
            sql = "INSERT INTO riga_imp_comp (id_imp, id_comp, qt_comp, data_cons_comp, id_produzione) VALUES (%s, %s, %s, %s, %s)"
            val = (idImp, item["id_comp"], item["qt_comp"], data_cons, "0")
            mioDB.execute(sql, val)
            #prendo l' indice della riga
            id_riga = mioDB.lastrowid
        #1 -> ID_RIGA_COMP NUMERICO, AGGIORNO INSERIMENTO
        else:
            #idArt non può essere null, filtro su inserimento dati
            #query string per settare la riga nel DB
            data_cons = datetime.datetime.strptime(item["data_cons_comp"], '%d/%m/%Y').date()
            sql = "UPDATE riga_imp_comp SET qt_comp = %s, data_cons_comp = %s WHERE id_riga_imp_comp = %s"
            val = (item["qt_comp"], data_cons, item["id_riga_imp_comp"])
            mioDB.execute(sql, val)
            #prendo l' indice della riga
            id_riga = item["id_riga_imp_comp"]
        #incremento
        cont = cont + 1
    #aggiorno e chiudo il DB
    mydb.commit()
    mydb.close()
    return cont

#SALVO LA RIGA NEL BACKUP
def saveBackupDett(riga):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #prendo la vecchia riga
    vecchio = getRigaDett(riga["id_riga_dett"])
    #salvo i Dati
    sql = "INSERT INTO backup_riga_dett (id_riga_dett_b, id_riga_imp_b, id_comp_b, qt_comp_b, id_produzione_b, pos_comp_imp_b, cod_ordine_b, scadenza_b) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE cod_ordine_b = %s"
    val = (vecchio["id_riga_dett"], vecchio["id_riga_imp"], vecchio["id_comp"], vecchio["qt_comp"], vecchio["id_produzione"], vecchio["pos_comp_imp"], vecchio["cod_ordine"], vecchio["scadenza"], vecchio["cod_ordine"])
    mioDB.execute(sql, val)
    mydb.commit()
    return "OK"

#PRENDO LA RIGA DETT
def getRigaDett(idRiga):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #prendo la vecchia riga
    mioDB.execute("SELECT * FROM riga_dett WHERE id_riga_dett = '" + idRiga + "'")
    row = mioDB.fetchone()
    #salvo i Dati
    riga = {"id_riga_dett": row["id_riga_dett"], "id_riga_imp": row["id_riga_imp"], "id_comp": row["id_comp"], "qt_comp": row["qt_comp"], "id_produzione": row["id_produzione"], "pos_comp_imp": row["pos_comp_imp"], "cod_ordine": row["cod_ordine"], "scadenza": row["scadenza"]}
    return riga

#SALVO LA RIGA NEL BACKUP COMP SINGOLO
def saveBackupCompSingolo(riga):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    print("SECONDO")
    print(riga)
    #prendo la vecchia riga
    vecchio = getRigaCompSingolo(riga["id_riga_imp_comp"])
    #salvo i Dati
    sql = "INSERT INTO backup_riga_imp_comp (id_riga_imp_comp_b, id_imp_b, id_comp_b, qt_comp_b, data_cons_comp_b, id_produzione_b, pos_comp_sing_imp_b, cod_ordine_b, scadenza_b) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE cod_ordine_b = %s"
    val = (vecchio["id_riga_imp_comp"], vecchio["id_imp"], vecchio["id_comp"], vecchio["qt_comp"], vecchio["data_cons_comp"], vecchio["id_produzione"], vecchio["pos_comp_sing_imp"], vecchio["cod_ordine"], vecchio["scadenza"], vecchio["cod_ordine"])
    mioDB.execute(sql, val)
    mydb.commit()
    return "OK"

#PRENDO LA RIGA COMP SINGOLO ORIGINALE
def getRigaCompSingolo(idRiga):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #prendo la vecchia riga
    mioDB.execute("SELECT * FROM riga_imp_comp WHERE id_riga_imp_comp = '" + idRiga + "'")
    row = mioDB.fetchone()
    #salvo i Dati
    riga = {"id_riga_imp_comp": row["id_riga_imp_comp"], "id_imp": row["id_imp"], "id_comp": row["id_comp"], "qt_comp": row["qt_comp"], "data_cons_comp": row["data_cons_comp"], "id_produzione": row["id_produzione"], "pos_comp_sing_imp": row["pos_comp_sing_imp"], "cod_ordine": row["cod_ordine"], "scadenza": row["scadenza"]}
    return riga


'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
FUNZIONI PER IDA
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
def get_DaOrdinare(namePage, id):
    #controllo se Articolo o componenti singoli
    flag = id[0]
    #articolo
    id = id[2:]

    #ARTICOLO
    if flag == "A":
        array_art = getArtFromIdRigaImp(id)
        #impegno
        array_imp = getImpFromIDimp(array_art["id_imp"])
        #creo array per la prima tabella
        array_imp_art = {"cod_art": array_art["cod_art"], "desc_art": array_art["desc_art"], "cliente": array_imp["cliente"], "cod_imp": array_imp["cod_imp"], "cliente": array_imp["cliente"], "data_cons_art": array_art["data_cons_art"]}
        #prendo i componenti in produzione dell' articolo
        compInArticolo = getFiltroDaOrdinare(id)
        #creo e trasmetto il messaggio
        daOrdinare = {"t_imp_art": [array_imp_art], "t_compAcq": compInArticolo}
        risposta = {"pagina": namePage,"azione": "get_DaOrdinare" , "messaggio": daOrdinare}

    #COMPONENTI SINGOLI
    elif flag == "I":
        #impegno
        array_imp = getImpFromIDimp(id)
        #prendo i componenti in produzione dell' articolo
        compSing = getFiltroDaOrdinareSing(id)
        #creo array per la prima tabella
        array_imp_art = {"cod_art": "-", "desc_art": "-", "cliente": array_imp["cliente"], "cod_imp": array_imp["cod_imp"], "cliente": array_imp["cliente"], "data_cons_art": compSing[0]["data_cons_comp"]}
        #creo e trasmetto il messaggio
        daOrdinare = {"t_imp_art": [array_imp_art], "t_compAcq": compSing}
        risposta = {"pagina": namePage,"azione": "get_DaOrdinare" , "messaggio": daOrdinare}

    #COMPONENTE IN ARTICOLO
    elif flag == "C":
        #prendo il COMPONENTE
        comp = getCompFromIdRigaDett(id)
        #articolo
        array_art = getArtFromIdRigaImp(comp["id_riga_imp"])
        #impegno
        array_imp = getImpFromIDimp(array_art["id_imp"])
        #creo array per la prima tabella
        array_imp_art = {"cod_art": array_art["cod_art"], "desc_art": array_art["desc_art"], "cliente": array_imp["cliente"], "cod_imp": array_imp["cod_imp"], "cliente": array_imp["cliente"], "data_cons_art": array_art["data_cons_art"]}
        daOrdinare = {"t_imp_art": [array_imp_art], "t_compAcq": [comp]}
        risposta = {"pagina": namePage,"azione": "get_DaOrdinare" , "messaggio": daOrdinare}

    #COMPONENTE IN COMPONENTE SINGOLO
    elif flag == "S":
        #prendo il COMPONENTE
        comp = getCompFromIdRigaImpComp(id)
        #impegno
        array_imp = getImpFromIDimp(comp["id_imp"])
        #creo array per la prima tabella
        array_imp_art = {"cod_art": "-", "desc_art": "-", "cliente": array_imp["cliente"], "cod_imp": array_imp["cod_imp"], "cliente": array_imp["cliente"], "data_cons_art": comp["data_cons_comp"]}
        #creo e trasmetto il messaggio
        daOrdinare = {"t_imp_art": [array_imp_art], "t_compAcq": [comp]}
        risposta = {"pagina": namePage,"azione": "get_DaOrdinare" , "messaggio": daOrdinare}

    #chiusura funzione
    return risposta

#seleziono il componente in articolo selezionato
def getCompFromIdRigaDett(ric_id_dett):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #prendo i componenti e la loro descrizione
    mioDB.execute("SELECT * FROM riga_dett INNER JOIN componente ON riga_dett.ID_comp=componente.ID_comp  WHERE riga_dett.id_riga_dett = '" + str(ric_id_dett) + "'")
    row = mioDB.fetchone()
    #stampo
    if row:
        if row["scadenza"]:
            data = row["scadenza"].strftime("%d/%m/%Y")
        else:
            data = None
        arr_CompInArtImp = {"id_riga_dett": row["id_riga_dett"], "id_riga_imp": row["id_riga_imp"], "cod_comp": row["cod_comp"],"id_comp": row["id_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"],"qt_comp": row["qt_comp"],"id_produzione": row["id_produzione"],"pos_comp_imp": row["pos_comp_imp"], "cod_ordine": row["cod_ordine"], "grezzo": row["grezzo"], "scadenza": data}
    #chiusura
    mydb.close()
    return arr_CompInArtImp

#seleziono il componente in componente singolo selezionato
def getCompFromIdRigaImpComp(ric_id_dett):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #prendo i componenti e la loro descrizione
    mioDB.execute("SELECT * FROM riga_imp_comp INNER JOIN componente ON riga_imp_comp.ID_comp=componente.ID_comp  WHERE riga_imp_comp.id_riga_imp_comp = '" + str(ric_id_dett) + "'")
    row = mioDB.fetchone()
    #stampo
    if row:
        if row["scadenza"]:
            data = row["scadenza"].strftime("%d/%m/%Y")
        else:
            data = None

        data_cons = row["data_cons_comp"].strftime("%d/%m/%Y")
        arr_CompInArtImp = {"id_riga_dett": row["id_riga_imp_comp"], "id_imp": row["id_imp"], "cod_comp": row["cod_comp"],"id_comp": row["id_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"],"qt_comp": row["qt_comp"],"id_produzione": row["id_produzione"],"pos_comp_sing_imp": row["pos_comp_sing_imp"], "cod_ordine": row["cod_ordine"], "scadenza": data, "grezzo": row["grezzo"], "data_cons_comp": data_cons}
    #chiusura
    mydb.close()
    return arr_CompInArtImp

#seleziono i comp nell' articolo selezionato che interessano ad Ida
def getFiltroDaOrdinare(ric_id_art_imp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #prendo i componenti e la loro descrizione
    mioDB.execute("SELECT * FROM riga_dett INNER JOIN componente ON riga_dett.ID_comp=componente.ID_comp  WHERE riga_dett.ID_riga_imp = '" + str(ric_id_art_imp) + "' ORDER BY riga_dett.ID_riga_dett ASC")
    risultato = mioDB.fetchall()
    #variabili array COMPONENTI IN ARTICOLO
    arr_CompInArtImp = []
    #ciclo tutti i componenti
    flag = False
    for row in risultato:
        flag = True
        #controllo se serve per Acquisti
        if row["id_produzione"] == 1 or row["id_produzione"] == 5 or row["id_produzione"] == 6:
            #controllo date
            if row["scadenza"]:
                data = row["scadenza"].strftime("%d/%m/%Y")
            else:
                data = None
            arr_CompInArtImp.append({"id_riga_dett": row["id_riga_dett"], "cod_comp": row["cod_comp"],"id_comp": row["id_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"],"qt_comp": row["qt_comp"],"id_produzione": row["id_produzione"],"pos_comp_imp": row["pos_comp_imp"], "cod_ordine": row["cod_ordine"], "grezzo": row["grezzo"], "scadenza": data})
    #chiusura
    mydb.close()
    return arr_CompInArtImp

#seleziono i comp singoli che interessano ad Ida
def getFiltroDaOrdinareSing(ric_id_art_imp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #prendo i componenti e la loro descrizione
    mioDB.execute("SELECT * FROM riga_imp_comp INNER JOIN componente ON riga_imp_comp.ID_comp=componente.ID_comp  WHERE riga_imp_comp.ID_imp = '" + str(ric_id_art_imp) + "' ORDER BY riga_imp_comp.ID_riga_imp_comp ASC")
    risultato = mioDB.fetchall()
    #variabili array COMPONENTI IN ARTICOLO
    arr_CompInArtImp = []
    #ciclo tutti i componenti
    flag = False
    for row in risultato:
        flag = True
        #controllo se serve per Acquisti
        if row["id_produzione"] == 1 or row["id_produzione"] == 5 or row["id_produzione"] == 6:
            #controllo date
            if row["scadenza"]:
                data = row["scadenza"].strftime("%d/%m/%Y")
            else:
                data = None
            data_cons = row["data_cons_comp"].strftime("%d/%m/%Y")

            #assegno gli ID uguali a quelli di riga_dett per popolare la tabella
            arr_CompInArtImp.append({"id_riga_dett": row["id_riga_imp_comp"], "cod_comp": row["cod_comp"],"id_comp": row["id_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"],"qt_comp": row["qt_comp"],"id_produzione": row["id_produzione"],"pos_comp_sing_imp": row["pos_comp_sing_imp"], "cod_ordine": row["cod_ordine"], "scadenza": data, "grezzo": row["grezzo"], "data_cons_comp": data_cons})
    #chiusura
    mydb.close()
    return arr_CompInArtImp


def getArtFromIdRigaImp(ric_id_riga_imp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #seleziono gli id_riga_imp dell' impegno ricercato
    mioDB.execute("SELECT * FROM riga_imp INNER JOIN articolo ON riga_imp.ID_art=articolo.ID_art  WHERE riga_imp.id_riga_imp = '" + str(ric_id_riga_imp) + "' ORDER BY riga_imp.ID_riga_imp ASC")
    row = mioDB.fetchone()
    #variabili array ARTICOLI
    if row:
        data = row["data_cons_art"].strftime("%d/%m/%Y")
        #creo array
        arr_Articoli = {"id_imp": row["id_imp"], "id_riga_imp": row["id_riga_imp"], "cod_art": row["cod_art"],"id_art": row["id_art"],"desc_art": row["desc_art"],"qt_art": row["qt_art"],"data_cons_art": data}
    #chiusura
    mydb.close()
    return arr_Articoli

#RICERCA IMPEGNO INSERITO DA ID IMP
def getImpFromIDimp(ricIDImpegno):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #istruzione query string -> seleziono impegno ricercato
    mioDB.execute("SELECT * FROM impegno WHERE id_imp='" + str(ricIDImpegno) + "'")
    row = mioDB.fetchone()
    if row:
        #salvo i dati articolo
        #elaboro la data
        data = row["data_ord"].strftime("%d/%m/%Y")
        arrayImp = {"id_imp": row["id_imp"], "cod_imp": row["cod_imp"],"cliente": row["cliente"],"cod_ord_cli": row["cod_ord_cli"],"data_ord": data}
    #chiusura
    mydb.close()
    return arrayImp

#SALVO LA LAVORAZIONE COMPIUTA DA ACQUISTI
def setAzioneOrdine(namePage, articolo):
    #DISTINZIONE SE ARTICOLO O COMPONENTI SINGOLI
    isArticolo = articolo["t_imp_art"][0]["cod_art"]
    if isArticolo == "-":
        #comp singolo
        #ciclo i componenti da salvare
        comp = articolo["t_compAcq"]
        for x in comp:
            #salvo nel DB Backup
            saveBackupCompSingoloORDINE(x)
            #salvo la nuova Azione
            #apro la connessione al database
            mydb = connessione()
            mioDB = mydb.cursor(dictionary=True)
            if x["scadenza"]:
                scad = datetime.datetime.strptime(x["scadenza"], '%d/%m/%Y').date()
            else:
                scad = None
            sql = "UPDATE riga_imp_comp SET  qt_comp = %s, id_produzione = %s, cod_ordine = %s, scadenza = %s WHERE id_riga_imp_comp = %s"
            val = (x["qt_comp"], x["id_produzione"], x["cod_ordine"], scad, x["id_riga_dett"])
            mioDB.execute(sql, val)

    else:
        #articolo con componenti
        componenti = articolo["t_compAcq"]
        for x in componenti:
            #salvo nel DB Backup
            saveBackupDett(x)
            #salvo la nuova Azione
            #apro la connessione al database
            mydb = connessione()
            mioDB = mydb.cursor(dictionary=True)
            if x["scadenza"]:
                scad = datetime.datetime.strptime(x["scadenza"], '%d/%m/%Y').date()
            else:
                scad = None
            sql = "UPDATE riga_dett SET qt_comp = %s, id_produzione = %s, cod_ordine = %s, scadenza = %s WHERE id_riga_dett = %s"
            val = (x["qt_comp"], x["id_produzione"], x["cod_ordine"], scad, x["id_riga_dett"])
            mioDB.execute(sql, val)

    #fine
    risposta = {"pagina": namePage,"azione": "aggiorna_comp" , "messaggio": "AGGIORNATO CON SUCCESSO"}
    return risposta

#SALVO LA RIGA NEL BACKUP COMP SINGOLO
def saveBackupCompSingoloORDINE(riga):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #prendo la vecchia riga
    vecchio = getRigaCompSingolo(riga["id_riga_dett"])
    #salvo i Dati
    sql = "INSERT INTO backup_riga_imp_comp (id_riga_imp_comp_b, id_imp_b, id_comp_b, qt_comp_b, data_cons_comp_b, id_produzione_b, pos_comp_sing_imp_b, cod_ordine_b, scadenza_b) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (vecchio["id_riga_imp_comp"], vecchio["id_imp"], vecchio["id_comp"], vecchio["qt_comp"], vecchio["data_cons_comp"], vecchio["id_produzione"], vecchio["pos_comp_sing_imp"], vecchio["cod_ordine"], vecchio["scadenza"])
    mioDB.execute(sql, val)
    mydb.commit()
    return "OK"

#CERCO IL MATERIALE ORDINATO MA SCADUTO
def getOrdineScaduto(namePage):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #1
    #cerco i componenti all' interno di un articolo con data consegna scaduta
    mioDB.execute("SELECT * FROM riga_dett INNER JOIN componente ON riga_dett.ID_comp=componente.ID_comp  WHERE riga_dett.scadenza < CURRENT_TIME() AND riga_dett.id_produzione = 5 ORDER BY riga_dett.ID_riga_dett ASC")
    risultato = mioDB.fetchall()
    #variabili array COMPONENTI IN ARTICOLO
    arr_CompScaduti = []
    #ciclo tutti i componenti
    for row in risultato:
        #controllo date
        if row["scadenza"]:
            data = row["scadenza"].strftime("%d/%m/%Y")
        else:
            data = None
        arr_CompScaduti.append({"id_riga_dett": row["id_riga_dett"], "cod_comp": row["cod_comp"],"id_comp": row["id_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"],"qt_comp": row["qt_comp"],"id_produzione": row["id_produzione"], "cod_ordine": row["cod_ordine"], "grezzo": row["grezzo"], "scadenza": data})

    #2
    #cerco i componenti singoli con data consegna scaduta
    mioDB.execute("SELECT * FROM riga_imp_comp INNER JOIN componente ON riga_imp_comp.ID_comp=componente.ID_comp  WHERE riga_imp_comp.scadenza < CURRENT_TIME() AND riga_imp_comp.id_produzione = 5 ORDER BY riga_imp_comp.ID_riga_imp_comp ASC")
    risultato = mioDB.fetchall()
    #variabili array COMPONENTI IN ARTICOLO
    #ciclo tutti i componenti
    for row in risultato:
        #controllo date
        if row["scadenza"]:
            data = row["scadenza"].strftime("%d/%m/%Y")
        else:
            data = None
        arr_CompScaduti.append({"id_riga_dett": row["id_riga_imp_comp"], "cod_comp": row["cod_comp"],"id_comp": row["id_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"],"qt_comp": row["qt_comp"],"id_produzione": row["id_produzione"], "cod_ordine": row["cod_ordine"], "grezzo": row["grezzo"], "scadenza": data})

    #3
    #cerco i componenti all' interno di un articolo con data consegna in scadenza in 7 giorni
    mioDB.execute("SELECT * FROM riga_dett INNER JOIN componente ON riga_dett.ID_comp=componente.ID_comp  WHERE (riga_dett.scadenza BETWEEN CURRENT_TIME() AND (CURRENT_TIME() + INTERVAL 7 DAY)) AND (riga_dett.id_produzione = 5) ORDER BY riga_dett.ID_riga_dett ASC")
    risultato = mioDB.fetchall()
    #variabili array COMPONENTI IN ARTICOLO
    arr_CompInScadenza = []
    #ciclo tutti i componenti
    for row in risultato:
        #controllo date
        if row["scadenza"]:
            data = row["scadenza"].strftime("%d/%m/%Y")
        else:
            data = None
        arr_CompInScadenza.append({"id_riga_dett": row["id_riga_dett"], "cod_comp": row["cod_comp"],"id_comp": row["id_comp"],"desc_comp": row["desc_comp"],"dim_comp": row["dim_comp"],"mat_comp": row["mat_comp"],"qt_comp": row["qt_comp"],"id_produzione": row["id_produzione"], "cod_ordine": row["cod_ordine"], "grezzo": row["grezzo"], "scadenza": data})

    #4

    #chiusura
    mydb.close()
    #creo e trasmetto il messaggio
    daOrdinare = {"t_compScaduti": arr_CompScaduti, "t_compInScadenza": arr_CompInScadenza}
    print(daOrdinare)
    risposta = {"pagina": namePage,"azione": "scaduti" , "messaggio": daOrdinare}
    return risposta
