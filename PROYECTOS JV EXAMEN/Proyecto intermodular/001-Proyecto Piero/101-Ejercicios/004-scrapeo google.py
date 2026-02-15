import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin, urlparse

# ----------------------------
# CONFIG
# ----------------------------
SEARCH_QUERY = "ardilla"
URL = f"https://www.google.com/search?q={SEARCH_QUERY}&tbm=isch&hl=es"
OUTPUT_DIR = "google_images"
TIMEOUT = 15
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Crear carpeta si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------
# Descargar HTML
# ----------------------------
print(f"Buscando imágenes de '{SEARCH_QUERY}' en Google...")
try:
    response = requests.get(URL, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error al conectar con Google: {e}")
    exit(1)

html = response.text

soup = BeautifulSoup(html, "html.parser")

image_urls = set()

# ----------------------------
# 1. Extraer <img src="...">
# ----------------------------
for img in soup.find_all("img"):
    src = img.get("src")
    if src:
        full_url = urljoin(URL, src)
        image_urls.add(full_url)

# ----------------------------
# 2. Extraer CSS background-image dentro de style=""
#    Ejemplo: style="background-image:url('img/bg.jpg');"
# ----------------------------
pattern = re.compile(r"background-image\s*:\s*url\(['\"]?(.*?)['\"]?\)", re.IGNORECASE)

for elem in soup.find_all(style=True):
    styles = elem["style"]
    matches = pattern.findall(styles)
    for m in matches:
        full_url = urljoin(URL, m)
        image_urls.add(full_url)

# ----------------------------
# Descargar todas las imágenes encontradas
# ----------------------------
print(f"\nEncontradas {len(image_urls)} imágenes:")
for img_url in image_urls:
    print(" -", img_url)

print("\nDescargando imágenes...\n")

for img_url in image_urls:
    try:
        filename = os.path.basename(urlparse(img_url).path)
        if not filename:  # fallback
            filename = "image_" + str(abs(hash(img_url))) + ".jpg"

        filepath = os.path.join(OUTPUT_DIR, filename)

        img_data = requests.get(img_url, headers=HEADERS, timeout=TIMEOUT).content

        with open(filepath, "wb") as f:
            f.write(img_data)

        print(f"✔ Guardada: {filepath}")

    except Exception as e:
        print(f"✘ Error con {img_url}: {e}")

print("\nTerminado.")

