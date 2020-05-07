import os.path

#controllo la presenza della cartella
def setFolder(codImp):
    #controllo la presenza della cartella iniziale
    test = setGfolder()
    path = 'C:/Produzione Python/' + str(codImp)
    if test:
        #creo la cartella dell' IMPEGNO
        if os.path.isdir(path):
            #mex di ritorno
            messaggio = "GIA PRESENTE"
        else:
            #mex di ritorno
            messaggio = "CREAZIONE"
            #creo la cartella
            os.makedirs(path)
    else:
        messaggio = "ERRORE CREAZIONE"
    return messaggio

def setGfolder():
    #controllo la presenza della cartella iniziale
    if os.path.isdir("C:/Produzione Python"):
        risposta = True
    else:
        risposta = False
        #creo la cartella
        os.makedirs("C:/Produzione Python")
    return risposta
