# OpenClaw — Personal AI Assistant

![OpenClaw Logo](docs/images/openclaw-logo.png)

## Introducción

**OpenClaw** es una plataforma de asistente personal de inteligencia artificial de código abierto, diseñada como un sistema **multicanal** que conecta a un único agente IA con más de 30 canales de mensajería distintos — WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Microsoft Teams, Matrix, Nostr, y muchos más. La arquitectura se basa en un **monorepo TypeScript** con Node.js 22+, gestionado con pnpm, que abarca desde la CLI hasta aplicaciones nativas iOS/Android/macOS, pasando por un gateway WebSocket, un panel de control web construido con Lit Web Components y un sistema de plugins extensible. Este proyecto demuestra el dominio de prácticamente todas las capas del desarrollo de software moderno: desde Docker y despliegue en la nube hasta interfaces reactivas y seguridad de nivel empresarial.

---

## Desarrollo de las partes

### 1. Arquitectura CLI con Commander.js

El punto de entrada de OpenClaw es una interfaz de línea de comandos construida con **Commander.js**, que gestiona más de 20 subcomandos (gateway, agent, config, channels, doctor, etc.).

- **`src/cli/program/build-program.ts`** (línea 8): La función `buildProgram()` crea la instancia de Commander, configura el contexto global, registra los hooks de pre-acción y delega en `registerProgramCommands` la carga de todos los subcomandos.
- **`src/entry.ts`** (líneas 1-163): El entry point real del CLI. Gestiona la normalización de argumentos en Windows, la supresión de warnings experimentales de Node.js, el re-spawn del proceso si es necesario, y los perfiles CLI.

```typescript
// src/cli/program/build-program.ts — Construcción del programa CLI
export function buildProgram() {
  const program = new Command();
  const ctx = createProgramContext();
  configureProgramHelp(program, ctx);
  registerPreActionHooks(program, ctx.programVersion);
  registerProgramCommands(program, ctx, argv);
  return program;
}
```

### 2. Gateway WebSocket — El corazón del sistema

El **gateway** es el servidor central que orquesta todas las comunicaciones. Se implementa como un servidor WebSocket con autenticación por tokens, gestión de sesiones, catálogo de modelos de IA, sistema de cron, y canal de control.

- **`src/gateway/server.impl.ts`** (línea 155): `startGatewayServer()` — función asíncrona de ~480 líneas que inicializa todo: carga de configuración, migración legacy, registro de plugins, arranque de canales, health checks, TLS, discovery, y el servidor WebSocket.
- **`src/gateway/client.ts`** (líneas 83-99): La clase `GatewayClient` mantiene la conexión WebSocket con reconexión automática (backoff exponencial), detección de stalls, y secuenciación de mensajes.

```typescript
// src/gateway/client.ts — Cliente WebSocket con estado de conexión
export class GatewayClient {
  private ws: WebSocket | null = null;
  private pending = new Map<string, Pending>();
  private backoffMs = 1000;
  private closed = false;
  private lastSeq: number | null = null;
  private tickIntervalMs = 30_000; // Detección de stalls silenciosos
}
```

### 3. Sistema de Canales y Plugin Registry

La arquitectura de canales permite que OpenClaw se comunique a través de **30+ plataformas de mensajería** mediante un sistema de plugins unificado.

- **`src/channels/plugins/index.ts`** (líneas 12-52): `listChannelPlugins()` resuelve los canales desde el plugin registry, los deduplica, y los ordena según la prioridad definida en `CHAT_CHANNEL_ORDER`.
- **`extensions/`**: Directorio con 30+ plugins de canal como paquetes workspace (discord, telegram, whatsapp, signal, slack, matrix, msteams, nostr, voice-call, zalo, y más).

```typescript
// src/channels/plugins/index.ts — Registro unificado de canales
export function listChannelPlugins(): ChannelPlugin[] {
  const combined = dedupeChannels(listPluginChannels());
  return combined.toSorted((a, b) => {
    const orderA = a.meta.order ?? (indexA === -1 ? 999 : indexA);
    const orderB = b.meta.order ?? (indexB === -1 ? 999 : indexB);
    return orderA !== orderB ? orderA - orderB : a.id.localeCompare(b.id);
  });
}
```

### 4. Panel de Control Web — Lit Web Components + Vite

El **Control UI** es una aplicación web SPA construida con **Lit 3.3** (Web Components nativos), empaquetada con **Vite 7.3**, que permite gestionar toda la plataforma desde el navegador.

- **`ui/src/ui/app.ts`** (líneas 1-80): `OpenClawApp` extiende `LitElement` con más de 40 propiedades reactivas (`@state`), gestionando el estado de chat, configuración, canales, cron jobs, logs, sesiones, skills y más.
- **`ui/src/ui/app-render.ts`** (1007 líneas): El render principal que compone las vistas de chat, configuración, canales, agents, nodes, skills, logs, etc.
- **`ui/src/styles/base.css`** (líneas 1-60): Sistema de design tokens con CSS Custom Properties — más de 80 variables que definen el tema completo (colores, sombras, tipografía, animaciones).

```css
/* ui/src/styles/base.css — Design System con Custom Properties */
:root {
  --bg: #12141a;
  --accent: #ff5c5c;
  --accent-2: #14b8a6;
  --ok: #22c55e;
  --text: #e4e4e7;
  /* + 80 variables más para todo el sistema visual */
}
```

### 5. Configuración Tipada con Zod

El sistema de configuración utiliza **Zod** para la validación de esquemas, soporta **JSON5**, y gestiona la migración automática de configuraciones legacy.

- **`src/config/config.ts`**: Barrel module que exporta `loadConfig`, `parseConfigJson5`, `writeConfigFile`, `validateConfigObject`, y el esquema `OpenClawSchema`.
- **`src/config/zod-schema.ts`** (línea 17+): Esquema Zod completo con tipos fuertemente tipados para todas las secciones: agents, channels (whatsapp, telegram, discord, etc.), gateway, hooks, cron, plugins, security, memory, TTS, y más.
- **`src/config/types.ts`**: Los tipos se dividen en más de 20 módulos especializados (`types.agents.ts`, `types.channels.ts`, `types.gateway.ts`, etc.) para mantener cada archivo conciso.

```typescript
// src/config/config.ts — API centralizada de configuración
export { loadConfig, parseConfigJson5, writeConfigFile } from "./io.js";
export { migrateLegacyConfig } from "./legacy-migrate.js";
export { validateConfigObject } from "./validation.js";
export { OpenClawSchema } from "./zod-schema.js";
```

### 6. Seguridad — Auditoría Multinivel

OpenClaw incluye un sistema de **auditoría de seguridad** completo que analiza la configuración, los permisos del sistema de archivos, la exposición del gateway, los hooks, y la superficie de ataque.

- **`src/security/audit.ts`** (987 líneas): Implementa `runSecurityAudit()` que genera un `SecurityAuditReport` con findings categorizados en tres niveles de severidad: `info`, `warn`, `critical`.
- Las verificaciones incluyen: permisos de archivos de estado, secretos en configuración, higiene de modelos IA, riesgos de modelos pequeños, confianza de plugins, y sondeo profundo del gateway.

```typescript
// src/security/audit.ts — Sistema de auditoría de seguridad
export type SecurityAuditFinding = {
  checkId: string;
  severity: "info" | "warn" | "critical";
  title: string;
  detail: string;
  remediation?: string;
};
export async function runSecurityAudit(opts: SecurityAuditOptions): Promise<SecurityAuditReport>;
```

### 7. Containerización — Docker y Docker Compose

La plataforma está completamente containerizada con una imagen Docker basada en **Node 22 (Bookworm)**, con builds multi-stage, usuario non-root, y orquestación con Docker Compose.

- **`Dockerfile`** (48 líneas): Build completo con pnpm + Bun, compilación del backend y del UI, hardening de seguridad (user `node`), y HEALTHCHECK automático.
- **`docker-compose.yml`**: Define dos servicios — `openclaw-gateway` (servidor con límites de recursos) y `openclaw-cli` (terminal interactiva), con volúmenes para configuración y workspace persistentes.

```dockerfile
# Dockerfile — Security hardening + health check
USER node
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD node -e "const http=require('http');const r=http.get('http://127.0.0.1:18789/health',{timeout:4000},s=>{process.exit(s.statusCode===200?0:1)});r.on('error',()=>process.exit(1))"
CMD ["node", "dist/index.js", "gateway", "--allow-unconfigured"]
```

### 8. Utilidades y Normalización de Datos

El módulo de utilidades (`src/utils.ts`, 339 líneas) contiene funciones críticas para la normalización de números de teléfono, generación de JIDs de WhatsApp, y la lógica de detección de "self-chat mode".

- **`src/utils.ts`** (líneas 44-72): `normalizeE164()` normaliza números de teléfono al formato E.164 internacional, y `isSelfChatMode()` detecta cuando el usuario y el bot comparten el mismo número de WhatsApp.
- **`src/globals.ts`** (57 líneas): Estado global tipado para verbose logging y confirmación automática, con integración directa con el subsistema de logging.

```typescript
// src/utils.ts — Normalización E.164 para comunicaciones
export function normalizeE164(number: string): string {
  const withoutPrefix = number.replace(/^whatsapp:/, "").trim();
  const digits = withoutPrefix.replace(/[^\d+]/g, "");
  return digits.startsWith("+") ? `+${digits.slice(1)}` : `+${digits}`;
}
```

### 9. Boot System — Automatización al Arranque

El sistema de **boot** permite ejecutar instrucciones automatizadas cuando el gateway arranca, leyendo un archivo `BOOT.md` y delegando su ejecución al agente IA.

- **`src/gateway/boot.ts`** (100 líneas): `runBootOnce()` carga el archivo BOOT.md, construye un prompt especializado, y ejecuta el comando `agentCommand` con la sesión principal. Si el archivo ordena enviar mensajes, el agente los envía a los canales correspondientes.

```typescript
// src/gateway/boot.ts — Ejecución automática de instrucciones al arranque
function buildBootPrompt(content: string) {
  return [
    "You are running a boot check. Follow BOOT.md instructions exactly.",
    "", "BOOT.md:", content, "",
    "If BOOT.md asks you to send a message, use the message tool.",
    `After sending, reply with ONLY: ${SILENT_REPLY_TOKEN}.`,
  ].join("\n");
}
```

### 10. Aplicaciones Nativas Multiplataforma

OpenClaw incluye **aplicaciones nativas** para iOS, Android y macOS, con código compartido en el directorio `apps/shared/`.

- **`apps/ios/`**: Aplicación Swift/SwiftUI con framework `Observation` para gestión de estado reactivo.
- **`apps/android/`**: Aplicación Kotlin con Gradle (versionName sincronizado con el CLI).
- **`apps/macos/`**: App de barra de menús que ejecuta el gateway como proceso local, con notarización para distribución.
- **`apps/shared/`**: Lógica compartida entre las tres plataformas (protocolo de gateway, autenticación de dispositivos, schemas).

---

## Presentación del proyecto

**OpenClaw** es, en esencia, un hub de inteligencia artificial personal. Imagina tener un asistente IA que puedas alcanzar desde cualquier plataforma — escribiéndole por WhatsApp desde el móvil, por Telegram desde el ordenador, por Discord en tu servidor de gaming, o directamente desde la terminal con el CLI.

El flujo de trabajo completo funciona así: el usuario instala OpenClaw y ejecuta `openclaw gateway` para levantar el servidor. Se abre automáticamente el **Control Panel** (web UI) donde se configuran los canales deseados (escanear QR de WhatsApp, introducir token de Telegram, conectar bot de Discord). Una vez configurados, cualquier mensaje enviado a estos canales es recibido por el gateway, procesado por el agente IA, y la respuesta se envía de vuelta al canal correspondiente.

El **panel de control web** ofrece una vista completa del sistema: chat en tiempo real con streaming, configuración visual de todos los parámetros, gestión de canales con estado en vivo, programación de tareas cron, visor de logs con filtros por nivel, gestión de sesiones y agents, marketplace de skills, y un sistema de aprobación de ejecución de comandos para máxima seguridad.

La **seguridad** está presente en cada capa: autenticación por tokens en el gateway, perfiles de dispositivo con firma criptográfica, auditoría automática de la configuración, ejecución en contenedores Docker como usuario non-root, y un sistema de pairing para autorizar nuevos dispositivos.

El sistema de **plugins/extensiones** permite añadir nuevos canales de comunicación sin modificar el core — cada extensión es un paquete workspace independiente que se registra en el plugin registry. Esto permite que la comunidad contribuya nuevos canales (como Nostr, Twitch, MS Teams, o una extensión de voz) siguiendo una interfaz uniforme.

---

## Conclusión

**OpenClaw** representa un proyecto de ingeniería de software de alcance extraordinario. No se trata de una aplicación web típica — es una **plataforma completa** que abarca CLI, servidor WebSocket, aplicaciones nativas para tres plataformas, una web app SPA con Web Components, un sistema de plugins, containerización Docker, seguridad multinivel, y soporte para más de 30 canales de comunicación.

Los pilares técnicos del proyecto son:
- **TypeScript strict** de principio a fin, con Zod para validación en runtime
- **Arquitectura de plugins** que permite escalar los canales sin tocar el core
- **Lit Web Components** para una UI moderna, reactiva y estándar del navegador
- **Docker + security hardening** para despliegue reproducible y seguro
- **Monorepo pnpm** con workspace packages que mantiene el código organizado
- **Testing con Vitest** (cobertura V8 al 70%) y tests e2e reales contra los canales

Este proyecto demuestra que es posible construir una plataforma de asistente IA completa, desde la terminal hasta el móvil, manteniendo la calidad del código, la seguridad, y la extensibilidad como prioridades. La combinación de un gateway WebSocket robusto, un sistema de canales extensible, y aplicaciones nativas multiplataforma muestra un dominio integral del stack tecnológico moderno.
