import { execSync } from "child_process";
import { writeFileSync, readFileSync } from "fs";

// Read the HTML
const html = readFileSync("./OPENCLAW_MANUAL.html", "utf-8");

// Create a simple text version for WhatsApp
const textContent = `
🦞 OPENCLAW - MANUAL COMPLETO 🦞
================================

📱 CANALES:
✅ WhatsApp: +34692145043 (conectado)
❌ Discord: deshabilitado (necesita Message Content Intent)

🎤 AUDIO:
• Transcripción: OpenAI Whisper (whisper-1)
• Voz: OpenAI TTS (tts-1, voz alloy)
• Modo: responde con voz cuando recibe audio

🖼️ MEDIA:
✅ Imágenes (GPT-4o Vision)
✅ Videos
✅ Documentos (PDF, Excel, Word)

📦 25 SKILLS INSTALADOS:
1. youtube-mbo - "Resume este video: [URL]"
2. email-triage - "Revisa mis emails"
3. pr-reviewer - "Revisa este PR: [URL]"
4. ve-exchange-rates - "Tasa del dólar Venezuela"
5. twitter-sum/u7c - "¿Qué trending en Twitter?"
6. pdf-qdx/h65 - Envía PDF y pregunta
7. excel-orp - Envía Excel para análisis
8. browser-agent-* - "Abre [sitio] y haz [acción]"
9. coding-agent-* - "Escribe código para..."
10. grokipedia - "¿Qué es [concepto]?"
11. weeek-tasks - "Crea tarea en WEEEK"
12. moltbook-wrt - Red social MoltBook
13. molttok - Publicar en MoltTok
14. legacy-testimony - Dead Man's Switch
15. user-cognitive-profiles - Analizar perfil
16. whatsapp-* - Control avanzado WhatsApp
17. skills-security-check-* - Seguridad

🛠️ SKILLS PREINSTALADOS:
• weather - "¿Tiempo en Madrid?"
• openai-image-gen - "Genera imagen de..."
• tmux - "Ejecuta comando"
• skill-creator - "Crea skill para..."
• clawhub - "Instala skill [nombre]"
• bird - "Publica en Twitter"

💻 COMANDOS:
• Iniciar: pnpm openclaw gateway run
• Detener: pnpm openclaw gateway stop  
• Skills: npx clawhub list
• Instalar: npx clawhub install [nombre]

📁 ARCHIVOS:
• ~/.openclaw/openclaw.json - Config
• ~/.openclaw/agents/main/agent/auth-profiles.json - API keys

🚀 INICIO RÁPIDO:
1. cd ~/openclaw && pnpm openclaw gateway run &
2. pnpm openclaw node run &
3. Envía WhatsApp a +34692145043

📄 PDF completo en: ~/openclaw/OPENCLAW_MANUAL.html
(Abre en navegador y guarda como PDF)

Generado: 2 febrero 2026
`;

writeFileSync("./MANUAL_WHATSAPP.txt", textContent);
console.log("✅ Manual texto creado: MANUAL_WHATSAPP.txt");

// Try to send via WhatsApp using the whatsapp skill
console.log("Intentando enviar por WhatsApp...");
