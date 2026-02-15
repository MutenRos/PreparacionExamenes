from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os
import zipfile
from uuid import uuid4
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Carpetas para ficheros temporales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/unir", methods=["POST"])
def unir_pdf():
    """
    Une varios archivos PDF enviados desde el formulario
    y devuelve un único PDF descargable.
    """
    files = request.files.getlist("pdfs")

    # Filtramos solo los PDF válidos
    pdf_files = [f for f in files if f and allowed_file(f.filename)]

    if not pdf_files:
        return "No se han enviado PDFs válidos", 400

    merger = PdfMerger()
    temp_paths = []

    try:
        # Guardamos y añadimos cada PDF al merger
        for f in pdf_files:
            filename = secure_filename(f.filename)
            temp_path = os.path.join(UPLOAD_FOLDER, f"{uuid4()}_{filename}")
            f.save(temp_path)
            temp_paths.append(temp_path)
            merger.append(temp_path)

        # Guardamos el resultado
        output_filename = f"unido_{uuid4()}.pdf"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        merger.write(output_path)
        merger.close()

        return send_file(
            output_path,
            as_attachment=True,
            download_name="unido.pdf",
            mimetype="application/pdf",
        )

    finally:
        # Limpieza básica de archivos temporales de entrada
        for path in temp_paths:
            if os.path.exists(path):
                os.remove(path)


@app.route("/separar", methods=["POST"])
def separar_pdf():
    """
    Separa un PDF en páginas individuales y devuelve un ZIP
    con un PDF por cada página.
    """
    file = request.files.get("pdf")

    if not file or not allowed_file(file.filename):
        return "Debes enviar un archivo PDF válido", 400

    # Guardamos el PDF original
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, f"{uuid4()}_{filename}")
    file.save(input_path)

    temp_outputs = []
    zip_path = None

    try:
        reader = PdfReader(input_path)

        # Carpeta temporal específica para este trabajo
        job_id = uuid4()
        job_folder = os.path.join(OUTPUT_FOLDER, f"split_{job_id}")
        os.makedirs(job_folder, exist_ok=True)

        # Creamos un PDF por página
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            page_filename = f"page_{i+1}.pdf"
            page_path = os.path.join(job_folder, page_filename)
            with open(page_path, "wb") as out_f:
                writer.write(out_f)
            temp_outputs.append(page_path)

        # Empaquetamos todo en un ZIP
        zip_filename = f"paginas_{job_id}.zip"
        zip_path = os.path.join(OUTPUT_FOLDER, zip_filename)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for path in temp_outputs:
                arcname = os.path.basename(path)
                zipf.write(path, arcname=arcname)

        return send_file(
            zip_path,
            as_attachment=True,
            download_name="paginas_separadas.zip",
            mimetype="application/zip",
        )

    finally:
        # Limpieza: borramos el PDF original
        if os.path.exists(input_path):
            os.remove(input_path)
        # Podrías borrar también job_folder si no quieres conservarlo


if __name__ == "__main__":
    # Para desarrollo; en producción usar WSGI (gunicorn, etc.)
    app.run(debug=True)

