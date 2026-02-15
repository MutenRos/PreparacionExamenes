from PyPDF2 import PdfMerger

pdfs = ["uno.pdf", "dos.pdf"]

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("unido.pdf")
merger.close()

