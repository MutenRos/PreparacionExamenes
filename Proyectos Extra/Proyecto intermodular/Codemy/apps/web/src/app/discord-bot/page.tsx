'use client';

import { useState } from 'react';
import { CheckCircle, Bot, Code2 } from 'lucide-react';

export default function DiscordBotPage() {
  const [hoveredLesson, setHoveredLesson] = useState<number | null>(null);

  const lessons = [
    {
      id: 1,
      title: '¿Qué es un bot de Discord?',
      description: 'Funcionalidades, casos de uso y ejemplos reales',
      icon: '🤖',
      duration: '15 min',
    },
    {
      id: 2,
      title: 'Configura Node.js y Discord.js',
      description: 'Instalación y creación de aplicación en Discord Developer Portal',
      icon: '⚙️',
      duration: '20 min',
    },
    {
      id: 3,
      title: 'Tu primer bot: ¡Hola Mundo!',
      description: 'Conecta el bot y responde a mensajes básicos',
      icon: '👋',
      duration: '25 min',
    },
    {
      id: 4,
      title: 'Comandos slash (/) modernos',
      description: 'Sistema de comandos oficial de Discord',
      icon: '⚡',
      duration: '30 min',
    },
    {
      id: 5,
      title: 'Gestión de eventos',
      description: 'messageCreate, guildMemberAdd, reacciones y más',
      icon: '📡',
      duration: '30 min',
    },
    {
      id: 6,
      title: 'Embeds y mensajes ricos',
      description: 'Crea mensajes con formato, imágenes y botones',
      icon: '🎨',
      duration: '25 min',
    },
    {
      id: 7,
      title: 'Sistema de moderación',
      description: 'Kick, ban, mute, warns y logs automáticos',
      icon: '🛡️',
      duration: '35 min',
    },
    {
      id: 8,
      title: 'Bot de música',
      description: 'Reproduce música de YouTube y Spotify',
      icon: '🎵',
      duration: '40 min',
    },
    {
      id: 9,
      title: 'Base de datos con MongoDB',
      description: 'Guarda configuraciones, economía y estadísticas',
      icon: '💾',
      duration: '35 min',
    },
    {
      id: 10,
      title: 'Mini-juegos y economía',
      description: 'Sistema de monedas, tienda, inventario y juegos',
      icon: '🎮',
      duration: '40 min',
    },
    {
      id: 11,
      title: 'Hosting 24/7',
      description: 'Despliega tu bot en Heroku, Railway o VPS',
      icon: '☁️',
      duration: '30 min',
    },
    {
      id: 12,
      title: 'Bot verificado y avanzado',
      description: 'Slash commands globales, sharding, optimización',
      icon: '✅',
      duration: '35 min',
    },
  ];

  const learningObjectives = [
    'Crear bots de Discord desde cero con Node.js',
    'Implementar comandos slash, eventos y moderación',
    'Construir sistemas de música, economía y mini-juegos',
    'Desplegar tu bot 24/7 en la nube',
  ];

  const features = [
    {
      title: 'Bot de moderación',
      description: 'Auto-moderación, warns, mutes y sistema de logs completo',
      icon: '🛡️',
    },
    {
      title: 'Bot de música',
      description: 'Cola de reproducción, controles, letras y playlists',
      icon: '🎵',
    },
    {
      title: 'Sistema de economía',
      description: 'Monedas virtuales, tienda, inventario y trading',
      icon: '💰',
    },
    {
      title: 'Mini-juegos',
      description: 'Trivia, ruleta, blackjack, duelos y rankings',
      icon: '🎲',
    },
    {
      title: 'Utilidades',
      description: 'Encuestas, recordatorios, clima, traducción automática',
      icon: '🔧',
    },
    {
      title: 'Gestión de roles',
      description: 'Roles automáticos, reacción para roles, niveles',
      icon: '🎭',
    },
  ];

  const techStack = [
    { name: 'Node.js', icon: '🟢', description: 'JavaScript en servidor' },
    { name: 'Discord.js v14', icon: '💜', description: 'Librería oficial' },
    { name: 'MongoDB', icon: '🍃', description: 'Base de datos NoSQL' },
    { name: 'Heroku/Railway', icon: '☁️', description: 'Hosting gratuito' },
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
              <span className="text-sm text-stone-400">Curso de Discord Bot</span>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-stone-500 to-stone-600 mb-6 shadow-lg shadow-indigo-500/30">
            <Bot className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-stone-400 via-purple-400 to-stone-500 bg-clip-text text-transparent">
            Crea tu Propio Bot de Discord
          </h1>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto mb-8">
            Aprende a programar bots de Discord desde cero. Moderación automática, música, economía, mini-juegos y mucho más con Node.js y Discord.js.
          </p>

          {/* Course Stats */}
          <div className="flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-400"></div>
              <span className="text-stone-400">12 lecciones</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-400"></div>
              <span className="text-stone-400">~6 horas</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-500"></div>
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
                className="flex items-start gap-3 p-4 rounded-xl bg-stone-900/40 border border-stone-900/20 hover:border-stone-700/40 transition-all"
              >
                <CheckCircle className="w-5 h-5 text-stone-400 flex-shrink-0 mt-0.5" />
                <span className="text-stone-300">{objective}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Tech Stack */}
        <div className="mb-12 p-6 rounded-xl bg-stone-900/40 border border-stone-900/20">
          <h3 className="text-lg font-semibold text-stone-300 mb-4">
            🛠️ Tecnologías que usarás
          </h3>
          <div className="grid md:grid-cols-4 gap-4">
            {techStack.map((tech, index) => (
              <div key={index} className="flex flex-col items-center p-4 rounded-lg bg-slate-800/30 hover:bg-slate-800/50 transition-all">
                <div className="text-3xl mb-2">{tech.icon}</div>
                <h4 className="font-semibold text-white text-sm mb-1">{tech.name}</h4>
                <p className="text-xs text-stone-400 text-center">{tech.description}</p>
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

        {/* Features Preview */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Tipos de bots que crearás
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <div key={index} className="p-6 rounded-xl bg-gradient-to-br from-stone-900/20 to-stone-900/20 border border-stone-700/30 hover:border-stone-600/50 transition-all hover:scale-105">
                <div className="text-3xl mb-3">{feature.icon}</div>
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-sm text-stone-400">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Code Preview */}
        <div className="mb-12 p-6 rounded-xl bg-stone-900/60 border border-stone-900/30">
          <div className="flex items-center gap-2 mb-4">
            <Code2 className="w-5 h-5 text-stone-400" />
            <h3 className="text-lg font-semibold text-stone-300">
              Ejemplo de código
            </h3>
          </div>
          <pre className="bg-stone-950/80 p-4 rounded-lg overflow-x-auto">
            <code className="text-sm text-stone-300 font-mono">
{`// Tu bot respondiendo a comandos slash
client.on('interactionCreate', async interaction => {
  if (interaction.commandName === 'hello') {
    await interaction.reply('¡Hola! 👋');
  }
  
  if (interaction.commandName === 'servidor') {
    await interaction.reply({
      embeds: [{
        title: '📊 Estadísticas del servidor',
        color: 0x5865F2,
        fields: [
          { name: 'Miembros', value: \`\${interaction.guild.memberCount}\` },
          { name: 'Creado', value: '<t:1234567890:R>' }
        ]
      }]
    });
  }
});`}
            </code>
          </pre>
        </div>

        {/* CTA Section */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-stone-600 via-purple-600 to-stone-700 p-12 text-center shadow-2xl shadow-indigo-500/20">
          <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
          <div className="relative">
            <h2 className="text-3xl font-bold text-white mb-4">
              Dale vida a tu servidor de Discord
            </h2>
            <p className="text-stone-100 mb-8 max-w-2xl mx-auto">
              Aprende a crear bots desde cero con JavaScript. Sin límites, sin pagos mensuales, 100% personalizado a tu gusto.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/course/discord-bot-intro"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-white text-stone-700 font-semibold hover:bg-amber-50 transition-all hover:scale-105 shadow-lg"
              >
                Comenzar ahora
              </a>
              <a
                href="/skill-tree-javascript"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-amber-800/50 backdrop-blur-sm text-white font-semibold hover:bg-amber-800/70 transition-all border border-white/20"
              >
                Ver roadmap JavaScript
              </a>
            </div>
          </div>
        </div>

        {/* Why Discord Bots */}
        <div className="mt-12 p-6 rounded-xl bg-gradient-to-r from-green-900/20 to-emerald-900/20 border border-green-700/30">
          <h3 className="text-lg font-semibold text-green-300 mb-4">
            💡 ¿Por qué crear un bot de Discord?
          </h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold text-white mb-2">Para servidores</h4>
              <ul className="space-y-1 text-sm text-stone-300">
                <li>• Automatiza moderación y gestión</li>
                <li>• Entretén a tu comunidad con juegos</li>
                <li>• Música y entretenimiento 24/7</li>
                <li>• Personalización total sin límites</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-2">Para aprender</h4>
              <ul className="space-y-1 text-sm text-stone-300">
                <li>• Práctica real de JavaScript/Node.js</li>
                <li>• Aprende APIs, bases de datos y async</li>
                <li>• Proyecto visible para tu portfolio</li>
                <li>• Posible fuente de ingresos (comisiones)</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Popular Bots Reference */}
        <div className="mt-12 p-6 rounded-xl bg-stone-900/40 border border-stone-900/20">
          <h3 className="text-lg font-semibold text-stone-300 mb-4">
            🚀 Inspiración: Bots populares
          </h3>
          <div className="grid md:grid-cols-4 gap-4 text-center">
            <div className="p-4">
              <div className="text-2xl mb-2">🎵</div>
              <h4 className="font-semibold text-white text-sm mb-1">MEE6</h4>
              <p className="text-xs text-stone-400">Moderación + Niveles</p>
            </div>
            <div className="p-4">
              <div className="text-2xl mb-2">🎮</div>
              <h4 className="font-semibold text-white text-sm mb-1">Mudae</h4>
              <p className="text-xs text-stone-400">Gacha de waifus</p>
            </div>
            <div className="p-4">
              <div className="text-2xl mb-2">🎶</div>
              <h4 className="font-semibold text-white text-sm mb-1">Groovy</h4>
              <p className="text-xs text-stone-400">Bot de música</p>
            </div>
            <div className="p-4">
              <div className="text-2xl mb-2">🤖</div>
              <h4 className="font-semibold text-white text-sm mb-1">Dyno</h4>
              <p className="text-xs text-stone-400">Auto-moderación</p>
            </div>
          </div>
          <p className="text-center text-sm text-stone-400 mt-4">
            Aprende a crear bots como estos (¡o mejores!) desde cero
          </p>
        </div>
      </main>
    </div>
  );
}
