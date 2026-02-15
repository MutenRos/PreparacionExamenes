'use client';

import { useState } from 'react';
import { CheckCircle, Shield, AlertTriangle } from 'lucide-react';

export default function HackingEticoPage() {
  const [hoveredLesson, setHoveredLesson] = useState<number | null>(null);

  const lessons = [
    {
      id: 1,
      title: '¿Qué es el hacking ético?',
      description: 'Diferencia entre white hat, black hat y grey hat',
      icon: '🎩',
      duration: '15 min',
    },
    {
      id: 2,
      title: 'Legalidad y ética',
      description: 'Qué puedes y qué NO puedes hacer (muy importante)',
      icon: '⚖️',
      duration: '20 min',
    },
    {
      id: 3,
      title: 'Instala Kali Linux',
      description: 'Máquina virtual o dual boot con todas las herramientas',
      icon: '🐉',
      duration: '25 min',
    },
    {
      id: 4,
      title: 'Fundamentos de redes',
      description: 'TCP/IP, puertos, direcciones MAC, protocolos',
      icon: '🌐',
      duration: '30 min',
    },
    {
      id: 5,
      title: 'Escaneo de redes con Nmap',
      description: 'Descubre dispositivos y puertos abiertos',
      icon: '🔍',
      duration: '30 min',
    },
    {
      id: 6,
      title: 'Análisis WiFi con Wireshark',
      description: 'Captura y analiza paquetes de red',
      icon: '📡',
      duration: '35 min',
    },
    {
      id: 7,
      title: 'Ataques WEP y WPA/WPA2',
      description: 'Crackea tu propia WiFi (solo TU red)',
      icon: '🔓',
      duration: '40 min',
    },
    {
      id: 8,
      title: 'Evil Twin y Phishing WiFi',
      description: 'Crea puntos de acceso falsos (en entorno controlado)',
      icon: '👥',
      duration: '35 min',
    },
    {
      id: 9,
      title: 'Sniffing y Man-in-the-Middle',
      description: 'Intercepta tráfico con ARP spoofing',
      icon: '🕵️',
      duration: '40 min',
    },
    {
      id: 10,
      title: 'Protección y mitigación',
      description: 'Cómo defenderte de estos ataques',
      icon: '🛡️',
      duration: '30 min',
    },
    {
      id: 11,
      title: 'WPA3 y redes modernas',
      description: 'Seguridad actual y tendencias futuras',
      icon: '🔐',
      duration: '25 min',
    },
    {
      id: 12,
      title: 'Proyecto final: Auditoría completa',
      description: 'Informe profesional de seguridad de red',
      icon: '📋',
      duration: '45 min',
    },
  ];

  const learningObjectives = [
    'Entender cómo funcionan los ataques a redes WiFi',
    'Usar herramientas profesionales (Kali, Wireshark, Aircrack)',
    'Realizar auditorías de seguridad en TU propia red',
    'Protegerte contra ataques comunes',
  ];

  const tools = [
    { name: 'Kali Linux', icon: '🐉', description: 'SO con 600+ herramientas de pentesting' },
    { name: 'Wireshark', icon: '🦈', description: 'Análisis de tráfico de red' },
    { name: 'Aircrack-ng', icon: '📡', description: 'Suite completa WiFi hacking' },
    { name: 'Nmap', icon: '🗺️', description: 'Escaneo de redes y puertos' },
    { name: 'Metasploit', icon: '💣', description: 'Framework de explotación' },
    { name: 'Burp Suite', icon: '🕷️', description: 'Testing de aplicaciones web' },
  ];

  const attackTypes = [
    {
      name: 'WEP Cracking',
      difficulty: 'Fácil',
      time: '~5 min',
      description: 'Protocolo obsoleto muy vulnerable',
      color: 'text-green-400',
    },
    {
      name: 'WPA/WPA2 Handshake',
      difficulty: 'Medio',
      time: '~1-24h',
      description: 'Captura handshake + diccionario',
      color: 'text-yellow-400',
    },
    {
      name: 'WPS PIN Attack',
      difficulty: 'Medio',
      time: '~2-8h',
      description: 'Vulnerabilidad en WPS habilitado',
      color: 'text-yellow-400',
    },
    {
      name: 'Evil Twin',
      difficulty: 'Avanzado',
      time: 'Variable',
      description: 'Red falsa + phishing',
      color: 'text-red-400',
    },
  ];

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <header className="border-b border-white/10 bg-black/50 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-3">
              <a
                href="/skill-tree"
                className="text-red-400 hover:text-red-300 transition-colors"
              >
                ← Volver
              </a>
              <div className="h-6 w-px bg-red-900/30" />
              <span className="text-sm text-stone-400">Curso de Hacking Ético</span>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-red-500 to-orange-600 mb-6 shadow-lg shadow-red-500/30">
            <Shield className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-red-400 via-orange-400 to-red-500 bg-clip-text text-transparent">
            Hacking Ético WiFi
          </h1>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto mb-8">
            Aprende seguridad de redes desde dentro. Entiende cómo funcionan los ataques WiFi para protegerte mejor. Solo en entornos controlados y legales.
          </p>

          {/* Course Stats */}
          <div className="flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-red-400"></div>
              <span className="text-stone-400">12 lecciones</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-orange-400"></div>
              <span className="text-stone-400">~6 horas</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-red-500"></div>
              <span className="text-stone-400">Avanzado</span>
            </div>
          </div>
        </div>

        {/* LEGAL WARNING */}
        <div className="mb-12 p-6 rounded-xl bg-gradient-to-r from-red-900/30 to-orange-900/30 border-2 border-red-500/50">
          <div className="flex items-start gap-4">
            <AlertTriangle className="w-8 h-8 text-red-400 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-xl font-bold text-red-300 mb-2">
                ⚠️ ADVERTENCIA LEGAL MUY IMPORTANTE
              </h3>
              <div className="space-y-2 text-stone-300">
                <p className="font-semibold">
                  Este curso es EXCLUSIVAMENTE educativo y para uso en TUS PROPIAS REDES.
                </p>
                <ul className="space-y-1 text-sm ml-4">
                  <li>🚫 Atacar redes ajenas es ILEGAL (hasta 3 años de cárcel)</li>
                  <li>✅ Solo practica en TU WiFi o entornos de laboratorio autorizados</li>
                  <li>📚 El objetivo es APRENDER seguridad, no romper la ley</li>
                  <li>🛡️ Úsalo para PROTEGER, no para atacar</li>
                </ul>
                <p className="text-xs text-red-200 mt-3">
                  Ni el curso ni sus creadores se hacen responsables del mal uso de esta información.
                  Conocer las técnicas te hace un mejor profesional de ciberseguridad.
                </p>
              </div>
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
                className="flex items-start gap-3 p-4 rounded-xl bg-stone-900/40 border border-red-900/20 hover:border-red-700/40 transition-all"
              >
                <CheckCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                <span className="text-stone-300">{objective}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Tools */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            🛠️ Herramientas profesionales
          </h2>
          <div className="grid md:grid-cols-3 gap-4">
            {tools.map((tool, index) => (
              <div
                key={index}
                className="p-6 rounded-xl bg-stone-900/40 border border-red-900/20 hover:border-red-700/40 transition-all hover:scale-105"
              >
                <div className="text-4xl mb-3">{tool.icon}</div>
                <h3 className="text-lg font-semibold text-white mb-2">{tool.name}</h3>
                <p className="text-sm text-stone-400">{tool.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Attack Types */}
        <div className="mb-12 p-6 rounded-xl bg-stone-900/40 border border-red-900/20">
          <h3 className="text-lg font-semibold text-red-300 mb-4">
            🎯 Tipos de ataques que estudiarás
          </h3>
          <div className="space-y-4">
            {attackTypes.map((attack, index) => (
              <div key={index} className="flex items-center justify-between p-4 rounded-lg bg-slate-800/30">
                <div className="flex-1">
                  <h4 className="font-semibold text-white mb-1">{attack.name}</h4>
                  <p className="text-sm text-stone-400">{attack.description}</p>
                </div>
                <div className="text-right ml-4">
                  <div className={`text-sm font-semibold ${attack.color} mb-1`}>{attack.difficulty}</div>
                  <div className="text-xs text-stone-500">{attack.time}</div>
                </div>
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
                className="group relative p-6 rounded-xl bg-stone-900/40 border border-red-900/20 hover:border-red-700/50 transition-all duration-300 hover:shadow-lg hover:shadow-red-500/10"
              >
                <div className="flex items-start gap-4">
                  <div className="text-4xl flex-shrink-0 transition-transform group-hover:scale-110">
                    {lesson.icon}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-semibold text-white group-hover:text-red-300 transition-colors">
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
                  <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-red-500/5 to-orange-500/5 pointer-events-none" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-red-600 via-orange-600 to-red-700 p-12 text-center shadow-2xl shadow-red-500/20">
          <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
          <div className="relative">
            <h2 className="text-3xl font-bold text-white mb-4">
              Conviértete en experto en seguridad WiFi
            </h2>
            <p className="text-red-100 mb-8 max-w-2xl mx-auto">
              Aprende las técnicas que usan los profesionales. Solo para uso ético y educativo en entornos controlados.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/course/hacking-wifi-intro"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-white text-red-700 font-semibold hover:bg-red-50 transition-all hover:scale-105 shadow-lg"
              >
                Comenzar ahora
              </a>
              <a
                href="/redes-seguras"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-red-800/50 backdrop-blur-sm text-white font-semibold hover:bg-red-800/70 transition-all border border-white/20"
              >
                Ver curso de protección
              </a>
            </div>
          </div>
        </div>

        {/* Career Paths */}
        <div className="mt-12 p-6 rounded-xl bg-gradient-to-r from-stone-900/20 to-cyan-900/20 border border-stone-700/30">
          <h3 className="text-lg font-semibold text-stone-300 mb-4">
            💼 Salidas profesionales
          </h3>
          <div className="grid md:grid-cols-3 gap-4">
            <div>
              <h4 className="font-semibold text-white mb-2 text-sm">Pentester</h4>
              <p className="text-xs text-stone-400">Auditorías de seguridad en empresas (30-60k€/año)</p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-2 text-sm">Consultor de ciberseguridad</h4>
              <p className="text-xs text-stone-400">Asesoramiento y protección corporativa</p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-2 text-sm">Bug Bounty Hunter</h4>
              <p className="text-xs text-stone-400">Encuentra vulnerabilidades, gana recompensas</p>
            </div>
          </div>
        </div>

        {/* Defense Tips */}
        <div className="mt-12 p-6 rounded-xl bg-stone-900/40 border border-red-900/20">
          <h3 className="text-lg font-semibold text-red-300 mb-4">
            🛡️ Cómo proteger TU WiFi
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3">
              <span className="text-2xl">✅</span>
              <div>
                <h4 className="font-semibold text-white text-sm mb-1">Usa WPA3 o WPA2</h4>
                <p className="text-xs text-stone-400">Nunca WEP, deshabilita WPS</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-2xl">🔐</span>
              <div>
                <h4 className="font-semibold text-white text-sm mb-1">Contraseña fuerte</h4>
                <p className="text-xs text-stone-400">+20 caracteres aleatorios, no diccionario</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-2xl">📡</span>
              <div>
                <h4 className="font-semibold text-white text-sm mb-1">Oculta SSID</h4>
                <p className="text-xs text-stone-400">Y cambia el nombre por defecto del router</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-2xl">🔄</span>
              <div>
                <h4 className="font-semibold text-white text-sm mb-1">Actualiza firmware</h4>
                <p className="text-xs text-stone-400">Router siempre con última versión de seguridad</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
