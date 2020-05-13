import openpyxl
from openpyxl.styles import Font
import os
from datetime import datetime
from shutil import copy2
import datetime
import pprint
import os.path
from app import set_folder as s     #s verrà usata per richiamare le funzioni in set_folder

def save_xlsx_Taglio(array):
    #OTTENGO UN SINGOLO ARTICOLO
    #prendo le variabili da salvare
    t_imp = array['t_imp'][0]
    t_art = array['t_art'][0]
    cod_art = t_art['cod_art']

    #controllo e creo la cartella
    imp = t_imp["cod_imp"]
    imp_folder = imp.replace("/","-")
    #1 - creo DIR
    s.setFolder(imp_folder)
    #controllo se esiste già -> creo file ARTICOLO-1
    path = 'C:/Produzione Python/'+imp_folder+'/'+cod_art+'.xlsx'
    contPath = 0
    while True:
        if os.path.isfile(path):
            #esiste
            contPath += 1
            path = 'C:/Produzione Python/'+imp_folder+'/'+cod_art+'-'+str(contPath)+'.xlsx'
        else:
            break
    #creo il file excel
    copy2('template taglio.xlsx', path)

    #vado a popolare il file
    popolateFile(array, path)










    '''
    col_arr = {'id_riga_dett':1, 'qt_comp':2, 'cod_comp':4, 'desc_comp':11, 'dim_comp':17, 'mat_comp':25}
    row_arr = [8,10,12,14,16,18,20,22,24,26,28,30,32,34,36]

    t_imp = array['t_imp'][0]
    t_art = array['t_art'][0]
    t_comp = array['t_comp']
    cod_imp = t_imp['cod_imp']
    imp = cod_imp.replace('/','-')
    cod_art = t_art['cod_art']

    create_dir(imp)
    path = 'C:Produzione Python/'+imp+'/'+cod_art+'.xlsx'
    copy2('vuota.xlsx', path)

    wb = openpyxl.load_workbook(path)
    ws = wb['TAGLIO']

    #Riempie la descrizione articolo
    coord_arr = get_cell_coord(wb, 'cod_imp')
    ws[coord_arr[0]] = cod_imp

    coord_arr = get_cell_coord(wb, 'id_riga_imp')
    ws[coord_arr[0]] = 'ID_RIGA_IMP*' + t_art['id_riga_imp']

    coord_arr = get_cell_coord(wb, 'cliente')
    ws[coord_arr[0]] = t_imp['cliente']

    coord_arr = get_cell_coord(wb, 'desc_art')
    ws[coord_arr[0]] = t_art['desc_art']

    coord_arr = get_cell_coord(wb, 'data_cons_art')
    ws[coord_arr[0]] = t_art['data_cons_art']

    coord_arr = get_cell_coord(wb, 'cod_art')
    ws[coord_arr[0]] = t_art['cod_art']

    now = datetime.now()
    current_time = now.strftime('%d/%m/%y')
    coord_arr = get_cell_coord(wb, 'data_comp')
    ws[coord_arr[0]] = current_time

    #Riempie le righe dei componenti
    row_arr = row_arr[0:len(t_comp)]
    index = 0
    for r in row_arr:
        arr = t_comp[index]
        for c_name, c in col_arr.items():
            cell = ws.cell(row=r, column=c)
            if c_name == 'id_riga_dett':
                cell.value = 'ID_RIGA_DETT*' + arr[c_name]
            else:
                cell.value = arr[c_name]
        index += 1

    wb.active = ws
    wb.save(path)

    '''
    return 'file excel modificato'

def popolateFile(insieme, fileName):
    #prendo i dati dell' ordine
    t_imp = insieme['t_imp'][0]
    t_art = insieme['t_art'][0]
    t_comp = t_art['t_comp']
    #popolo INTESTAZIONE -> ARTICOLO ED IMPEGNO
    wb = openpyxl.load_workbook(fileName)
    #creo array pagine e ciclo le pagine!!!!!
    arrayPage = ["TAGLIO", "ORDINE"]
    for page in arrayPage:
        ws = wb[page]
        ws["A1"] = "*ART." + str(t_art["id_riga_imp"]) + "*"    #ID RIGA ART
        ws["B3"] = str(t_imp["cliente"])                        #CLIENTE ORDINE
        ws["O1"] = str(t_imp["cod_imp"])                        #CODICE IMPEGNO
        ws["V1"] = str(t_art["data_cons_art"])                  #DATA CONSEGNA
        ws["AD1"] = str(adesso())                               #DATA COMPILAZIONE
        ws["O3"] = str(t_art["desc_art"])                       #DESCRIZIONE ARTICOLO
        ws["AB3"] = str(t_art["cod_art"])                       #CODICE ARTICOLO
    #fine ciclo header

    #popolo TABELLA -> COMPONENTI
    contT = 6
    contO = 6
    contRow = 6
    for comp in t_comp:
        #INSERISCO LA RIGA SOLO SE QT > 0
        if comp["qt_comp"] > 0:
            #controllo se da tagliare o se da ordinare
            #TAGLIO
            if comp["id_produzione"] == 2:
                #setto il foglio
                ws = wb[arrayPage[0]]
                contT += 2
                contRow = contT
            #ORDINE
            elif comp["id_produzione"] == 1:
                #setto il foglio
                ws = wb[arrayPage[1]]
                contO += 2
                contRow = contO
            #inserisco la riga componente
            print(ws)
            ws["A" + str(contRow)] = "*COMP." + str(comp["id_riga_dett"]) + "*"     #ID RIGA COMP
            ws["B" + str(contRow)] = str(comp["qt_comp"])                           #QT COMPO
            ws["D" + str(contRow)] = str(comp["cod_comp"])                          #DIS PARTICOLARE
            ws["K" + str(contRow)] = str(comp["desc_comp"])                         #DESCRIZIONE
            ws["Q" + str(contRow)] = str(comp["dim_comp"])                          #DIMENSIONI
            ws["Y" + str(contRow)] = str(comp["mat_comp"])                          #MATERIALE

    #fine ciclo componenti
    wb.active = ws
    wb.save(fileName)

    return "OK"

def adesso():
    now = datetime.datetime.now()
    dataOra = now.strftime("%d/%m/%Y")
    return dataOra

def get_cell_coord(wb, range_name):
    my_range = wb.defined_names[range_name]
    dests = my_range.destinations # returns a generator of (worksheet title, cell range) tuples
    coord_arr = []
    for title, coord in dests:
        coord_arr.append(coord)
    return coord_arr

    # Give the location of the file
#    path = "template taglio.xlsx"
    #Open an xlsx for reading
#    wb = openpyxl.load_workbook(path)

#    if sh_name in wb.sheetnames:
#        ws = wb.get_sheet_by_name(sh_name)
#        print('sheet exist')
#        ws['A1'] = 10
#        ws['A2'] = 5
#        ws['C1'] = '=SUM(A1:A10)'

#        c1 = sheet.cell(row = 1, column = 5, value = 'test')
#    else:
#        ws2 = wb.create_sheet(title=sh_name)
#        print('sheet doesn\'t exist')
    #ws = wb.get_sheet_by_name("Sheet1")
    #ws = wb.get_active_sheet()
    #ws2 = wb.create_sheet(title=filename)

#    wb.save(path)

#    return 'file excel modificato'
