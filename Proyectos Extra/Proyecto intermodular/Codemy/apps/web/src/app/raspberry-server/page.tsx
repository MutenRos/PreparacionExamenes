'use client';

import { useState } from 'react';
import { CheckCircle, Server, AlertTriangle } from 'lucide-react';

export default function RaspberryServerPage() {
  const [hoveredLesson, setHoveredLesson] = useState<number | null>(null);

  const lessons = [
    {
      id: 1,
      title: '¿Qué es una Raspberry Pi?',
      description: 'Conoce este mini-ordenador y sus posibilidades',
      icon: '🥧',
      duration: '15 min',
    },
    {
      id: 2,
      title: 'Instalación de Raspberry Pi OS',
      description: 'Configura el sistema operativo desde cero',
      icon: '💾',
      duration: '25 min',
    },
    {
      id: 3,
      title: 'Configuración inicial y SSH',
      description: 'Acceso remoto seguro a tu servidor',
      icon: '🔐',
      duration: '20 min',
    },
    {
      id: 4,
      title: 'Servidor web con Apache/Nginx',
      description: 'Hosting de tu propia web desde casa',
      icon: '🌐',
      duration: '30 min',
    },
    {
      id: 5,
      title: 'Servidor de archivos (NAS)',
      description: 'Tu propia nube personal con Samba/NextCloud',
      icon: '☁️',
      duration: '35 min',
    },
    {
      id: 6,
      title: 'Servidor multimedia (Plex)',
      description: 'Streaming de películas y series en casa',
      icon: '🎬',
      duration: '30 min',
    },
    {
      id: 7,
      title: 'Pi-hole: Bloquea anuncios',
      description: 'Adiós publicidad en toda tu red',
      icon: '🛡️',
      duration: '25 min',
    },
    {
      id: 8,
      title: 'VPN casera con PiVPN',
      description: 'Conexión segura desde cualquier lugar',
      icon: '🔒',
      duration: '35 min',
    },
    {
      id: 9,
      title: 'Monitorización y backups',
      description: 'Mantén tu servidor seguro y respaldado',
      icon: '📊',
      duration: '30 min',
    },
    {
      id: 10,
      title: 'Docker y contenedores',
      description: 'Despliega múltiples servicios fácilmente',
      icon: '🐳',
      duration: '40 min',
    },
  ];

  const learningObjectives = [
    'Instalar y configurar Raspberry Pi OS',
    'Crear servidores web, NAS y multimedia',
    'Configurar VPN y seguridad de red',
    'Administrar servicios con Docker',
  ];

  const hardwareNeeded = [
    { item: 'Raspberry Pi 4 (4GB/8GB)', price: '~60-80€', icon: '🥧' },
    { item: 'MicroSD 32GB+ (Clase 10)', price: '~10-15€', icon: '💾' },
    { item: 'Fuente 5V 3A USB-C', price: '~10€', icon: '🔌' },
    { item: 'Carcasa con ventilación', price: '~8€', icon: '📦' },
    { item: 'Cable Ethernet (opcional)', price: '~5€', icon: '🔗' },
  ];

  const projects = [
    {
      title: 'Nube personal',
      description: 'NextCloud con 1TB de almacenamiento accesible desde cualquier lugar',
      icon: '☁️',
    },
    {
      title: 'Centro multimedia',
      description: 'Plex o Jellyfin para toda tu colección de películas y series',
      icon: '🎥',
    },
    {
      title: 'Red sin publicidad',
      description: 'Pi-hole bloqueando anuncios en todos tus dispositivos',
      icon: '🚫',
    },
    {
      title: 'Servidor de juegos',
      description: 'Minecraft, Terraria o servidor de Discord bot',
      icon: '🎮',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-red-950 to-slate-950">
      {/* Header */}
      <header className="border-b border-red-900/20 bg-stone-950/50 backdrop-blur-sm">
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
              <span className="text-sm text-stone-400">Curso de Servidores</span>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-red-500 to-amber-600 mb-6 shadow-lg shadow-red-500/30">
            <Server className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-red-400 via-pink-400 to-red-500 bg-clip-text text-transparent">
            Servidor Casero con Raspberry Pi
          </h1>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto mb-8">
            Crea tu propio servidor doméstico. Hosting web, nube personal, servidor multimedia, VPN y mucho más con una Raspberry Pi.
          </p>

          {/* Course Stats */}
          <div className="flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-red-400"></div>
              <span className="text-stone-400">10 lecciones</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-400"></div>
              <span className="text-stone-400">~5 horas</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-red-500"></div>
              <span className="text-stone-400">Intermedio</span>
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

        {/* Hardware Section */}
        <div className="mb-12 p-6 rounded-xl bg-stone-900/40 border border-red-900/20">
          <h3 className="text-lg font-semibold text-red-300 mb-4">
            🛒 Hardware necesario
          </h3>
          <div className="space-y-3 mb-4">
            {hardwareNeeded.map((hw, index) => (
              <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-slate-800/30">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{hw.icon}</span>
                  <span className="text-stone-300">{hw.item}</span>
                </div>
                <span className="text-red-400 font-semibold">{hw.price}</span>
              </div>
            ))}
          </div>
          <div className="p-4 rounded-lg bg-green-900/20 border border-green-700/30">
            <p className="text-green-300 font-semibold mb-1">💰 Inversión total: ~100€</p>
            <p className="text-sm text-stone-400">
              Menos que un mes de servicios en la nube. Pagas una vez y es tuyo para siempre.
            </p>
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
                Para aprovechar al máximo este curso, es recomendable:
              </p>
              <ul className="space-y-1 text-stone-400">
                <li>• Conocimientos básicos de Linux (línea de comandos)</li>
                <li>• Nociones de redes (IP, puertos, router)</li>
                <li>• Ganas de aprender y experimentar</li>
              </ul>
              <a
                href="/skill-tree-devops"
                className="inline-block mt-4 text-red-400 hover:text-red-300 transition-colors"
              >
                Ver roadmap de DevOps y Linux →
              </a>
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
                  <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-red-500/5 to-amber-500/5 pointer-events-none" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-red-600 via-pink-600 to-red-700 p-12 text-center shadow-2xl shadow-red-500/20">
          <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
          <div className="relative">
            <h2 className="text-3xl font-bold text-white mb-4">
              Tu propio servidor por menos de 100€
            </h2>
            <p className="text-red-100 mb-8 max-w-2xl mx-auto">
              Independízate de servicios en la nube. Controla tus datos, aprende Linux y ahorra dinero a largo plazo.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/course/raspberry-server-intro"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-white text-red-700 font-semibold hover:bg-red-50 transition-all hover:scale-105 shadow-lg"
              >
                Comenzar ahora
              </a>
              <a
                href="/skill-tree-devops"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-red-800/50 backdrop-blur-sm text-white font-semibold hover:bg-red-800/70 transition-all border border-white/20"
              >
                Ver roadmap DevOps
              </a>
            </div>
          </div>
        </div>

        {/* Projects Preview */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Proyectos que crearás
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {projects.map((project, index) => (
              <div key={index} className="p-6 rounded-xl bg-gradient-to-br from-red-900/20 to-amber-900/20 border border-red-700/30">
                <div className="text-3xl mb-3">{project.icon}</div>
                <h3 className="text-lg font-semibold text-white mb-2">{project.title}</h3>
                <p className="text-sm text-stone-400">
                  {project.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Why Raspberry Pi */}
        <div className="mt-12 p-6 rounded-xl bg-gradient-to-r from-stone-900/20 to-cyan-900/20 border border-stone-700/30">
          <h3 className="text-lg font-semibold text-stone-300 mb-4">
            🥧 ¿Por qué Raspberry Pi?
          </h3>
          <div className="grid md:grid-cols-2 gap-4 text-stone-300">
            <div>
              <h4 className="font-semibold text-white mb-2">Ventajas</h4>
              <ul className="space-y-1 text-sm text-stone-400">
                <li>• Bajo consumo eléctrico (~5W, &lt;3€/mes)</li>
                <li>• Silenciosa y compacta</li>
                <li>• Gran comunidad y soporte</li>
                <li>• Muchos proyectos y tutoriales</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-2">Ahorro vs Cloud</h4>
              <ul className="space-y-1 text-sm text-stone-400">
                <li>• Dropbox 2TB: 10€/mes = 120€/año</li>
                <li>• VPS básico: 5€/mes = 60€/año</li>
                <li>• Plex Pass: 5€/mes = 60€/año</li>
                <li>• <strong className="text-green-400">Tu Raspberry: 100€ una vez</strong></li>
              </ul>
            </div>
          </div>
        </div>

        {/* Advanced Topics */}
        <div className="mt-12 p-6 rounded-xl bg-stone-900/40 border border-red-900/20">
          <h3 className="text-lg font-semibold text-red-300 mb-4">
            🚀 Bonus: Temas avanzados
          </h3>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="flex items-start gap-3">
              <div className="text-2xl">🔄</div>
              <div>
                <h4 className="font-semibold text-white text-sm">Alta disponibilidad</h4>
                <p className="text-xs text-stone-400">Cluster de Raspberry Pi para redundancia</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="text-2xl">📡</div>
              <div>
                <h4 className="font-semibold text-white text-sm">DynDNS</h4>
                <p className="text-xs text-stone-400">Acceso desde internet con IP dinámica</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="text-2xl">📈</div>
              <div>
                <h4 className="font-semibold text-white text-sm">Monitorización</h4>
                <p className="text-xs text-stone-400">Grafana + Prometheus para métricas</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="text-2xl">🔐</div>
              <div>
                <h4 className="font-semibold text-white text-sm">Fail2ban</h4>
                <p className="text-xs text-stone-400">Protección contra ataques de fuerza bruta</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="text-2xl">🎯</div>
              <div>
                <h4 className="font-semibold text-white text-sm">Reverse Proxy</h4>
                <p className="text-xs text-stone-400">Nginx con SSL para múltiples servicios</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="text-2xl">⚡</div>
              <div>
                <h4 className="font-semibold text-white text-sm">Portainer</h4>
                <p className="text-xs text-stone-400">Gestión visual de Docker containers</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
