'use client';

import { useState } from 'react';
import { CheckCircle, Coins } from 'lucide-react';

export default function NFTsPage() {
  const [hoveredLesson, setHoveredLesson] = useState<number | null>(null);

  const lessons = [
    { id: 1, title: '¿Qué son los NFTs?', description: 'Blockchain, tokens únicos y casos de uso reales', icon: '🎨', duration: '20 min' },
    { id: 2, title: 'Wallets: MetaMask y más', description: 'Crea tu billetera cripto en 5 minutos', icon: '👛', duration: '15 min' },
    { id: 3, title: 'Ethereum y gas fees', description: 'Cómo funciona la red y los costos de transacción', icon: '⛽', duration: '25 min' },
    { id: 4, title: 'Crea tu arte digital', description: 'Herramientas: Procreate, Photoshop, Blender', icon: '🖼️', duration: '40 min' },
    { id: 5, title: 'OpenSea: Tu primera colección', description: 'Sube y lista tus NFTs sin código', icon: '🌊', duration: '30 min' },
    { id: 6, title: 'Rarible y otras marketplaces', description: 'Alternativas y ventajas de cada plataforma', icon: '🛒', duration: '25 min' },
    { id: 7, title: 'Marketing de NFTs', description: 'Twitter, Discord, promoción y comunidad', icon: '📣', duration: '35 min' },
    { id: 8, title: 'Smart contracts básicos', description: 'Solidity para crear colecciones programables', icon: '📜', duration: '45 min' },
    { id: 9, title: 'Royalties y monetización', description: 'Gana en cada reventa automáticamente', icon: '💰', duration: '20 min' },
    { id: 10, title: 'Rareza y colecciones generativas', description: 'Crea 10,000 NFTs únicos con código', icon: '🎲', duration: '50 min' },
    { id: 11, title: 'Polygon y blockchains baratas', description: 'Evita fees altos con L2', icon: '🟣', duration: '25 min' },
    { id: 12, title: 'Vende tu primera colección', description: 'Estrategia de lanzamiento y pricing', icon: '🚀', duration: '30 min' },
  ];

  const objectives = [
    'Crear y vender NFTs en OpenSea y Rarible',
    'Entender blockchain, wallets y smart contracts',
    'Generar colecciones de 10k+ NFTs automáticamente',
    'Monetizar con royalties en cada reventa',
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950">
      <header className="border-b border-stone-900/20 bg-stone-950/50 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-3">
              <a href="/skill-tree" className="text-stone-400 hover:text-stone-300 transition-colors">← Volver</a>
              <div className="h-6 w-px bg-amber-900/30" />
              <span className="text-sm text-stone-400">Curso de NFTs</span>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-stone-500 to-amber-600 mb-6 shadow-lg shadow-amber-500/30">
            <Coins className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-stone-400 via-pink-400 to-stone-500 bg-clip-text text-transparent">
            Crea y Vende NFTs
          </h1>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto mb-8">
            Aprende a crear, programar y vender NFTs. Desde arte digital hasta colecciones generativas de 10,000 tokens únicos.
          </p>
          <div className="flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-amber-400"></div><span className="text-stone-400">12 lecciones</span></div>
            <div className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-amber-400"></div><span className="text-stone-400">~6 horas</span></div>
            <div className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-amber-500"></div><span className="text-stone-400">Intermedio</span></div>
          </div>
        </div>

        <div className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6">¿Qué aprenderás?</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {objectives.map((obj, i) => (
              <div key={i} className="flex items-start gap-3 p-4 rounded-xl bg-stone-900/40 border border-stone-900/20 hover:border-stone-700/40 transition-all">
                <CheckCircle className="w-5 h-5 text-stone-400 flex-shrink-0 mt-0.5" />
                <span className="text-stone-300">{obj}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6">Contenido del curso</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {lessons.map((lesson) => (
              <div key={lesson.id} onMouseEnter={() => setHoveredLesson(lesson.id)} onMouseLeave={() => setHoveredLesson(null)}
                className="group relative p-6 rounded-xl bg-stone-900/40 border border-stone-900/20 hover:border-stone-700/50 transition-all duration-300 hover:shadow-lg hover:shadow-amber-500/10">
                <div className="flex items-start gap-4">
                  <div className="text-4xl flex-shrink-0 transition-transform group-hover:scale-110">{lesson.icon}</div>
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-semibold text-white group-hover:text-stone-300 transition-colors">{lesson.title}</h3>
                      <span className="text-xs text-stone-500 bg-slate-800/50 px-2 py-1 rounded">{lesson.duration}</span>
                    </div>
                    <p className="text-sm text-stone-400 leading-relaxed">{lesson.description}</p>
                  </div>
                </div>
                {hoveredLesson === lesson.id && <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-stone-500/5 to-amber-500/5 pointer-events-none" />}
              </div>
            ))}
          </div>
        </div>

        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-stone-600 via-pink-600 to-stone-700 p-12 text-center shadow-2xl shadow-amber-500/20">
          <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
          <div className="relative">
            <h2 className="text-3xl font-bold text-white mb-4">Monetiza tu arte digital</h2>
            <p className="text-stone-100 mb-8 max-w-2xl mx-auto">
              Desde colecciones simples hasta proyectos de 10k NFTs con smart contracts. Gana royalties en cada reventa.
            </p>
            <a href="/course/nfts-intro" className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-white text-stone-700 font-semibold hover:bg-amber-50 transition-all hover:scale-105 shadow-lg">
              Comenzar ahora
            </a>
          </div>
        </div>
      </main>
    </div>
  );
}
