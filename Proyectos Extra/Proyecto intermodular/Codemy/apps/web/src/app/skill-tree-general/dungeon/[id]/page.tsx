'use client';

import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { useRef, useEffect, useState, useCallback, useMemo } from 'react';

// ═══════════════════════════════════════════════════════════════
// CONSTANTES PIXEL ART
// ═══════════════════════════════════════════════════════════════

const PX = 4; // Tamaño base de pixel

const PAL = {
  BK: '#0a0a0f',
  BK2: '#12121a',
  S0: '#1a1a24',
  S1: '#2a2a38',
  S2: '#3a3a4c',
  S3: '#4a4a5c',
  S4: '#6a6a7c',
  S5: '#8a8a9c',
  WH: '#e8e8f0',
  // Colores temáticos
  G0: '#0a200a',
  G1: '#1a3818',
  G2: '#2a5028',
  G3: '#3a6838',
  G4: '#4a8048',
  // Marrón
  B0: '#1a1008',
  B1: '#2a1810',
  B2: '#3a2818',
  B3: '#4a3820',
  B4: '#5a4830',
  // Azul
  U0: '#081020',
  U1: '#102040',
  U2: '#203060',
  U3: '#304080',
  U4: '#4060a0',
  // Rojo
  R0: '#200808',
  R1: '#401010',
  R2: '#602020',
  R3: '#903030',
  R4: '#c04040',
  // Amarillo/Oro
  Y0: '#201808',
  Y1: '#403010',
  Y2: '#604820',
  Y3: '#907030',
  Y4: '#c0a040',
  Y5: '#e0c060',
  // Púrpura
  P0: '#100818',
  P1: '#201030',
  P2: '#381850',
  P3: '#502070',
  P4: '#7030a0',
};

const DCOL: Record<string, { main: string; dark: string; light: string }> = {
  beginner: { main: '#30a030', dark: '#1a5018', light: '#50c050' },
  intermediate: { main: '#3070c0', dark: '#183860', light: '#50a0f0' },
  advanced: { main: '#9030c0', dark: '#481860', light: '#b050e0' },
  legendary: { main: '#c03030', dark: '#601818', light: '#e05050' },
};

// ═══════════════════════════════════════════════════════════════
// DATOS DE MAZMORRAS
// ═══════════════════════════════════════════════════════════════

interface Room {
  id: string;
  title: string;
  enemies: number;
  xp: number;
  status: 'completed' | 'available' | 'locked';
  type: 'entrance' | 'room' | 'treasure' | 'boss';
}

interface DungeonData {
  id: string;
  title: string;
  diff: 'beginner' | 'intermediate' | 'advanced' | 'legendary';
  boss: string;
  totalXp: number;
  courseHref: string;
  theme: 'forest' | 'tech' | 'cave' | 'castle' | 'volcano' | 'void';
  rooms: Room[];
}

const DUNGEON_DATA: Record<string, DungeonData> = {
  intro: {
    id: 'intro', title: 'BOSQUE DEL CODIGO', diff: 'beginner', boss: 'SLIME SYNTAX',
    totalXp: 500, courseHref: '/intro-programacion', theme: 'forest',
    rooms: [
      { id: 'r1', title: 'QUE ES PROGRAMAR', enemies: 2, xp: 50, status: 'completed', type: 'entrance' },
      { id: 'r2', title: 'PENSAMIENTO LOGICO', enemies: 3, xp: 60, status: 'completed', type: 'room' },
      { id: 'r3', title: 'ALGORITMOS', enemies: 3, xp: 55, status: 'available', type: 'room' },
      { id: 'r4', title: 'TU PRIMER IDE', enemies: 2, xp: 70, status: 'locked', type: 'treasure' },
      { id: 'r5', title: 'HOLA MUNDO', enemies: 3, xp: 80, status: 'locked', type: 'room' },
      { id: 'r6', title: 'TIPOS LENGUAJES', enemies: 4, xp: 90, status: 'locked', type: 'room' },
      { id: 'r7', title: 'SLIME SYNTAX', enemies: 1, xp: 150, status: 'locked', type: 'boss' },
    ],
  },
  discord: {
    id: 'discord', title: 'SALON DE BOTS', diff: 'beginner', boss: 'BOT REBELDE',
    totalXp: 800, courseHref: '/discord-bot', theme: 'tech',
    rooms: [
      { id: 'r1', title: 'CREAR APP', enemies: 2, xp: 80, status: 'available', type: 'entrance' },
      { id: 'r2', title: 'TOKEN PERMISOS', enemies: 3, xp: 90, status: 'locked', type: 'room' },
      { id: 'r3', title: 'BOT ONLINE', enemies: 2, xp: 85, status: 'locked', type: 'treasure' },
      { id: 'r4', title: 'EVENTOS', enemies: 3, xp: 100, status: 'locked', type: 'room' },
      { id: 'r5', title: 'COMANDOS SLASH', enemies: 4, xp: 120, status: 'locked', type: 'room' },
      { id: 'r6', title: 'EMBEDS BOTONES', enemies: 4, xp: 130, status: 'locked', type: 'room' },
      { id: 'r7', title: 'BOT REBELDE', enemies: 1, xp: 200, status: 'locked', type: 'boss' },
    ],
  },
  streaming: {
    id: 'streaming', title: 'ARENA STREAMING', diff: 'beginner', boss: 'TROLL CHAT',
    totalXp: 400, courseHref: '/streaming', theme: 'tech',
    rooms: [
      { id: 'r1', title: 'CONFIGURAR OBS', enemies: 2, xp: 60, status: 'available', type: 'entrance' },
      { id: 'r2', title: 'ESCENAS FUENTES', enemies: 3, xp: 80, status: 'locked', type: 'room' },
      { id: 'r3', title: 'AUDIO PRO', enemies: 2, xp: 70, status: 'locked', type: 'treasure' },
      { id: 'r4', title: 'OVERLAYS', enemies: 3, xp: 75, status: 'locked', type: 'room' },
      { id: 'r5', title: 'TROLL CHAT', enemies: 1, xp: 150, status: 'locked', type: 'boss' },
    ],
  },
  python: {
    id: 'python', title: 'CAVERNA PYTHON', diff: 'intermediate', boss: 'SERPIENTE ANCESTRAL',
    totalXp: 1500, courseHref: '/skill-tree-python', theme: 'cave',
    rooms: [
      { id: 'r1', title: 'VARIABLES TIPOS', enemies: 3, xp: 100, status: 'available', type: 'entrance' },
      { id: 'r2', title: 'OPERADORES', enemies: 3, xp: 90, status: 'locked', type: 'room' },
      { id: 'r3', title: 'STRINGS', enemies: 4, xp: 110, status: 'locked', type: 'room' },
      { id: 'r4', title: 'LISTAS', enemies: 4, xp: 120, status: 'locked', type: 'room' },
      { id: 'r5', title: 'DICCIONARIOS', enemies: 4, xp: 130, status: 'locked', type: 'treasure' },
      { id: 'r6', title: 'CONDICIONALES', enemies: 4, xp: 115, status: 'locked', type: 'room' },
      { id: 'r7', title: 'BUCLES', enemies: 5, xp: 140, status: 'locked', type: 'room' },
      { id: 'r8', title: 'FUNCIONES', enemies: 4, xp: 150, status: 'locked', type: 'room' },
      { id: 'r9', title: 'CLASES POO', enemies: 5, xp: 180, status: 'locked', type: 'treasure' },
      { id: 'r10', title: 'SERPIENTE ANCESTRAL', enemies: 1, xp: 350, status: 'locked', type: 'boss' },
    ],
  },
  web: {
    id: 'web', title: 'CASTILLO FRONTEND', diff: 'intermediate', boss: 'COLOSO DOM',
    totalXp: 2000, courseHref: '/skill-tree-web', theme: 'castle',
    rooms: [
      { id: 'r1', title: 'HTML BASICO', enemies: 3, xp: 100, status: 'available', type: 'entrance' },
      { id: 'r2', title: 'ETIQUETAS', enemies: 3, xp: 110, status: 'locked', type: 'room' },
      { id: 'r3', title: 'FORMULARIOS', enemies: 4, xp: 120, status: 'locked', type: 'room' },
      { id: 'r4', title: 'CSS BASICO', enemies: 4, xp: 130, status: 'locked', type: 'room' },
      { id: 'r5', title: 'FLEXBOX', enemies: 4, xp: 140, status: 'locked', type: 'treasure' },
      { id: 'r6', title: 'CSS GRID', enemies: 4, xp: 150, status: 'locked', type: 'room' },
      { id: 'r7', title: 'JAVASCRIPT', enemies: 4, xp: 140, status: 'locked', type: 'room' },
      { id: 'r8', title: 'DOM', enemies: 5, xp: 180, status: 'locked', type: 'room' },
      { id: 'r9', title: 'REACT', enemies: 6, xp: 220, status: 'locked', type: 'treasure' },
      { id: 'r10', title: 'COLOSO DOM', enemies: 1, xp: 400, status: 'locked', type: 'boss' },
    ],
  },
  minecraft: {
    id: 'minecraft', title: 'MINA MINECRAFT', diff: 'intermediate', boss: 'CREEPER LEGENDARIO',
    totalXp: 1200, courseHref: '/minecraft-mods', theme: 'cave',
    rooms: [
      { id: 'r1', title: 'JAVA PARA MC', enemies: 3, xp: 100, status: 'available', type: 'entrance' },
      { id: 'r2', title: 'FORGE SETUP', enemies: 3, xp: 110, status: 'locked', type: 'room' },
      { id: 'r3', title: 'PRIMER MOD', enemies: 4, xp: 130, status: 'locked', type: 'treasure' },
      { id: 'r4', title: 'ITEMS CUSTOM', enemies: 4, xp: 140, status: 'locked', type: 'room' },
      { id: 'r5', title: 'BLOQUES', enemies: 4, xp: 150, status: 'locked', type: 'room' },
      { id: 'r6', title: 'ENTIDADES', enemies: 5, xp: 160, status: 'locked', type: 'room' },
      { id: 'r7', title: 'CREEPER LEGENDARIO', enemies: 1, xp: 340, status: 'locked', type: 'boss' },
    ],
  },
  arduino: {
    id: 'arduino', title: 'TALLER INVENTOR', diff: 'intermediate', boss: 'CORTO CIRCUITO',
    totalXp: 1400, courseHref: '/skill-tree-arduino', theme: 'tech',
    rooms: [
      { id: 'r1', title: 'INTRO ARDUINO', enemies: 2, xp: 80, status: 'available', type: 'entrance' },
      { id: 'r2', title: 'LEDS', enemies: 3, xp: 100, status: 'locked', type: 'room' },
      { id: 'r3', title: 'BOTONES', enemies: 3, xp: 110, status: 'locked', type: 'room' },
      { id: 'r4', title: 'SERVOS PWM', enemies: 4, xp: 130, status: 'locked', type: 'treasure' },
      { id: 'r5', title: 'SENSORES', enemies: 4, xp: 140, status: 'locked', type: 'room' },
      { id: 'r6', title: 'LCD DISPLAY', enemies: 4, xp: 150, status: 'locked', type: 'room' },
      { id: 'r7', title: 'WIFI ESP32', enemies: 5, xp: 180, status: 'locked', type: 'room' },
      { id: 'r8', title: 'CORTO CIRCUITO', enemies: 1, xp: 310, status: 'locked', type: 'boss' },
    ],
  },
  java: {
    id: 'java', title: 'TORRE BACKEND', diff: 'advanced', boss: 'GUARDIAN BEANS',
    totalXp: 2500, courseHref: '/skill-tree-java', theme: 'castle',
    rooms: [
      { id: 'r1', title: 'JAVA BASICS', enemies: 4, xp: 120, status: 'available', type: 'entrance' },
      { id: 'r2', title: 'POO', enemies: 4, xp: 140, status: 'locked', type: 'room' },
      { id: 'r3', title: 'EXCEPCIONES', enemies: 5, xp: 160, status: 'locked', type: 'room' },
      { id: 'r4', title: 'COLECCIONES', enemies: 5, xp: 170, status: 'locked', type: 'room' },
      { id: 'r5', title: 'STREAMS', enemies: 5, xp: 180, status: 'locked', type: 'treasure' },
      { id: 'r6', title: 'SPRING BOOT', enemies: 5, xp: 200, status: 'locked', type: 'room' },
      { id: 'r7', title: 'REST APIS', enemies: 6, xp: 220, status: 'locked', type: 'room' },
      { id: 'r8', title: 'JPA DATABASE', enemies: 6, xp: 240, status: 'locked', type: 'treasure' },
      { id: 'r9', title: 'GUARDIAN BEANS', enemies: 1, xp: 460, status: 'locked', type: 'boss' },
    ],
  },
  devops: {
    id: 'devops', title: 'CIELOS NUBE', diff: 'advanced', boss: 'TITAN DEPLOY',
    totalXp: 2200, courseHref: '/skill-tree-devops', theme: 'tech',
    rooms: [
      { id: 'r1', title: 'LINUX BASICS', enemies: 3, xp: 100, status: 'available', type: 'entrance' },
      { id: 'r2', title: 'BASH SCRIPT', enemies: 4, xp: 130, status: 'locked', type: 'room' },
      { id: 'r3', title: 'GIT AVANZADO', enemies: 4, xp: 140, status: 'locked', type: 'room' },
      { id: 'r4', title: 'DOCKER', enemies: 5, xp: 170, status: 'locked', type: 'room' },
      { id: 'r5', title: 'COMPOSE', enemies: 5, xp: 180, status: 'locked', type: 'treasure' },
      { id: 'r6', title: 'CI CD', enemies: 5, xp: 190, status: 'locked', type: 'room' },
      { id: 'r7', title: 'KUBERNETES', enemies: 6, xp: 240, status: 'locked', type: 'room' },
      { id: 'r8', title: 'TITAN DEPLOY', enemies: 1, xp: 400, status: 'locked', type: 'boss' },
    ],
  },
  cpp: {
    id: 'cpp', title: 'VOLCAN RENDIMIENTO', diff: 'legendary', boss: 'DEMONIO MEMORY LEAK',
    totalXp: 5000, courseHref: '/skill-tree-cpp', theme: 'volcano',
    rooms: [
      { id: 'r1', title: 'CPP BASICS', enemies: 5, xp: 200, status: 'available', type: 'entrance' },
      { id: 'r2', title: 'PUNTEROS', enemies: 6, xp: 280, status: 'locked', type: 'room' },
      { id: 'r3', title: 'REFERENCIAS', enemies: 6, xp: 260, status: 'locked', type: 'room' },
      { id: 'r4', title: 'MEMORIA', enemies: 7, xp: 320, status: 'locked', type: 'treasure' },
      { id: 'r5', title: 'SMART PTRS', enemies: 7, xp: 350, status: 'locked', type: 'room' },
      { id: 'r6', title: 'STL', enemies: 6, xp: 300, status: 'locked', type: 'room' },
      { id: 'r7', title: 'TEMPLATES', enemies: 7, xp: 380, status: 'locked', type: 'room' },
      { id: 'r8', title: 'THREADS', enemies: 8, xp: 420, status: 'locked', type: 'treasure' },
      { id: 'r9', title: 'DEMONIO MEMORY LEAK', enemies: 1, xp: 640, status: 'locked', type: 'boss' },
    ],
  },
  hacking: {
    id: 'hacking', title: 'ABISMO HACKING', diff: 'legendary', boss: 'HACKER OSCURO',
    totalXp: 6000, courseHref: '/hacking-wifi', theme: 'void',
    rooms: [
      { id: 'r1', title: 'SEGURIDAD', enemies: 5, xp: 220, status: 'available', type: 'entrance' },
      { id: 'r2', title: 'NETWORKING', enemies: 6, xp: 280, status: 'locked', type: 'room' },
      { id: 'r3', title: 'LINUX HACK', enemies: 6, xp: 300, status: 'locked', type: 'room' },
      { id: 'r4', title: 'RECON', enemies: 7, xp: 350, status: 'locked', type: 'room' },
      { id: 'r5', title: 'SCANNING', enemies: 7, xp: 380, status: 'locked', type: 'treasure' },
      { id: 'r6', title: 'WEB VULNS', enemies: 8, xp: 420, status: 'locked', type: 'room' },
      { id: 'r7', title: 'SQL INJECT', enemies: 8, xp: 450, status: 'locked', type: 'room' },
      { id: 'r8', title: 'METASPLOIT', enemies: 9, xp: 550, status: 'locked', type: 'treasure' },
      { id: 'r9', title: 'HACKER OSCURO', enemies: 1, xp: 670, status: 'locked', type: 'boss' },
    ],
  },
};

const DEFAULT_DUNGEON: DungeonData = {
  id: 'unknown', title: 'MAZMORRA DESCONOCIDA', diff: 'beginner', boss: 'GUARDIAN',
  totalXp: 500, courseHref: '/courses', theme: 'cave',
  rooms: [
    { id: 'r1', title: 'ENTRADA', enemies: 2, xp: 100, status: 'available', type: 'entrance' },
    { id: 'r2', title: 'SALA 1', enemies: 3, xp: 150, status: 'locked', type: 'room' },
    { id: 'r3', title: 'BOSS', enemies: 1, xp: 250, status: 'locked', type: 'boss' },
  ],
};

// ═══════════════════════════════════════════════════════════════
// TEMAS DE MAZMORRA
// ═══════════════════════════════════════════════════════════════

const THEMES: Record<string, { floor: string[]; wall: string[]; path: string }> = {
  forest: { floor: [PAL.G0, PAL.G1], wall: [PAL.B1, PAL.B2, PAL.B3], path: PAL.G2 },
  tech: { floor: [PAL.U0, PAL.U1], wall: [PAL.S0, PAL.S1, PAL.S2], path: PAL.U2 },
  cave: { floor: [PAL.P0, PAL.P1], wall: [PAL.S0, PAL.S1, PAL.S2], path: PAL.P2 },
  castle: { floor: [PAL.B0, PAL.B1], wall: [PAL.S1, PAL.S2, PAL.S3], path: PAL.Y2 },
  volcano: { floor: [PAL.R0, PAL.R1], wall: [PAL.B1, PAL.B2, PAL.R1], path: PAL.R2 },
  void: { floor: [PAL.BK, PAL.BK2], wall: [PAL.P1, PAL.P2, PAL.P3], path: PAL.P3 },
};

// ═══════════════════════════════════════════════════════════════
// FUNCIONES DE DIBUJO PIXEL ART
// ═══════════════════════════════════════════════════════════════

function px(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, c: string) {
  ctx.fillStyle = c;
  ctx.fillRect(Math.floor(x) * PX, Math.floor(y) * PX, w * PX, h * PX);
}

function hash(x: number, y: number, s: number = 0): number {
  let h = x * 374761393 + y * 668265263 + s * 1013904223;
  h = (h ^ (h >> 13)) * 1274126177;
  return ((h ^ (h >> 16)) >>> 0) / 4294967296;
}

// Dibujar puerta 8-bit
function drawDoor(ctx: CanvasRenderingContext2D, x: number, y: number, room: Room, frame: number, theme: string, hovered: boolean, diffCol: { main: string; dark: string; light: string }) {
  const t = THEMES[theme] || THEMES.cave;
  const isBoss = room.type === 'boss';
  const isTreasure = room.type === 'treasure';
  const isCompleted = room.status === 'completed';
  const isAvailable = room.status === 'available';
  const isLocked = room.status === 'locked';
  
  const ox = hovered ? -1 : 0;
  const oy = hovered ? -1 : 0;
  
  // Base/marco de piedra
  const frameC = isBoss ? PAL.R2 : isTreasure ? PAL.Y3 : t.wall[2];
  const frameD = isBoss ? PAL.R1 : isTreasure ? PAL.Y2 : t.wall[1];
  
  // Marco exterior
  px(ctx, x - 8 + ox, y - 12 + oy, 16, 16, frameD);
  px(ctx, x - 7 + ox, y - 11 + oy, 14, 14, frameC);
  
  // Interior de la puerta
  let doorC = PAL.S0;
  if (isCompleted) doorC = PAL.G2;
  else if (isAvailable) doorC = diffCol.dark;
  else if (isBoss) doorC = PAL.R0;
  
  px(ctx, x - 5 + ox, y - 9 + oy, 10, 11, doorC);
  
  // Detalles según tipo
  if (isBoss) {
    // Calavera
    px(ctx, x - 3 + ox, y - 7 + oy, 6, 5, PAL.WH);
    px(ctx, x - 2 + ox, y - 6 + oy, 1, 2, PAL.BK);
    px(ctx, x + 1 + ox, y - 6 + oy, 1, 2, PAL.BK);
    px(ctx, x - 1 + ox, y - 3 + oy, 2, 1, PAL.BK);
    // Cuernos
    px(ctx, x - 4 + ox, y - 8 + oy, 1, 3, PAL.R3);
    px(ctx, x + 3 + ox, y - 8 + oy, 1, 3, PAL.R3);
    // Llamas animadas
    if (!isLocked) {
      const fl = Math.floor(frame / 8) % 3;
      px(ctx, x - 6 + ox, y - 6 - fl, 2, 3 + fl, PAL.R4);
      px(ctx, x + 4 + ox, y - 6 - fl, 2, 3 + fl, PAL.R4);
    }
  } else if (isTreasure) {
    // Cofre
    px(ctx, x - 3 + ox, y - 5 + oy, 6, 4, PAL.Y3);
    px(ctx, x - 2 + ox, y - 4 + oy, 4, 2, PAL.Y4);
    // Cerradura
    px(ctx, x - 1 + ox, y - 4 + oy, 2, 2, isLocked ? PAL.S3 : PAL.Y5);
    // Brillo
    if (!isLocked) {
      const sh = Math.sin(frame * 0.1) > 0;
      if (sh) px(ctx, x + 1 + ox, y - 5 + oy, 1, 1, PAL.WH);
    }
  } else {
    // Puerta normal - arco
    px(ctx, x - 4 + ox, y - 8 + oy, 8, 2, frameC);
    px(ctx, x - 3 + ox, y - 9 + oy, 6, 1, frameC);
    // Antorchas si disponible
    if (isAvailable) {
      const fl = Math.floor(frame / 6) % 2;
      px(ctx, x - 6 + ox, y - 4, 1, 4, PAL.B3);
      px(ctx, x + 5 + ox, y - 4, 1, 4, PAL.B3);
      px(ctx, x - 6 + ox, y - 5 - fl, 1, 2, PAL.Y4);
      px(ctx, x + 5 + ox, y - 5 - fl, 1, 2, PAL.Y4);
    }
    // Candado si bloqueada
    if (isLocked) {
      px(ctx, x - 2 + ox, y - 4 + oy, 4, 4, PAL.S2);
      px(ctx, x - 1 + ox, y - 5 + oy, 2, 2, PAL.S3);
      px(ctx, x - 1 + ox, y - 3 + oy, 2, 2, PAL.Y2);
    }
    // Check si completada
    if (isCompleted) {
      px(ctx, x - 2 + ox, y - 5 + oy, 1, 2, PAL.G4);
      px(ctx, x - 1 + ox, y - 4 + oy, 1, 3, PAL.G4);
      px(ctx, x + ox, y - 3 + oy, 1, 2, PAL.G4);
    }
  }
  
  // Sombra
  px(ctx, x - 4, y + 3, 8, 1, PAL.BK);
}

// Dibujar jugador 8-bit
function drawPlayer(ctx: CanvasRenderingContext2D, x: number, y: number, frame: number) {
  const bob = Math.floor(Math.sin(frame * 0.15) * 1);
  const yy = y + bob;
  
  // Sombra
  ctx.fillStyle = 'rgba(0,0,0,0.4)';
  ctx.beginPath();
  ctx.ellipse(x * PX, (y + 4) * PX, 3 * PX, 1 * PX, 0, 0, Math.PI * 2);
  ctx.fill();
  
  // Cuerpo (túnica)
  px(ctx, x - 2, yy, 4, 4, PAL.U2);
  px(ctx, x - 1, yy + 1, 2, 2, PAL.U3);
  
  // Brazos
  px(ctx, x - 3, yy + 1, 1, 2, PAL.U2);
  px(ctx, x + 2, yy + 1, 1, 2, PAL.U2);
  
  // Cabeza
  px(ctx, x - 2, yy - 3, 4, 3, '#e0b090');
  
  // Pelo/sombrero
  px(ctx, x - 2, yy - 4, 4, 2, PAL.B3);
  px(ctx, x - 1, yy - 5, 2, 1, PAL.B3);
  
  // Ojos
  if (frame % 120 > 5) {
    px(ctx, x - 1, yy - 2, 1, 1, PAL.BK);
    px(ctx, x + 1, yy - 2, 1, 1, PAL.BK);
  }
  
  // Bastón
  const sw = Math.sin(frame * 0.08);
  px(ctx, x + 3, yy - 2 + Math.floor(sw), 1, 5, PAL.B2);
  px(ctx, x + 3, yy - 3 + Math.floor(sw), 1, 1, PAL.Y4);
}

// ═══════════════════════════════════════════════════════════════
// COMPONENTE PRINCIPAL
// ═══════════════════════════════════════════════════════════════

export default function DungeonInterior() {
  const params = useParams();
  const router = useRouter();
  const dungeonId = params.id as string;
  const dungeon = DUNGEON_DATA[dungeonId] || { ...DEFAULT_DUNGEON, id: dungeonId };
  const theme = THEMES[dungeon.theme] || THEMES.cave;
  const diffCol = DCOL[dungeon.diff];

  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [sz, setSz] = useState({ w: 800, h: 600 });
  const [selectedRoom, setSelectedRoom] = useState<Room | null>(null);
  const [hoveredRoom, setHoveredRoom] = useState<number | null>(null);
  const [playerPos, setPlayerPos] = useState(0);
  const [playerXY, setPlayerXY] = useState({ x: 0, y: 0 });
  const [frame, setFrame] = useState(0);

  // Posiciones de salas
  const roomPositions = useMemo(() => {
    const positions: { x: number; y: number }[] = [];
    const numRooms = dungeon.rooms.length;
    const ROOM_SPACING = 50; // en unidades de pixel (x4 = 200px)
    const START_X = 30;
    const START_Y = 25;
    
    let x = START_X;
    let y = START_Y;
    let dir = 1;
    
    for (let i = 0; i < numRooms; i++) {
      positions.push({ x, y });
      
      if ((i + 1) % 3 === 0 && i < numRooms - 1) {
        y += 40;
        dir *= -1;
      } else {
        x += ROOM_SPACING * dir;
      }
    }
    
    return positions;
  }, [dungeon.rooms.length]);

  // Calcular tamaño del mapa
  const mapSize = useMemo(() => {
    if (roomPositions.length === 0) return { w: 200, h: 150 };
    const maxX = Math.max(...roomPositions.map(p => p.x)) + 40;
    const maxY = Math.max(...roomPositions.map(p => p.y)) + 50;
    return { w: Math.max(maxX, 200), h: Math.max(maxY, 120) };
  }, [roomPositions]);

  // Animación
  useEffect(() => {
    const iv = setInterval(() => setFrame(f => f + 1), 50);
    return () => clearInterval(iv);
  }, []);

  // Resize
  useEffect(() => {
    const upd = () => setSz({ w: window.innerWidth, h: window.innerHeight - 80 });
    upd();
    window.addEventListener('resize', upd);
    return () => window.removeEventListener('resize', upd);
  }, []);

  // Inicializar posición jugador
  useEffect(() => {
    if (roomPositions.length > 0) {
      setPlayerXY({ x: roomPositions[0].x, y: roomPositions[0].y + 18 });
    }
  }, [roomPositions]);

  // Mover jugador hacia sala seleccionada
  useEffect(() => {
    if (roomPositions.length === 0) return;
    const target = roomPositions[playerPos];
    if (!target) return;
    
    const iv = setInterval(() => {
      setPlayerXY(prev => {
        const tx = target.x;
        const ty = target.y + 18;
        const dx = tx - prev.x;
        const dy = ty - prev.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist < 1) return { x: tx, y: ty };
        
        const speed = 2;
        return {
          x: prev.x + (dx / dist) * speed,
          y: prev.y + (dy / dist) * speed,
        };
      });
    }, 30);
    
    return () => clearInterval(iv);
  }, [playerPos, roomPositions]);

  // Dibujar canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    ctx.imageSmoothingEnabled = false;
    
    // Fondo
    ctx.fillStyle = theme.floor[0];
    ctx.fillRect(0, 0, mapSize.w * PX, mapSize.h * PX);
    
    // Patrón de suelo
    for (let py = 0; py < mapSize.h; py += 8) {
      for (let ppx = 0; ppx < mapSize.w; ppx += 8) {
        if (hash(ppx, py, 1) > 0.7) {
          px(ctx, ppx, py, 4, 4, theme.floor[1]);
        }
        if (hash(ppx, py, 2) > 0.85) {
          px(ctx, ppx + 2, py + 2, 2, 2, theme.wall[0]);
        }
      }
    }
    
    // Paredes laterales
    for (let py = 0; py < mapSize.h; py += 4) {
      px(ctx, 0, py, 4, 4, theme.wall[Math.floor(hash(0, py, 3) * 3)]);
      px(ctx, mapSize.w - 4, py, 4, 4, theme.wall[Math.floor(hash(mapSize.w, py, 3) * 3)]);
    }
    
    // Caminos entre salas
    ctx.lineCap = 'round';
    for (let i = 0; i < roomPositions.length - 1; i++) {
      const from = roomPositions[i];
      const to = roomPositions[i + 1];
      const room = dungeon.rooms[i];
      
      const isCompleted = room?.status === 'completed';
      const pathCol = isCompleted ? PAL.G2 : theme.path;
      
      // Camino pixelado
      const steps = 20;
      for (let s = 0; s <= steps; s++) {
        const t = s / steps;
        const mx = from.x + (to.x - from.x) * t;
        const my = from.y + (to.y - from.y) * t + 4;
        const w = isCompleted ? 3 : 2;
        px(ctx, mx - w/2, my, w, 2, pathCol);
      }
    }
    
    // Ordenar elementos por Y para depth sorting
    const drawList: { y: number; fn: () => void }[] = [];
    
    // Salas
    roomPositions.forEach((pos, i) => {
      const room = dungeon.rooms[i];
      if (!room) return;
      drawList.push({
        y: pos.y,
        fn: () => drawDoor(ctx, pos.x, pos.y, room, frame, dungeon.theme, hoveredRoom === i, diffCol),
      });
    });
    
    // Jugador
    drawList.push({
      y: playerXY.y,
      fn: () => drawPlayer(ctx, playerXY.x, playerXY.y, frame),
    });
    
    // Dibujar ordenado
    drawList.sort((a, b) => a.y - b.y);
    drawList.forEach(d => d.fn());
    
    // Números de sala
    ctx.font = `bold ${PX * 3}px monospace`;
    ctx.textAlign = 'center';
    roomPositions.forEach((pos, i) => {
      const room = dungeon.rooms[i];
      if (!room) return;
      
      const col = room.status === 'completed' ? PAL.G4 : room.status === 'available' ? diffCol.light : PAL.S3;
      ctx.fillStyle = col;
      ctx.fillText(`${i + 1}`, pos.x * PX, (pos.y + 10) * PX);
    });
    
  }, [sz, frame, dungeon, roomPositions, playerXY, hoveredRoom, theme, diffCol, mapSize]);

  // Click handler
  const handleClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const mx = (e.clientX - rect.left) * scaleX / PX;
    const my = (e.clientY - rect.top) * scaleY / PX;
    
    for (let i = 0; i < roomPositions.length; i++) {
      const p = roomPositions[i];
      const room = dungeon.rooms[i];
      if (!p || !room) continue;
      
      if (Math.abs(mx - p.x) < 12 && Math.abs(my - p.y) < 12) {
        setPlayerPos(i);
        if (room.status !== 'locked') {
          setTimeout(() => setSelectedRoom(room), 400);
        }
        return;
      }
    }
  }, [roomPositions, dungeon.rooms]);

  // Hover handler
  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const mx = (e.clientX - rect.left) * scaleX / PX;
    const my = (e.clientY - rect.top) * scaleY / PX;
    
    let found = -1;
    for (let i = 0; i < roomPositions.length; i++) {
      const p = roomPositions[i];
      if (p && Math.abs(mx - p.x) < 12 && Math.abs(my - p.y) < 12) {
        found = i;
        break;
      }
    }
    setHoveredRoom(found >= 0 ? found : null);
  }, [roomPositions]);

  const completedRooms = dungeon.rooms.filter(r => r.status === 'completed').length;
  const earnedXp = dungeon.rooms.filter(r => r.status === 'completed').reduce((s, r) => s + r.xp, 0);
  const progress = Math.round((completedRooms / dungeon.rooms.length) * 100);

  return (
    <div className="h-screen flex flex-col overflow-hidden font-mono" style={{ backgroundColor: PAL.BK, imageRendering: 'pixelated' }}>
      {/* Header 8-bit */}
      <header className="flex-shrink-0 px-4 py-2" style={{ backgroundColor: PAL.BK2, borderBottom: `${PX}px solid ${diffCol.main}` }}>
        <div className="flex items-center justify-between max-w-6xl mx-auto">
          <div className="flex items-center gap-4">
            <button 
              onClick={() => router.push('/skill-tree-general')} 
              className="px-3 py-1 text-sm transition-colors"
              style={{ color: PAL.S4, backgroundColor: PAL.S0 }}
              onMouseEnter={e => { e.currentTarget.style.color = PAL.WH; e.currentTarget.style.backgroundColor = PAL.S1; }}
              onMouseLeave={e => { e.currentTarget.style.color = PAL.S4; e.currentTarget.style.backgroundColor = PAL.S0; }}
            >
              {'<'} SALIR
            </button>
            <div style={{ width: PX, height: 24, backgroundColor: PAL.S2 }} />
            <div>
              <h1 className="text-lg font-bold tracking-wider" style={{ color: diffCol.light }}>{dungeon.title}</h1>
              <div className="text-xs" style={{ color: PAL.S4 }}>{dungeon.rooms.length} SALAS</div>
            </div>
          </div>
          
          <div className="flex items-center gap-6">
            {/* Barra de progreso */}
            <div className="flex flex-col items-end gap-1">
              <div className="flex items-center gap-2 text-xs">
                <span style={{ color: PAL.S4 }}>{completedRooms}/{dungeon.rooms.length}</span>
                <span style={{ color: PAL.WH }}>{progress}%</span>
              </div>
              <div style={{ width: 120, height: PX * 2, backgroundColor: PAL.S0 }}>
                <div style={{ width: `${progress}%`, height: '100%', backgroundColor: diffCol.main }} />
              </div>
            </div>
            
            {/* XP */}
            <div className="text-center px-3 py-1" style={{ backgroundColor: PAL.S0 }}>
              <div className="text-sm font-bold" style={{ color: PAL.Y4 }}>{earnedXp}/{dungeon.totalXp}</div>
              <div className="text-xs" style={{ color: PAL.S4 }}>XP</div>
            </div>
            
            {/* Dificultad */}
            <div className="flex gap-1">
              {Array.from({ length: { beginner: 1, intermediate: 2, advanced: 3, legendary: 4 }[dungeon.diff] }).map((_, i) => (
                <div key={i} style={{ width: PX * 3, height: PX * 3, backgroundColor: diffCol.main }} />
              ))}
            </div>
          </div>
        </div>
      </header>

      {/* Canvas del mapa */}
      <main className="flex-1 overflow-auto flex items-center justify-center p-4">
        <canvas
          ref={canvasRef}
          width={mapSize.w * PX}
          height={mapSize.h * PX}
          onClick={handleClick}
          onMouseMove={handleMouseMove}
          className="cursor-pointer max-w-full max-h-full"
          style={{ imageRendering: 'pixelated' }}
        />
      </main>

      {/* Leyenda */}
      <div 
        className="fixed bottom-4 left-4 p-3 text-xs"
        style={{ backgroundColor: PAL.BK2, border: `${PX}px solid ${PAL.S2}` }}
      >
        <div className="mb-2 font-bold" style={{ color: PAL.S4 }}>LEYENDA</div>
        <div className="grid gap-1">
          <div className="flex items-center gap-2">
            <div style={{ width: PX * 2, height: PX * 2, backgroundColor: PAL.G3 }} />
            <span style={{ color: PAL.S5 }}>COMPLETADA</span>
          </div>
          <div className="flex items-center gap-2">
            <div style={{ width: PX * 2, height: PX * 2, backgroundColor: diffCol.main }} />
            <span style={{ color: PAL.S5 }}>DISPONIBLE</span>
          </div>
          <div className="flex items-center gap-2">
            <div style={{ width: PX * 2, height: PX * 2, backgroundColor: PAL.S2 }} />
            <span style={{ color: PAL.S5 }}>BLOQUEADA</span>
          </div>
          <div className="flex items-center gap-2">
            <div style={{ width: PX * 2, height: PX * 2, backgroundColor: PAL.Y3 }} />
            <span style={{ color: PAL.S5 }}>TESORO</span>
          </div>
          <div className="flex items-center gap-2">
            <div style={{ width: PX * 2, height: PX * 2, backgroundColor: PAL.R3 }} />
            <span style={{ color: PAL.S5 }}>BOSS</span>
          </div>
        </div>
      </div>

      {/* Info Boss */}
      <div 
        className="fixed bottom-4 right-4 p-3 text-xs"
        style={{ backgroundColor: PAL.BK2, border: `${PX}px solid ${PAL.R2}` }}
      >
        <div className="font-bold mb-1" style={{ color: PAL.R4 }}>BOSS FINAL</div>
        <div style={{ color: PAL.WH }}>{dungeon.boss}</div>
        <div style={{ color: PAL.Y4 }}>{dungeon.rooms.find(r => r.type === 'boss')?.xp || 0} XP</div>
      </div>

      {/* Modal de sala */}
      {selectedRoom && (
        <div 
          className="fixed inset-0 z-50 flex items-center justify-center"
          style={{ backgroundColor: 'rgba(0,0,0,0.9)' }}
          onClick={() => setSelectedRoom(null)}
        >
          <div 
            className="max-w-md w-full mx-4 p-6"
            style={{ 
              backgroundColor: PAL.BK2,
              border: `${PX}px solid ${selectedRoom.type === 'boss' ? PAL.R3 : selectedRoom.type === 'treasure' ? PAL.Y3 : diffCol.main}`,
            }}
            onClick={e => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-xl font-bold tracking-wider" style={{ color: PAL.WH }}>{selectedRoom.title}</h2>
                <div className="flex gap-4 mt-2 text-sm">
                  <span style={{ color: PAL.R4 }}>{selectedRoom.enemies} ENEMIGOS</span>
                  <span style={{ color: PAL.Y4 }}>{selectedRoom.xp} XP</span>
                </div>
              </div>
              <button 
                onClick={() => setSelectedRoom(null)}
                className="text-xl px-2"
                style={{ color: PAL.S4 }}
              >
                X
              </button>
            </div>

            {/* Estado */}
            {selectedRoom.status === 'completed' ? (
              <div 
                className="p-4 mb-6 text-center"
                style={{ backgroundColor: PAL.G0, border: `${PX}px solid ${PAL.G2}` }}
              >
                <div className="font-bold text-lg" style={{ color: PAL.G4 }}>SALA CONQUISTADA</div>
                <div style={{ color: PAL.G3 }}>{selectedRoom.xp} XP GANADOS</div>
              </div>
            ) : (
              <div className="grid grid-cols-3 gap-3 mb-6">
                <div className="text-center p-3" style={{ backgroundColor: PAL.S0 }}>
                  <div className="font-bold text-lg" style={{ color: PAL.R4 }}>{selectedRoom.enemies}</div>
                  <div className="text-xs" style={{ color: PAL.S4 }}>ENEMIGOS</div>
                </div>
                <div className="text-center p-3" style={{ backgroundColor: PAL.S0 }}>
                  <div className="font-bold text-lg" style={{ color: PAL.Y4 }}>{selectedRoom.xp}</div>
                  <div className="text-xs" style={{ color: PAL.S4 }}>XP</div>
                </div>
                <div className="text-center p-3" style={{ backgroundColor: PAL.S0 }}>
                  <div className="font-bold text-lg" style={{ color: PAL.WH }}>1</div>
                  <div className="text-xs" style={{ color: PAL.S4 }}>LECCION</div>
                </div>
              </div>
            )}

            {/* Botones */}
            <div className="flex gap-3">
              <Link 
                href={dungeon.courseHref}
                className="flex-1 text-center py-3 font-bold tracking-wider transition-all"
                style={{ 
                  backgroundColor: selectedRoom.type === 'boss' ? PAL.R2 : diffCol.main,
                  color: PAL.WH,
                }}
              >
                {selectedRoom.status === 'completed' ? 'REVISAR' : selectedRoom.type === 'boss' ? 'ENFRENTAR BOSS' : 'ENTRAR'}
              </Link>
              <button 
                onClick={() => setSelectedRoom(null)}
                className="px-6 py-3"
                style={{ backgroundColor: PAL.S1, color: PAL.S4 }}
              >
                CERRAR
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
