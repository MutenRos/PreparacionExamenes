'use client';

import { useMemo } from 'react';

export type EnemyType = 'slime' | 'skeleton' | 'goblin' | 'orc' | 'dragon' | 'boss';

interface EnemySpriteProps {
  type: EnemyType;
  size?: number;
  className?: string;
  defeated?: boolean;
  hp?: number;
  maxHp?: number;
  name?: string;
}

const ENEMY_CONFIGS: Record<EnemyType, { color: string; accent: string; eyeColor: string }> = {
  slime: { color: '#4ECDC4', accent: '#45B7D1', eyeColor: '#2D3436' },
  skeleton: { color: '#DFE6E9', accent: '#B2BEC3', eyeColor: '#E74C3C' },
  goblin: { color: '#00B894', accent: '#55EFC4', eyeColor: '#FDCB6E' },
  orc: { color: '#6C5CE7', accent: '#A29BFE', eyeColor: '#E74C3C' },
  dragon: { color: '#E74C3C', accent: '#C0392B', eyeColor: '#F1C40F' },
  boss: { color: '#2D3436', accent: '#636E72', eyeColor: '#E74C3C' },
};

export default function EnemySprite({ type, size = 64, className = '', defeated = false, hp, maxHp, name }: EnemySpriteProps) {
  const config = ENEMY_CONFIGS[type];
  
  const generateEnemy = useMemo(() => {
    const transparent = 'transparent';
    const sprite: string[][] = Array(16).fill(null).map(() => Array(16).fill(transparent));
    
    if (type === 'slime') {
      for (let y = 8; y <= 14; y++) for (let x = 4; x <= 11; x++) sprite[y][x] = config.color;
      for (let x = 5; x <= 10; x++) sprite[7][x] = config.color;
      for (let x = 6; x <= 9; x++) sprite[6][x] = config.accent;
      sprite[10][6] = config.eyeColor; sprite[10][9] = config.eyeColor;
    } else if (type === 'skeleton') {
      for (let y = 2; y <= 6; y++) for (let x = 5; x <= 10; x++) sprite[y][x] = config.color;
      sprite[4][6] = config.eyeColor; sprite[4][9] = config.eyeColor;
      for (let y = 7; y <= 11; y++) { sprite[y][7] = config.color; sprite[y][8] = config.color; }
      sprite[12][6] = config.color; sprite[13][6] = config.color; sprite[12][9] = config.color; sprite[13][9] = config.color;
    } else if (type === 'goblin') {
      for (let y = 2; y <= 6; y++) for (let x = 5; x <= 10; x++) sprite[y][x] = config.color;
      sprite[3][4] = config.color; sprite[3][11] = config.color;
      sprite[4][6] = config.eyeColor; sprite[4][9] = config.eyeColor;
      for (let y = 7; y <= 11; y++) for (let x = 5; x <= 10; x++) sprite[y][x] = '#8B4513';
    } else if (type === 'orc') {
      for (let y = 1; y <= 7; y++) for (let x = 4; x <= 11; x++) sprite[y][x] = config.color;
      sprite[6][4] = '#FFEAA7'; sprite[6][11] = '#FFEAA7';
      sprite[4][6] = config.eyeColor; sprite[4][9] = config.eyeColor;
      for (let y = 8; y <= 12; y++) for (let x = 4; x <= 11; x++) sprite[y][x] = '#636E72';
    } else if (type === 'dragon') {
      for (let y = 2; y <= 5; y++) for (let x = 6; x <= 11; x++) sprite[y][x] = config.color;
      sprite[1][6] = config.accent; sprite[0][5] = config.accent;
      sprite[3][8] = config.eyeColor; sprite[3][10] = config.eyeColor;
      for (let y = 6; y <= 11; y++) for (let x = 5; x <= 10; x++) sprite[y][x] = config.color;
      for (let y = 6; y <= 9; y++) { sprite[y][3] = config.accent; sprite[y][12] = config.accent; }
    } else if (type === 'boss') {
      sprite[0][5] = '#F1C40F'; sprite[0][7] = '#F1C40F'; sprite[0][10] = '#F1C40F';
      for (let x = 5; x <= 10; x++) sprite[1][x] = '#F1C40F';
      for (let y = 2; y <= 6; y++) for (let x = 4; x <= 11; x++) sprite[y][x] = config.color;
      sprite[4][5] = config.eyeColor; sprite[4][6] = config.eyeColor;
      sprite[4][9] = config.eyeColor; sprite[4][10] = config.eyeColor;
      for (let y = 7; y <= 12; y++) for (let x = 3; x <= 12; x++) sprite[y][x] = '#636E72';
    }
    
    return sprite;
  }, [type, config]);
  
  return (
    <div className={`inline-block ${className}`}>
      <div className={`relative transition-all ${defeated ? 'opacity-30 grayscale' : ''}`} style={{ width: size, height: size, imageRendering: 'pixelated' }}>
        <svg width={size} height={size} viewBox="0 0 16 16" style={{ imageRendering: 'pixelated' }} className={defeated ? '' : 'animate-pulse'}>
          {generateEnemy.map((row, y) => row.map((color, x) => color !== 'transparent' && <rect key={`${x}-${y}`} x={x} y={y} width={1} height={1} fill={color} />))}
        </svg>
        {defeated && <div className="absolute inset-0 flex items-center justify-center"><span className="text-2xl">💀</span></div>}
      </div>
      {name && (
        <div className="text-center mt-1">
          <div className="text-xs font-bold text-white">{name}</div>
          {hp !== undefined && maxHp !== undefined && (
            <div className="w-full bg-gray-700 rounded-full h-1.5 mt-1">
              <div className="h-full rounded-full bg-gradient-to-r from-red-600 to-red-400" style={{ width: `${(hp / maxHp) * 100}%` }} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
