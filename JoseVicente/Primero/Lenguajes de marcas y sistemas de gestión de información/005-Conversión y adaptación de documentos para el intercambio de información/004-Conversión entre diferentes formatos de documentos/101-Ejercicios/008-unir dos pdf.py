from PyPDF2 import PdfMerger

merger = PdfMerger()

merger.append("uno.pdf")
merger.append("dos.pdf")

merger.write("unido.pdf")
merger.close()
