'use client';

import { useMemo } from 'react';

// 16-bit color palette (reduced colors for retro aesthetic)
const SKIN_COLORS = ['#FFDBB4', '#EAC086', '#C68642', '#8D5524', '#6B4423'];
const HAIR_COLORS = ['#090806', '#2C222B', '#71635A', '#B7A69E', '#D6C4C2', '#CABFB1', '#DA680F', '#91361C', '#E7C27D', '#A55728'];
const SHIRT_COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF', '#5F27CD', '#01A3A4', '#2D3436'];
const PANTS_COLORS = ['#2D3436', '#636E72', '#0984E3', '#6C5CE7', '#00B894', '#E17055'];
const EYE_COLORS = ['#2D3436', '#6B4423', '#0984E3', '#00B894', '#E17055'];

interface SpriteGeneratorProps {
  seed: string; // User ID or email as seed
  size?: number;
  className?: string;
  showStats?: boolean;
  stats?: {
    level: number;
    hp: number;
    maxHp: number;
    attack: number;
    defense: number;
  };
}

// Simple hash function for consistent generation
function hashCode(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash);
}

// Generate deterministic random from seed
function seededRandom(seed: number, index: number): number {
  const x = Math.sin(seed + index * 9999) * 10000;
  return x - Math.floor(x);
}

export function generateSpriteData(seed: string) {
  const hash = hashCode(seed);
  
  return {
    skinColor: SKIN_COLORS[Math.floor(seededRandom(hash, 0) * SKIN_COLORS.length)],
    hairColor: HAIR_COLORS[Math.floor(seededRandom(hash, 1) * HAIR_COLORS.length)],
    shirtColor: SHIRT_COLORS[Math.floor(seededRandom(hash, 2) * SHIRT_COLORS.length)],
    pantsColor: PANTS_COLORS[Math.floor(seededRandom(hash, 3) * PANTS_COLORS.length)],
    eyeColor: EYE_COLORS[Math.floor(seededRandom(hash, 4) * EYE_COLORS.length)],
    hairStyle: Math.floor(seededRandom(hash, 5) * 4), // 0-3 hair styles
    accessory: Math.floor(seededRandom(hash, 6) * 5), // 0-4 accessories (0 = none)
    gender: seededRandom(hash, 7) > 0.5 ? 'male' : 'female',
  };
}

export default function SpriteGenerator({ seed, size = 64, className = '', showStats = false, stats }: SpriteGeneratorProps) {
  const spriteData = useMemo(() => generateSpriteData(seed), [seed]);
  
  const pixelSize = size / 16; // 16x16 grid
  
  // 16x16 pixel art sprite definition (each row is 16 pixels)
  const generateSprite = () => {
    const { skinColor, hairColor, shirtColor, pantsColor, eyeColor, hairStyle, accessory, gender } = spriteData;
    const transparent = 'transparent';
    const outline = '#1a1a2e';
    
    // Base sprite grid (16x16)
    const sprite: string[][] = Array(16).fill(null).map(() => Array(16).fill(transparent));
    
    // Hair (rows 0-4)
    const hairPatterns = [
      // Style 0: Short spiky
      [[5,0],[6,0],[7,0],[8,0],[9,0],[10,0],
       [4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],
       [4,2],[5,2],[11,2]],
      // Style 1: Long
      [[5,0],[6,0],[7,0],[8,0],[9,0],[10,0],
       [4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],
       [3,2],[4,2],[11,2],[12,2],
       [3,3],[12,3],
       [3,4],[12,4]],
      // Style 2: Mohawk
      [[7,0],[8,0],
       [6,1],[7,1],[8,1],[9,1],
       [4,2],[5,2],[6,2],[9,2],[10,2],[11,2]],
      // Style 3: Bald/Short
      [[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],
       [4,2],[5,2],[10,2],[11,2]]
    ];
    
    const currentHair = hairPatterns[hairStyle] || hairPatterns[0];
    currentHair.forEach(([x, y]) => {
      if (sprite[y] && sprite[y][x] !== undefined) sprite[y][x] = hairColor;
    });
    
    // Head/Face (rows 2-6)
    for (let y = 2; y <= 6; y++) {
      for (let x = 5; x <= 10; x++) {
        if (sprite[y][x] === transparent) sprite[y][x] = skinColor;
      }
    }
    
    // Eyes (row 4)
    sprite[4][6] = eyeColor;
    sprite[4][9] = eyeColor;
    
    // Mouth (row 5)
    sprite[5][7] = outline;
    sprite[5][8] = outline;
    
    // Body/Shirt (rows 7-10)
    for (let y = 7; y <= 10; y++) {
      for (let x = 4; x <= 11; x++) {
        sprite[y][x] = shirtColor;
      }
    }
    
    // Arms (rows 8-10)
    sprite[8][3] = skinColor;
    sprite[9][3] = skinColor;
    sprite[10][3] = skinColor;
    sprite[8][12] = skinColor;
    sprite[9][12] = skinColor;
    sprite[10][12] = skinColor;
    
    // Hands
    sprite[11][3] = skinColor;
    sprite[11][12] = skinColor;
    
    // Pants (rows 11-13)
    for (let y = 11; y <= 13; y++) {
      for (let x = 5; x <= 10; x++) {
        sprite[y][x] = pantsColor;
      }
    }
    
    // Legs split
    sprite[13][7] = transparent;
    sprite[13][8] = transparent;
    
    // Feet (row 14-15)
    for (let x = 5; x <= 6; x++) {
      sprite[14][x] = outline;
      sprite[15][x] = outline;
    }
    for (let x = 9; x <= 10; x++) {
      sprite[14][x] = outline;
      sprite[15][x] = outline;
    }
    
    // Accessories
    if (accessory === 1) {
      // Glasses
      sprite[4][5] = '#2D3436';
      sprite[4][10] = '#2D3436';
      sprite[3][6] = '#2D3436';
      sprite[3][7] = '#2D3436';
      sprite[3][8] = '#2D3436';
      sprite[3][9] = '#2D3436';
    } else if (accessory === 2) {
      // Hat
      for (let x = 4; x <= 11; x++) sprite[0][x] = '#E74C3C';
      for (let x = 3; x <= 12; x++) sprite[1][x] = '#E74C3C';
    } else if (accessory === 3) {
      // Headband
      for (let x = 4; x <= 11; x++) sprite[2][x] = '#F39C12';
    } else if (accessory === 4) {
      // Cape (behind shoulders)
      sprite[7][3] = '#9B59B6';
      sprite[7][12] = '#9B59B6';
      sprite[8][2] = '#9B59B6';
      sprite[8][13] = '#9B59B6';
      sprite[9][2] = '#9B59B6';
      sprite[9][13] = '#9B59B6';
      sprite[10][2] = '#8E44AD';
      sprite[10][13] = '#8E44AD';
      sprite[11][2] = '#8E44AD';
      sprite[11][13] = '#8E44AD';
    }
    
    return sprite;
  };
  
  const sprite = useMemo(() => generateSprite(), [spriteData]);
  
  return (
    <div className={`inline-block ${className}`}>
      <div 
        className="relative"
        style={{ 
          width: size, 
          height: size,
          imageRendering: 'pixelated',
        }}
      >
        {/* Sprite Canvas */}
        <svg 
          width={size} 
          height={size} 
          viewBox="0 0 16 16"
          style={{ imageRendering: 'pixelated' }}
        >
          {sprite.map((row, y) =>
            row.map((color, x) => 
              color !== 'transparent' && (
                <rect
                  key={`${x}-${y}`}
                  x={x}
                  y={y}
                  width={1}
                  height={1}
                  fill={color}
                />
              )
            )
          )}
        </svg>
        
        {/* Level badge */}
        {showStats && stats && (
          <div className="absolute -bottom-1 -right-1 bg-yellow-500 text-black text-[8px] font-bold rounded-full w-4 h-4 flex items-center justify-center border border-yellow-600">
            {stats.level}
          </div>
        )}
      </div>
      
      {/* Stats panel */}
      {showStats && stats && (
        <div className="mt-2 text-xs font-mono bg-gray-900/80 rounded px-2 py-1 border border-gray-700">
          <div className="flex items-center gap-1">
            <span className="text-red-400">❤️</span>
            <div className="flex-1 bg-gray-700 rounded-full h-2 overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-red-600 to-red-400"
                style={{ width: `${(stats.hp / stats.maxHp) * 100}%` }}
              />
            </div>
            <span className="text-gray-400 text-[10px]">{stats.hp}/{stats.maxHp}</span>
          </div>
          <div className="flex gap-2 mt-1 text-[10px]">
            <span className="text-orange-400">⚔️{stats.attack}</span>
            <span className="text-blue-400">🛡️{stats.defense}</span>
          </div>
        </div>
      )}
    </div>
  );
}

// Export sprite as data URL for use in other contexts
export function getSpriteDataURL(seed: string, size: number = 64): string {
  const spriteData = generateSpriteData(seed);
  // This would need to be implemented with canvas for actual data URL
  // For now, we just return a placeholder
  return '';
}
