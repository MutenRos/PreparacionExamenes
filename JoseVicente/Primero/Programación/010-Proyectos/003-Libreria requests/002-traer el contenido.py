#pip3 install requests --break-system-packages
import requests

url = "https://jocarsa.com"

response = requests.get(url)
content = response.text
print(content)
