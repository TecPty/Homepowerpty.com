import openpyxl, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"c:\Users\HP 15\Homepowerpty.com\EXCEL DE PRODUCTOS PARA MKT.xlsx"
wb = openpyxl.load_workbook(path, data_only=True)
ws = wb.active

found = []
for row in ws.iter_rows(values_only=True):
    non_empty = [str(c).strip() for c in row if c is not None and str(c).strip() not in ('', 'None')]
    if len(non_empty) >= 2:
        found.append(non_empty)

for r in found:
    print(' | '.join(r[:5]))
