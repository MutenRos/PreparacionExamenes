# OpenClaw — Personal AI Assistant (Upstream Public)

![OpenClaw Header](README-header.png)

## Introducción

**OpenClaw** es una plataforma **open-source** de asistente personal de inteligencia artificial que funciona en cualquier dispositivo y se comunica a través de más de 30 canales de mensajería — WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Microsoft Teams, Matrix, Nostr, y más. Este repositorio es la versión pública upstream del proyecto, que incluye un componente exclusivo: **Swabble**, un demonio de activación por voz construido con Swift 6.2 y Speech.framework para macOS 26. El monorepo TypeScript abarca CLI, Gateway WebSocket, panel de control web (Lit), apps nativas iOS/Android/macOS, sistema de plugins, contenedores Docker con sandboxing, y un marco de testing con Vitest. Es, en esencia, un proyecto que toca absolutamente todas las capas del desarrollo de software moderno.

---

## Desarrollo de las partes

### 1. Arquitectura CLI — Commander.js + Entry Point

El CLI es la puerta de entrada a todo OpenClaw. Soporta más de 20 subcomandos y se ejecuta con `openclaw <comando>`.

- **`src/entry.ts`** (líneas 1-60): Entry point real. Establece el título de proceso como "openclaw", instala filtros de warnings experimentales de Node.js, gestiona la normalización de argumentos en Windows, y re-spawn del proceso con las flags adecuadas.
- **`src/index.ts`** (líneas 1-94): Punto de entrada del módulo. Carga `.env`, normaliza el entorno, habilita captura de console, valida el runtime mínimo (Node 22+), y construye el programa CLI con `buildProgram()`.
- **`src/cli/program/build-program.ts`** (líneas 8-19): Crea el `Command` de Commander.js, configura la ayuda, registra hooks pre-acción, y delega el registro de todos los comandos.

```typescript
// src/index.ts — Arranque del CLI con validaciones de seguridad
loadDotEnv({ quiet: true });
normalizeEnv();
ensureOpenClawCliOnPath();
enableConsoleCapture();
assertSupportedRuntime();
const program = buildProgram();
```

### 2. Gateway WebSocket — Servidor Central

El **gateway** es el núcleo que conecta todos los clientes (CLI, web, móvil) con los canales de mensajería y el agente IA.

- **`src/gateway/server.impl.ts`** (591 líneas): `startGatewayServer()` inicializa la configuración, migra datos legacy, carga plugins, arranca canales, configura TLS/discovery/health checks, y levanta el servidor WebSocket.
- **`src/gateway/client.ts`** (líneas 83-99): Clase `GatewayClient` con reconexión automática (backoff exponencial), detección de stalls silenciosos cada 30s, y gestión de mensajes pendientes.
- **`src/gateway/boot.ts`** (líneas 20-32): Sistema de arranque automático que lee un archivo `BOOT.md` del workspace y ejecuta sus instrucciones a través del agente IA.

```typescript
// src/gateway/client.ts — Opciones del cliente WebSocket
export type GatewayClientOptions = {
  url?: string;              // ws://127.0.0.1:18789
  token?: string;            // Autenticación por token
  deviceIdentity?: DeviceIdentity;  // Firma criptográfica
  onEvent?: (evt: EventFrame) => void;
  onClose?: (code: number, reason: string) => void;
};
```

### 3. Sistema de Canales — Plugin Registry

Los canales son el mecanismo por el que OpenClaw recibe y envía mensajes. Cada canal es un plugin independiente.

- **`src/channels/plugins/index.ts`** (85 líneas): Registro central de canales. `listChannelPlugins()` descubre plugins desde el registry, los deduplica, y los ordena por prioridad.
- **`extensions/`**: Directorio con 29 plugins de canal como paquetes workspace independientes: whatsapp, telegram, discord, signal, slack, matrix, msteams, nostr, twitch, voice-call, zalo, bluebubbles, googlechat, line, mattermost, nextcloud-talk, y más.

```typescript
// src/channels/plugins/index.ts — Resolución de plugins de canal
export function listChannelPlugins(): ChannelPlugin[] {
  const combined = dedupeChannels(listPluginChannels());
  return combined.toSorted((a, b) => {
    const orderA = a.meta.order ?? (indexA === -1 ? 999 : indexA);
    return orderA !== orderB ? orderA - orderB : a.id.localeCompare(b.id);
  });
}
```

### 4. Panel de Control Web — Lit 3.3 + Vite 7

El **Control UI** es una aplicación web SPA construida con Web Components nativos usando **Lit**.

- **`ui/src/ui/app.ts`** (516 líneas): `OpenClawApp` extiende `LitElement` con más de 40 propiedades reactivas `@state` — chat, configuración, canales, cron, logs, sesiones, skills, tema visual.
- **`ui/src/ui/app-render.ts`** (1007 líneas): Renderizado completo de la UI con función `renderApp()` que compone todas las vistas.
- **`ui/src/styles/base.css`** (389 líneas): Design system completo con 80+ CSS Custom Properties que definen colores, sombras, tipografía, animaciones, stagger delays, y modo claro/oscuro.

```css
/* ui/src/styles/base.css — Tokens del sistema de diseño */
:root {
  --accent: #ff5c5c;       /* Rojo firma de OpenClaw */
  --accent-2: #14b8a6;     /* Teal secundario */
  --ok: #22c55e;            /* Éxito */
  --focus-ring: 0 0 0 2px var(--bg), 0 0 0 4px var(--ring);
}
```

### 5. Configuración Tipada — Zod + JSON5

El sistema de configuración garantiza que cada ajuste sea válido en tiempo de ejecución mediante **Zod schemas**.

- **`src/config/config.ts`**: Barrel que exporta `loadConfig`, `parseConfigJson5`, `writeConfigFile`, `validateConfigObject`, `migrateLegacyConfig`, y `OpenClawSchema`.
- **`src/config/types.ts`**: Más de 20 módulos de tipos especializados (`types.agents.ts`, `types.channels.ts`, `types.gateway.ts`, `types.whatsapp.ts`, `types.telegram.ts`, etc.) — cada uno para una sección de la configuración.
- **`src/config/zod-schema.ts`**: Esquema Zod completo con validación de todos los campos: booleanos opcionales, arrays de strings, números enteros no negativos, etc.

```typescript
// src/config/zod-schema.ts — Ejemplo de validación con Zod
mode: z.literal("efficient").optional(),
enabled: z.boolean().optional(),
allowProfiles: z.array(z.string()).optional(),
retentionDays: z.number().int().nonnegative().optional(),
```

### 6. Seguridad — Auditoría Multinivel (987 LOC)

OpenClaw integra un sistema de auditoría de seguridad que analiza toda la configuración y la infraestructura.

- **`src/security/audit.ts`** (987 líneas): Función `runSecurityAudit()` que genera un `SecurityAuditReport` con findings categorizados en `info`, `warn`, `critical`.
- Checks realizados: permisos de archivos, secretos en la configuración, higiene de modelos IA, riesgos de modelos pequeños, confianza de plugins, análisis del filesystem de estado, y sondeo profundo del gateway.

```typescript
// src/security/audit.ts — Estructura de hallazgos de seguridad
export type SecurityAuditFinding = {
  checkId: string;
  severity: "info" | "warn" | "critical";
  title: string;
  detail: string;
  remediation?: string;  // Instrucción para resolver
};
```

### 7. Docker — Producción, Sandbox y Sandbox-Browser

El proyecto incluye **tres Dockerfiles** para diferentes escenarios: producción, sandbox mínimo, y sandbox con navegador.

- **`Dockerfile`** (48 líneas): Build completo con Node 22 + Bun + pnpm, compilación backend/UI, hardening con usuario `node`, y HEALTHCHECK HTTP automático.
- **`Dockerfile.sandbox`** (17 líneas): Imagen mínima Debian Bookworm con herramientas básicas (bash, curl, git, jq, python3, ripgrep). Para ejecutar agentes en entornos aislados.
- **`docker-compose.yml`**: Dos servicios — `openclaw-gateway` con límites de recursos (2G RAM, 2 CPUs) y `openclaw-cli` con terminal interactiva.

```dockerfile
# Dockerfile — Seguridad: usuario non-root
USER node
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD node -e "const http=require('http');..."
```

### 8. Swabble — Demonio de Activación por Voz (Swift 6.2)

**Swabble** es un componente único de este repositorio: un demonio de wake-word construido en Swift para macOS 26, usando `Speech.framework` para reconocimiento de voz local (sin red).

- **`Swabble/Sources/swabble/main.swift`** (152 líneas): CLI principal con Commander. Registra los comandos (`serve`, `setup`, `doctor`, `health`, `mic`, `status`, `test-hook`, `transcribe`) y los despacha según el subcomando.
- **`Swabble/Sources/swabble/Commands/ServeCommand.swift`**: Demonio foreground que escucha el micrófono y activa el hook cuando detecta la wake-word "clawd".
- **`Swabble/README.md`**: Documentación del componente — compilación con SwiftPM, uso como librería (`SwabbleKit`), configuración de hooks.

```swift
// Swabble/Sources/swabble/main.swift — Despacho de comandos
switch sub {
case "mic":  try await dispatchMic(parsed: parsed, path: path)
case "service": try await dispatchService(path: path)
default:
    let handlers = swabbleHandlers(parsed: parsed)
    guard let handler = handlers[sub] else {
        throw CommanderProgramError.unknownSubcommand(command: "swabble", name: sub)
    }
    try await handler()
}
```

### 9. Utilidades y Normalización — E.164 y JID

Las utilidades centrales gestionan la normalización de datos esencial para las comunicaciones multicanal.

- **`src/utils.ts`** (339 líneas): `normalizeE164()` convierte cualquier formato de número al estándar internacional E.164. `toWhatsappJid()` genera JIDs de WhatsApp. `isSelfChatMode()` detecta el modo auto-chat cuando usuario y bot comparten número.
- **`src/globals.ts`** (57 líneas): Estado global tipado para verbose logging y modo confirmación automática (`--yes`). Integración directa con el subsistema de logging estructurado.

```typescript
// src/utils.ts — Detección de modo auto-chat
export function isSelfChatMode(
  selfE164: string | null | undefined,
  allowFrom?: Array<string | number> | null,
): boolean {
  const normalizedSelf = normalizeE164(selfE164);
  return allowFrom.some(n => normalizeE164(String(n)) === normalizedSelf);
}
```

### 10. Testing — Vitest + V8 Coverage + E2E

El framework de testing cubre tests unitarios, de integración, y end-to-end con una configuración sofisticada.

- **`vitest.config.ts`** (105 líneas): Configuración principal con detección automática de CI, ajuste de workers por plataforma (Windows: 2, CI Linux: 3, local: hasta 16), timeouts adaptados, y umbrales de cobertura V8 al 70%.
- **`vitest.e2e.config.ts`**, **`vitest.gateway.config.ts`**, **`vitest.live.config.ts`**: Configs especializadas para E2E, gateway, y tests live con claves reales.

```typescript
// vitest.config.ts — Workers adaptativos y umbrales
const isCI = process.env.CI === "true";
const localWorkers = Math.max(4, Math.min(16, os.cpus().length));
test: {
  pool: "forks",
  maxWorkers: isCI ? ciWorkers : localWorkers,
  coverage: { thresholds: { lines: 70, functions: 70 } }
}
```

---

## Presentación del proyecto

**OpenClaw** es una plataforma completa de asistente personal de IA que se ejecuta localmente. El usuario instala el paquete npm (`npm install -g openclaw`), ejecuta el asistente de configuración (`openclaw onboard`), y en minutos tiene un gateway operativo que conecta su agente IA con todos sus canales de mensajería.

El **flujo principal** funciona así: cualquier mensaje enviado al bot (por WhatsApp, Telegram, Discord, etc.) llega al Gateway WebSocket, pasa por el sistema de routing que identifica el canal y la sesión, se procesa mediante el agente IA con el modelo configurado (Anthropic Claude o OpenAI), y la respuesta se envía de vuelta al canal de origen. Todo esto se gestiona visualmente desde el **Control Panel** web, que muestra el chat en tiempo real, el estado de los canales, la configuración en vivo, tareas cron programadas, logs filtrados por nivel, y el marketplace de skills.

Lo que hace especial a este repositorio es la inclusión de **Swabble**: un demonio Swift nativo para macOS 26 que utiliza Speech.framework para detectar la wake-word "clawd" y activar el asistente por voz, sin enviar datos a ningún servidor — todo el reconocimiento de voz es local.

La **seguridad** permea todo el proyecto: autenticación del gateway, firma de dispositivos, auditoría automática de 987 líneas, ejecución en contenedores non-root, y un sandbox Docker dedicado para aislar la ejecución de agentes.

---

## Conclusión

**OpenClaw** demuestra que es posible construir un ecosistema completo de asistente IA personal que abarque desde la terminal hasta aplicaciones nativas, pasando por un panel web moderno. El proyecto destaca por su:

- **Alcance excepcional**: CLI + Gateway WebSocket + Web UI + Apps nativas (iOS/Android/macOS) + Demonio de voz (Swift)
- **Arquitectura extensible**: 29 plugins de canal como paquetes independientes, sistema de skills, y hooks configurables
- **Seguridad de nivel empresarial**: Auditoría automatizada, sandboxing Docker, autenticación por firma, ejecución non-root
- **Calidad de código**: TypeScript strict, Zod para validación en runtime, Vitest con 70% de cobertura V8, configs especializadas por entorno
- **Stack moderno**: Node 22+, Lit 3.3 Web Components, Vite 7, pnpm monorepo, Swift 6.2 con Speech.framework

La combinación de todas estas tecnologías en un monorepo coherente, mantenible, y documentado refleja un dominio integral del desarrollo de software actual — desde los protocolos de red hasta las interfaces de usuario, pasando por la seguridad, los tests y el despliegue en contenedores.
