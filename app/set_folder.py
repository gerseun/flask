import os.path

#controllo la presenza della cartella
def setFolder(codImp, codPath):
    #controllo la presenza della cartella iniziale
    setGfolder()
    
    return "ok"

def setGfolder():
    #controllo la presenza della cartella iniziale
    if os.path.isdir("G:\Produzione Python"):
        risposta = "esiste"
    else:
        risposta = "non esiste"
        #creo la cartella
        os.makedirs("G:\Produzione Python")
