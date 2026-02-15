import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"


def llamar_ollama(messages, stream=True):
    """
    Llama a la API /api/chat de Ollama en localhost con el historial 'messages'.
    Devuelve el texto completo de la respuesta del asistente.
    Si stream=True, va imprimiendo mientras recibe.
    """
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": stream,
    }

    # stream=True de requests -> lectura chunk a chunk
    response = requests.post(OLLAMA_URL, json=payload, stream=stream)
    response.raise_for_status()

    full_text = ""

    if stream:
        # La API devuelve múltiples líneas JSON, cada una con un "message" parcial
        for line in response.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            if "message" in data and "content" in data["message"]:
                chunk_text = data["message"]["content"]
                full_text += chunk_text
                print(chunk_text, end="", flush=True)
            # Cuando 'done' es True, se acabó la respuesta
            if data.get("done"):
                break
        print()  # salto de línea al final
    else:
        data = response.json()
        full_text = data["message"]["content"]
        print(full_text)

    return full_text


def chat_loop():
    messages = []
    print(f"Chat con {MODEL} en http://localhost:11434")
    print("Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ").strip()
        if user_input.lower() in ("salir", "exit", "quit"):
            print("Saliendo del chat...")
            break

        # Añadimos mensaje del usuario al historial
        messages.append({"role": "user", "content": user_input})

        print("IA: ", end="", flush=True)
        # Llamada a Ollama con historial completo
        assistant_reply = llamar_ollama(messages, stream=True)

        # Guardamos respuesta en el historial
        messages.append({"role": "assistant", "content": assistant_reply})


if __name__ == "__main__":
    chat_loop()

