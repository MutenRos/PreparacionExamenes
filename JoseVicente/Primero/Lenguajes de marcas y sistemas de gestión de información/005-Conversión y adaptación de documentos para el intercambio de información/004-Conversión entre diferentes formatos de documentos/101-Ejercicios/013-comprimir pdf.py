import subprocess

input_pdf = "uno.pdf"
output_pdf = "unocomprimido.pdf"

cmd = [
    "gs",
    "-sDEVICE=pdfwrite",
    "-dCompatibilityLevel=1.4",
    "-dPDFSETTINGS=/screen",  # /screen, /ebook, /printer, /prepress, /default
    "-dNOPAUSE",
    "-dQUIET",
    "-dBATCH",
    f"-sOutputFile={output_pdf}",
    input_pdf
]

subprocess.run(cmd)
print("Compressed:", output_pdf)

