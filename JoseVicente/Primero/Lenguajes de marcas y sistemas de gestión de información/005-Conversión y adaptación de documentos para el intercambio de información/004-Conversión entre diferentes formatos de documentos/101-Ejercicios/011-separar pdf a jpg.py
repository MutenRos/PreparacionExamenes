from pdf2image import convert_from_path

input_pdf = "uno.pdf"

# Convertir todas las páginas
pages = convert_from_path(input_pdf, dpi=300)

for i, page in enumerate(pages):
    output_filename = f"page_{i+1}.jpg"
    page.save(output_filename, "JPEG")
    print(f"Created: {output_filename}")

