#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import textwrap

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"

# ====== ANSI COLORS & STYLES ======
RESET = "\033[0m"
BOLD = "\033[1m"

FG_CYAN = "\033[36m"
FG_GREEN = "\033[32m"
FG_YELLOW = "\033[33m"
FG_MAGENTA = "\033[35m"
FG_WHITE = "\033[97m"
FG_RED = "\033[31m"
FG_BLUE = "\033[34m"

DIM = "\033[2m"

# ====== BOXED OUTPUT ======

BOX_WIDTH = 100  # ancho interior de la caja


def wrap_text_preserving_paragraphs(text, width):
    """
    Envuelve el texto respetando saltos de línea.
    Cada línea se wrappea por separado.
    """
    text = text.replace("\r\n", "\n")
    paragraphs = text.split("\n")
    result_lines = []
    for p in paragraphs:
        if not p.strip():
            # línea en blanco -> separador
            result_lines.append("")
        else:
            result_lines.extend(textwrap.wrap(p, width=width))
    return result_lines


def print_box(text, color=FG_WHITE):
    """
    Muestra el texto dentro de una caja con bordes ASCII bonitos.
    No mezclar ANSI dentro del texto para que el padding salga bien.
    """
    lines = wrap_text_preserving_paragraphs(text, BOX_WIDTH)
    top = f"{color}┌{'─' * BOX_WIDTH}┐{RESET}"
    bottom = f"{color}└{'─' * BOX_WIDTH}┘{RESET}"

    print(top)
    for line in lines:
        # Rellenamos con espacios a la derecha hasta BOX_WIDTH
        padded = line.ljust(BOX_WIDTH)
        print(f"{color}│{RESET} {padded[:BOX_WIDTH-1]}{color}│{RESET}")
    print(bottom)


# ====== OLLAMA CALL ======

def call_ollama(messages):
    """
    Llama a Ollama en localhost usando /api/chat sin streaming,
    y devuelve el texto completo de la respuesta.
    """
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False  # -> recibimos una sola respuesta JSON
    }

    resp = requests.post(OLLAMA_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()

    return data["message"]["content"]


# ====== UI HELPERS ======

def clear_last_line():
    """Borra la última línea en consola (para quitar 'IA está escribiendo...')."""
    # Mover el cursor una línea arriba y limpiar esa línea
    print("\x1b[1A\x1b[2K", end="")


def print_header():
    print(f"{FG_CYAN}{BOLD}╔═══════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{FG_CYAN}{BOLD}║   💬 Chat local con Ollama ({MODEL})                                  ║{RESET}")
    print(f"{FG_CYAN}{BOLD}║   🔗 Endpoint: http://localhost:11434/api/chat                        ║{RESET}")
    print(f"{FG_CYAN}{BOLD}╚═══════════════════════════════════════════════════════════════════════╝{RESET}")
    print()
    print(f"{DIM}Escribe 'salir', 'exit' o 'quit' para terminar.{RESET}\n")


# ====== MAIN CHAT LOOP ======

def chat_loop():
    messages = []
    print_header()

    while True:
        try:
            user_input = input(f"{FG_GREEN}🧑‍💻 Tú > {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{FG_YELLOW}👋 Saliendo del chat...{RESET}")
            break

        if user_input.lower() in ("salir", "exit", "quit"):
            print(f"{FG_YELLOW}👋 Saliendo del chat...{RESET}")
            break

        if not user_input:
            continue

        # Mostrar lo que ha escrito el usuario en una caja verde
        print_box(user_input, color=FG_GREEN)

        # Añadimos el mensaje del usuario al historial
        messages.append({"role": "user", "content": user_input})

        # Indicamos que la IA está pensando
        print(f"{FG_YELLOW}🤖 IA está escribiendo...{RESET}")

        try:
            assistant_reply = call_ollama(messages)
        except Exception as e:
            clear_last_line()
            error_msg = f"⚠️ Error al llamar a Ollama: {e}"
            print_box(error_msg, color=FG_RED)
            # No añadimos mensaje de assistant al historial si ha fallado
            continue

        # Borramos la línea de "IA está escribiendo..."
        clear_last_line()

        # Guardamos la respuesta en el historial
        messages.append({"role": "assistant", "content": assistant_reply})

        # Mostramos la respuesta en una caja azul/cian
        print_box(assistant_reply, color=FG_CYAN)


if __name__ == "__main__":
    chat_loop()

