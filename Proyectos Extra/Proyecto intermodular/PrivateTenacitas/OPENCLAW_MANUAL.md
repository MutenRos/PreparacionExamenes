# 🦞 OpenClaw - Manual Completo

## Información del Sistema

- **Versión**: 2026.2.1
- **Modelo IA**: OpenAI GPT-4o
- **Usuario**: dario
- **WhatsApp**: +34692145043

---

## 📱 Canales Configurados

### WhatsApp ✅

- **Estado**: Conectado y funcionando
- **Número**: +34692145043
- **Modo**: Self-chat habilitado (puedes hablarte a ti mismo)
- **Políticas**: DM allowlist, Groups allowlist

### Discord ❌

- **Estado**: Deshabilitado
- **Razón**: Necesita "Message Content Intent" en Discord Developer Portal
- **Para habilitar**:
  1. Ve a https://discord.com/developers/applications
  2. Selecciona tu bot
  3. Ve a "Bot" → Habilita "Message Content Intent"
  4. Ejecuta: `pnpm openclaw config set channels.discord.enabled true`

---

## 🎤 Funciones de Audio

### Transcripción de Audio (Speech-to-Text)

- **Proveedor**: OpenAI Whisper
- **Modelo**: whisper-1
- **Cómo usar**: Envía un mensaje de voz por WhatsApp y se transcribirá automáticamente

### Respuesta con Voz (Text-to-Speech)

- **Proveedor**: OpenAI TTS
- **Modelo**: tts-1
- **Voz**: alloy (neutral)
- **Modo**: `inbound` - responde con voz cuando recibe audio
- **Cómo usar**: Envía un audio y recibirás la respuesta también como audio

---

## 🖼️ Procesamiento de Media

### Imágenes

- **Estado**: ✅ Habilitado
- **Modelo**: GPT-4o Vision
- **Cómo usar**: Envía una imagen y pregunta sobre ella

### Videos

- **Estado**: ✅ Habilitado
- **Cómo usar**: Envía un video corto para análisis

### Documentos

- **Formatos soportados**: PDF, Excel, Word
- **Requiere**: Skills de pdf-_ o excel-_ instalados

---

## 📦 Skills Instalados desde ClawHub

### youtube-mbo

**Descripción**: Resumir videos de YouTube, extraer transcripciones
**Uso**: "Resume este video de YouTube: [URL]"

### email-triage

**Descripción**: Clasificar emails con IA vía IMAP
**Uso**: "Revisa mis emails y clasifícalos por prioridad"
**Configuración requerida**: Credenciales IMAP

### pr-reviewer

**Descripción**: Review automático de Pull Requests en GitHub
**Uso**: "Revisa este PR: [URL]"

### ve-exchange-rates

**Descripción**: Tasas de cambio de Venezuela (BCV oficial)
**Uso**: "¿Cuál es la tasa del dólar en Venezuela?"

### twitter-sum / twitter-u7c

**Descripción**: Monitorear X/Twitter, trends, búsquedas
**Uso**: "¿Qué está trending en Twitter?" o "Busca tweets sobre [tema]"

### pdf-qdx / pdf-h65

**Descripción**: Trabajar con archivos PDF
**Uso**: Envía un PDF y pregunta sobre su contenido

### excel-orp

**Descripción**: Trabajar con archivos Excel
**Uso**: Envía un Excel y pide análisis o modificaciones

### browser-agent-\*

**Descripción**: Automatización de navegador web
**Uso**: "Abre [sitio web] y haz [acción]"

### coding-agent-\*

**Descripción**: Tareas de programación
**Uso**: "Escribe código para [tarea]" o "Arregla este bug"

### grokipedia

**Descripción**: Búsqueda de información tipo Wikipedia
**Uso**: "¿Qué es [concepto]?"

### weeek-tasks

**Descripción**: Gestión de tareas WEEEK
**Uso**: "Crea una tarea en WEEEK" (requiere API key)

### moltbook-wrt

**Descripción**: Red social MoltBook para agentes IA
**Uso**: Interacción con la red social MoltBook

### molttok

**Descripción**: Publicar arte en MoltTok (estilo TikTok)
**Uso**: "Publica en MoltTok"

### legacy-testimony-skill

**Descripción**: Dead Man's Switch - mensajes programados
**Uso**: Configurar mensajes que se envíen automáticamente

### user-cognitive-profiles

**Descripción**: Analizar exportaciones de ChatGPT
**Uso**: "Analiza mi perfil cognitivo"

### whatsapp-guf / whatsapp-qgs

**Descripción**: Control avanzado de WhatsApp
**Uso**: "Envía un mensaje de WhatsApp a [contacto]"

### skills-security-check-\*

**Descripción**: Operaciones de seguridad
**Uso**: "Verifica la seguridad de [sistema]"

---

## 🔧 Skills Bundled (Preinstalados)

### weather 🌤️

**Uso**: "¿Qué tiempo hace en Madrid?"

### openai-image-gen 🖼️

**Uso**: "Genera una imagen de [descripción]"

### openai-whisper-api ☁️

**Uso**: Automático para transcripción de audio

### tmux 🧵

**Uso**: "Ejecuta [comando] en tmux"

### oracle 🧿

**Uso**: Ejecutar prompts con archivos adjuntos

### skill-creator 📦

**Uso**: "Crea un nuevo skill para [funcionalidad]"

### clawhub 📦

**Uso**: "Instala el skill [nombre]"

### mcporter 📦

**Uso**: Integración con servidores MCP

### bird 🐦

**Uso**: "Publica en Twitter: [mensaje]"

### bluebubbles 📦

**Uso**: iMessage via BlueBubbles (requiere macOS)

---

## 💻 Comandos de Terminal

### Iniciar Gateway

```bash
cd ~/openclaw && pnpm openclaw gateway run
```

### Detener Gateway

```bash
cd ~/openclaw && pnpm openclaw gateway stop
```

### Iniciar Node Host (para skills)

```bash
cd ~/openclaw && pnpm openclaw node run
```

### Ver configuración

```bash
cat ~/.openclaw/openclaw.json
```

### Modificar configuración

```bash
pnpm openclaw config set [ruta] [valor]
```

### Ver skills disponibles

```bash
pnpm openclaw skills list
```

### Instalar skill de ClawHub

```bash
npx clawhub install [nombre-skill]
```

### Buscar skills

```bash
npx clawhub search "[término]"
```

### Explorar skills recientes

```bash
npx clawhub explore
```

---

## 📁 Archivos Importantes

| Archivo                                            | Descripción             |
| -------------------------------------------------- | ----------------------- |
| `~/.openclaw/openclaw.json`                        | Configuración principal |
| `~/.openclaw/agents/main/agent/auth-profiles.json` | API keys                |
| `~/.openclaw/.env`                                 | Variables de entorno    |
| `/tmp/openclaw/openclaw-*.log`                     | Logs del gateway        |
| `~/openclaw/skills/`                               | Skills instalados       |

---

## 🔑 API Keys Configuradas

### OpenAI

- **Ubicación**: `~/.openclaw/agents/main/agent/auth-profiles.json`
- **Usos**: GPT-4o, Whisper, TTS, DALL-E

---

## 🚀 Inicio Rápido

1. **Iniciar el sistema**:

```bash
cd ~/openclaw
pnpm openclaw gateway run &
pnpm openclaw node run &
```

2. **Enviar mensaje por WhatsApp** a tu propio número

3. **Probar funciones**:
   - Texto: "Hola, ¿qué puedes hacer?"
   - Audio: Envía un mensaje de voz
   - Imagen: Envía una foto y pregunta sobre ella
   - YouTube: "Resume este video: [URL]"
   - Clima: "¿Qué tiempo hace en [ciudad]?"

---

## ❓ Solución de Problemas

### El gateway no inicia

```bash
pnpm openclaw gateway stop
kill -9 $(lsof -t -i:18789)
pnpm openclaw gateway run
```

### No responde mensajes de WhatsApp

- Verifica que el gateway esté corriendo
- Revisa los logs: `tail -f /tmp/openclaw/openclaw-*.log`

### No transcribe audios

- Verifica configuración: `cat ~/.openclaw/openclaw.json | grep -A5 "audio"`
- Debe tener `tools.media.audio.enabled: true`

### No responde con voz

- Verifica TTS: `cat ~/.openclaw/openclaw.json | grep -A10 "tts"`
- Debe tener `messages.tts.auto: "inbound"`

---

## 📞 Soporte

- **Repositorio**: https://github.com/openclaw/openclaw
- **ClawHub**: https://clawhub.com

---

_Generado automáticamente el 2 de febrero de 2026_
