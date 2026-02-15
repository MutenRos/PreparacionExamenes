from pdf2image import convert_from_path

input_pdf = "uno.pdf"

# Convertir todas las páginas a imágenes PIL
pages = convert_from_path(input_pdf, dpi=300)

for i, page in enumerate(pages):
    output_filename = f"page_{i+1}.png"
    page.save(output_filename, "PNG")
    print(f"Created: {output_filename}")

