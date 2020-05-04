import openpyxl

def save_xlsx(array):
    imp = array['t_imp'][0]['cod_imp']
    sh_name = imp.replace('/','-')

    # Give the location of the file
    path = "vuota.xlsx"
    #Open an xlsx for reading
    wb = openpyxl.load_workbook(path)

    if sh_name in wb.sheetnames:
        ws = wb.get_sheet_by_name(sh_name)
        print('sheet exist')
        ws['A1'] = 10
        ws['A2'] = 5
        ws['C1'] = '=SUM(A1:A10)'

        c1 = sheet.cell(row = 1, column = 5, value = 'test')
    else:
        ws2 = wb.create_sheet(title=sh_name)
        print('sheet doesn\'t exist')
    #ws = wb.get_sheet_by_name("Sheet1")
    #ws = wb.get_active_sheet()
    #ws2 = wb.create_sheet(title=filename)

    wb.save(path)

    return 'file excel modificato'
