sudo apt install ollama

echo "deb [signed-by=/usr/share/keyrings/ollama.gpg] https://repo.ollama.com/deb stable main" | sudo tee /etc/apt/sources.list.d/ollama.list
curl -fsSL https://repo.ollama.com/ollama.gpg | sudo tee /usr/share/keyrings/ollama.gpg > /dev/null
sudo apt update
sudo apt install ollama
