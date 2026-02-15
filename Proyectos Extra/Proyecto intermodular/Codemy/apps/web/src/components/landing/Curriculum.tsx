'use client'

import { useState } from 'react'
import { Code2, Database, Gamepad2, Smartphone, Cloud, ArrowRight, CheckCircle } from 'lucide-react'

export function Curriculum() {
  const [activeTrack, setActiveTrack] = useState('fundamentals')

  const tracks = [
    {
      id: 'python',
      name: 'Python & IA',
      icon: Code2,
      color: 'from-blue-600 to-blue-700',
      description: 'Desde Python básico hasta Inteligencia Artificial avanzada con PyTorch y TensorFlow',
      duration: '16-20 semanas',
      level: 'L0-L5',
      lessons: 81,
      courses: [
        'Python Introducción (4 lecciones)',
        'Variables y Tipos (5 lecciones)',
        'Control de Flujo (6 lecciones)',
        'Funciones Avanzadas (6 lecciones)',
        'POO con Python (6 lecciones)',
        'NumPy (6 lecciones)',
        'Pandas (6 lecciones)',
        'Matplotlib (6 lecciones)',
        'Scikit-Learn (6 lecciones)',
        'PyTorch (6 lecciones)',
        'TensorFlow (6 lecciones)',
        'NLP (6 lecciones)',
        'Computer Vision (6 lecciones)',
        'LLM y GPT (6 lecciones)',
        'Master IA (8 lecciones)'
      ]
    },
    {
      id: 'cpp',
      name: 'C++ Completo',
      icon: Code2,
      color: 'from-purple-600 to-purple-700',
      description: 'C++ desde fundamentos hasta programación avanzada y optimización',
      duration: '14-18 semanas',
      level: 'L1-L4',
      lessons: 42,
      courses: [
        'C++ Introducción (6 lecciones)',
        'POO en C++ (6 lecciones)',
        'STL - Standard Library (6 lecciones)',
        'Gestión de Memoria (6 lecciones)',
        'C++ Avanzado (8 lecciones)',
        'C++ Master (10 lecciones)'
      ]
    },
    {
      id: 'hardware',
      name: 'Raspberry Pi',
      icon: Smartphone,
      color: 'from-orange-600 to-orange-700',
      description: 'Crea tu propio servidor casero: web hosting, NAS, media server, VPN y más',
      duration: '4-6 semanas',
      level: 'L2-L3',
      lessons: 10,
      courses: [
        'Introducción a Raspberry Pi',
        'Instalación del OS',
        'SSH y configuración remota',
        'Servidor Web (Apache/Nginx)',
        'NAS - Tu nube personal',
        'Media Server (Plex)',
        'Pi-hole - Bloquea anuncios',
        'VPN casera con PiVPN',
        'Monitorización y backups',
        'Docker y contenedores'
      ]
    }
  ]

  const languages = [
    { name: 'Python', logo: '🐍', popularity: 92 },
    { name: 'JavaScript', logo: '⚡', popularity: 88 },
    { name: 'C#', logo: '🔷', popularity: 75 },
    { name: 'Java', logo: '☕', popularity: 70 },
    { name: 'C++', logo: '⚙️', popularity: 65 },
    { name: 'Rust', logo: '🦀', popularity: 45 }
  ]

  const currentTrack = tracks.find(track => track.id === activeTrack)
  const IconComponent = currentTrack?.icon || Code2

  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Curriculum{' '}
            <span className="bg-gradient-to-r from-stone-600 to-amber-600 bg-clip-text text-transparent">
              Profesional
            </span>
          </h2>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto leading-relaxed">
            3 tracks principales completamente desarrollados: Python (básico a IA avanzada), 
            C++ (fundamentos a experto) y Raspberry Pi Server. 133+ lecciones listas para aprender.
          </p>
        </div>

        {/* Language Support */}
        <div className="mb-12">
          <h3 className="text-center text-lg font-semibold text-white mb-6">
            Soporte Multi-lenguaje
          </h3>
          <div className="flex flex-wrap justify-center items-center gap-4">
            {languages.map((lang) => (
              <div 
                key={lang.name}
                className="flex items-center space-x-2 bg-slate-800/50 backdrop-blur-sm rounded-full px-4 py-2 border border-stone-500/30 shadow-sm"
              >
                <span className="text-2xl">{lang.logo}</span>
                <span className="font-medium text-stone-200">{lang.name}</span>
                <div className="flex items-center space-x-1">
                  <div className="w-16 bg-gray-200 rounded-full h-1.5">
                    <div 
                      className="bg-gradient-to-r from-stone-600 to-amber-600 h-1.5 rounded-full"
                      style={{ width: `${lang.popularity}%` }}
                    />
                  </div>
                  <span className="text-xs text-stone-400">{lang.popularity}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Track Selector */}
          <div className="lg:col-span-1">
            <h3 className="text-xl font-bold text-white mb-6">Especialízate</h3>
            <div className="space-y-2">
              {tracks.map((track) => {
                const TrackIcon = track.icon
                return (
                  <button
                    key={track.id}
                    onClick={() => setActiveTrack(track.id)}
                    className={`w-full p-4 rounded-xl border-2 transition-all duration-200 text-left ${
                      activeTrack === track.id
                        ? 'border-stone-600 bg-amber-900/30'
                        : 'border-stone-500/30 hover:border-gray-300 bg-white'
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-lg bg-gradient-to-r ${track.color}`}>
                        <TrackIcon className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-white">{track.name}</h4>
                        <p className="text-sm text-stone-300">{track.level} • {track.duration}</p>
                      </div>
                    </div>
                  </button>
                )
              })}
            </div>
          </div>

          {/* Track Details */}
          <div className="lg:col-span-2">
            {currentTrack && (
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-stone-500/30 overflow-hidden shadow-sm">
                {/* Header */}
                <div className={`bg-gradient-to-r ${currentTrack.color} p-6 text-white`}>
                  <div className="flex items-center space-x-3 mb-3">
                    <IconComponent className="w-8 h-8" />
                    <h3 className="text-2xl font-bold">{currentTrack.name}</h3>
                  </div>
                  <p className="text-white/90 text-lg mb-4">{currentTrack.description}</p>
                  <div className="flex items-center space-x-6">
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-white/80 rounded-full" />
                      <span className="text-sm">Nivel {currentTrack.level}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-white/80 rounded-full" />
                      <span className="text-sm">{currentTrack.duration}</span>
                    </div>
                  </div>
                </div>

                {/* Content */}
                <div className="p-6">
                  <h4 className="text-lg font-bold text-white mb-4">
                    Cursos incluidos ({currentTrack.courses.length})
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {currentTrack.courses.map((course, index) => (
                      <div key={index} className="flex items-center space-x-3 p-3 rounded-lg bg-stone-900/50 hover:bg-stone-800/70 transition-colors">
                        <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                        <span className="text-stone-200 font-medium">{course}</span>
                      </div>
                    ))}
                  </div>

                  {/* CTA */}
                  <div className="mt-6 pt-6 border-t border-stone-500/30">
                    <button className={`w-full bg-gradient-to-r ${currentTrack.color} text-white py-3 px-6 rounded-full font-semibold hover:shadow-lg transition-all duration-200 flex items-center justify-center space-x-2`}>
                      <span>Empezar {currentTrack.name}</span>
                      <ArrowRight className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Bottom Stats */}
        <div className="mt-16 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-stone-500/30 p-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-white mb-2">22</div>
              <div className="text-stone-300">Cursos Completos</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white mb-2">133+</div>
              <div className="text-stone-300">Lecciones</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white mb-2">3</div>
              <div className="text-stone-300">Tracks Principales</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white mb-2">100+</div>
              <div className="text-stone-300">Horas de Contenido</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}