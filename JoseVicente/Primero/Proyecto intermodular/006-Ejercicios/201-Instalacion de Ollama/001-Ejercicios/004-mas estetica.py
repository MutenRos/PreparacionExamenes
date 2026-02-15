import requests
import json
import time
import sys
import shutil

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"


# ================================
# DECORACIÓN ANSI + BUBBLES
# ================================
RESET   = "\033[0m"
BOLD    = "\033[1m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
MAGENTA = "\033[95m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
GRAY    = "\033[90m"
WHITE   = "\033[97m"

USER_AVATAR = f"{CYAN}🧑‍💻 Tú{RESET}"
BOT_AVATAR  = f"{MAGENTA}🤖 IA{RESET}"

def bubble(text, color):
    """
    Crea una burbuja ASCII con el texto dentro.
    """
    width = shutil.get_terminal_size().columns - 4
    wrapped = []
    line = ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            wrapped.append(line)
            line = ""
        line += word + " "
    if line:
        wrapped.append(line)

    top = f"{color}┌" + "─" * (width) + f"┐{RESET}"
    bottom = f"{color}└" + "─" * (width) + f"┘{RESET}"

    body = "\n".join(
        f"{color}│{RESET} {w.ljust(width-1)}{color}│{RESET}"
        for w in wrapped
    )

    return f"{top}\n{body}\n{bottom}"


def typing_effect(text):
    """
    Imprime un texto con efecto "typing".
    """
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.004)
    print()


# ================================
# PETICIÓN A OLLAMA (STREAMING)
# ================================
def call_ollama(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": True
    }

    response = requests.post(OLLAMA_URL, json=payload, stream=True)
    response.raise_for_status()

    full = ""

    for line in response.iter_lines():
        if not line:
            continue
        data = json.loads(line.decode("utf-8"))

        if "message" in data and "content" in data["message"]:
            chunk = data["message"]["content"]
            full += chunk
            typing_effect(chunk)

        if data.get("done"):
            break

    return full


# ================================
# LOOP PRINCIPAL
# ================================
def chat():
    messages = []

    print(f"""
{MAGENTA}{BOLD}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ⭐ Bienvenido al SUPER-CHAT de OLLAMA ⭐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Modelo: {MODEL}
Escribe "salir" para terminar.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{RESET}
""")

    while True:
        user = input(f"{USER_AVATAR} > ").strip()

        if user.lower() in ("salir", "exit", "quit"):
            print(f"{YELLOW}👋 Saliendo... ¡Hasta la próxima!{RESET}")
            break

        # Mostrar mensaje del usuario en burbuja
        print(bubble(user, CYAN))

        # Añadir al historial
        messages.append({"role": "user", "content": user})

        # Mostrar que la IA está escribiendo
        print(f"{BOT_AVATAR} {GRAY}está escribiendo...{RESET}\n")

        # Obtener respuesta
        answer = call_ollama(messages)

        # Mostrar burbuja de respuesta
        print(bubble(answer, MAGENTA))

        # Guardarla en el historial
        messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    chat()

