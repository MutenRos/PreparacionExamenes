const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");

// Contador de mensajes enviados
let messageCount = 0;

function el(tag, cls) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  return n;
}

function addMessage(role, text) {
  // Remove initial hint the first time a real message is added
  const hint = chat.querySelector(".hint");
  if (hint) hint.remove();

  const row = el("div", `msg ${role}`);
  const avatar = el("div", "avatar");
  avatar.textContent = role === "user" ? "USR" : "AI";

  const bubble = el("div", "bubble");
  bubble.textContent = text;

  row.appendChild(avatar);
  row.appendChild(bubble);
  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;

  return { row, bubble };
}

function setTyping(on) {
  if (on) {
    const m = addMessage("assistant", "…");
    m.bubble.classList.add("typing");
    m.row.dataset.typing = "1";
  } else {
    const t = chat.querySelector('[data-typing="1"]');
    if (t) t.remove();
  }
}

function autosize() {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 180) + "px";
}

async function send() {
  const msg = (input.value || "").trim();
  if (!msg) return;

  addMessage("user", msg);
  messageCount++;
  input.value = "";
  autosize();

  setTyping(true);
  sendBtn.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    setTyping(false);

    if (!data.ok) {
      addMessage("assistant", `Error: ${data.error || "unknown"}`);
      return;
    }

    addMessage("assistant", data.answer || "");
  } catch (e) {
    setTyping(false);
    addMessage("assistant", `Error: ${String(e)}`);
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

sendBtn.addEventListener("click", send);
clearBtn.addEventListener("click", () => {
  chat.innerHTML = '<div class="hint">Escribe una pregunta y pulsa <b>Enviar</b>. Usa <b>Shift+Enter</b> para salto de línea.</div>';
  messageCount = 0;
  input.focus();
});

input.addEventListener("input", autosize);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    send();
  }
});

autosize();
input.focus();

