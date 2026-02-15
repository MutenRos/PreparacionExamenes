'use client';

import Link from 'next/link';
import { BookOpen, Gamepad2, Code, Zap, ArrowRight, CheckCircle, Diamond } from 'lucide-react';

export default function MinecraftMods() {
  const lessons = [
    {
      id: 1,
      title: '¿Qué son los mods?',
      description: 'Entiende cómo funcionan los mods de Minecraft',
      duration: '5 min',
      icon: '🎮',
    },
    {
      id: 2,
      title: 'Instalar Java y el JDK',
      description: 'Configura tu entorno de desarrollo',
      duration: '10 min',
      icon: '☕',
    },
    {
      id: 3,
      title: 'Forge y tu primer mod',
      description: 'Crea la estructura básica de tu mod',
      duration: '15 min',
      icon: '🔧',
    },
    {
      id: 4,
      title: 'Tu primer bloque',
      description: 'Añade un bloque personalizado al juego',
      duration: '20 min',
      icon: '🧱',
    },
    {
      id: 5,
      title: 'Items y herramientas',
      description: 'Crea espadas, picos y objetos únicos',
      duration: '25 min',
      icon: '⚔️',
    },
    {
      id: 6,
      title: 'Texturas personalizadas',
      description: 'Diseña el aspecto de tus items y bloques',
      duration: '20 min',
      icon: '🎨',
    },
    {
      id: 7,
      title: 'Recetas de crafteo',
      description: 'Define cómo se fabrican tus items',
      duration: '15 min',
      icon: '📋',
    },
    {
      id: 8,
      title: 'Mobs personalizados',
      description: 'Crea criaturas únicas con IA propia',
      duration: '30 min',
      icon: '🦎',
    },
    {
      id: 9,
      title: 'Eventos y mecánicas',
      description: 'Añade lógica personalizada al juego',
      duration: '25 min',
      icon: '⚡',
    },
    {
      id: 10,
      title: 'Publicar tu mod',
      description: 'Comparte tu creación con el mundo',
      duration: '15 min',
      icon: '🌍',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-green-900 to-slate-900">
      {/* Header */}
      <div className="bg-black/30 backdrop-blur-sm border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold text-white">
              Code Dungeon
            </Link>
            <Link href="/skill-tree" className="text-sm text-white/80 hover:text-white font-medium">
              ← Volver a Roadmaps
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-600 to-emerald-600 rounded-2xl mb-6">
            <Diamond className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold text-white mb-4">
            Crea tus propios Mods de Minecraft
          </h1>
          <p className="text-xl text-white/80 mb-6">
            Aprende Java creando mods increíbles para Minecraft
          </p>
          <div className="flex items-center justify-center gap-6 text-white/70">
            <div className="flex items-center gap-2">
              <BookOpen className="w-5 h-5" />
              <span>10 lecciones</span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="w-5 h-5" />
              <span>3 horas</span>
            </div>
            <div className="flex items-center gap-2">
              <Gamepad2 className="w-5 h-5" />
              <span>Intermedio</span>
            </div>
          </div>
        </div>

        {/* What you'll learn */}
        <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-8 mb-8 border border-white/10">
          <h2 className="text-2xl font-bold text-white mb-4">¿Qué aprenderás?</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
              <div>
                <p className="text-white font-semibold">Programar en Java</p>
                <p className="text-white/70 text-sm">Aprende Java de forma práctica y divertida</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
              <div>
                <p className="text-white font-semibold">Crear bloques e items</p>
                <p className="text-white/70 text-sm">Añade contenido personalizado al juego</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
              <div>
                <p className="text-white font-semibold">Diseñar criaturas</p>
                <p className="text-white/70 text-sm">Crea mobs con comportamientos únicos</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
              <div>
                <p className="text-white font-semibold">Publicar tu mod</p>
                <p className="text-white/70 text-sm">Compártelo con millones de jugadores</p>
              </div>
            </div>
          </div>
        </div>

        {/* Prerequisites */}
        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-2xl p-6 mb-8">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 bg-yellow-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-2xl">💡</span>
            </div>
            <div>
              <h3 className="text-white font-bold mb-2">Requisitos previos</h3>
              <p className="text-white/80 text-sm mb-3">
                Este curso requiere conocimientos básicos de programación. Te recomendamos completar primero:
              </p>
              <Link 
                href="/intro-programacion"
                className="inline-flex items-center gap-2 text-yellow-400 hover:text-yellow-300 font-semibold text-sm"
              >
                💡 Introducción a la Programación
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>

        {/* Lessons */}
        <div className="space-y-4 mb-8">
          <h2 className="text-2xl font-bold text-white mb-6">Contenido del curso</h2>
          {lessons.map((lesson) => (
            <div
              key={lesson.id}
              className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:bg-white/10 transition-all group cursor-pointer"
            >
              <div className="flex items-center gap-4">
                <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-green-600 to-emerald-600 rounded-xl flex items-center justify-center text-2xl">
                  {lesson.icon}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-white/50 text-sm font-semibold">Lección {lesson.id}</span>
                    <span className="text-white/50 text-sm">•</span>
                    <span className="text-white/50 text-sm">{lesson.duration}</span>
                  </div>
                  <h3 className="text-white font-bold text-lg mb-1">{lesson.title}</h3>
                  <p className="text-white/70 text-sm">{lesson.description}</p>
                </div>
                <ArrowRight className="w-5 h-5 text-white/50 group-hover:text-white group-hover:translate-x-1 transition-all" />
              </div>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="bg-gradient-to-br from-green-600 to-emerald-600 rounded-2xl p-8 text-center">
          <h3 className="text-2xl font-bold text-white mb-4">
            ¿Listo para crear tu primer mod?
          </h3>
          <p className="text-white/90 mb-6">
            Aprende Java de la forma más divertida: ¡creando mods para Minecraft!
          </p>
          <div className="flex items-center justify-center gap-4">
            <Link
              href="/course/minecraft-intro"
              className="inline-flex items-center gap-2 bg-white text-green-600 px-8 py-3 rounded-lg font-bold hover:bg-white/90 transition-all"
            >
              Comenzar ahora
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="/skill-tree-java"
              className="inline-flex items-center gap-2 bg-white/20 text-white px-8 py-3 rounded-lg font-bold hover:bg-white/30 transition-all backdrop-blur-sm"
            >
              Ver roadmap Java
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
