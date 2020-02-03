<<<<<<< HEAD
def my_function():
    print("sboret")
=======
import mysql.connector

#funzione per la connessione al database
def connessione():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="db_progresso"
    )
    return mydb;

def testDB():
    #apro la connessione al database
    mydb = connessione()
    mioDB = mydb.cursor()
    #query string
    mioDB.execute("SHOW TABLES")

    for x in mioDB:
        print(x)

    mydb.close()
>>>>>>> 429c2b8779e4ba63a7874d1db8db01a0c54827ed
