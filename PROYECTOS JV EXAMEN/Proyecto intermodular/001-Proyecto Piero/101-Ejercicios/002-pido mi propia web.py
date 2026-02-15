import requests

url = "https://jocarsa.com"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    # si quieres ver el código de estado
    print("Status:", response.status_code)
    print("Encoding:", response.encoding)

    # y aquí tienes el HTML completito
    html = response.text
    print(html)

except requests.exceptions.ConnectionError:
    print("Error: no se pudo conectar con el servidor.")
except requests.exceptions.Timeout:
    print("Error: la petición tardó demasiado.")
except requests.exceptions.HTTPError as e:
    print(f"Error HTTP: {e}")

