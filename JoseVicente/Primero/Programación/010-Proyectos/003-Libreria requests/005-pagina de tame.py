# pip3 install requests lxml --break-system-packages

import requests
from lxml import html
import re

url = "https://tameformacion.com/"

# 1. Petición HTTP
response = requests.get(
    url,
    timeout=10,
    headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120"
    }
)
response.raise_for_status()

html_content = response.text

# 2. Parsear HTML
tree = html.fromstring(response.content)

# 3. Leer <title>
title = tree.xpath("//title/text()")
print("WEB TITLE:")
print(title[0].strip() if title else "No title found")

# 4. Leer todos los <a href="">
links = tree.xpath("//a/@href")

print("\nLINKS:")
for i, href in enumerate(links, start=1):
    print(f"{i}: {href}")

# 5. Buscar emails en el HTML plano con regex
email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emails = sorted(set(re.findall(email_regex, html_content)))

print("\nEMAILS FOUND:")
if emails:
    for i, email in enumerate(emails, start=1):
        print(f"{i}: {email}")
else:
    print("No emails found")

