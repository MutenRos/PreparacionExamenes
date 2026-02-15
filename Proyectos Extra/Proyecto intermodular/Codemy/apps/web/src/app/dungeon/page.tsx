'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Sword, Shield, Heart, Star, Trophy } from 'lucide-react';
import { SpriteGenerator, EnemySprite, DungeonMap } from '@/components/game';

export default function DungeonDemoPage() {
  const [userId] = useState('demo-user-12345');
  
  // Demo dungeon rooms (lessons)
  const demoRooms = [
    { id: 1, title: 'Variables', type: 'entrance' as const, status: 'completed' as const, enemies: 3, xp: 50 },
    { id: 2, title: 'Tipos de datos', type: 'room' as const, status: 'completed' as const, enemies: 4, xp: 60 },
    { id: 3, title: 'Operadores', type: 'room' as const, status: 'available' as const, enemies: 5, xp: 70 },
    { id: 4, title: 'Condicionales', type: 'room' as const, status: 'locked' as const, enemies: 4, xp: 80 },
    { id: 5, title: 'Bucles', type: 'room' as const, status: 'locked' as const, enemies: 6, xp: 90 },
    { id: 6, title: 'Funciones', type: 'room' as const, status: 'locked' as const, enemies: 5, xp: 100 },
    { id: 7, title: 'Arrays', type: 'room' as const, status: 'locked' as const, enemies: 4, xp: 80 },
    { id: 8, title: 'Boss Final', type: 'boss' as const, status: 'locked' as const, enemies: 1, xp: 200 },
  ];

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <header className="bg-gray-900 border-b border-gray-800 p-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="text-gray-400 hover:text-white transition-colors">
              <ArrowLeft className="w-6 h-6" />
            </Link>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-amber-400 to-red-500 bg-clip-text text-transparent">
              ⚔️ Code Dungeon
            </h1>
          </div>
          
          {/* Player Info */}
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <Heart className="w-5 h-5 text-red-500" />
              <span>100/100</span>
            </div>
            <div className="flex items-center gap-2">
              <Star className="w-5 h-5 text-amber-400" />
              <span>1,250 XP</span>
            </div>
            <div className="flex items-center gap-2">
              <Trophy className="w-5 h-5 text-purple-400" />
              <span>Nivel 5</span>
            </div>
            <SpriteGenerator seed={userId} size={48} />
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto p-6">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">🏰 Sistema de Mazmorras</h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Cada curso es una mazmorra. Cada lección es una cámara. Cada ejercicio es un enemigo. 
            ¡Derrota a todos los enemigos para conquistar el conocimiento!
          </p>
        </div>

        {/* Player Card */}
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 mb-8">
          <h3 className="text-xl font-bold mb-4">👤 Tu Aventurero</h3>
          <div className="flex items-start gap-8">
            <SpriteGenerator 
              seed={userId} 
              size={128} 
              showStats 
              stats={{ level: 5, hp: 100, maxHp: 100, attack: 15, defense: 10 }} 
            />
            <div className="flex-1">
              <h4 className="text-lg font-bold text-amber-400">Guerrero del Código</h4>
              <p className="text-gray-400 mb-4">Sprite generado proceduralmente basado en tu ID de usuario</p>
              
              <div className="grid grid-cols-4 gap-4">
                <div className="bg-gray-800 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-green-400">12</div>
                  <div className="text-xs text-gray-400">Mazmorras</div>
                </div>
                <div className="bg-gray-800 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-blue-400">47</div>
                  <div className="text-xs text-gray-400">Cámaras</div>
                </div>
                <div className="bg-gray-800 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-red-400">156</div>
                  <div className="text-xs text-gray-400">Enemigos</div>
                </div>
                <div className="bg-gray-800 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-amber-400">1,250</div>
                  <div className="text-xs text-gray-400">XP Total</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Dungeon Map Demo */}
        <DungeonMap 
          courseId="py-intro"
          courseTitle="Python: Primeros Pasos"
          courseIcon="🐍"
          rooms={demoRooms}
          totalXP={730}
          earnedXP={110}
        />

        {/* Enemy Types Demo */}
        <div className="mt-8 bg-gray-900 rounded-xl p-6 border border-gray-800">
          <h3 className="text-xl font-bold mb-4">👹 Tipos de Enemigos</h3>
          <p className="text-gray-400 mb-6">Cada ejercicio genera un enemigo diferente basado en su dificultad</p>
          
          <div className="grid grid-cols-6 gap-6">
            <div className="text-center">
              <EnemySprite type="slime" size={64} name="Slime" hp={100} maxHp={100} />
              <p className="text-xs text-gray-400 mt-2">Fácil</p>
            </div>
            <div className="text-center">
              <EnemySprite type="goblin" size={64} name="Goblin" hp={100} maxHp={100} />
              <p className="text-xs text-gray-400 mt-2">Normal</p>
            </div>
            <div className="text-center">
              <EnemySprite type="skeleton" size={64} name="Esqueleto" hp={100} maxHp={100} />
              <p className="text-xs text-gray-400 mt-2">Normal</p>
            </div>
            <div className="text-center">
              <EnemySprite type="orc" size={64} name="Orco" hp={100} maxHp={100} />
              <p className="text-xs text-gray-400 mt-2">Difícil</p>
            </div>
            <div className="text-center">
              <EnemySprite type="dragon" size={64} name="Dragón" hp={100} maxHp={100} />
              <p className="text-xs text-gray-400 mt-2">Muy Difícil</p>
            </div>
            <div className="text-center">
              <EnemySprite type="boss" size={64} name="Jefe Final" hp={100} maxHp={100} />
              <p className="text-xs text-gray-400 mt-2">Boss</p>
            </div>
          </div>
        </div>

        {/* Defeated Enemies */}
        <div className="mt-8 bg-gray-900 rounded-xl p-6 border border-gray-800">
          <h3 className="text-xl font-bold mb-4">💀 Enemigos Derrotados</h3>
          <div className="flex gap-6">
            <EnemySprite type="slime" size={64} defeated name="Slime" hp={0} maxHp={100} />
            <EnemySprite type="goblin" size={64} defeated name="Goblin" hp={0} maxHp={100} />
            <EnemySprite type="skeleton" size={64} defeated name="Esqueleto" hp={0} maxHp={100} />
          </div>
        </div>

        {/* Multiple Sprite Demo */}
        <div className="mt-8 bg-gray-900 rounded-xl p-6 border border-gray-800">
          <h3 className="text-xl font-bold mb-4">🎮 Generación Procedural de Sprites</h3>
          <p className="text-gray-400 mb-6">Cada usuario tiene un sprite único generado a partir de su ID</p>
          
          <div className="flex gap-4 flex-wrap">
            {['user1@test.com', 'user2@test.com', 'player123', 'coder456', 'dev789', 'admin', 'guest', 'pro_gamer'].map((seed) => (
              <div key={seed} className="text-center">
                <SpriteGenerator seed={seed} size={64} />
                <p className="text-xs text-gray-400 mt-1 truncate w-16">{seed.split('@')[0]}</p>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="mt-12 text-center">
          <Link href="/dashboard" className="inline-flex items-center gap-2 bg-gradient-to-r from-amber-500 to-red-500 hover:from-amber-400 hover:to-red-400 px-8 py-4 rounded-xl font-bold text-lg transition-all transform hover:scale-105">
            <Sword className="w-6 h-6" />
            ¡Comenzar Aventura!
          </Link>
        </div>
      </main>
    </div>
  );
}
