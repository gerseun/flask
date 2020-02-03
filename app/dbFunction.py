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

def newArticolo(assieme):
    #CREAZIONE NUOVO ARTICOLO - CILINDRO
    #echo "<br>REPORT NEW ARTICOLO:<br>";
    articolo = assieme["newArticolo"]["t_art"]
    componenti = assieme["newArticolo"]["t_comp"]
    #variabili del cilindro per settarlo
    codArticolo = articolo[0]["cod_art"]
    descrizione = articolo[0]["desc_art"]
    cliente = articolo[0]["cli_art"]
    codCliente = articolo[0]["cod_cli_art"]
    #echo "<br>".$codArticolo."<br>";
    #setto l' articolo
    setArticolo(codArticolo, descrizione, cliente, codCliente)
    #vado a salvare le componenti del cilindro
    setComponenteInArticolo(codArticolo, componenti)

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

#RICEVO TUTTI I CODICI IMPEGNO
def getCodImpegni():
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #istruzione query string -> seleziono tutti gli impegni inseriti
    mioDB.execute("SELECT cod_imp FROM impegno")
    result = mioDB.fetchall()
    #ricevo tutte le righe
    cont = 0
    arr_Impegno = []
    for x in result:
        #salvo l' array codici impegni
        arr_Impegno.append(x["cod_imp"])
        cont = cont + 1
    #se non sono presenti righe, passo casella VUOTA
    if cont == 0:
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
    cont = 0
    arr_Componente = []
    for x in result:
        #salvo l' array codici componente
        arr_Componente.append(x["cod_comp"])
        cont = cont + 1
    #se non sono presenti righe, passo casella VUOTA
    if cont == 0:
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
    cont = 0
    arr_Articolo = []
    for x in result:
        #salvo l' array codici articoli
        arr_Articolo.append(x["cod_art"])
        cont = cont + 1
    #se non sono presenti righe, passo casella VUOTA
    if cont == 0:
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
    return false

#ricerco ID COMPONENTE
def getIDcomponente(comp):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #istruzione query string
    mioDB.execute("SELECT id_comp FROM componente WHERE cod_comp='".$comp."';")
    result = mioDB.fetchall()
    #controllo se componente già salvato
    for x in result:
      #componente gia inserito -> salvo i dati componente
      idcomp = x["id_comp"]
      mydb.close()
      return idcomp
    #non esiste
    mydb.close()
    return false

#SETTO UN NUOVO ARTICOLO
def setArticolo(codArt, desc, cli, codCli):
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #variabili per la formattazione delle DATE da salvare
    now = datetime.datetime.now()
    dataOra = now.strftime("%Y/%m/%d") #("Y-m-d") data odierna
    #inserisco la riga articolo
    sql = "INSERT INTO articolo (cod_art, desc_art, cli_art, cod_cli_art, kit_art, data_art) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (codArt, desc, cli, codCli, "0", dataOra)
    mioDB.execute(sql, val)
    mydb.commit()
    print("1 record inserted, ID:", mioDB.lastrowid)
    mydb.close()

#INSERISCO I COMPONENTI NELLA TABELLA DELL' ARTICOLO
def setComponenteInArticolo(codArt, codComponenti):
    flag_anag_comp = 0       #0 -> nuovo comp
                             #num -> anagrafica già inserita
    #variabili per la formattazione delle DATE da salvare
    now = datetime.datetime.now()
    dataOra = now.strftime("%Y/%m/%d") #("Y-m-d") data odierna
    #prendo l' indice di articolo
    idArt = varDB->getIDarticolo(codArt)
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor(dictionary=True)
    #ciclo tutti i componenti
    cont = 0
    foreach(codComponenti as componente){
        #echo "<br>".$cont."<br>";
        #salvo variabili del componente
        codComp = componente["cod_comp"]
        desc = componente["desc_comp"]
        dim = componente["dim_comp"]
        mat = componente["mat_comp"]
        qt = componente["qt_comp"]
        #controllo se l' anagrafica componente esiste già
        flag_anag_comp = getIDcomponente(codComp)
        if flag_anag_comp == false:
            #salvo il codice componente nell' anagrafica componente
            #inserisco la riga componente
            sql = "INSERT INTO componente (cod_comp, desc_comp, dim_comp, mat_comp, pos_comp, data_comp) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (codComp, desc, dim, mat, "0", dataOra)
            mioDB.execute(sql, val)
            mydb.commit()
            #prendo l' indice di componente
            idComp = mioDB.lastrowid
            print("1 record inserted, ID:", idComp)
        #salvo la riga nella tabella articolo_componenti
        
'''


  //salvo la riga nella tabella articolo_componenti
  $istruzione = "INSERT INTO `articolo_componenti` (`id_art`, `id_comp`, `qt_comp`)
                VALUES ('".$idArt."','".$idComp."','".$qt."')
                ON DUPLICATE KEY UPDATE qt_comp = '".$qt."';";
  if (mysqli_query($connessione,$istruzione)) {
    echo $codComp.": inserito nella descrizione articolo ".$codArt."<br>";
  }
  else {
    echo "Errore inserimento descrizione articolo: ".$codComp." - ". $connessione->error."<br>";
  }
  //incremento il contatore
  $cont = $cont +1;
}
//disconnessione
mysqli_close($connessione);
return true;
}
else{
return false;
}
}
'''
