'use client';

import { useState } from 'react';
import { CheckCircle, Box, AlertTriangle } from 'lucide-react';

export default function Impresion3DPage() {
  const [hoveredLesson, setHoveredLesson] = useState<number | null>(null);

  const lessons = [
    {
      id: 1,
      title: '¿Qué es la impresión 3D?',
      description: 'Tecnologías FDM, SLA, SLS y sus aplicaciones',
      icon: '🖨️',
      duration: '20 min',
    },
    {
      id: 2,
      title: 'Tu primera impresora',
      description: 'Montaje, calibración y primeros pasos',
      icon: '🔧',
      duration: '30 min',
    },
    {
      id: 3,
      title: 'Diseño 3D con Tinkercad',
      description: 'Crea tus primeros modelos sin experiencia previa',
      icon: '🎨',
      duration: '45 min',
    },
    {
      id: 4,
      title: 'Slicing con Cura',
      description: 'Prepara tus modelos para imprimir',
      icon: '📐',
      duration: '35 min',
    },
    {
      id: 5,
      title: 'Parámetros de impresión',
      description: 'Velocidad, temperatura, relleno y soportes',
      icon: '⚙️',
      duration: '40 min',
    },
    {
      id: 6,
      title: 'Modelado avanzado: Fusion 360',
      description: 'Diseño paramétrico profesional',
      icon: '🏗️',
      duration: '60 min',
    },
    {
      id: 7,
      title: 'Diseño orgánico con Blender',
      description: 'Esculturas, figuras y formas complejas',
      icon: '🗿',
      duration: '50 min',
    },
    {
      id: 8,
      title: 'Impresión multimaterial',
      description: 'Combina colores y materiales flexibles',
      icon: '🌈',
      duration: '30 min',
    },
    {
      id: 9,
      title: 'Post-procesado profesional',
      description: 'Lijado, pintura y acabados de calidad',
      icon: '✨',
      duration: '35 min',
    },
    {
      id: 10,
      title: 'Proyectos y venta online',
      description: 'Monetiza tus diseños en Etsy, Cults3D y Thingiverse',
      icon: '💰',
      duration: '25 min',
    },
  ];

  const learningObjectives = [
    'Diseñar modelos 3D desde cero',
    'Dominar software CAD profesional',
    'Optimizar impresiones para calidad y velocidad',
    'Crear y vender tus propios diseños',
  ];

  const softwareList = [
    { name: 'Tinkercad', description: 'Diseño 3D para principiantes (gratis)', icon: '🟢' },
    { name: 'Fusion 360', description: 'CAD profesional (gratis para estudiantes)', icon: '🔵' },
    { name: 'Blender', description: 'Modelado orgánico (gratis y open source)', icon: '🟠' },
    { name: 'Cura', description: 'Slicer más popular (gratis)', icon: '🟣' },
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
              <span className="text-sm text-stone-400">Curso Especializado</span>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-stone-500 to-amber-600 mb-6 shadow-lg shadow-amber-500/30">
            <Box className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-stone-400 via-pink-400 to-stone-500 bg-clip-text text-transparent">
            Impresión 3D & Diseño
          </h1>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto mb-8">
            Aprende a diseñar e imprimir cualquier cosa que imagines. Desde figuras personalizadas hasta piezas funcionales y prototipos profesionales.
          </p>

          {/* Course Stats */}
          <div className="flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-400"></div>
              <span className="text-stone-400">10 lecciones</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-400"></div>
              <span className="text-stone-400">~6 horas</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-500"></div>
              <span className="text-stone-400">Todos los niveles</span>
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

        {/* Software Section */}
        <div className="mb-12 p-6 rounded-xl bg-stone-900/40 border border-stone-900/20">
          <h3 className="text-lg font-semibold text-stone-300 mb-4">
            Software que usaremos
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            {softwareList.map((software, index) => (
              <div key={index} className="flex items-start gap-3 p-3 rounded-lg bg-slate-800/30">
                <span className="text-2xl">{software.icon}</span>
                <div>
                  <h4 className="font-semibold text-white">{software.name}</h4>
                  <p className="text-sm text-stone-400">{software.description}</p>
                </div>
              </div>
            ))}
          </div>
          <p className="text-sm text-stone-500 mt-4">
            💡 Todo el software es gratuito o tiene versiones free para estudiantes
          </p>
        </div>

        {/* Prerequisites Warning */}
        <div className="mb-12 p-6 rounded-xl bg-gradient-to-r from-amber-900/20 to-orange-900/20 border border-amber-700/30">
          <div className="flex items-start gap-4">
            <AlertTriangle className="w-6 h-6 text-amber-400 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-lg font-semibold text-amber-300 mb-2">
                ¿Necesito una impresora 3D?
              </h3>
              <p className="text-stone-300 mb-3">
                No es obligatorio. Puedes aprender diseño 3D sin impresora y:
              </p>
              <ul className="space-y-1 text-stone-400">
                <li>• Usar servicios online de impresión (envían a tu casa)</li>
                <li>• Vender diseños digitales en plataformas como Cults3D</li>
                <li>• Acceder a FabLabs o makerspaces de tu ciudad</li>
                <li>• Comprar una impresora más adelante (~150-300€ para empezar)</li>
              </ul>
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

        {/* CTA Section */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-stone-600 via-pink-600 to-stone-700 p-12 text-center shadow-2xl shadow-amber-500/20">
          <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
          <div className="relative">
            <h2 className="text-3xl font-bold text-white mb-4">
              Da vida a tus ideas
            </h2>
            <p className="text-stone-100 mb-8 max-w-2xl mx-auto">
              Desde figuras personalizadas hasta prototipos funcionales. Aprende a diseñar, imprimir y monetizar tus creaciones.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/course/impresion3d-intro"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-white text-stone-700 font-semibold hover:bg-amber-50 transition-all hover:scale-105 shadow-lg"
              >
                Comenzar ahora
              </a>
              <a
                href="/skill-tree"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-amber-800/50 backdrop-blur-sm text-white font-semibold hover:bg-amber-800/70 transition-all border border-white/20"
              >
                Ver todos los cursos
              </a>
            </div>
          </div>
        </div>

        {/* Projects Preview */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Proyectos que crearás
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-gradient-to-br from-stone-900/20 to-amber-900/20 border border-stone-700/30">
              <div className="text-3xl mb-3">🎮</div>
              <h3 className="text-lg font-semibold text-white mb-2">Accesorios gaming</h3>
              <p className="text-sm text-stone-400">
                Soportes para mandos, organizadores de cables, stands personalizados
              </p>
            </div>
            <div className="p-6 rounded-xl bg-gradient-to-br from-amber-900/20 to-stone-900/20 border border-amber-700/30">
              <div className="text-3xl mb-3">🏠</div>
              <h3 className="text-lg font-semibold text-white mb-2">Piezas funcionales</h3>
              <p className="text-sm text-stone-400">
                Repuestos para casa, organizadores, carcasas para electrónica
              </p>
            </div>
            <div className="p-6 rounded-xl bg-gradient-to-br from-stone-900/20 to-stone-800/20 border border-stone-700/30">
              <div className="text-3xl mb-3">🎨</div>
              <h3 className="text-lg font-semibold text-white mb-2">Arte y figuras</h3>
              <p className="text-sm text-stone-400">
                Miniaturas, esculturas, regalos personalizados y merchandising
              </p>
            </div>
          </div>
        </div>

        {/* Business Opportunities */}
        <div className="mt-12 p-6 rounded-xl bg-gradient-to-r from-green-900/20 to-emerald-900/20 border border-green-700/30">
          <h3 className="text-lg font-semibold text-green-300 mb-3">
            💼 Oportunidades de negocio
          </h3>
          <div className="grid md:grid-cols-2 gap-4 text-stone-300">
            <div>
              <h4 className="font-semibold text-white mb-2">Vende diseños digitales</h4>
              <ul className="space-y-1 text-sm text-stone-400">
                <li>• Cults3D, MyMiniFactory, Thingiverse</li>
                <li>• Gana dinero mientras duermes</li>
                <li>• Sin necesidad de inventario</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-2">Servicio de impresión</h4>
              <ul className="space-y-1 text-sm text-stone-400">
                <li>• Imprime bajo demanda para clientes</li>
                <li>• Prototipos para empresas locales</li>
                <li>• Regalos personalizados (bodas, eventos)</li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
