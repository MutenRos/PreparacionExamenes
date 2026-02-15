import json
import smtplib
import ssl
import base64
import mimetypes
from email.message import EmailMessage
from pathlib import Path

from bs4 import BeautifulSoup  # pip install beautifulsoup4


# ---------- Carga de configuración y plantilla ----------

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_html_template(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ---------- Conversión de imágenes locales a base64 ----------

def inline_local_images(html: str, base_dir: Path) -> str:
    """
    Busca <img src="..."> en el HTML.
    Si el src es un archivo local, lo convierte a data:image/...;base64,...
    y reemplaza el atributo src.
    """
    soup = BeautifulSoup(html, "html.parser")

    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue

        # Ignorar URLs absolutas o ya inline
        if (
            src.startswith("http://")
            or src.startswith("https://")
            or src.startswith("data:")
        ):
            continue

        # Construir ruta de fichero
        img_path = Path(src)
        if not img_path.is_absolute():
            img_path = (base_dir / src).resolve()

        if not img_path.exists():
            print(f"[AVISO] Imagen no encontrada, se deja tal cual: {src}")
            continue

        try:
            # Deducir tipo MIME
            mime_type, _ = mimetypes.guess_type(str(img_path))
            if mime_type is None:
                # Valor por defecto razonable
                mime_type = "image/png"

            with open(img_path, "rb") as f:
                data = f.read()

            b64 = base64.b64encode(data).decode("ascii")
            data_uri = f"data:{mime_type};base64,{b64}"

            img["src"] = data_uri

            print(f"[OK] Imagen inlined como base64: {src}")

        except Exception as e:
            print(f"[ERROR] No se pudo inlinear {src}: {e}")

    return str(soup)


# ---------- Creación del mensaje ----------

def create_message(cfg: dict) -> EmailMessage:
    email_cfg = cfg["email"]

    msg = EmailMessage()
    msg["From"] = email_cfg["from"]
    msg["To"] = ", ".join(email_cfg["to"]) if isinstance(email_cfg["to"], list) else email_cfg["to"]
    msg["Subject"] = email_cfg["subject"]

    # Parte de texto plano (fallback)
    msg.set_content(email_cfg.get("body_text", "Ver este correo en modo HTML."))

    # Cargar plantilla HTML
    html_template_path = Path(email_cfg["html_template"]).resolve()
    html_raw = load_html_template(html_template_path)

    # Directorio base donde están las imágenes (el del template)
    base_dir = html_template_path.parent

    # Reemplazar imágenes locales por data:...;base64
    html_inlined = inline_local_images(html_raw, base_dir)

    # Añadir parte HTML
    msg.add_alternative(html_inlined, subtype="html")

    return msg


# ---------- Envío del correo ----------

def send_email(cfg: dict) -> None:
    smtp_cfg = cfg["smtp"]
    host = smtp_cfg["host"]
    port = smtp_cfg["port"]
    user = smtp_cfg["user"]
    password = smtp_cfg["password"]
    use_tls = smtp_cfg.get("use_tls", False)

    msg = create_message(cfg)

    if port == 465:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(user, password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(host, port) as server:
            if use_tls:
                server.starttls()
            server.login(user, password)
            server.send_message(msg)

    print("Correo enviado.")


if __name__ == "__main__":
    config = load_config("config2.json")
    send_email(config)

