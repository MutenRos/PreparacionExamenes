from PyPDF2 import PdfReader, PdfWriter

input_pdf = "uno.pdf"
reader = PdfReader(input_pdf)

for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)

    output_filename = f"page_{i+1}.pdf"
    with open(output_filename, "wb") as output:
        writer.write(output)

    print(f"Created: {output_filename}")

