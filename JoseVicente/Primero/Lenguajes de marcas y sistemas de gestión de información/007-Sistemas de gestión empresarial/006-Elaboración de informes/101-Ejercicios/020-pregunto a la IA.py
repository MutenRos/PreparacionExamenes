import requests
import json

url = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen2.5-coder:7b",
    "prompt": "¿Qué es Python?",
    "stream": False
}

response = requests.post(url, json=payload)

data = response.json()
print(data["response"])

