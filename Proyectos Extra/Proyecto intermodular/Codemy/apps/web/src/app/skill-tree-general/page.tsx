'use client';

import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import Link from 'next/link';

// ═══════════════════════════════════════════════════════════════
// SISTEMA 8-BIT AAA - Todos los píxeles tamaño uniforme
// ═══════════════════════════════════════════════════════════════
const PX = 4; // Tamaño de cada píxel del juego (4x4 píxeles reales)
const TILE = 32;
const MW = 160, MH = 120;
const CHUNK = 256;
const CENTER_X = 80, CENTER_Y = 60;

// Paleta 8-bit NES style - colores limitados y vibrantes
const PAL8 = {
  // Hierba - tonos suaves y cercanos
  G0: '#287028', G1: '#308030', G2: '#388838', G3: '#409040',
  // Agua  
  W0: '#101850', W1: '#182868', W2: '#204080', W3: '#3060a0',
  // Arena
  S0: '#a08040', S1: '#c0a050', S2: '#d8b860',
  // Piedra
  R0: '#303030', R1: '#484848', R2: '#606060', R3: '#787878', R4: '#909090',
  // Madera
  B0: '#301808', B1: '#482810', B2: '#603818', B3: '#784820',
  // Piel
  K0: '#c08060', K1: '#d8a080', K2: '#f0c0a0',
  // Rojo
  X0: '#800000', X1: '#b00020', X2: '#d80040', X3: '#f01060',
  // Azul
  U0: '#000080', U1: '#0020b0', U2: '#0040d8', U3: '#2060f0',
  // Oro
  Y0: '#806000', Y1: '#a08000', Y2: '#c0a000', Y3: '#e0c020',
  // Púrpura
  P0: '#400060', P1: '#602090', P2: '#8040c0',
  // Blanco/Negro
  BK: '#000000', WH: '#f0f0f0', GY: '#808080',
};

interface Dungeon {
  id: string; title: string; desc: string; href: string;
  x: number; y: number;
  diff: 'beginner' | 'intermediate' | 'advanced' | 'legendary';
  icon: string; enemies: number; boss: string; xp: number;
}

interface NPC {
  id: string; name: string; role: string; x: number; y: number;
  dialog: string; quest?: string; sprite: string;
}

// Mazmorras en anillos concéntricos alrededor de la fortaleza
// Posiciones calculadas para estar en tierra firme con progresión lógica
const DUNGEONS: Dungeon[] = [
  // Beginner - cerca de fortaleza, fácil acceso
  { id: 'intro', title: 'Bosque del Código', desc: 'Tu primera mazmorra', href: '/intro-programacion', x: CENTER_X - 20, y: CENTER_Y - 15, diff: 'beginner', icon: '🌲', enemies: 8, boss: 'Slime del Syntax', xp: 500 },
  { id: 'discord', title: 'Salón de los Bots', desc: 'Crea bots de Discord', href: '/discord-bot', x: CENTER_X + 20, y: CENTER_Y - 15, diff: 'beginner', icon: '🤖', enemies: 10, boss: 'Bot Rebelde', xp: 800 },
  { id: 'streaming', title: 'Arena del Streaming', desc: 'OBS y monetización', href: '/streaming', x: CENTER_X, y: CENTER_Y + 20, diff: 'beginner', icon: '🎥', enemies: 6, boss: 'Troll del Chat', xp: 400 },
  
  // Intermediate - anillo medio
  { id: 'python', title: 'Caverna de Python', desc: 'Python hasta IA', href: '/skill-tree-python', x: CENTER_X + 40, y: CENTER_Y - 25, diff: 'intermediate', icon: '🐍', enemies: 15, boss: 'Serpiente Ancestral', xp: 1500 },
  { id: 'web', title: 'Castillo del Frontend', desc: 'HTML, CSS, React', href: '/skill-tree-web', x: CENTER_X + 45, y: CENTER_Y + 15, diff: 'intermediate', icon: '🏰', enemies: 20, boss: 'Coloso del DOM', xp: 2000 },
  { id: 'minecraft', title: 'Mina de Minecraft', desc: 'Mods con Java', href: '/minecraft-mods', x: CENTER_X - 40, y: CENTER_Y + 25, diff: 'intermediate', icon: '⛏️', enemies: 12, boss: 'Creeper Legendario', xp: 1200 },
  { id: 'arduino', title: 'Taller del Inventor', desc: 'Arduino y ESP32', href: '/skill-tree-arduino', x: CENTER_X - 45, y: CENTER_Y - 20, diff: 'intermediate', icon: '🔌', enemies: 14, boss: 'Corto Circuito', xp: 1400 },
  
  // Advanced - anillo exterior
  { id: 'java', title: 'Torre del Backend', desc: 'Java y Spring Boot', href: '/skill-tree-java', x: CENTER_X + 60, y: CENTER_Y, diff: 'advanced', icon: '☕', enemies: 25, boss: 'Guardián de Beans', xp: 2500 },
  { id: 'devops', title: 'Cielos de la Nube', desc: 'Docker, K8s, CI/CD', href: '/skill-tree-devops', x: CENTER_X - 60, y: CENTER_Y, diff: 'advanced', icon: '☁️', enemies: 22, boss: 'Titán del Deploy', xp: 2200 },
  
  // Legendary - extremos del mapa
  { id: 'cpp', title: 'Volcán del Rendimiento', desc: 'C++ puro', href: '/skill-tree-cpp', x: CENTER_X - 65, y: CENTER_Y + 40, diff: 'legendary', icon: '🔥', enemies: 30, boss: 'Demonio Memory Leak', xp: 5000 },
  { id: 'hacking', title: 'Abismo del Hacking', desc: 'Hacking ético', href: '/hacking-wifi', x: CENTER_X + 65, y: CENTER_Y - 40, diff: 'legendary', icon: '💀', enemies: 35, boss: 'Hacker Oscuro', xp: 6000 },
];

// NPCs en la fortaleza central
const NPCS: NPC[] = [
  { id: 'tabernero', name: 'Bartolo', role: 'Tabernero', x: CENTER_X - 6, y: CENTER_Y + 4, dialog: '¡Bienvenido viajero! ¿Una cerveza antes de la aventura?', quest: 'intro', sprite: 'tavern' },
  { id: 'herrero', name: 'Vulkan', role: 'Herrero', x: CENTER_X + 6, y: CENTER_Y + 4, dialog: 'El acero se forja con paciencia... como el código.', quest: 'python', sprite: 'smith' },
  { id: 'mago', name: 'Archimago Codex', role: 'Sabio', x: CENTER_X, y: CENTER_Y - 5, dialog: 'Los antiguos frameworks guardan secretos...', quest: 'web', sprite: 'mage' },
  { id: 'capitan', name: 'Capitán Rex', role: 'Guardia', x: CENTER_X - 10, y: CENTER_Y, dialog: 'Las mazmorras no esperan. ¡Prepárate!', quest: 'discord', sprite: 'guard' },
  { id: 'mercader', name: 'Luna', role: 'Mercader', x: CENTER_X + 10, y: CENTER_Y, dialog: 'Tengo recursos exóticos de todos los repos...', quest: 'streaming', sprite: 'merchant' },
];

// Caminos que conectan mazmorras - progresión lógica
// [origen, destino] - se dibujan como caminos de tierra
const PATHS: [string, string][] = [
  // Desde fortaleza a beginners
  ['fort', 'intro'],
  ['fort', 'discord'],
  ['fort', 'streaming'],
  // Beginners a intermediates
  ['intro', 'arduino'],
  ['discord', 'python'],
  ['streaming', 'minecraft'],
  ['streaming', 'web'],
  // Intermediates a advanced
  ['python', 'java'],
  ['web', 'java'],
  ['arduino', 'devops'],
  ['minecraft', 'devops'],
  // Advanced a legendary
  ['java', 'hacking'],
  ['devops', 'cpp'],
];

// Obtener posición de un nodo (mazmorra o fortaleza)
function getNodePos(id: string): { x: number; y: number } {
  if (id === 'fort') return { x: CENTER_X, y: CENTER_Y };
  const d = DUNGEONS.find(d => d.id === id);
  return d ? { x: d.x, y: d.y } : { x: CENTER_X, y: CENTER_Y };
}

// Generar puntos del camino con curvas orgánicas (Bézier con ruido)
function generatePathPoints(from: string, to: string, seed: number = 12345): { x: number; y: number }[] {
  const p1 = getNodePos(from);
  const p2 = getNodePos(to);
  const points: { x: number; y: number }[] = [];
  const dist = Math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2);
  const steps = Math.ceil(dist * 3);
  
  // Punto de control para curva Bézier (perpendicular al camino)
  const mx = (p1.x + p2.x) / 2;
  const my = (p1.y + p2.y) / 2;
  const dx = p2.x - p1.x;
  const dy = p2.y - p1.y;
  // Perpendicular normalizado
  const len = Math.sqrt(dx * dx + dy * dy) || 1;
  const px = -dy / len;
  const py = dx / len;
  // Offset aleatorio para la curva
  const offset = (hash2D(Math.floor(p1.x), Math.floor(p1.y), seed) - 0.5) * dist * 0.4;
  const cx = mx + px * offset;
  const cy = my + py * offset;
  
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    // Curva Bézier cuadrática
    const u = 1 - t;
    const bx = u * u * p1.x + 2 * u * t * cx + t * t * p2.x;
    const by = u * u * p1.y + 2 * u * t * cy + t * t * p2.y;
    // Añadir pequeño ruido para irregularidad
    const noise = (hash2D(i, Math.floor(bx * 10), seed) - 0.5) * 0.8;
    points.push({
      x: bx + noise,
      y: by + noise
    });
  }
  return points;
}

// Todos los puntos de camino precalculados
const ALL_PATH_POINTS: { x: number; y: number }[] = [];
for (const [from, to] of PATHS) {
  ALL_PATH_POINTS.push(...generatePathPoints(from, to, from.charCodeAt(0) + to.charCodeAt(0)));
}

const DCOL = { beginner: '#30b030', intermediate: '#e0a000', advanced: '#9040c0', legendary: '#e02020' };

// ═══════════════════════════════════════════════════════════════
// RUIDO MEJORADO - Más natural, menos "manchas de pintura"
// ═══════════════════════════════════════════════════════════════

// Hash rápido para ruido
function hash2D(x: number, y: number, seed: number): number {
  let h = seed + x * 374761393 + y * 668265263;
  h = (h ^ (h >> 13)) * 1274126177;
  return ((h ^ (h >> 16)) & 0xffff) / 65535;
}

// Ruido simple para posicionar objetos
function noise(x: number, y: number, seed: number): number {
  return hash2D(Math.floor(x * 100), Math.floor(y * 100), seed) * 2 - 1;
}

// Ruido de valor con interpolación suave
function valueNoise(x: number, y: number, seed: number): number {
  const x0 = Math.floor(x), y0 = Math.floor(y);
  const fx = x - x0, fy = y - y0;
  
  // Interpolación quintica (más suave que cúbica)
  const sx = fx * fx * fx * (fx * (fx * 6 - 15) + 10);
  const sy = fy * fy * fy * (fy * (fy * 6 - 15) + 10);
  
  const n00 = hash2D(x0, y0, seed);
  const n10 = hash2D(x0 + 1, y0, seed);
  const n01 = hash2D(x0, y0 + 1, seed);
  const n11 = hash2D(x0 + 1, y0 + 1, seed);
  
  const nx0 = n00 * (1 - sx) + n10 * sx;
  const nx1 = n01 * (1 - sx) + n11 * sx;
  
  return (nx0 * (1 - sy) + nx1 * sy) * 2 - 1;
}

// FBM con múltiples octavas para detalle natural
function fbm(x: number, y: number, seed: number): number {
  let value = 0;
  let amplitude = 0.5;
  let frequency = 1;
  let maxValue = 0;
  
  // 5 octavas para más detalle
  for (let i = 0; i < 5; i++) {
    value += valueNoise(x * frequency, y * frequency, seed + i * 100) * amplitude;
    maxValue += amplitude;
    amplitude *= 0.5;
    frequency *= 2.1; // No exactamente 2 para evitar patrones
  }
  
  return value / maxValue;
}

// Ruido de dominio warped - distorsiona las coordenadas para formas más orgánicas
function warpedNoise(x: number, y: number, seed: number): number {
  // Primera capa de distorsión
  const warpX = fbm(x + 0.5, y + 0.5, seed + 1000) * 0.4;
  const warpY = fbm(x + 3.2, y + 1.3, seed + 2000) * 0.4;
  
  // Ruido principal con coordenadas distorsionadas
  return fbm(x + warpX, y + warpY, seed);
}

function distToFort(x: number, y: number): number {
  return Math.sqrt((x - CENTER_X) ** 2 + (y - CENTER_Y) ** 2);
}

// Distancia mínima a cualquier mazmorra
function distToDungeon(x: number, y: number): number {
  let minDist = Infinity;
  for (const d of DUNGEONS) {
    const dist = Math.sqrt((x - d.x) ** 2 + (y - d.y) ** 2);
    if (dist < minDist) minDist = dist;
  }
  return minDist;
}

// Distancia mínima a cualquier punto de camino
function distToPath(x: number, y: number): number {
  let minDist = Infinity;
  for (const p of ALL_PATH_POINTS) {
    const dist = Math.sqrt((x - p.x) ** 2 + (y - p.y) ** 2);
    if (dist < minDist) minDist = dist;
  }
  return minDist;
}

// Modificador del ruido basado en distancia (suave, sin bordes duros)
function getTerrainBias(x: number, y: number): number {
  const dFort = distToFort(x, y);
  const dDung = distToDungeon(x, y);
  const dPath = distToPath(x, y);
  
  // Bias positivo = más probable tierra, negativo = más probable agua
  let bias = 0;
  
  // Fortaleza: gradiente suave desde centro
  if (dFort < 30) {
    bias += (30 - dFort) / 30 * 0.5;
  }
  
  // Mazmorras: gradiente suave
  if (dDung < 15) {
    bias += (15 - dDung) / 15 * 0.4;
  }
  
  // Caminos: gradiente muy suave
  if (dPath < 6) {
    bias += (6 - dPath) / 6 * 0.35;
  }
  
  return bias;
}

function isWater(x: number, y: number, seed: number): boolean {
  const baseNoise = warpedNoise(x * 0.03, y * 0.03, seed);
  const bias = getTerrainBias(x, y);
  return (baseNoise + bias) < -0.15;
}

// Verificar si un punto está en un camino (para dibujar tierra)
function isOnPath(x: number, y: number): boolean {
  return distToPath(x, y) < 2.5;
}

function buildPathGrid(paths: { x: number; y: number }[]): Map<string, boolean> {
  const grid = new Map<string, boolean>();
  for (const p of paths) {
    const gx = Math.floor(p.x), gy = Math.floor(p.y);
    for (let dx = -2; dx <= 2; dx++) {
      for (let dy = -2; dy <= 2; dy++) {
        grid.set(`${gx + dx},${gy + dy}`, true);
      }
    }
  }
  return grid;
}

const terrainCache = new Map<string, ImageData>();

// Colores fijos de paleta 8-bit - tonos suaves de verde
const TERRAIN_PAL = {
  grass: [[40, 112, 40], [44, 120, 44], [48, 128, 48], [52, 136, 52]],
  water: [[16, 48, 128], [24, 56, 144], [32, 64, 160], [40, 80, 176]],
  sand: [[192, 160, 80], [200, 168, 88], [208, 176, 96]],
  path: [[160, 130, 80], [150, 120, 70], [145, 115, 65]], // Camino de tierra
};

// Hash pseudoaleatorio sin patrones visibles
function tileHash(x: number, y: number, seed: number): number {
  const n = Math.sin(x * 12.9898 + y * 78.233 + seed) * 43758.5453;
  return n - Math.floor(n);
}

function renderTerrainChunk(cx: number, cy: number, pathGrid: Map<string, boolean>, paths: { x: number; y: number }[], seed: number): ImageData {
  const key = `${cx},${cy}`;
  const cached = terrainCache.get(key);
  if (cached) return cached;
  
  const data = new ImageData(CHUNK, CHUNK);
  const pxData = data.data;
  
  // Renderizar en bloques de PXxPX para píxeles uniformes
  for (let ly = 0; ly < CHUNK; ly += PX) {
    for (let lx = 0; lx < CHUNK; lx += PX) {
      // Coordenadas en game pixels
      const gpx = Math.floor((cx * CHUNK + lx) / PX);
      const gpy = Math.floor((cy * CHUNK + ly) / PX);
      
      // Coordenadas de mundo (en tiles)
      const wx = gpx * PX / TILE;
      const wy = gpy * PX / TILE;
      
      // Hash para variación local
      const h = tileHash(gpx, gpy, seed);
      
      // Determinar tipo de terreno
      let col: number[];
      
      // Verificar si estamos en un camino
      const dPath = distToPath(wx, wy);
      
      if (dPath < 2) {
        // Camino de tierra
        col = TERRAIN_PAL.path[Math.floor(h * 3) % 3];
      } else {
        // Ruido con bias suave para zonas importantes
        const baseNoise = warpedNoise(wx * 0.03, wy * 0.03, seed);
        const bias = getTerrainBias(wx, wy);
        const n = baseNoise + bias;
        
        // Agua profunda
        if (n < -0.3) {
          col = TERRAIN_PAL.water[0];
        }
        // Agua
        else if (n < -0.15) {
          col = TERRAIN_PAL.water[1 + Math.floor(h * 3) % 3];
        }
        // Arena/playa
        else if (n < -0.05) {
          col = TERRAIN_PAL.sand[Math.floor(h * 3) % 3];
        }
        // Hierba
        else {
          col = TERRAIN_PAL.grass[Math.floor(h * 4) % 4];
        }
      }
      
      // Escribir bloque PXxPX con color sólido (píxel uniforme)
      for (let dy = 0; dy < PX; dy++) {
        for (let dx = 0; dx < PX; dx++) {
          const i = ((ly + dy) * CHUNK + lx + dx) * 4;
          pxData[i] = col[0];
          pxData[i + 1] = col[1];
          pxData[i + 2] = col[2];
          pxData[i + 3] = 255;
        }
      }
    }
  }
  
  terrainCache.set(key, data);
  if (terrainCache.size > 80) {
    const firstKey = terrainCache.keys().next().value;
    if (firstKey) terrainCache.delete(firstKey);
  }
  
  return data;
}

// Pixel art helper - TODOS los píxeles son PXxPX
function px(ctx: CanvasRenderingContext2D, gx: number, gy: number, gw: number, gh: number, c: string) {
  ctx.fillStyle = c;
  ctx.fillRect(Math.floor(gx) * PX, Math.floor(gy) * PX, Math.ceil(gw) * PX, Math.ceil(gh) * PX);
}

// Dibujar un píxel del juego en coordenadas de pantalla
function pxs(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, c: string) {
  ctx.fillStyle = c;
  // Alinear a grid de PX
  const ax = Math.floor(x / PX) * PX;
  const ay = Math.floor(y / PX) * PX;
  const aw = Math.ceil(w / PX) * PX;
  const ah = Math.ceil(h / PX) * PX;
  ctx.fillRect(ax, ay, aw, ah);
}

// Brizna de césped 8-bit
function drawGrass8(ctx: CanvasRenderingContext2D, x: number, y: number, f: number, seed: number) {
  const sway = Math.floor(Math.sin(f * 0.05 + seed * 0.1) * PX);
  pxs(ctx, x + sway, y - 3*PX, PX, 3*PX, PAL8.G2);
  pxs(ctx, x + sway, y - 3*PX, PX, PX, PAL8.G3);
}

// Flor 8-bit simple
function drawFlower8(ctx: CanvasRenderingContext2D, x: number, y: number, type: number) {
  pxs(ctx, x, y - 2*PX, PX, 2*PX, PAL8.G2);
  const colors = [PAL8.X2, PAL8.Y2, PAL8.P1, PAL8.U2];
  pxs(ctx, x - PX, y - 3*PX, 3*PX, 2*PX, colors[type % 4]);
  pxs(ctx, x, y - 3*PX, PX, PX, PAL8.Y3);
}

// Árbol 8-bit - proporciones ajustadas (más grandes, visibles)
function drawTree8(ctx: CanvasRenderingContext2D, x: number, y: number, t: number, f: number) {
  if (t === 0) {
    // PINO - triángulo clásico (alto: ~16 game pixels)
    // Tronco
    pxs(ctx, x - PX, y - PX, 2*PX, 5*PX, PAL8.B2);
    // Copa triangular escalonada
    pxs(ctx, x - 5*PX, y - 5*PX, 10*PX, 4*PX, PAL8.G1);
    pxs(ctx, x - 4*PX, y - 9*PX, 8*PX, 4*PX, PAL8.G2);
    pxs(ctx, x - 3*PX, y - 12*PX, 6*PX, 3*PX, PAL8.G2);
    pxs(ctx, x - 2*PX, y - 14*PX, 4*PX, 2*PX, PAL8.G3);
    pxs(ctx, x - PX, y - 15*PX, 2*PX, PX, PAL8.G3);
  } else if (t === 1) {
    // ROBLE - copa redondeada grande (alto: ~14 game pixels)
    // Tronco grueso
    pxs(ctx, x - PX, y - 2*PX, 3*PX, 6*PX, PAL8.B1);
    // Copa redondeada
    pxs(ctx, x - 5*PX, y - 6*PX, 10*PX, 4*PX, PAL8.G1);
    pxs(ctx, x - 6*PX, y - 10*PX, 12*PX, 4*PX, PAL8.G2);
    pxs(ctx, x - 5*PX, y - 13*PX, 10*PX, 3*PX, PAL8.G2);
    pxs(ctx, x - 3*PX, y - 14*PX, 6*PX, PX, PAL8.G3);
  } else {
    // ARBUSTO - pequeño pero visible (alto: ~6 game pixels)
    pxs(ctx, x - PX, y - PX, 2*PX, 3*PX, PAL8.B2);
    pxs(ctx, x - 4*PX, y - 3*PX, 8*PX, 3*PX, PAL8.G1);
    pxs(ctx, x - 3*PX, y - 5*PX, 6*PX, 2*PX, PAL8.G2);
  }
}

// Roca 8-bit - más visible
function drawRock8(ctx: CanvasRenderingContext2D, x: number, y: number, size: number = 1) {
  pxs(ctx, x - 4*PX, y - 2*PX, 8*PX, 3*PX, PAL8.R1);
  pxs(ctx, x - 3*PX, y - 4*PX, 6*PX, 2*PX, PAL8.R2);
  pxs(ctx, x - 2*PX, y - 4*PX, 3*PX, PX, PAL8.R3);
}

// ═══════════════════════════════════════════════════════════════
// FORTALEZA CENTRAL - Castillo épico 8-bit (GRANDE)
// ═══════════════════════════════════════════════════════════════
function drawFortress8(ctx: CanvasRenderingContext2D, ox: number, oy: number, f: number) {
  const cx = CENTER_X * TILE - ox;
  const cy = CENTER_Y * TILE - oy;
  const x = Math.floor(cx / PX) * PX;
  const y = Math.floor(cy / PX) * PX;
  
  // Tamaños en game pixels - GRANDE para proporciones correctas
  const W = 80; // ancho muralla (~320px reales)
  const H = 60; // alto muralla (~240px reales)
  
  // ─── SUELO DEL PATIO ───
  for (let gy = -H/2 + 4; gy < H/2 - 4; gy++) {
    for (let gx = -W/2 + 4; gx < W/2 - 4; gx++) {
      const pattern = ((Math.abs(gx) + Math.abs(gy)) % 4);
      const col = pattern === 0 ? PAL8.S1 : pattern === 1 ? PAL8.S0 : pattern === 2 ? PAL8.S2 : PAL8.R1;
      pxs(ctx, x + gx*PX, y + gy*PX, PX, PX, col);
    }
  }
  
  // ─── MURALLAS EXTERIORES (gruesas) ───
  // Norte (con almenas)
  for (let gx = -W/2; gx < W/2; gx++) {
    pxs(ctx, x + gx*PX, y - H/2*PX, PX, 4*PX, PAL8.R2);
    if (gx % 4 === 0) pxs(ctx, x + gx*PX, y - (H/2+2)*PX, 3*PX, 2*PX, PAL8.R3);
  }
  // Sur
  for (let gx = -W/2; gx < W/2; gx++) {
    pxs(ctx, x + gx*PX, y + (H/2-4)*PX, PX, 4*PX, PAL8.R2);
    if (gx % 4 === 0) pxs(ctx, x + gx*PX, y + H/2*PX, 3*PX, 2*PX, PAL8.R3);
  }
  // Oeste
  for (let gy = -H/2; gy < H/2; gy++) {
    pxs(ctx, x - W/2*PX, y + gy*PX, 4*PX, PX, PAL8.R2);
  }
  // Este
  for (let gy = -H/2; gy < H/2; gy++) {
    pxs(ctx, x + (W/2-4)*PX, y + gy*PX, 4*PX, PX, PAL8.R2);
  }
  
  // ─── TORRES ESQUINAS (grandes) ───
  const towerSize = 12;
  const corners = [
    [-W/2-2, -H/2-2], [W/2-towerSize+2, -H/2-2], 
    [-W/2-2, H/2-towerSize+2], [W/2-towerSize+2, H/2-towerSize+2]
  ];
  corners.forEach(([tx, ty], idx) => {
    // Base torre (12x12)
    for (let gy = 0; gy < towerSize; gy++) {
      for (let gx = 0; gx < towerSize; gx++) {
        const corner = (gx < 2 || gx >= towerSize-2) && (gy < 2 || gy >= towerSize-2);
        if (!corner) {
          pxs(ctx, x + (tx+gx)*PX, y + (ty+gy)*PX, PX, PX, PAL8.R2);
        }
      }
    }
    // Borde superior torre
    pxs(ctx, x + (tx+2)*PX, y + (ty-1)*PX, 8*PX, PX, PAL8.R3);
    // Almenas torre
    for (let i = 0; i < 4; i++) {
      pxs(ctx, x + (tx+2+i*2)*PX, y + (ty-3)*PX, 2*PX, 2*PX, PAL8.R3);
    }
    // Techo cónico
    pxs(ctx, x + (tx+1)*PX, y + (ty-5)*PX, 10*PX, 2*PX, PAL8.X1);
    pxs(ctx, x + (tx+2)*PX, y + (ty-7)*PX, 8*PX, 2*PX, PAL8.X1);
    pxs(ctx, x + (tx+3)*PX, y + (ty-9)*PX, 6*PX, 2*PX, PAL8.X2);
    pxs(ctx, x + (tx+4)*PX, y + (ty-11)*PX, 4*PX, 2*PX, PAL8.X2);
    pxs(ctx, x + (tx+5)*PX, y + (ty-13)*PX, 2*PX, 2*PX, PAL8.X2);
    // Bandera con ondeo
    const wave = Math.floor(Math.sin(f * 0.08 + idx * 1.5) * 3);
    pxs(ctx, x + (tx+6)*PX, y + (ty-20)*PX, PX, 7*PX, PAL8.B2);
    pxs(ctx, x + (tx+7)*PX + wave, y + (ty-20)*PX, 5*PX, 3*PX, PAL8.Y2);
    pxs(ctx, x + (tx+7)*PX + wave, y + (ty-17)*PX, 4*PX, 2*PX, PAL8.Y1);
    // Ventanas torre
    pxs(ctx, x + (tx+4)*PX, y + (ty+4)*PX, 3*PX, 4*PX, PAL8.U2);
    pxs(ctx, x + (tx+5)*PX, y + (ty+5)*PX, 2*PX, 2*PX, PAL8.U3);
  });
  
  // ─── TORRE CENTRAL (KEEP) - muy grande ───
  const kw = 32, kh = 28;
  // Base
  for (let gy = -kh/2; gy < kh/2; gy++) {
    for (let gx = -kw/2; gx < kw/2; gx++) {
      pxs(ctx, x + gx*PX, y + gy*PX, PX, PX, PAL8.R3);
    }
  }
  // Almenas del keep
  for (let gx = -kw/2; gx < kw/2; gx += 3) {
    pxs(ctx, x + gx*PX, y - (kh/2+1)*PX, 2*PX, 2*PX, PAL8.R4);
  }
  // Techo keep (triangular grande)
  for (let i = 0; i < 8; i++) {
    const tw = kw - i * 4;
    pxs(ctx, x + (-tw/2)*PX, y + (-kh/2-i*2-2)*PX, tw*PX, 2*PX, PAL8.X1);
  }
  pxs(ctx, x - 2*PX, y + (-kh/2-18)*PX, 4*PX, 2*PX, PAL8.X2);
  // Ventanas del keep (grandes)
  pxs(ctx, x - 12*PX, y - 6*PX, 4*PX, 6*PX, PAL8.U2);
  pxs(ctx, x - 11*PX, y - 5*PX, 2*PX, 4*PX, PAL8.U3);
  pxs(ctx, x + 8*PX, y - 6*PX, 4*PX, 6*PX, PAL8.U2);
  pxs(ctx, x + 9*PX, y - 5*PX, 2*PX, 4*PX, PAL8.U3);
  // Ventana central (rosetón grande)
  pxs(ctx, x - 5*PX, y - 8*PX, 10*PX, 8*PX, PAL8.U2);
  pxs(ctx, x - 3*PX, y - 6*PX, 6*PX, 4*PX, PAL8.U3);
  pxs(ctx, x - PX, y - 5*PX, 2*PX, 2*PX, PAL8.Y2);
  // Cruz de la ventana
  pxs(ctx, x, y - 8*PX, PX, 8*PX, PAL8.R3);
  pxs(ctx, x - 5*PX, y - 4*PX, 10*PX, PX, PAL8.R3);
  
  // ─── PUERTA PRINCIPAL (grande) ───
  // Arco
  pxs(ctx, x - 8*PX, y + 6*PX, 16*PX, 10*PX, PAL8.R2);
  pxs(ctx, x - 6*PX, y + 6*PX, 12*PX, 2*PX, PAL8.R3);
  // Apertura
  pxs(ctx, x - 5*PX, y + 8*PX, 10*PX, 8*PX, PAL8.BK);
  // Puerta de madera (doble)
  pxs(ctx, x - 5*PX, y + 9*PX, 5*PX, 7*PX, PAL8.B1);
  pxs(ctx, x, y + 9*PX, 5*PX, 7*PX, PAL8.B2);
  // Herrajes
  pxs(ctx, x - 3*PX, y + 11*PX, 2*PX, 2*PX, PAL8.Y1);
  pxs(ctx, x + PX, y + 11*PX, 2*PX, 2*PX, PAL8.Y1);
  pxs(ctx, x - 3*PX, y + 14*PX, 2*PX, PX, PAL8.Y1);
  pxs(ctx, x + PX, y + 14*PX, 2*PX, PX, PAL8.Y1);
  
  // ─── ANTORCHAS ANIMADAS (más) ───
  const torchPos = [
    [-W/2+4, -10], [W/2-5, -10],   // Muralla norte
    [-W/2+4, H/2-8], [W/2-5, H/2-8], // Muralla sur
    [-10, 8], [9, 8],              // Entrada
    [-kw/2-2, -2], [kw/2+1, -2]    // Keep
  ];
  torchPos.forEach(([tx, ty], i) => {
    pxs(ctx, x + tx*PX, y + ty*PX, 2*PX, 4*PX, PAL8.B2);
    const flicker = Math.floor(Math.sin(f * 0.18 + i * 0.7) * 2);
    const flicker2 = Math.floor(Math.cos(f * 0.22 + i) * 2);
    pxs(ctx, x + tx*PX + flicker, y + (ty-3)*PX, 2*PX, 2*PX, PAL8.Y3);
    pxs(ctx, x + tx*PX + flicker2, y + (ty-5)*PX, 2*PX, 2*PX, PAL8.Y2);
    pxs(ctx, x + tx*PX, y + (ty-7)*PX + Math.abs(flicker), 2*PX, 2*PX, PAL8.X2);
  });
  
  // ─── ESTANDARTES GRANDES ───
  const bannerWave = Math.floor(Math.sin(f * 0.06) * 2);
  // Estandarte izquierdo
  pxs(ctx, x - 8*PX, y - 12*PX, 2*PX, 10*PX, PAL8.B2);
  pxs(ctx, x - 6*PX + bannerWave, y - 12*PX, 4*PX, 8*PX, PAL8.X1);
  pxs(ctx, x - 5*PX + bannerWave, y - 10*PX, 2*PX, 4*PX, PAL8.Y2);
  // Estandarte derecho
  pxs(ctx, x + 6*PX, y - 12*PX, 2*PX, 10*PX, PAL8.B2);
  pxs(ctx, x + 8*PX - bannerWave, y - 12*PX, 4*PX, 8*PX, PAL8.X1);
  pxs(ctx, x + 9*PX - bannerWave, y - 10*PX, 2*PX, 4*PX, PAL8.Y2);
}


// NPC 8-bit - proporcional (altura ~10 game pixels, comparable a puertas del castillo)
function drawNPC8(ctx: CanvasRenderingContext2D, npc: NPC, ox: number, oy: number, f: number, hovered: boolean) {
  const cx = npc.x * TILE - ox;
  const cy = npc.y * TILE - oy;
  const x = Math.floor(cx / PX) * PX;
  const y = Math.floor(cy / PX) * PX;
  const bob = Math.floor(Math.sin(f * 0.04 + npc.id.charCodeAt(0))) * PX;
  
  const cols: Record<string, { body: string; acc: string }> = {
    'tavern': { body: PAL8.B2, acc: PAL8.Y1 },
    'smith': { body: PAL8.R1, acc: PAL8.X1 },
    'mage': { body: PAL8.P1, acc: PAL8.U2 },
    'guard': { body: PAL8.U1, acc: PAL8.Y2 },
    'merchant': { body: PAL8.G2, acc: PAL8.Y2 },
  };
  const c = cols[npc.sprite] || cols['tavern'];
  
  // Sprite ~6x10 game pixels (proporcional)
  // Piernas
  pxs(ctx, x - 2*PX, y + bob, 2*PX, 3*PX, c.body);
  pxs(ctx, x, y + bob, 2*PX, 3*PX, c.body);
  // Cuerpo
  pxs(ctx, x - 2*PX, y - 3*PX + bob, 4*PX, 4*PX, c.body);
  // Brazos
  pxs(ctx, x - 3*PX, y - 2*PX + bob, PX, 3*PX, c.body);
  pxs(ctx, x + 2*PX, y - 2*PX + bob, PX, 3*PX, c.body);
  // Cabeza
  pxs(ctx, x - 2*PX, y - 6*PX + bob, 4*PX, 3*PX, PAL8.K1);
  // Pelo/sombrero
  pxs(ctx, x - 2*PX, y - 7*PX + bob, 4*PX, PX, c.acc);
  // Ojos
  pxs(ctx, x - PX, y - 5*PX + bob, PX, PX, PAL8.BK);
  pxs(ctx, x, y - 5*PX + bob, PX, PX, PAL8.BK);
  
  if (hovered) {
    // Indicador flotante
    const fy = Math.floor(Math.sin(f * 0.1) * 2);
    pxs(ctx, x - PX, y - 10*PX + fy, 2*PX, 2*PX, PAL8.Y3);
    pxs(ctx, x, y - 8*PX + fy, PX, PX, PAL8.Y2);
  }
}

// Mazmorra 8-bit - Entrada épica según dificultad (PROPORCIONAL A HUMANOS ~10px)
function drawDungeon8(ctx: CanvasRenderingContext2D, d: Dungeon, hover: boolean, f: number, ox: number, oy: number) {
  const cx = d.x * TILE - ox;
  const cy = d.y * TILE - oy;
  const x = Math.floor(cx / PX) * PX;
  const y = Math.floor(cy / PX) * PX;
  const c = DCOL[d.diff];
  
  // Diferentes estilos según dificultad - TAMAÑO ~30-40 game pixels (3-4x humano)
  if (d.diff === 'beginner') {
    // ─── CABAÑA GRANDE CON TALLER ───
    // Dimensiones: ~28x24 game pixels
    // Base piedra cimientos
    pxs(ctx, x - 14*PX, y - 2*PX, 28*PX, 4*PX, PAL8.R1);
    pxs(ctx, x - 13*PX, y - 4*PX, 26*PX, 2*PX, PAL8.R2);
    // Paredes de madera
    pxs(ctx, x - 12*PX, y - 14*PX, 24*PX, 10*PX, PAL8.B2);
    pxs(ctx, x - 11*PX, y - 13*PX, 22*PX, 8*PX, PAL8.B1);
    // Vigas decorativas
    pxs(ctx, x - 12*PX, y - 10*PX, 24*PX, PX, PAL8.B0);
    pxs(ctx, x - 12*PX, y - 6*PX, 24*PX, PX, PAL8.B0);
    pxs(ctx, x - 6*PX, y - 14*PX, PX, 10*PX, PAL8.B0);
    pxs(ctx, x + 5*PX, y - 14*PX, PX, 10*PX, PAL8.B0);
    // Techo de paja grande
    pxs(ctx, x - 16*PX, y - 16*PX, 32*PX, 3*PX, PAL8.B2);
    pxs(ctx, x - 14*PX, y - 19*PX, 28*PX, 3*PX, PAL8.B1);
    pxs(ctx, x - 11*PX, y - 21*PX, 22*PX, 2*PX, PAL8.B1);
    pxs(ctx, x - 8*PX, y - 23*PX, 16*PX, 2*PX, PAL8.B2);
    pxs(ctx, x - 5*PX, y - 24*PX, 10*PX, PX, PAL8.B2);
    pxs(ctx, x - 2*PX, y - 25*PX, 4*PX, PX, PAL8.B1);
    // Chimenea
    pxs(ctx, x + 7*PX, y - 24*PX, 4*PX, 6*PX, PAL8.R2);
    pxs(ctx, x + 8*PX, y - 25*PX, 2*PX, PX, PAL8.R3);
    const smoke = Math.floor(Math.sin(f * 0.08) * PX);
    pxs(ctx, x + 8*PX, y - 27*PX + smoke, 2*PX, 2*PX, PAL8.R4);
    // Puerta grande de madera
    pxs(ctx, x - 4*PX, y - 3*PX, 8*PX, 11*PX, PAL8.B0);
    pxs(ctx, x - 3*PX, y - 2*PX, 6*PX, 9*PX, '#2a1a0a');
    pxs(ctx, x - 4*PX, y - 8*PX, 8*PX, PX, PAL8.Y1); // Bisagra superior
    pxs(ctx, x - 4*PX, y - 3*PX, 8*PX, PX, PAL8.Y1); // Bisagra inferior
    pxs(ctx, x + 2*PX, y - 6*PX, 2*PX, 2*PX, PAL8.Y2); // Picaporte
    // Ventanas grandes
    pxs(ctx, x - 10*PX, y - 11*PX, 4*PX, 5*PX, PAL8.B0);
    pxs(ctx, x - 9*PX, y - 10*PX, 2*PX, 3*PX, PAL8.Y2);
    pxs(ctx, x + 6*PX, y - 11*PX, 4*PX, 5*PX, PAL8.B0);
    pxs(ctx, x + 7*PX, y - 10*PX, 2*PX, 3*PX, PAL8.Y2);
    // Letrero grande colgante
    pxs(ctx, x - 18*PX, y - 8*PX, PX, 10*PX, PAL8.B2);
    pxs(ctx, x - 22*PX, y - 12*PX, 6*PX, 4*PX, PAL8.B1);
    pxs(ctx, x - 21*PX, y - 11*PX, 4*PX, 2*PX, PAL8.Y1); // Símbolo espada
    // Barril decorativo
    pxs(ctx, x + 14*PX, y - 3*PX, 4*PX, 5*PX, PAL8.B2);
    pxs(ctx, x + 14*PX, y - 2*PX, 4*PX, PX, PAL8.B0);
    
  } else if (d.diff === 'intermediate') {
    // ─── ENTRADA DE CAVERNA GRANDE/RUINAS ANTIGUAS ───
    // Dimensiones: ~36x30 game pixels
    // Formación rocosa masiva
    pxs(ctx, x - 18*PX, y - 6*PX, 36*PX, 10*PX, PAL8.R1);
    pxs(ctx, x - 16*PX, y - 12*PX, 32*PX, 6*PX, PAL8.R1);
    pxs(ctx, x - 14*PX, y - 18*PX, 28*PX, 6*PX, PAL8.R2);
    pxs(ctx, x - 10*PX, y - 22*PX, 20*PX, 4*PX, PAL8.R2);
    pxs(ctx, x - 6*PX, y - 25*PX, 12*PX, 3*PX, PAL8.R3);
    pxs(ctx, x - 3*PX, y - 27*PX, 6*PX, 2*PX, PAL8.R3);
    // Entrada oscura grande
    pxs(ctx, x - 10*PX, y - 8*PX, 20*PX, 12*PX, PAL8.BK);
    pxs(ctx, x - 8*PX, y - 14*PX, 16*PX, 6*PX, PAL8.BK);
    pxs(ctx, x - 5*PX, y - 16*PX, 10*PX, 2*PX, PAL8.BK);
    // Columnas ruinosas grandes
    pxs(ctx, x - 12*PX, y - 10*PX, 4*PX, 14*PX, PAL8.R3);
    pxs(ctx, x + 8*PX, y - 10*PX, 4*PX, 14*PX, PAL8.R3);
    pxs(ctx, x - 12*PX, y - 12*PX, 4*PX, 2*PX, PAL8.R4);
    pxs(ctx, x + 8*PX, y - 12*PX, 4*PX, 2*PX, PAL8.R4);
    // Capiteles rotos
    pxs(ctx, x - 13*PX, y - 14*PX, 6*PX, 2*PX, PAL8.R4);
    pxs(ctx, x + 7*PX, y - 14*PX, 6*PX, 2*PX, PAL8.R4);
    // Musgo/vegetación abundante
    pxs(ctx, x - 16*PX, y - 8*PX, 3*PX, 2*PX, PAL8.G1);
    pxs(ctx, x + 13*PX, y - 6*PX, 3*PX, 2*PX, PAL8.G2);
    pxs(ctx, x - 14*PX, y - 16*PX, 2*PX, 3*PX, PAL8.G1);
    pxs(ctx, x + 12*PX, y - 14*PX, 2*PX, 3*PX, PAL8.G2);
    pxs(ctx, x - 4*PX, y - 26*PX, 2*PX, PX, PAL8.G2);
    // Ojos brillantes grandes en la oscuridad
    const blink = Math.sin(f * 0.05) > 0.9;
    if (!blink) {
      pxs(ctx, x - 5*PX, y - 5*PX, 2*PX, 2*PX, c);
      pxs(ctx, x + 3*PX, y - 5*PX, 2*PX, 2*PX, c);
    }
    // Huesos/cráneos en la entrada
    pxs(ctx, x - 8*PX, y - 2*PX, 3*PX, 2*PX, PAL8.WH);
    pxs(ctx, x + 5*PX, y - 3*PX, 2*PX, 3*PX, PAL8.WH);
    // Antorchas apagadas
    pxs(ctx, x - 14*PX, y - 6*PX, PX, 4*PX, PAL8.B0);
    pxs(ctx, x + 13*PX, y - 6*PX, PX, 4*PX, PAL8.B0);
    
  } else if (d.diff === 'advanced') {
    // ─── TORRE MÁGICA ALTA ───
    // Dimensiones: ~24x45 game pixels (torre alta)
    // Base torre masiva
    pxs(ctx, x - 12*PX, y - 6*PX, 24*PX, 10*PX, PAL8.R2);
    pxs(ctx, x - 11*PX, y - 5*PX, 22*PX, 8*PX, PAL8.R3);
    // Cuerpo de la torre (3 niveles)
    pxs(ctx, x - 10*PX, y - 18*PX, 20*PX, 12*PX, PAL8.R3);
    pxs(ctx, x - 9*PX, y - 30*PX, 18*PX, 12*PX, PAL8.R3);
    pxs(ctx, x - 8*PX, y - 38*PX, 16*PX, 8*PX, PAL8.R3);
    // Cornisas entre niveles
    pxs(ctx, x - 11*PX, y - 18*PX, 22*PX, 2*PX, PAL8.R2);
    pxs(ctx, x - 10*PX, y - 30*PX, 20*PX, 2*PX, PAL8.R2);
    // Techo puntiagudo grande
    pxs(ctx, x - 10*PX, y - 40*PX, 20*PX, 2*PX, PAL8.P1);
    pxs(ctx, x - 8*PX, y - 43*PX, 16*PX, 3*PX, PAL8.P1);
    pxs(ctx, x - 6*PX, y - 46*PX, 12*PX, 3*PX, PAL8.P1);
    pxs(ctx, x - 4*PX, y - 48*PX, 8*PX, 2*PX, PAL8.P2);
    pxs(ctx, x - 2*PX, y - 50*PX, 4*PX, 2*PX, PAL8.P2);
    pxs(ctx, x - PX, y - 52*PX, 2*PX, 2*PX, PAL8.P2);
    // Orbe mágico grande en la cima
    const glow = Math.floor(Math.sin(f * 0.1) * 2);
    pxs(ctx, x - 2*PX, y - 56*PX + glow, 4*PX, 4*PX, c);
    pxs(ctx, x - PX, y - 55*PX + glow, 2*PX, 2*PX, PAL8.WH);
    // Rayos de energía desde el orbe
    const ray = Math.sin(f * 0.15) > 0;
    if (ray) {
      pxs(ctx, x - 4*PX, y - 54*PX + glow, PX, 2*PX, c);
      pxs(ctx, x + 3*PX, y - 54*PX + glow, PX, 2*PX, c);
    }
    // Ventanas mágicas (múltiples niveles)
    // Nivel 1
    pxs(ctx, x - 7*PX, y - 14*PX, 4*PX, 5*PX, c);
    pxs(ctx, x + 3*PX, y - 14*PX, 4*PX, 5*PX, c);
    // Nivel 2
    pxs(ctx, x - 6*PX, y - 26*PX, 3*PX, 4*PX, c);
    pxs(ctx, x + 3*PX, y - 26*PX, 3*PX, 4*PX, c);
    pxs(ctx, x - PX, y - 27*PX, 2*PX, 5*PX, c);
    // Nivel 3
    pxs(ctx, x - 4*PX, y - 36*PX, 3*PX, 4*PX, c);
    pxs(ctx, x + PX, y - 36*PX, 3*PX, 4*PX, c);
    // Puerta arcana grande
    pxs(ctx, x - 5*PX, y - 4*PX, 10*PX, 12*PX, PAL8.P0);
    pxs(ctx, x - 4*PX, y - 3*PX, 8*PX, 10*PX, PAL8.P1);
    pxs(ctx, x - 3*PX, y - 2*PX, 6*PX, 8*PX, PAL8.BK);
    // Arco sobre puerta
    pxs(ctx, x - 5*PX, y - 6*PX, 10*PX, 2*PX, PAL8.P2);
    // Runas grandes animadas
    const runeGlow = Math.sin(f * 0.08) > 0 ? c : PAL8.P1;
    pxs(ctx, x - 7*PX, y - 6*PX, 2*PX, 2*PX, runeGlow);
    pxs(ctx, x + 5*PX, y - 6*PX, 2*PX, 2*PX, runeGlow);
    pxs(ctx, x - 8*PX, y - 12*PX, PX, PX, runeGlow);
    pxs(ctx, x + 7*PX, y - 12*PX, PX, PX, runeGlow);
    // Escalones
    pxs(ctx, x - 6*PX, y + 2*PX, 12*PX, 2*PX, PAL8.R2);
    pxs(ctx, x - 7*PX, y + 4*PX, 14*PX, 2*PX, PAL8.R1);
    
  } else {
    // ─── LEGENDARY: PORTAL DEMONÍACO MASIVO ───
    // Dimensiones: ~40x50 game pixels
    // Base de piedra volcánica
    pxs(ctx, x - 20*PX, y - 2*PX, 40*PX, 6*PX, PAL8.R0);
    pxs(ctx, x - 18*PX, y - 6*PX, 36*PX, 4*PX, PAL8.R0);
    pxs(ctx, x - 16*PX, y - 8*PX, 32*PX, 2*PX, PAL8.R1);
    // Lava en la base
    const lavaPhase = Math.sin(f * 0.1);
    pxs(ctx, x - 18*PX, y + 2*PX, 6*PX, 2*PX, lavaPhase > 0 ? PAL8.X2 : PAL8.X1);
    pxs(ctx, x + 12*PX, y + 2*PX, 6*PX, 2*PX, lavaPhase < 0 ? PAL8.X2 : PAL8.X1);
    // Marco del portal gigante (huesos/piedra oscura)
    pxs(ctx, x - 16*PX, y - 40*PX, 6*PX, 38*PX, PAL8.R0);
    pxs(ctx, x + 10*PX, y - 40*PX, 6*PX, 38*PX, PAL8.R0);
    pxs(ctx, x - 16*PX, y - 46*PX, 32*PX, 8*PX, PAL8.R0);
    // Detalles del marco (calaveras esculpidas)
    pxs(ctx, x - 14*PX, y - 32*PX, 4*PX, 4*PX, PAL8.R1);
    pxs(ctx, x + 10*PX, y - 32*PX, 4*PX, 4*PX, PAL8.R1);
    pxs(ctx, x - 14*PX, y - 22*PX, 4*PX, 4*PX, PAL8.R1);
    pxs(ctx, x + 10*PX, y - 22*PX, 4*PX, 4*PX, PAL8.R1);
    pxs(ctx, x - 14*PX, y - 12*PX, 4*PX, 4*PX, PAL8.R1);
    pxs(ctx, x + 10*PX, y - 12*PX, 4*PX, 4*PX, PAL8.R1);
    // Gran calavera en la cima
    pxs(ctx, x - 6*PX, y - 48*PX, 12*PX, 10*PX, PAL8.WH);
    pxs(ctx, x - 5*PX, y - 46*PX, 3*PX, 4*PX, PAL8.BK); // Ojo izq
    pxs(ctx, x + 2*PX, y - 46*PX, 3*PX, 4*PX, PAL8.BK); // Ojo der
    pxs(ctx, x - 2*PX, y - 42*PX, 4*PX, 2*PX, PAL8.BK); // Nariz
    pxs(ctx, x - 4*PX, y - 40*PX, 8*PX, 2*PX, PAL8.BK); // Boca
    // Cuernos
    pxs(ctx, x - 8*PX, y - 52*PX, 3*PX, 6*PX, PAL8.R0);
    pxs(ctx, x + 5*PX, y - 52*PX, 3*PX, 6*PX, PAL8.R0);
    pxs(ctx, x - 9*PX, y - 54*PX, 2*PX, 3*PX, PAL8.R0);
    pxs(ctx, x + 7*PX, y - 54*PX, 2*PX, 3*PX, PAL8.R0);
    // Portal interior (animado con vórtice)
    const portalPhase = (f * 0.03) % (Math.PI * 2);
    for (let py = -36; py < -6; py += 2) {
      for (let px = -8; px < 8; px += 2) {
        const dist = Math.sqrt(px*px + (py+21)*(py+21));
        const wave = Math.sin(dist * 0.3 - portalPhase);
        const col = wave > 0.3 ? PAL8.X2 : wave > -0.3 ? PAL8.X1 : PAL8.X0;
        pxs(ctx, x + px*PX, y + py*PX, 2*PX, 2*PX, col);
      }
    }
    // Centro del vórtice
    pxs(ctx, x - 3*PX, y - 23*PX, 6*PX, 6*PX, PAL8.X2);
    pxs(ctx, x - 2*PX, y - 22*PX, 4*PX, 4*PX, PAL8.Y3);
    pxs(ctx, x - PX, y - 21*PX, 2*PX, 2*PX, PAL8.WH);
    // Cráneos decorativos laterales
    pxs(ctx, x - 14*PX, y - 44*PX, 4*PX, 4*PX, PAL8.WH);
    pxs(ctx, x - 13*PX, y - 43*PX, PX, PX, PAL8.BK);
    pxs(ctx, x - 11*PX, y - 43*PX, PX, PX, PAL8.BK);
    pxs(ctx, x + 10*PX, y - 44*PX, 4*PX, 4*PX, PAL8.WH);
    pxs(ctx, x + 11*PX, y - 43*PX, PX, PX, PAL8.BK);
    pxs(ctx, x + 13*PX, y - 43*PX, PX, PX, PAL8.BK);
    // Llamas grandes a los lados
    const flame1 = Math.floor(Math.sin(f * 0.2) * 2);
    const flame2 = Math.floor(Math.cos(f * 0.18) * 2);
    // Llama izquierda (brasero)
    pxs(ctx, x - 20*PX, y - 6*PX, 4*PX, 4*PX, PAL8.R0);
    pxs(ctx, x - 19*PX, y - 10*PX + flame1, 2*PX, 6*PX, PAL8.X2);
    pxs(ctx, x - 19*PX, y - 14*PX + flame1, 2*PX, 4*PX, PAL8.Y2);
    pxs(ctx, x - 19*PX, y - 16*PX + flame1, PX, 2*PX, PAL8.Y3);
    // Llama derecha (brasero)
    pxs(ctx, x + 16*PX, y - 6*PX, 4*PX, 4*PX, PAL8.R0);
    pxs(ctx, x + 17*PX, y - 10*PX + flame2, 2*PX, 6*PX, PAL8.X2);
    pxs(ctx, x + 17*PX, y - 14*PX + flame2, 2*PX, 4*PX, PAL8.Y2);
    pxs(ctx, x + 18*PX, y - 16*PX + flame2, PX, 2*PX, PAL8.Y3);
    // Cadenas colgantes
    for (let i = 0; i < 8; i++) {
      const swing = Math.sin(f * 0.05 + i) * PX;
      pxs(ctx, x - 14*PX + swing, y - 40*PX + i*3*PX, PX, 2*PX, PAL8.R2);
      pxs(ctx, x + 13*PX + swing, y - 40*PX + i*3*PX, PX, 2*PX, PAL8.R2);
    }
  }
  
  // ─── ICONO Y NOMBRE ───
  ctx.font = '18px serif';
  ctx.textAlign = 'center';
  ctx.fillStyle = c;
  ctx.fillText(d.icon, x, y - 25*PX);
  
  if (hover) {
    // Halo de selección
    ctx.strokeStyle = c;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(x - 10*PX, y - 22*PX, 20*PX, 28*PX, 4);
    ctx.stroke();
    // Nombre
    ctx.fillStyle = '#000';
    ctx.fillRect(x - 50, y + 6*PX, 100, 16);
    ctx.fillStyle = c;
    ctx.font = 'bold 11px monospace';
    ctx.fillText(d.title, x, y + 18*PX);
  }
}

// Jugador 8-bit - proporcional (~10 game pixels alto)
function drawPlayer8(ctx: CanvasRenderingContext2D, x: number, y: number, mov: boolean, f: number, dir: number) {
  const px = Math.floor(x / PX) * PX;
  const py = Math.floor(y / PX) * PX;
  const bob = mov ? Math.floor(Math.sin(f * 0.25)) * PX : 0;
  const leg = mov ? Math.floor(Math.sin(f * 0.3) * 2) : 0;
  
  // Sprite 6x10 game pixels (proporcional con NPCs)
  const cDir = dir > 0 ? 1 : -1;
  
  // Piernas
  pxs(ctx, px - 2*PX, py + bob + leg, 2*PX, 3*PX, PAL8.U1);
  pxs(ctx, px, py + bob - leg, 2*PX, 3*PX, PAL8.U1);
  // Cuerpo (armadura)
  pxs(ctx, px - 2*PX, py - 4*PX + bob, 4*PX, 4*PX, PAL8.R2);
  pxs(ctx, px - 2*PX, py - 2*PX + bob, 4*PX, PX, PAL8.Y1); // Cinturón
  // Brazos
  pxs(ctx, px - 3*PX, py - 3*PX + bob, PX, 3*PX, PAL8.R1);
  pxs(ctx, px + 2*PX, py - 3*PX + bob, PX, 3*PX, PAL8.R1);
  // Capa
  pxs(ctx, px + cDir * -3*PX, py - 3*PX + bob, 2*PX, 5*PX, PAL8.X1);
  // Cabeza
  pxs(ctx, px - 2*PX, py - 7*PX + bob, 4*PX, 3*PX, PAL8.K1);
  // Pelo
  pxs(ctx, px - 2*PX, py - 8*PX + bob, 4*PX, PX, PAL8.B0);
  // Ojos
  pxs(ctx, px - PX, py - 6*PX + bob, PX, PX, PAL8.BK);
  pxs(ctx, px, py - 6*PX + bob, PX, PX, PAL8.BK);
  // Corona
  pxs(ctx, px - 2*PX, py - 9*PX + bob, PX, PX, PAL8.Y2);
  pxs(ctx, px - PX, py - 10*PX + bob, 2*PX, PX, PAL8.Y2);
  pxs(ctx, px + PX, py - 9*PX + bob, PX, PX, PAL8.Y2);
  // Espada
  pxs(ctx, px + dir * 3*PX, py - 5*PX + bob, PX, 6*PX, PAL8.GY);
  pxs(ctx, px + dir * 3*PX, py - 6*PX + bob, PX, PX, PAL8.R4);
  pxs(ctx, px + dir * 3*PX, py - 2*PX + bob, 2*PX, PX, PAL8.Y2); // Guarda
}

function genWorld(seed: number) {
  // Sin caminos - terreno limpio
  const paths: { x: number; y: number }[] = [];
  
  const trees: { x: number; y: number; t: number }[] = [];
  const rocks: { x: number; y: number; s: number }[] = [];
  const grass: { x: number; y: number; seed: number }[] = [];
  const flowers: { x: number; y: number; type: number }[] = [];
  
  // Más árboles para mundo más grande
  for (let i = 0; i < 600; i++) {
    const tx = 4 + (noise(i, 0, seed) * 0.5 + 0.5) * (MW - 8);
    const ty = 4 + (noise(0, i, seed + 50) * 0.5 + 0.5) * (MH - 8);
    const nearD = DUNGEONS.some(d => Math.abs(d.x - tx) < 6 && Math.abs(d.y - ty) < 6);
    const nearP = paths.some(p => Math.abs(p.x - tx) < 2.5 && Math.abs(p.y - ty) < 2.5);
    const nearFort = distToFort(tx, ty) < 22;
    if (!nearD && !nearP && !nearFort && !isWater(tx, ty, seed) && fbm(tx * 0.08, ty * 0.08, seed) > -0.1) {
      trees.push({ x: tx, y: ty, t: Math.floor((noise(tx, ty, seed) * 0.5 + 0.5) * 3) });
    }
  }
  
  for (let i = 0; i < 200; i++) {
    const rx = 3 + (noise(i + 500, 0, seed) * 0.5 + 0.5) * (MW - 6);
    const ry = 3 + (noise(0, i + 500, seed) * 0.5 + 0.5) * (MH - 6);
    const nearFort = distToFort(rx, ry) < 20;
    if (!DUNGEONS.some(d => Math.abs(d.x - rx) < 5 && Math.abs(d.y - ry) < 5) && !nearFort && !isWater(rx, ry, seed)) {
      rocks.push({ x: rx, y: ry, s: 0.8 + (noise(rx, ry, seed) * 0.5 + 0.5) * 0.5 });
    }
  }
  
  for (let i = 0; i < 600; i++) {
    const gx = 2 + (noise(i + 1000, 0, seed) * 0.5 + 0.5) * (MW - 4);
    const gy = 2 + (noise(0, i + 1000, seed) * 0.5 + 0.5) * (MH - 4);
    const nearFort = distToFort(gx, gy) < 18;
    if (!nearFort && !isWater(gx, gy, seed)) {
      grass.push({ x: gx, y: gy, seed: i * 17.3 });
    }
  }
  
  for (let i = 0; i < 120; i++) {
    const fx = 4 + (noise(i + 2000, 0, seed) * 0.5 + 0.5) * (MW - 8);
    const fy = 4 + (noise(0, i + 2000, seed) * 0.5 + 0.5) * (MH - 8);
    const nearFort = distToFort(fx, fy) < 18;
    if (!nearFort && !isWater(fx, fy, seed)) {
      flowers.push({ x: fx, y: fy, type: i % 4 });
    }
  }
  
  return { paths, trees, rocks, grass, flowers };
}

export default function SkillTreeGeneral() {
  const ref = useRef<HTMLCanvasElement>(null);
  const [sz, setSz] = useState({ w: 1200, h: 800 });
  const [pos, setPos] = useState({ x: CENTER_X, y: CENTER_Y + 8 });
  const [tgt, setTgt] = useState({ x: CENTER_X, y: CENTER_Y + 8 });
  const [mov, setMov] = useState(false);
  const [dir, setDir] = useState(1);
  const [cam, setCam] = useState({ x: 0, y: 0 });
  const [world, setWorld] = useState<ReturnType<typeof genWorld> | null>(null);
  const [hov, setHov] = useState<Dungeon | null>(null);
  const [hovNpc, setHovNpc] = useState<NPC | null>(null);
  const [sel, setSel] = useState<Dungeon | null>(null);
  const [selNpc, setSelNpc] = useState<NPC | null>(null);
  
  useEffect(() => {
    const upd = () => setSz({ w: window.innerWidth, h: window.innerHeight - 56 });
    upd();
    window.addEventListener('resize', upd);
    return () => window.removeEventListener('resize', upd);
  }, []);
  
  useEffect(() => { setWorld(genWorld(42)); }, []);
  
  useEffect(() => {
    const m = 12 * TILE;
    const pxPos = pos.x * TILE - cam.x, pyPos = pos.y * TILE - cam.y;
    let nx = cam.x, ny = cam.y;
    if (pxPos < m) nx = Math.max(0, pos.x * TILE - m);
    else if (pxPos > sz.w - m) nx = Math.min(MW * TILE - sz.w, pos.x * TILE - sz.w + m);
    if (pyPos < m) ny = Math.max(0, pos.y * TILE - m);
    else if (pyPos > sz.h - m) ny = Math.min(MH * TILE - sz.h, pos.y * TILE - sz.h + m);
    if (nx !== cam.x || ny !== cam.y) setCam({ x: nx, y: ny });
  }, [pos, cam, sz]);
  
  useEffect(() => {
    const iv = setInterval(() => {
      setPos(c => {
        const dx = tgt.x - c.x, dy = tgt.y - c.y;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d < 0.15) { setMov(false); return tgt; }
        
        const nx = c.x + (dx / d) * 0.12;
        const ny = c.y + (dy / d) * 0.12;
        
        if (isWater(nx, ny, 42)) {
          setMov(false);
          return c;
        }
        
        setMov(true);
        if (dx > 0.1) setDir(1); else if (dx < -0.1) setDir(-1);
        return { x: nx, y: ny };
      });
    }, 16);
    return () => clearInterval(iv);
  }, [tgt]);
  
  const onClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const cv = ref.current;
    if (!cv) return;
    const r = cv.getBoundingClientRect();
    const cx = (e.clientX - r.left + cam.x) / TILE;
    const cy = (e.clientY - r.top + cam.y) / TILE;
    
    const npc = NPCS.find(n => Math.abs(cx - n.x) < 2 && Math.abs(cy - n.y) < 2);
    if (npc) {
      const dist = Math.sqrt((pos.x - npc.x) ** 2 + (pos.y - npc.y) ** 2);
      if (dist < 4) setSelNpc(npc);
      else setTgt({ x: npc.x, y: npc.y + 1.5 });
      return;
    }
    
    const cl = DUNGEONS.find(d => Math.abs(cx - d.x) < 3 && Math.abs(cy - d.y) < 3);
    if (cl) {
      const dist = Math.sqrt((pos.x - cl.x) ** 2 + (pos.y - cl.y) ** 2);
      if (dist < 5) setSel(cl);
      else if (!isWater(cl.x, cl.y + 2.5, 42)) setTgt({ x: cl.x, y: cl.y + 2.5 });
    } else {
      if (!isWater(cx, cy, 42)) setTgt({ x: cx, y: cy });
      setSel(null);
      setSelNpc(null);
    }
  }, [pos, cam]);
  
  const onMv = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const cv = ref.current;
    if (!cv) return;
    const r = cv.getBoundingClientRect();
    const mx = (e.clientX - r.left + cam.x) / TILE;
    const my = (e.clientY - r.top + cam.y) / TILE;
    setHov(DUNGEONS.find(d => Math.abs(mx - d.x) < 3 && Math.abs(my - d.y) < 3) || null);
    setHovNpc(NPCS.find(n => Math.abs(mx - n.x) < 2 && Math.abs(my - n.y) < 2) || null);
  }, [cam]);
  
  const pathGrid = useMemo(() => world ? buildPathGrid(world.paths) : new Map(), [world]);
  
  useEffect(() => {
    const cv = ref.current;
    if (!cv || !world) return;
    const ctx = cv.getContext('2d');
    if (!ctx) return;
    
    let id: number, fr = 0;
    const seed = 42;
    
    const offscreen = document.createElement('canvas');
    offscreen.width = sz.w + CHUNK * 2;
    offscreen.height = sz.h + CHUNK * 2;
    const offCtx = offscreen.getContext('2d')!;
    let lastCamChunkX = -999, lastCamChunkY = -999;
    
    const render = () => {
      fr++;
      ctx.imageSmoothingEnabled = false;
      
      const camChunkX = Math.floor(cam.x / CHUNK);
      const camChunkY = Math.floor(cam.y / CHUNK);
      
      if (camChunkX !== lastCamChunkX || camChunkY !== lastCamChunkY) {
        lastCamChunkX = camChunkX;
        lastCamChunkY = camChunkY;
        const chunksX = Math.ceil(sz.w / CHUNK) + 2;
        const chunksY = Math.ceil(sz.h / CHUNK) + 2;
        for (let cy = 0; cy < chunksY; cy++) {
          for (let cx = 0; cx < chunksX; cx++) {
            const chunkData = renderTerrainChunk(camChunkX + cx, camChunkY + cy, pathGrid, world.paths, seed);
            offCtx.putImageData(chunkData, cx * CHUNK, cy * CHUNK);
          }
        }
      }
      
      ctx.drawImage(offscreen, -(cam.x % CHUNK), -(cam.y % CHUNK));
      
      const objs: { y: number; fn: () => void }[] = [];
      
      // Flores
      world.flowers.forEach(fl => {
        const fx = fl.x * TILE - cam.x, fy = fl.y * TILE - cam.y;
        if (fx > -20 && fx < sz.w + 20 && fy > -20 && fy < sz.h + 20) {
          objs.push({ y: fl.y * TILE - 200, fn: () => drawFlower8(ctx, fx, fy, fl.type) });
        }
      });
      
      // Césped
      world.grass.forEach(g => {
        const gx = g.x * TILE - cam.x, gy = g.y * TILE - cam.y;
        if (gx > -20 && gx < sz.w + 20 && gy > -20 && gy < sz.h + 20) {
          objs.push({ y: g.y * TILE - 150, fn: () => drawGrass8(ctx, gx, gy, fr, g.seed) });
        }
      });
      
      world.rocks.forEach(r => {
        const rx = r.x * TILE - cam.x, ry = r.y * TILE - cam.y;
        if (rx > -50 && rx < sz.w + 50 && ry > -50 && ry < sz.h + 50) {
          objs.push({ y: r.y * TILE, fn: () => drawRock8(ctx, rx, ry, r.s) });
        }
      });
      
      world.trees.forEach(t => {
        const tx = t.x * TILE - cam.x, ty = t.y * TILE - cam.y;
        if (tx > -100 && tx < sz.w + 100 && ty > -150 && ty < sz.h + 100) {
          objs.push({ y: t.y * TILE, fn: () => drawTree8(ctx, tx, ty, t.t, fr) });
        }
      });
      
      objs.push({ y: CENTER_Y * TILE + 100, fn: () => drawFortress8(ctx, cam.x, cam.y, fr) });
      
      NPCS.forEach(n => {
        const nx = n.x * TILE - cam.x, ny = n.y * TILE - cam.y;
        if (nx > -60 && nx < sz.w + 60 && ny > -80 && ny < sz.h + 60) {
          objs.push({ y: n.y * TILE, fn: () => drawNPC8(ctx, n, cam.x, cam.y, fr, n === hovNpc) });
        }
      });
      
      DUNGEONS.forEach(d => {
        const dx = d.x * TILE - cam.x, dy = d.y * TILE - cam.y;
        if (dx > -100 && dx < sz.w + 100 && dy > -150 && dy < sz.h + 80) {
          objs.push({ y: d.y * TILE, fn: () => drawDungeon8(ctx, d, d === hov, fr, cam.x, cam.y) });
        }
      });
      
      const psx = pos.x * TILE - cam.x, psy = pos.y * TILE - cam.y;
      objs.push({ y: pos.y * TILE, fn: () => drawPlayer8(ctx, psx, psy, mov, fr, dir) });
      
      objs.sort((a, b) => a.y - b.y);
      objs.forEach(o => o.fn());
      
      // Destino
      if (mov) {
        const tx = tgt.x * TILE - cam.x, ty = tgt.y * TILE - cam.y;
        ctx.strokeStyle = 'rgba(240,200,80,0.6)';
        ctx.lineWidth = 2;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.arc(tx, ty, 10 + Math.floor(Math.sin(fr * 0.1) * 3), 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);
      }
      
      id = requestAnimationFrame(render);
    };
    
    render();
    return () => cancelAnimationFrame(id);
  }, [world, pos, tgt, mov, dir, hov, hovNpc, cam, sz, pathGrid]);
  
  if (!world) return (
    <div className="h-screen bg-[#101820] flex flex-col items-center justify-center gap-4">
      <div className="text-6xl animate-bounce">🗺️</div>
      <div className="text-[#f0c040] text-2xl font-bold animate-pulse font-mono">Generando mundo...</div>
    </div>
  );
  
  return (
    <div className="h-screen bg-[#101820] flex flex-col overflow-hidden">
      <header className="bg-[#181828] border-b-4 border-[#302820] px-4 py-2 flex-shrink-0">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <div className="flex items-center gap-3">
            <span className="text-2xl">⚔️</span>
            <h1 className="text-xl font-bold text-[#f0c040] font-mono">Code Dungeon</h1>
          </div>
          <div className="flex items-center gap-6 text-sm font-mono">
            <div className="flex items-center gap-2 text-[#808080]">
              <span className="text-[#f0c040]">🏰</span>
              <span>Fortaleza del Gremio</span>
            </div>
            <div className="flex items-center gap-2 text-[#808080]">
              <span className="text-[#30b030]">🗡️</span>
              <span>{DUNGEONS.length} mazmorras</span>
            </div>
          </div>
        </div>
      </header>
      
      <main className="flex-1 overflow-hidden relative">
        <canvas 
          ref={ref} 
          width={sz.w} 
          height={sz.h} 
          onClick={onClick} 
          onMouseMove={onMv} 
          className="cursor-pointer" 
          style={{ imageRendering: 'pixelated' }} 
        />
      </main>
      
      {hovNpc && !selNpc && (
        <div className="fixed bottom-4 left-1/2 -translate-x-1/2 bg-[#181828] border-4 border-[#f0c040] p-4 min-w-[280px] z-50 font-mono">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-[#302820] flex items-center justify-center text-2xl border-2 border-[#504030]">👤</div>
            <div className="flex-1">
              <h3 className="font-bold text-white text-lg">{hovNpc.name}</h3>
              <p className="text-[#f0c040] text-sm">{hovNpc.role}</p>
            </div>
            <div className="text-[#f0c040] text-xl animate-bounce">!</div>
          </div>
        </div>
      )}
      
      {hov && !sel && !hovNpc && (
        <div className="fixed bottom-4 left-1/2 -translate-x-1/2 bg-[#181828] border-4 p-4 min-w-[300px] z-50 font-mono" style={{ borderColor: DCOL[hov.diff] }}>
          <div className="flex items-center gap-4">
            <div className="text-4xl p-2 bg-[#302820]">{hov.icon}</div>
            <div className="flex-1">
              <h3 className="font-bold text-white text-lg">{hov.title}</h3>
              <p className="text-[#808080] text-sm">{hov.desc}</p>
              <div className="flex items-center gap-1 mt-1">
                {Array.from({ length: { beginner: 1, intermediate: 2, advanced: 3, legendary: 4 }[hov.diff] }).map((_, i) => (
                  <span key={i} style={{ color: DCOL[hov.diff] }}>★</span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
      
      {selNpc && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={() => setSelNpc(null)}>
          <div className="bg-[#181828] border-4 border-[#f0c040] p-6 max-w-md w-full mx-4 font-mono" onClick={e => e.stopPropagation()}>
            <div className="flex items-start gap-4 mb-4">
              <div className="w-16 h-16 bg-[#302820] flex items-center justify-center text-3xl border-2 border-[#504030]">👤</div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-white">{selNpc.name}</h2>
                <p className="text-[#f0c040] text-lg">{selNpc.role}</p>
              </div>
              <button onClick={() => setSelNpc(null)} className="text-[#808080] hover:text-white text-2xl">✕</button>
            </div>
            <div className="bg-[#302820] p-4 mb-4 border-2 border-[#504030]">
              <p className="text-white text-lg italic">"{selNpc.dialog}"</p>
            </div>
            {selNpc.quest && (
              <Link 
                href={`/skill-tree-general/dungeon/${selNpc.quest}`} 
                className="block w-full text-center py-3 font-bold text-[#101020] bg-[#f0c040] hover:bg-[#f0d060] transition-colors text-lg"
              >
                ⚔️ Aceptar Misión: {DUNGEONS.find(d => d.id === selNpc.quest)?.title}
              </Link>
            )}
          </div>
        </div>
      )}
      
      {sel && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={() => setSel(null)}>
          <div className="bg-[#181828] border-4 p-6 max-w-md w-full mx-4 font-mono" style={{ borderColor: DCOL[sel.diff] }} onClick={e => e.stopPropagation()}>
            <div className="flex items-start gap-4 mb-4">
              <div className="text-5xl p-3 bg-[#302820]">{sel.icon}</div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-white">{sel.title}</h2>
                <p className="text-[#808080]">{sel.desc}</p>
                <div className="flex items-center gap-1 mt-2">
                  {Array.from({ length: { beginner: 1, intermediate: 2, advanced: 3, legendary: 4 }[sel.diff] }).map((_, i) => (
                    <span key={i} className="text-lg" style={{ color: DCOL[sel.diff] }}>★</span>
                  ))}
                  <span className="text-[#606060] text-sm ml-2 capitalize">{sel.diff}</span>
                </div>
              </div>
              <button onClick={() => setSel(null)} className="text-[#808080] hover:text-white text-2xl">✕</button>
            </div>
            <div className="grid grid-cols-3 gap-3 mb-4">
              <div className="bg-[#302820] p-3 text-center border-2 border-[#504030]">
                <div className="text-2xl mb-1">⚔️</div>
                <div className="text-white font-bold text-xl">{sel.enemies}</div>
                <div className="text-xs text-[#808080]">Enemigos</div>
              </div>
              <div className="bg-[#302820] p-3 text-center border-2 border-[#504030]">
                <div className="text-2xl mb-1">💀</div>
                <div className="text-white font-bold text-xs">{sel.boss}</div>
                <div className="text-xs text-[#808080]">Boss</div>
              </div>
              <div className="bg-[#302820] p-3 text-center border-2 border-[#504030]">
                <div className="text-2xl mb-1">⭐</div>
                <div className="text-[#f0c040] font-bold text-xl">{sel.xp}</div>
                <div className="text-xs text-[#808080]">XP</div>
              </div>
            </div>
            <Link 
              href={`/skill-tree-general/dungeon/${sel.id}`} 
              className="block w-full text-center py-3 font-bold text-white transition-colors text-lg" 
              style={{ backgroundColor: DCOL[sel.diff] }}
            >
              ⚔️ Entrar a la Mazmorra
            </Link>
          </div>
        </div>
      )}
      
      {/* Minimapa 16-bit */}
      <div className="fixed bottom-4 right-4 bg-[#181828] border-4 border-[#504030] p-2 z-20 font-mono">
        <div className="text-[10px] text-[#f0c040] text-center mb-1">MAPA</div>
        <div className="relative" style={{ width: 180, height: 135 }}>
          <div className="absolute inset-0 bg-[#206020]" />
          {/* Fortaleza */}
          <div className="absolute w-5 h-5 bg-[#f0c040] border-2 border-[#c08000] -translate-x-1/2 -translate-y-1/2" style={{ left: `${(CENTER_X / MW) * 100}%`, top: `${(CENTER_Y / MH) * 100}%` }} />
          {/* Viewport */}
          <div className="absolute border-2 border-white" style={{ left: `${(cam.x / (MW * TILE)) * 100}%`, top: `${(cam.y / (MH * TILE)) * 100}%`, width: `${(sz.w / (MW * TILE)) * 100}%`, height: `${(sz.h / (MH * TILE)) * 100}%` }} />
          {/* Dungeons */}
          {DUNGEONS.map(d => (
            <div key={d.id} className="absolute w-3 h-3 -translate-x-1/2 -translate-y-1/2 border border-white/50" style={{ left: `${(d.x / MW) * 100}%`, top: `${(d.y / MH) * 100}%`, backgroundColor: DCOL[d.diff] }} />
          ))}
          {/* Player */}
          <div className="absolute w-3 h-3 bg-white border-2 border-[#f0c040] -translate-x-1/2 -translate-y-1/2" style={{ left: `${(pos.x / MW) * 100}%`, top: `${(pos.y / MH) * 100}%` }} />
        </div>
      </div>
    </div>
  );
}
