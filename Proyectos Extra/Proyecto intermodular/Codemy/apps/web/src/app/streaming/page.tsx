'use client';

import { useState } from 'react';
import { CheckCircle, Video, Twitch } from 'lucide-react';

export default function StreamingPage() {
  const [hoveredLesson, setHoveredLesson] = useState<number | null>(null);

  const lessons = [
    {
      id: 1,
      title: 'El mundo del streaming',
      description: 'Twitch, YouTube, Kick: ¿Dónde empezar?',
      icon: '🌍',
      duration: '15 min',
    },
    {
      id: 2,
      title: 'Hardware necesario',
      description: 'PC, cámara, micro y capturadora',
      icon: '🎥',
      duration: '25 min',
    },
    {
      id: 3,
      title: 'Instalación de OBS Studio',
      description: 'Configuración óptima para streaming',
      icon: '⚙️',
      duration: '20 min',
    },
    {
      id: 4,
      title: 'Escenas y transiciones',
      description: 'Crea escenas profesionales multi-cámara',
      icon: '🎬',
      duration: '30 min',
    },
    {
      id: 5,
      title: 'Overlays y diseño de stream',
      description: 'StreamElements, banners, alertas y widgets',
      icon: '🎨',
      duration: '35 min',
    },
    {
      id: 6,
      title: 'Audio profesional',
      description: 'Filtros, eliminación de ruido, música sin copyright',
      icon: '🎧',
      duration: '30 min',
    },
    {
      id: 7,
      title: 'Bots de Twitch',
      description: 'Nightbot, StreamElements, comandos personalizados',
      icon: '🤖',
      duration: '25 min',
    },
    {
      id: 8,
      title: 'Engagement de audiencia',
      description: 'Chat interactivo, recompensas de canal, predicciones',
      icon: '💬',
      duration: '30 min',
    },
    {
      id: 9,
      title: 'Configuración de bitrate y calidad',
      description: 'Streaming 1080p 60fps sin lag',
      icon: '📊',
      duration: '25 min',
    },
    {
      id: 10,
      title: 'Monetización',
      description: 'Afiliado, socio, donaciones, sponsors',
      icon: '💰',
      duration: '30 min',
    },
    {
      id: 11,
      title: 'Networking y crecimiento',
      description: 'Colaboraciones, raids, promoción en redes',
      icon: '📈',
      duration: '25 min',
    },
    {
      id: 12,
      title: 'Grabación y clips',
      description: 'Highlights automáticos, edición rápida, YouTube',
      icon: '✂️',
      duration: '30 min',
    },
  ];

  const learningObjectives = [
    'Configurar OBS Studio para streaming profesional',
    'Crear overlays, escenas y alertas personalizadas',
    'Monetizar tu canal desde el día uno',
    'Aumentar tu audiencia con estrategias probadas',
  ];

  const platforms = [
    { name: 'Twitch', icon: '💜', color: 'from-stone-600 to-stone-800', pros: 'Comunidad gaming, mejor monetización' },
    { name: 'YouTube Live', icon: '🔴', color: 'from-red-600 to-red-800', pros: 'SEO, biblioteca permanente' },
    { name: 'Kick', icon: '🟢', color: 'from-green-600 to-green-800', pros: 'Mejores splits, menos restricciones' },
    { name: 'TikTok Live', icon: '🎵', color: 'from-amber-600 to-amber-800', pros: 'Crecimiento viral rápido' },
  ];

  const equipment = [
    {
      category: 'Básico (< 300€)',
      items: [
        'Webcam Logitech C920 (~70€)',
        'Micro USB como el Blue Snowball (~60€)',
        'Luz LED ring light (~30€)',
        'PC con GPU decente',
      ],
    },
    {
      category: 'Profesional (< 1000€)',
      items: [
        'Cámara réflex/mirrorless como Sony A6400',
        'Micrófono XLR + interfaz (Shure SM7B + Focusrite)',
        'Iluminación softbox profesional',
        'Stream Deck para controles',
      ],
    },
  ];

  const monetizationMethods = [
    {
      title: 'Subscripciones',
      description: 'Twitch Affiliate/Partner, YouTube membresías',
      icon: '⭐',
      potential: 'Recurrente',
    },
    {
      title: 'Donaciones',
      description: 'PayPal, StreamElements, bits de Twitch',
      icon: '💵',
      potential: 'Variable',
    },
    {
      title: 'Sponsors',
      description: 'Marcas gaming, energéticas, periféricos',
      icon: '🤝',
      potential: 'Alto',
    },
    {
      title: 'Afiliados',
      description: 'Amazon, G2A, programas de afiliados',
      icon: '🔗',
      potential: 'Pasivo',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950">
      {/* Header */}
      <header className="border-b border-stone-900/20 bg-stone-950/50 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-3">
              <a
                href="/skill-tree"
                className="text-stone-400 hover:text-stone-300 transition-colors"
              >
                ← Volver
              </a>
              <div className="h-6 w-px bg-amber-900/30" />
              <span className="text-sm text-stone-400">Curso de Streaming</span>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-stone-500 to-amber-600 mb-6 shadow-lg shadow-amber-500/30">
            <Twitch className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-stone-400 via-pink-400 to-stone-500 bg-clip-text text-transparent">
            Streaming Profesional
          </h1>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto mb-8">
            Aprende a crear streams de calidad profesional. Configuración de OBS, overlays personalizados, bots, monetización y estrategias de crecimiento.
          </p>

          {/* Course Stats */}
          <div className="flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-400"></div>
              <span className="text-stone-400">12 lecciones</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-400"></div>
              <span className="text-stone-400">~5.5 horas</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-500"></div>
              <span className="text-stone-400">Principiante</span>
            </div>
          </div>
        </div>

        {/* Learning Objectives */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6">¿Qué aprenderás?</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {learningObjectives.map((objective, index) => (
              <div
                key={index}
                className="flex items-start gap-3 p-4 rounded-xl bg-stone-900/40 border border-stone-900/20 hover:border-stone-700/40 transition-all"
              >
                <CheckCircle className="w-5 h-5 text-stone-400 flex-shrink-0 mt-0.5" />
                <span className="text-stone-300">{objective}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Platforms Comparison */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Plataformas de streaming
          </h2>
          <div className="grid md:grid-cols-4 gap-4">
            {platforms.map((platform, index) => (
              <div
                key={index}
                className={`p-6 rounded-xl bg-gradient-to-br ${platform.color} border border-white/10 hover:scale-105 transition-transform`}
              >
                <div className="text-4xl mb-3">{platform.icon}</div>
                <h3 className="text-xl font-bold text-white mb-2">{platform.name}</h3>
                <p className="text-sm text-white/80">{platform.pros}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Equipment Section */}
        <div className="mb-12 p-6 rounded-xl bg-stone-900/40 border border-stone-900/20">
          <h3 className="text-lg font-semibold text-stone-300 mb-4">
            🛒 Equipamiento necesario
          </h3>
          <div className="grid md:grid-cols-2 gap-6">
            {equipment.map((tier, index) => (
              <div key={index} className="p-4 rounded-lg bg-slate-800/30">
                <h4 className="font-semibold text-white mb-3 flex items-center gap-2">
                  <span className={index === 0 ? 'text-green-400' : 'text-stone-400'}>
                    {index === 0 ? '🟢' : '💜'}
                  </span>
                  {tier.category}
                </h4>
                <ul className="space-y-2">
                  {tier.items.map((item, idx) => (
                    <li key={idx} className="text-sm text-stone-300 flex items-start gap-2">
                      <span className="text-stone-400 mt-1">•</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Lessons Grid */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6">Contenido del curso</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {lessons.map((lesson) => (
              <div
                key={lesson.id}
                onMouseEnter={() => setHoveredLesson(lesson.id)}
                onMouseLeave={() => setHoveredLesson(null)}
                className="group relative p-6 rounded-xl bg-stone-900/40 border border-stone-900/20 hover:border-stone-700/50 transition-all duration-300 hover:shadow-lg hover:shadow-amber-500/10"
              >
                <div className="flex items-start gap-4">
                  <div className="text-4xl flex-shrink-0 transition-transform group-hover:scale-110">
                    {lesson.icon}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-semibold text-white group-hover:text-stone-300 transition-colors">
                        {lesson.title}
                      </h3>
                      <span className="text-xs text-stone-500 bg-slate-800/50 px-2 py-1 rounded">
                        {lesson.duration}
                      </span>
                    </div>
                    <p className="text-sm text-stone-400 leading-relaxed">
                      {lesson.description}
                    </p>
                  </div>
                </div>
                
                {hoveredLesson === lesson.id && (
                  <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-stone-500/5 to-amber-500/5 pointer-events-none" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Monetization */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            💰 Formas de monetización
          </h2>
          <div className="grid md:grid-cols-4 gap-4">
            {monetizationMethods.map((method, index) => (
              <div key={index} className="p-6 rounded-xl bg-gradient-to-br from-stone-900/20 to-amber-900/20 border border-stone-700/30">
                <div className="text-3xl mb-3">{method.icon}</div>
                <h3 className="text-lg font-semibold text-white mb-2">{method.title}</h3>
                <p className="text-sm text-stone-400 mb-2">{method.description}</p>
                <span className="text-xs px-2 py-1 rounded-full bg-amber-500/20 text-stone-300">
                  {method.potential}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-stone-600 via-pink-600 to-stone-700 p-12 text-center shadow-2xl shadow-amber-500/20">
          <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
          <div className="relative">
            <h2 className="text-3xl font-bold text-white mb-4">
              Comienza tu carrera como streamer
            </h2>
            <p className="text-stone-100 mb-8 max-w-2xl mx-auto">
              Desde la configuración técnica hasta la monetización. Todo lo que necesitas para destacar en Twitch, YouTube o Kick.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/course/streaming-intro"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-white text-stone-700 font-semibold hover:bg-amber-50 transition-all hover:scale-105 shadow-lg"
              >
                Comenzar ahora
              </a>
            </div>
          </div>
        </div>

        {/* Success Stories */}
        <div className="mt-12 p-6 rounded-xl bg-gradient-to-r from-green-900/20 to-emerald-900/20 border border-green-700/30">
          <h3 className="text-lg font-semibold text-green-300 mb-4">
            📊 Datos del streaming en 2024
          </h3>
          <div className="grid md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold text-white mb-1">8.5M+</div>
              <p className="text-sm text-stone-400">Streamers activos en Twitch</p>
            </div>
            <div>
              <div className="text-3xl font-bold text-white mb-1">31%</div>
              <p className="text-sm text-stone-400">Crecimiento anual del streaming</p>
            </div>
            <div>
              <div className="text-3xl font-bold text-white mb-1">$1500</div>
              <p className="text-sm text-stone-400">Ingreso promedio Partner (mes)</p>
            </div>
          </div>
        </div>

        {/* Tips */}
        <div className="mt-12 p-6 rounded-xl bg-stone-900/40 border border-stone-900/20">
          <h3 className="text-lg font-semibold text-stone-300 mb-4">
            💡 Consejos para empezar
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3">
              <span className="text-2xl">📅</span>
              <div>
                <h4 className="font-semibold text-white text-sm mb-1">Consistencia</h4>
                <p className="text-xs text-stone-400">Streams regulares, mismo horario, 3-4 veces/semana mínimo</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-2xl">🎮</span>
              <div>
                <h4 className="font-semibold text-white text-sm mb-1">Encuentra tu nicho</h4>
                <p className="text-xs text-stone-400">Juegos pequeños &gt; Fortnite/LoL saturados</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-2xl">💬</span>
              <div>
                <h4 className="font-semibold text-white text-sm mb-1">Interacción</h4>
                <p className="text-xs text-stone-400">Responde TODOS los mensajes, crea comunidad</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-2xl">📱</span>
              <div>
                <h4 className="font-semibold text-white text-sm mb-1">Cross-platform</h4>
                <p className="text-xs text-stone-400">Clips a TikTok/YouTube Shorts para viral</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
