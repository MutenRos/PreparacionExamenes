'use client';

import { useState } from 'react';
import { CheckCircle, Home, Wifi, AlertTriangle } from 'lucide-react';

export default function DomoticaPage() {
  const [hoveredLesson, setHoveredLesson] = useState<number | null>(null);

  const lessons = [
    {
      id: 1,
      title: '¿Qué es la domótica?',
      description: 'Introducción a las casas inteligentes y sus posibilidades',
      icon: '🏠',
      duration: '15 min',
    },
    {
      id: 2,
      title: 'Tu primer ESP32',
      description: 'Conoce el cerebro de tu casa inteligente',
      icon: '🧠',
      duration: '20 min',
    },
    {
      id: 3,
      title: 'Controlar LEDs por WiFi',
      description: 'Tu primera luz inteligente con control remoto',
      icon: '💡',
      duration: '25 min',
    },
    {
      id: 4,
      title: 'Sensores de temperatura',
      description: 'Monitoriza la temperatura de tu casa',
      icon: '🌡️',
      duration: '30 min',
    },
    {
      id: 5,
      title: 'Detector de movimiento',
      description: 'Crea un sistema de seguridad básico',
      icon: '🚶',
      duration: '25 min',
    },
    {
      id: 6,
      title: 'App móvil con Blynk',
      description: 'Controla todo desde tu smartphone',
      icon: '📱',
      duration: '35 min',
    },
    {
      id: 7,
      title: 'Automatizaciones inteligentes',
      description: 'Programa acciones automáticas (si-entonces)',
      icon: '⚡',
      duration: '30 min',
    },
    {
      id: 8,
      title: 'Asistente de voz',
      description: 'Integración con Alexa y Google Home',
      icon: '🎤',
      duration: '40 min',
    },
    {
      id: 9,
      title: 'Ahorro energético',
      description: 'Optimiza el consumo de tu hogar',
      icon: '🔋',
      duration: '25 min',
    },
    {
      id: 10,
      title: 'Tu sistema completo',
      description: 'Integra todos los componentes en un panel central',
      icon: '🎛️',
      duration: '45 min',
    },
  ];

  const learningObjectives = [
    'Programar dispositivos ESP32 y Arduino',
    'Crear redes de sensores IoT',
    'Desarrollar apps móviles de control',
    'Integrar con asistentes de voz',
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950">
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
              <div className="h-6 w-px bg-stone-900/30" />
              <span className="text-sm text-stone-400">Curso Especializado</span>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-stone-500 to-cyan-600 mb-6 shadow-lg shadow-stone-500/30">
            <Home className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-stone-400 via-cyan-400 to-stone-500 bg-clip-text text-transparent">
            Domótica & Smart Home
          </h1>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto mb-8">
            Convierte tu casa en un hogar inteligente. Aprende a crear sistemas de automatización, control remoto y ahorro energético.
          </p>

          {/* Course Stats */}
          <div className="flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-stone-400"></div>
              <span className="text-stone-400">10 lecciones</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-400"></div>
              <span className="text-stone-400">~5 horas</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-stone-500"></div>
              <span className="text-stone-400">Principiante-Intermedio</span>
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

        {/* Prerequisites Warning */}
        <div className="mb-12 p-6 rounded-xl bg-gradient-to-r from-amber-900/20 to-orange-900/20 border border-amber-700/30">
          <div className="flex items-start gap-4">
            <AlertTriangle className="w-6 h-6 text-amber-400 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-lg font-semibold text-amber-300 mb-2">
                Requisitos previos
              </h3>
              <p className="text-stone-300 mb-3">
                Para aprovechar al máximo este curso, es recomendable tener conocimientos básicos de:
              </p>
              <ul className="space-y-1 text-stone-400">
                <li>• Programación básica (variables, condicionales, funciones)</li>
                <li>• Conceptos básicos de Arduino (se explica desde cero)</li>
              </ul>
              <a
                href="/intro-programacion"
                className="inline-block mt-4 text-stone-400 hover:text-stone-300 transition-colors"
              >
                Ver curso de Introducción a la Programación →
              </a>
            </div>
          </div>
        </div>

        {/* Hardware Needed */}
        <div className="mb-12 p-6 rounded-xl bg-stone-900/40 border border-stone-900/20">
          <div className="flex items-start gap-4">
            <Wifi className="w-6 h-6 text-stone-400 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-lg font-semibold text-stone-300 mb-2">
                Hardware necesario
              </h3>
              <p className="text-stone-300 mb-3">
                Para seguir las prácticas del curso necesitarás:
              </p>
              <div className="grid md:grid-cols-2 gap-3 text-stone-400">
                <div className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-stone-400"></div>
                  <span>Placa ESP32 o Arduino</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-stone-400"></div>
                  <span>Sensor de temperatura DHT11/22</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-stone-400"></div>
                  <span>LEDs y resistencias</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-stone-400"></div>
                  <span>Sensor PIR (movimiento)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-stone-400"></div>
                  <span>Cables jumper y protoboard</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-stone-400"></div>
                  <span>Relés (opcional, para electrodomésticos)</span>
                </div>
              </div>
              <p className="text-sm text-stone-500 mt-4">
                💡 Precio total del kit: ~30-50€ (te servirá para muchos proyectos)
              </p>
            </div>
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
                className="group relative p-6 rounded-xl bg-stone-900/40 border border-stone-900/20 hover:border-stone-700/50 transition-all duration-300 hover:shadow-lg hover:shadow-stone-500/10"
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
                  <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-stone-500/5 to-cyan-500/5 pointer-events-none" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-stone-600 via-cyan-600 to-stone-700 p-12 text-center shadow-2xl shadow-stone-500/20">
          <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
          <div className="relative">
            <h2 className="text-3xl font-bold text-white mb-4">
              ¿Listo para automatizar tu hogar?
            </h2>
            <p className="text-stone-100 mb-8 max-w-2xl mx-auto">
              Empieza a construir tu casa inteligente desde cero. Control remoto, sensores, automatizaciones y mucho más.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/course/domotica-intro"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-white text-stone-700 font-semibold hover:bg-stone-50 transition-all hover:scale-105 shadow-lg"
              >
                Comenzar ahora
              </a>
              <a
                href="/skill-tree-arduino"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-stone-800/50 backdrop-blur-sm text-white font-semibold hover:bg-stone-800/70 transition-all border border-white/20"
              >
                Ver roadmap Arduino/IoT
              </a>
            </div>
          </div>
        </div>

        {/* Projects Preview */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Proyectos que construirás
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-gradient-to-br from-stone-900/20 to-cyan-900/20 border border-stone-700/30">
              <div className="text-3xl mb-3">🏡</div>
              <h3 className="text-lg font-semibold text-white mb-2">Sistema de iluminación</h3>
              <p className="text-sm text-stone-400">
                Control de luces por WiFi, programación horaria y detección de presencia
              </p>
            </div>
            <div className="p-6 rounded-xl bg-gradient-to-br from-cyan-900/20 to-stone-900/20 border border-cyan-700/30">
              <div className="text-3xl mb-3">🌡️</div>
              <h3 className="text-lg font-semibold text-white mb-2">Estación meteorológica</h3>
              <p className="text-sm text-stone-400">
                Monitoriza temperatura, humedad y calidad del aire en tiempo real
              </p>
            </div>
            <div className="p-6 rounded-xl bg-gradient-to-br from-stone-900/20 to-stone-800/20 border border-stone-700/30">
              <div className="text-3xl mb-3">🔐</div>
              <h3 className="text-lg font-semibold text-white mb-2">Sistema de seguridad</h3>
              <p className="text-sm text-stone-400">
                Detección de movimiento, alertas en tu móvil y cámara de vigilancia
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
