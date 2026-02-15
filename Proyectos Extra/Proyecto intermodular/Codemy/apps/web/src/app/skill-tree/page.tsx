'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowRight, Swords, Shield, Scroll, Crown, Map, Users } from 'lucide-react';
import EnemySprite from '@/components/game/EnemySprite';
import SpriteGenerator from '@/components/game/SpriteGenerator';

// Tipos de mazmorra
type DungeonDifficulty = 'beginner' | 'intermediate' | 'advanced' | 'legendary';

interface DungeonCourse {
  id: string;
  title: string;
  description: string;
  href: string;
  tags: string[];
  difficulty: DungeonDifficulty;
  enemies: number;
  boss: string;
  xpReward: number;
  goldReward: number;
  icon: string;
  enemyType: 'slime' | 'skeleton' | 'goblin' | 'orc' | 'dragon' | 'boss';
  region: 'forest' | 'castle' | 'cave' | 'volcano' | 'sky' | 'abyss';
}

const DIFFICULTY_CONFIG: Record<DungeonDifficulty, { color: string; border: string; glow: string; label: string }> = {
  beginner: { color: 'from-green-800 to-emerald-900', border: 'border-green-500/50', glow: 'shadow-green-500/20', label: '🌱 Principiante' },
  intermediate: { color: 'from-amber-800 to-orange-900', border: 'border-amber-500/50', glow: 'shadow-amber-500/20', label: '⚔️ Intermedio' },
  advanced: { color: 'from-purple-800 to-violet-900', border: 'border-purple-500/50', glow: 'shadow-purple-500/20', label: '🔮 Avanzado' },
  legendary: { color: 'from-red-800 to-rose-900', border: 'border-red-500/50', glow: 'shadow-red-500/20', label: '👑 Legendario' },
};

const REGION_BG: Record<string, string> = {
  forest: 'bg-gradient-to-b from-green-950 to-emerald-950',
  castle: 'bg-gradient-to-b from-stone-900 to-slate-950',
  cave: 'bg-gradient-to-b from-gray-900 to-zinc-950',
  volcano: 'bg-gradient-to-b from-red-950 to-orange-950',
  sky: 'bg-gradient-to-b from-cyan-950 to-blue-950',
  abyss: 'bg-gradient-to-b from-purple-950 to-black',
};

const dungeons: DungeonCourse[] = [
  {
    id: 'intro',
    title: 'Bosque del Código',
    description: 'Tu primera mazmorra. Aprende los fundamentos de la programación.',
    href: '/intro-programacion',
    tags: ['Fundamentos', 'IDE', 'Lógica'],
    difficulty: 'beginner',
    enemies: 8,
    boss: 'El Slime del Syntax',
    xpReward: 500,
    goldReward: 100,
    icon: '🌲',
    enemyType: 'slime',
    region: 'forest',
  },
  {
    id: 'python',
    title: 'Caverna de Python',
    description: 'Domina Python desde lo básico hasta Machine Learning e IA.',
    href: '/skill-tree-python',
    tags: ['Python', 'Data Science', 'IA'],
    difficulty: 'intermediate',
    enemies: 15,
    boss: 'La Serpiente Ancestral',
    xpReward: 1500,
    goldReward: 350,
    icon: '🐍',
    enemyType: 'dragon',
    region: 'cave',
  },
  {
    id: 'web',
    title: 'Castillo del Frontend',
    description: 'HTML, CSS, JavaScript, React y Next.js te esperan.',
    href: '/skill-tree-web',
    tags: ['Web', 'Frontend', 'Full-Stack'],
    difficulty: 'intermediate',
    enemies: 20,
    boss: 'El Coloso del DOM',
    xpReward: 2000,
    goldReward: 500,
    icon: '🏰',
    enemyType: 'orc',
    region: 'castle',
  },
  {
    id: 'java',
    title: 'Torre del Backend',
    description: 'POO, Collections, Spring Boot. El camino del guerrero Java.',
    href: '/skill-tree-java',
    tags: ['Java', 'Backend', 'Spring'],
    difficulty: 'advanced',
    enemies: 25,
    boss: 'El Guardián de los Beans',
    xpReward: 2500,
    goldReward: 600,
    icon: '☕',
    enemyType: 'boss',
    region: 'castle',
  },
  {
    id: 'minecraft',
    title: 'Mina de Minecraft',
    description: 'Crea mods épicos mientras aprendes Java de verdad.',
    href: '/minecraft-mods',
    tags: ['Minecraft', 'Java', 'Mods'],
    difficulty: 'intermediate',
    enemies: 12,
    boss: 'El Creeper Legendario',
    xpReward: 1200,
    goldReward: 280,
    icon: '⛏️',
    enemyType: 'goblin',
    region: 'cave',
  },
  {
    id: 'cpp',
    title: 'Volcán del Rendimiento',
    description: 'C++ puro. Solo los más fuertes sobreviven.',
    href: '/skill-tree-cpp',
    tags: ['C++', 'Sistemas', 'Rendimiento'],
    difficulty: 'legendary',
    enemies: 30,
    boss: 'El Demonio del Memory Leak',
    xpReward: 5000,
    goldReward: 1000,
    icon: '🔥',
    enemyType: 'dragon',
    region: 'volcano',
  },
  {
    id: 'arduino',
    title: 'Taller del Inventor',
    description: 'Arduino, sensores, ESP32. Crea máquinas reales.',
    href: '/skill-tree-arduino',
    tags: ['Arduino', 'IoT', 'Hardware'],
    difficulty: 'intermediate',
    enemies: 14,
    boss: 'El Corto Circuito',
    xpReward: 1400,
    goldReward: 320,
    icon: '🔌',
    enemyType: 'skeleton',
    region: 'cave',
  },
  {
    id: 'domotica',
    title: 'Casa Encantada',
    description: 'Automatiza todo. Tu hogar será tu mazmorra.',
    href: '/domotica',
    tags: ['Domótica', 'IoT', 'ESP32'],
    difficulty: 'advanced',
    enemies: 18,
    boss: 'El Fantasma del WiFi',
    xpReward: 1800,
    goldReward: 420,
    icon: '🏠',
    enemyType: 'skeleton',
    region: 'castle',
  },
  {
    id: 'devops',
    title: 'Cielos de la Nube',
    description: 'Docker, Kubernetes, CI/CD. Conquista la infraestructura.',
    href: '/skill-tree-devops',
    tags: ['DevOps', 'Docker', 'Cloud'],
    difficulty: 'advanced',
    enemies: 22,
    boss: 'El Titán del Deploy',
    xpReward: 2200,
    goldReward: 550,
    icon: '☁️',
    enemyType: 'orc',
    region: 'sky',
  },
  {
    id: 'raspberry-server',
    title: 'Fortaleza Raspberry',
    description: 'Monta tu propio servidor casero desde cero.',
    href: '/raspberry-server',
    tags: ['Linux', 'Servidor', 'Hardware'],
    difficulty: 'intermediate',
    enemies: 16,
    boss: 'El Kernel Panic',
    xpReward: 1600,
    goldReward: 380,
    icon: '🥧',
    enemyType: 'goblin',
    region: 'cave',
  },
  {
    id: 'discord-bot',
    title: 'Salón de los Bots',
    description: 'Crea bots con Node.js, música y comandos épicos.',
    href: '/discord-bot',
    tags: ['JavaScript', 'Bot', 'Discord'],
    difficulty: 'beginner',
    enemies: 10,
    boss: 'El Bot Rebelde',
    xpReward: 800,
    goldReward: 180,
    icon: '🤖',
    enemyType: 'slime',
    region: 'castle',
  },
  {
    id: 'streaming',
    title: 'Arena del Streaming',
    description: 'OBS, overlays, monetización. Hazte streamer pro.',
    href: '/streaming',
    tags: ['OBS', 'Twitch', 'YouTube'],
    difficulty: 'beginner',
    enemies: 6,
    boss: 'El Troll del Chat',
    xpReward: 400,
    goldReward: 90,
    icon: '🎥',
    enemyType: 'slime',
    region: 'castle',
  },
  {
    id: 'hacking',
    title: 'Abismo del Hacking',
    description: 'Hacking ético, WiFi, pentesting. Solo para valientes.',
    href: '/hacking-wifi',
    tags: ['Hacking', 'WiFi', 'Seguridad'],
    difficulty: 'legendary',
    enemies: 35,
    boss: 'El Hacker Oscuro',
    xpReward: 6000,
    goldReward: 1500,
    icon: '💀',
    enemyType: 'boss',
    region: 'abyss',
  },
  {
    id: '3d-printing',
    title: 'Fragua 3D',
    description: 'Impresión 3D, diseño CAD. Crea objetos reales.',
    href: '/impresion-3d',
    tags: ['3D', 'CAD', 'Maker'],
    difficulty: 'intermediate',
    enemies: 11,
    boss: 'El Atasco Filamento',
    xpReward: 1100,
    goldReward: 250,
    icon: '🖨️',
    enemyType: 'goblin',
    region: 'cave',
  },
];

// Componente de carta de mazmorra
function DungeonCard({ dungeon, index }: { dungeon: DungeonCourse; index: number }) {
  const config = DIFFICULTY_CONFIG[dungeon.difficulty];
  const [isHovered, setIsHovered] = useState(false);
  
  return (
    <Link
      href={dungeon.href}
      className={`
        group relative overflow-hidden rounded-xl border-2 ${config.border}
        bg-gradient-to-br ${config.color} p-4
        transition-all duration-300 transform
        hover:scale-[1.03] hover:shadow-xl ${config.glow}
        hover:border-white/40
      `}
      style={{ animationDelay: `${index * 50}ms` }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Dungeon entrance pattern */}
      <div className="absolute inset-0 opacity-10">
        <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
          <pattern id={`bricks-${dungeon.id}`} patternUnits="userSpaceOnUse" width="20" height="10">
            <rect width="20" height="10" fill="none" stroke="currentColor" strokeWidth="0.5"/>
            <line x1="10" y1="0" x2="10" y2="5" stroke="currentColor" strokeWidth="0.5"/>
            <line x1="0" y1="5" x2="10" y2="5" stroke="currentColor" strokeWidth="0.5"/>
          </pattern>
          <rect width="100" height="100" fill={`url(#bricks-${dungeon.id})`}/>
        </svg>
      </div>

      {/* Header with icon and enemy */}
      <div className="relative flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="text-4xl filter drop-shadow-lg">{dungeon.icon}</div>
          <div>
            <h2 className="text-lg font-bold text-white leading-tight">{dungeon.title}</h2>
            <span className="text-xs text-white/60">{config.label}</span>
          </div>
        </div>
        
        {/* Enemy sprite */}
        <div className="transform transition-transform group-hover:scale-110">
          <EnemySprite 
            type={dungeon.enemyType} 
            size={48} 
            className={isHovered ? 'animate-bounce' : ''}
          />
        </div>
      </div>

      {/* Description */}
      <p className="text-white/80 text-sm mb-3 line-clamp-2">{dungeon.description}</p>

      {/* Stats bar */}
      <div className="flex items-center gap-4 text-xs text-white/70 mb-3">
        <div className="flex items-center gap-1">
          <Swords className="w-3 h-3 text-red-400" />
          <span>{dungeon.enemies} enemigos</span>
        </div>
        <div className="flex items-center gap-1">
          <Crown className="w-3 h-3 text-yellow-400" />
          <span>{dungeon.xpReward} XP</span>
        </div>
        <div className="flex items-center gap-1">
          <span className="text-yellow-400">💰</span>
          <span>{dungeon.goldReward}</span>
        </div>
      </div>

      {/* Boss preview */}
      <div className="bg-black/30 rounded-lg px-3 py-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-red-400">💀</span>
          <span className="text-xs text-white/80">Boss: {dungeon.boss}</span>
        </div>
        <ArrowRight className="w-4 h-4 text-white/60 group-hover:translate-x-1 transition-transform" />
      </div>

      {/* Tags */}
      <div className="flex flex-wrap gap-1 mt-3">
        {dungeon.tags.map((tag) => (
          <span
            key={tag}
            className="px-2 py-0.5 bg-white/10 backdrop-blur-sm rounded text-[10px] font-medium text-white/80"
          >
            {tag}
          </span>
        ))}
      </div>
    </Link>
  );
}

// Componente del mapa del mundo
function WorldMap() {
  const regions = [
    { id: 'beginner', name: 'Tierras Iniciales', count: dungeons.filter(d => d.difficulty === 'beginner').length, color: 'bg-green-600' },
    { id: 'intermediate', name: 'Reinos Medios', count: dungeons.filter(d => d.difficulty === 'intermediate').length, color: 'bg-amber-600' },
    { id: 'advanced', name: 'Tierras Altas', count: dungeons.filter(d => d.difficulty === 'advanced').length, color: 'bg-purple-600' },
    { id: 'legendary', name: 'El Abismo', count: dungeons.filter(d => d.difficulty === 'legendary').length, color: 'bg-red-600' },
  ];

  return (
    <div className="bg-stone-900/50 rounded-xl p-4 border border-stone-700">
      <div className="flex items-center gap-2 mb-4">
        <Map className="w-5 h-5 text-amber-400" />
        <h3 className="text-lg font-bold text-white">Mapa del Mundo</h3>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {regions.map((region) => (
          <div key={region.id} className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${region.color}`} />
            <div>
              <div className="text-sm text-white font-medium">{region.name}</div>
              <div className="text-xs text-stone-400">{region.count} mazmorras</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// Hero section con personaje
function DungeonHero() {
  const [playerSeed, setPlayerSeed] = useState('adventurer');
  
  useEffect(() => {
    // Usar ID de usuario si está logueado, sino random
    setPlayerSeed('player-' + Math.random().toString(36).substring(7));
  }, []);

  return (
    <div className="relative bg-gradient-to-b from-stone-900 via-stone-800 to-stone-900 rounded-2xl p-8 mb-8 border-2 border-amber-900/50 overflow-hidden">
      {/* Background dungeon pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" 
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M54.627 0l.83.828-1.415 1.415L51.8 0h2.827zM5.373 0l-.83.828L5.96 2.243 8.2 0H5.374zM48.97 0l3.657 3.657-1.414 1.414L46.143 0h2.828zM11.03 0L7.372 3.657 8.787 5.07 13.857 0H11.03zm32.284 0L49.8 6.485 48.384 7.9l-7.9-7.9h2.83zM16.686 0L10.2 6.485 11.616 7.9l7.9-7.9h-2.83zM22.344 0L13.858 8.485 15.272 9.9l7.9-7.9h-.828zm5.656 0L19.515 8.485 20.93 9.9l8.485-8.485h-1.414zm5.656 0L25.172 8.485 26.586 9.9 35.07 1.414 33.656 0zm5.656 0l-8.485 8.485 1.414 1.414 8.485-8.485L35.656 0h-1.414zm5.656 0l-8.485 8.485 1.414 1.415 8.486-8.486L45.97 0h-1.414zM0 5.373l.828-.83 1.415 1.415L0 8.2V5.374zm0 5.656l.828-.829 1.415 1.415L0 13.857v-2.83zm0 5.656l.828-.828 1.415 1.414L0 19.515v-2.83zm0 5.657l.828-.828 1.415 1.414L0 25.172v-2.83zM60 5.373L59.17 4.54l-1.414 1.415L60 8.2V5.374zm0 5.656l-.828-.829-1.415 1.415L60 13.857v-2.83zm0 5.656l-.828-.828-1.415 1.414L60 19.515v-2.83zm0 5.657l-.828-.828-1.415 1.414L60 25.172v-2.83z' fill='%23ffffff' fill-opacity='1' fill-rule='evenodd'/%3E%3C/svg%3E")`,
          }}
        />
      </div>

      <div className="relative flex flex-col md:flex-row items-center gap-8">
        {/* Player sprite */}
        <div className="flex flex-col items-center">
          <div className="relative">
            <div className="absolute -inset-4 bg-amber-500/20 rounded-full blur-xl animate-pulse" />
            <SpriteGenerator 
              seed={playerSeed} 
              size={128} 
              showStats
              stats={{ level: 1, hp: 100, maxHp: 100, attack: 10, defense: 5 }}
            />
          </div>
          <div className="mt-2 text-amber-400 text-sm font-bold">Tu Aventurero</div>
        </div>

        {/* Text content */}
        <div className="flex-1 text-center md:text-left">
          <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-yellow-500 to-amber-400 mb-4">
            🗡️ Code Dungeon
          </h1>
          <p className="text-xl text-stone-300 mb-4">
            Elige tu mazmorra y conquista el conocimiento. Cada curso es una aventura épica con enemigos, 
            tesoros y un boss final que deberás derrotar.
          </p>
          <div className="flex flex-wrap gap-4 justify-center md:justify-start text-sm">
            <div className="flex items-center gap-2 bg-stone-800/50 px-4 py-2 rounded-lg">
              <Scroll className="w-4 h-4 text-amber-400" />
              <span className="text-stone-300">{dungeons.length} Mazmorras</span>
            </div>
            <div className="flex items-center gap-2 bg-stone-800/50 px-4 py-2 rounded-lg">
              <Swords className="w-4 h-4 text-red-400" />
              <span className="text-stone-300">{dungeons.reduce((acc, d) => acc + d.enemies, 0)}+ Enemigos</span>
            </div>
            <div className="flex items-center gap-2 bg-stone-800/50 px-4 py-2 rounded-lg">
              <Crown className="w-4 h-4 text-yellow-400" />
              <span className="text-stone-300">{dungeons.reduce((acc, d) => acc + d.xpReward, 0).toLocaleString()} XP Total</span>
            </div>
          </div>
        </div>

        {/* Decorative enemies */}
        <div className="hidden lg:flex flex-col gap-4">
          <EnemySprite type="slime" size={48} name="Slime Lv.1" />
          <EnemySprite type="goblin" size={48} name="Goblin Lv.5" />
          <EnemySprite type="dragon" size={48} name="Dragón Lv.20" />
        </div>
      </div>
    </div>
  );
}

export default function SkillTreeHub() {
  const [filter, setFilter] = useState<DungeonDifficulty | 'all'>('all');
  
  const filteredDungeons = filter === 'all' 
    ? dungeons 
    : dungeons.filter(d => d.difficulty === filter);

  return (
    <div className="min-h-screen bg-gradient-to-b from-stone-950 via-stone-900 to-stone-950">
      {/* Ambient particles */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-amber-400/30 rounded-full animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${2 + Math.random() * 2}s`,
            }}
          />
        ))}
      </div>

      <div className="relative max-w-7xl mx-auto px-4 py-12">
        {/* Hero */}
        <DungeonHero />
        
        {/* World Map */}
        <WorldMap />

        {/* Filter buttons */}
        <div className="flex flex-wrap gap-2 mt-8 mb-6">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg font-semibold transition-all ${
              filter === 'all' 
                ? 'bg-amber-600 text-white' 
                : 'bg-stone-800 text-stone-400 hover:bg-stone-700'
            }`}
          >
            🗺️ Todas ({dungeons.length})
          </button>
          {Object.entries(DIFFICULTY_CONFIG).map(([key, config]) => (
            <button
              key={key}
              onClick={() => setFilter(key as DungeonDifficulty)}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                filter === key 
                  ? 'bg-amber-600 text-white' 
                  : 'bg-stone-800 text-stone-400 hover:bg-stone-700'
              }`}
            >
              {config.label} ({dungeons.filter(d => d.difficulty === key).length})
            </button>
          ))}
        </div>

        {/* Dungeon grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDungeons.map((dungeon, index) => (
            <DungeonCard key={dungeon.id} dungeon={dungeon} index={index} />
          ))}
        </div>

        {/* Forum section */}
        <div className="mt-12">
          <Link
            href="/foro"
            className="block bg-gradient-to-r from-stone-800 to-stone-900 rounded-xl p-6 hover:scale-[1.01] transition-transform border-2 border-stone-700 hover:border-amber-600/50"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <Users className="w-12 h-12 text-amber-400" />
                <div>
                  <h2 className="text-2xl font-bold text-white mb-1">
                    💬 Taberna de Aventureros
                  </h2>
                  <p className="text-stone-400">
                    Comparte estrategias, pide ayuda y presume tus logros
                  </p>
                </div>
              </div>
              <ArrowRight className="w-8 h-8 text-amber-400" />
            </div>
          </Link>
        </div>

        {/* Tip box */}
        <div className="mt-8 bg-gradient-to-r from-green-900/30 to-emerald-900/30 border-2 border-green-700/50 rounded-xl p-6">
          <div className="flex items-start gap-4">
            <div className="text-4xl">🧭</div>
            <div>
              <h3 className="text-xl font-bold text-white mb-2">
                ¿Primera vez en las mazmorras?
              </h3>
              <p className="text-stone-300 mb-3">
                Te recomendamos empezar por el <strong className="text-green-400">Bosque del Código</strong> para 
                aprender los fundamentos, o elige <strong className="text-cyan-400">Caverna de Python</strong> si 
                quieres ir directo a programar.
              </p>
              <Link
                href="/intro-programacion"
                className="inline-flex items-center gap-2 bg-green-700 hover:bg-green-600 text-white px-6 py-2 rounded-lg font-semibold transition-colors"
              >
                <Swords className="w-4 h-4" />
                Comenzar Aventura
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
