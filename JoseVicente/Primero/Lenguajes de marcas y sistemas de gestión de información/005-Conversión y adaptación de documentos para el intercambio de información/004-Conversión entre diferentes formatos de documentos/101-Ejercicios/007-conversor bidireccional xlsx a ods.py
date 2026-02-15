import pandas as pd

def convert(file_in, file_out):
    if file_in.endswith(".ods"):
        df = pd.read_excel(file_in, engine="odf")
    else:
        df = pd.read_excel(file_in)

    if file_out.endswith(".ods"):
        from odf.opendocument import OpenDocumentSpreadsheet
        from odf.table import Table, TableRow, TableCell
        from odf.text import P

        ods = OpenDocumentSpreadsheet()
        table = Table(name="Sheet1")

        for row in df.itertuples(index=False):
            tr = TableRow()
            for value in row:
                cell = TableCell()
                cell.addElement(P(text=str(value)))
                tr.addElement(cell)
            table.addElement(tr)

        ods.spreadsheet.addElement(table)
        ods.save(file_out)

    else:
        df.to_excel(file_out, index=False)

# Example:
convert("empresa.xlsx", "empresaconvertida.ods")
convert("empresa.ods", "empresaconvertida.xlsx")

