'use client';

import { useState } from 'react';
import { CheckCircle, Shield, AlertTriangle } from 'lucide-react';

export default function RedesSocialesPage() {
  const [hoveredLesson, setHoveredLesson] = useState<number | null>(null);

  const lessons = [
    {
      id: 1,
      title: 'Tu huella digital',
      description: 'Qué información compartes y quién puede verla',
      icon: '👣',
      duration: '20 min',
    },
    {
      id: 2,
      title: 'Configuración de privacidad',
      description: 'Protege tus cuentas en Instagram, TikTok, X y más',
      icon: '🔒',
      duration: '30 min',
    },
    {
      id: 3,
      title: 'Contraseñas seguras',
      description: 'Gestores de contraseñas y autenticación 2FA',
      icon: '🔑',
      duration: '25 min',
    },
    {
      id: 4,
      title: 'Detectar fake news',
      description: 'Cómo verificar información antes de compartir',
      icon: '🕵️',
      duration: '30 min',
    },
    {
      id: 5,
      title: 'Phishing y estafas',
      description: 'Identifica enlaces maliciosos y mensajes sospechosos',
      icon: '🎣',
      duration: '25 min',
    },
    {
      id: 6,
      title: 'Ciberbullying y acoso',
      description: 'Cómo actuar, denunciar y protegerte',
      icon: '🛡️',
      duration: '35 min',
    },
    {
      id: 7,
      title: 'Sexting y sextorsión',
      description: 'Riesgos, prevención y qué hacer si pasa',
      icon: '⚠️',
      duration: '30 min',
    },
    {
      id: 8,
      title: 'Tu reputación online',
      description: 'Lo que publicas hoy te puede afectar mañana',
      icon: '📸',
      duration: '25 min',
    },
    {
      id: 9,
      title: 'Desconexión digital',
      description: 'Uso saludable, límites de tiempo, bienestar mental',
      icon: '🧘',
      duration: '30 min',
    },
    {
      id: 10,
      title: 'Tu plan de seguridad',
      description: 'Crea tu estrategia personal de protección',
      icon: '📋',
      duration: '20 min',
    },
  ];

  const learningObjectives = [
    'Configurar privacidad en todas tus redes',
    'Detectar amenazas y estafas online',
    'Proteger tu información personal',
    'Actuar ante situaciones de riesgo',
  ];

  const platforms = [
    { name: 'Instagram', icon: '📷', color: 'from-stone-500 to-amber-500' },
    { name: 'TikTok', icon: '🎵', color: 'from-cyan-500 to-stone-500' },
    { name: 'X (Twitter)', icon: '🐦', color: 'from-stone-400 to-cyan-400' },
    { name: 'WhatsApp', icon: '💬', color: 'from-green-500 to-emerald-500' },
    { name: 'Discord', icon: '🎮', color: 'from-stone-500 to-stone-500' },
    { name: 'Snapchat', icon: '👻', color: 'from-yellow-400 to-yellow-500' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-950">
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
              <span className="text-sm text-stone-400">Curso de Seguridad Digital</span>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-stone-500 to-stone-600 mb-6 shadow-lg shadow-indigo-500/30">
            <Shield className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-stone-400 via-purple-400 to-stone-500 bg-clip-text text-transparent">
            Redes Sociales Seguras
          </h1>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto mb-8">
            Aprende a protegerte en el mundo digital. Privacidad, seguridad y uso responsable de redes sociales para disfrutar sin riesgos.
          </p>

          {/* Course Stats */}
          <div className="flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-400"></div>
              <span className="text-stone-400">10 lecciones</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-400"></div>
              <span className="text-stone-400">~4 horas</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-500"></div>
              <span className="text-stone-400">Para todos</span>
            </div>
          </div>
        </div>

        {/* Alert Box */}
        <div className="mb-12 p-6 rounded-xl bg-gradient-to-r from-red-900/20 to-orange-900/20 border border-red-700/30">
          <div className="flex items-start gap-4">
            <AlertTriangle className="w-6 h-6 text-red-400 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-lg font-semibold text-red-300 mb-2">
                ¿Por qué es importante este curso?
              </h3>
              <p className="text-stone-300 mb-3">
                Cada día pasamos horas en redes sociales. Es importante saber:
              </p>
              <ul className="space-y-2 text-stone-400">
                <li>• El 60% de los adolescentes ha experimentado ciberacoso</li>
                <li>• 8 de cada 10 no configuran la privacidad correctamente</li>
                <li>• La información que compartes puede ser usada en tu contra</li>
                <li>• Las consecuencias de una mala decisión pueden durar años</li>
              </ul>
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

        {/* Platforms Covered */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Plataformas que cubrimos</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {platforms.map((platform, index) => (
              <div
                key={index}
                className="p-4 rounded-xl bg-stone-900/40 border border-stone-900/20 hover:border-stone-700/40 transition-all text-center"
              >
                <div className={`text-4xl mb-2 bg-gradient-to-br ${platform.color} bg-clip-text`}>
                  {platform.icon}
                </div>
                <p className="text-sm text-stone-300 font-medium">{platform.name}</p>
              </div>
            ))}
          </div>
          <p className="text-sm text-stone-500 mt-4 text-center">
            + Guías específicas para cada plataforma
          </p>
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
                className="group relative p-6 rounded-xl bg-stone-900/40 border border-stone-900/20 hover:border-stone-700/50 transition-all duration-300 hover:shadow-lg hover:shadow-indigo-500/10"
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
                  <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-stone-500/5 to-stone-500/5 pointer-events-none" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-stone-600 via-purple-600 to-stone-700 p-12 text-center shadow-2xl shadow-indigo-500/20">
          <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
          <div className="relative">
            <h2 className="text-3xl font-bold text-white mb-4">
              Toma el control de tu seguridad digital
            </h2>
            <p className="text-stone-100 mb-8 max-w-2xl mx-auto">
              No esperes a que algo malo pase. Aprende ahora a protegerte y disfrutar de las redes sociales de forma segura.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/course/redes-seguras-intro"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-white text-stone-700 font-semibold hover:bg-amber-50 transition-all hover:scale-105 shadow-lg"
              >
                Comenzar ahora
              </a>
              <a
                href="/skill-tree-security"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-amber-800/50 backdrop-blur-sm text-white font-semibold hover:bg-amber-800/70 transition-all border border-white/20"
              >
                Ver roadmap de Seguridad
              </a>
            </div>
          </div>
        </div>

        {/* Practical Tips */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Lo que aprenderás a hacer
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-gradient-to-br from-stone-900/20 to-stone-900/20 border border-stone-700/30">
              <div className="text-3xl mb-3">🔐</div>
              <h3 className="text-lg font-semibold text-white mb-2">Protección práctica</h3>
              <ul className="space-y-2 text-sm text-stone-400">
                <li>• Configurar privacidad paso a paso</li>
                <li>• Usar autenticación de dos factores</li>
                <li>• Crear contraseñas realmente seguras</li>
                <li>• Detectar cuentas falsas</li>
              </ul>
            </div>
            <div className="p-6 rounded-xl bg-gradient-to-br from-stone-900/20 to-stone-900/20 border border-stone-700/30">
              <div className="text-3xl mb-3">🚨</div>
              <h3 className="text-lg font-semibold text-white mb-2">Actuar ante problemas</h3>
              <ul className="space-y-2 text-sm text-stone-400">
                <li>• Denunciar acoso correctamente</li>
                <li>• Bloquear y reportar amenazas</li>
                <li>• Recuperar una cuenta hackeada</li>
                <li>• Buscar ayuda profesional</li>
              </ul>
            </div>
            <div className="p-6 rounded-xl bg-gradient-to-br from-stone-900/20 to-stone-800/20 border border-stone-700/30">
              <div className="text-3xl mb-3">💡</div>
              <h3 className="text-lg font-semibold text-white mb-2">Uso inteligente</h3>
              <ul className="space-y-2 text-sm text-stone-400">
                <li>• Verificar información antes de compartir</li>
                <li>• Gestionar tu tiempo en redes</li>
                <li>• Construir una buena reputación</li>
                <li>• Proteger a amigos y familia</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Resources */}
        <div className="mt-12 p-6 rounded-xl bg-stone-900/40 border border-stone-900/20">
          <h3 className="text-lg font-semibold text-stone-300 mb-4">
            📞 Recursos de ayuda incluidos
          </h3>
          <div className="grid md:grid-cols-2 gap-4 text-stone-300">
            <div>
              <h4 className="font-semibold text-white mb-2">En situaciones de emergencia</h4>
              <ul className="space-y-1 text-sm text-stone-400">
                <li>• Líneas de ayuda contra el acoso</li>
                <li>• Reportar a autoridades competentes</li>
                <li>• Apoyo psicológico gratuito</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-2">Herramientas útiles</h4>
              <ul className="space-y-1 text-sm text-stone-400">
                <li>• Gestores de contraseñas recomendados</li>
                <li>• Apps de control parental</li>
                <li>• Checklist de seguridad descargable</li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
