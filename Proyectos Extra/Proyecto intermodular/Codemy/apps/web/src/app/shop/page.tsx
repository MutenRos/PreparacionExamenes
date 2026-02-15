'use client';

import { Navigation } from '@/components/Navigation';
import { Footer } from '@/components/Footer';
import { ArrowRight, Check, Star } from 'lucide-react';
import Link from 'next/link';

export default function ShopPage() {
  const skillTrees = [
    {
      id: 'python',
      name: 'Python & IA',
      icon: '🐍',
      description: 'Desde Python básico hasta Inteligencia Artificial avanzada con PyTorch, TensorFlow y LLMs',
      price: 49.99,
      courses: 15,
      lessons: 81,
      duration: '16-20 semanas',
      level: 'L0-L5',
      color: 'from-blue-600 to-blue-700',
      highlights: [
        'Python desde cero',
        'NumPy, Pandas, Matplotlib',
        'Machine Learning con Scikit-Learn',
        'Deep Learning: PyTorch y TensorFlow',
        'NLP y Computer Vision',
        'LLMs y GPT avanzado',
        'Proyectos reales de IA',
        'Certificado de finalización'
      ],
      popular: true
    },
    {
      id: 'web',
      name: 'Desarrollo Web Full-Stack',
      icon: '🌐',
      description: 'HTML, CSS, JavaScript, React, Next.js, Node.js y Express - De frontend a backend completo',
      price: 44.99,
      courses: 12,
      lessons: 79,
      duration: '14-18 semanas',
      level: 'L0-L4',
      color: 'from-green-600 to-green-700',
      highlights: [
        'HTML5 y CSS3 desde cero',
        'Flexbox, Grid y Responsive Design',
        'JavaScript moderno (ES6+)',
        'TypeScript profesional',
        'React.js y Next.js',
        'Node.js y Express.js',
        'Full-Stack Master',
        'Certificado de finalización'
      ],
      popular: true
    },
    {
      id: 'cpp',
      name: 'C++ Completo',
      icon: '⚙️',
      description: 'C++ desde fundamentos hasta programación avanzada, STL y optimización de sistemas',
      price: 29.99,
      courses: 6,
      lessons: 42,
      duration: '12-16 semanas',
      level: 'L1-L4',
      color: 'from-purple-600 to-purple-700',
      highlights: [
        'Fundamentos de C++',
        'Programación Orientada a Objetos',
        'Standard Template Library (STL)',
        'Gestión de memoria y punteros',
        'C++ avanzado y optimización',
        'Proyecto final master',
        'Certificado de finalización'
      ],
      popular: false
    },
    {
      id: 'java',
      name: 'Java & Spring Boot',
      icon: '☕',
      description: 'Java desde básico hasta desarrollo backend empresarial con Spring Boot',
      price: 34.99,
      courses: 6,
      lessons: 41,
      duration: '10-14 semanas',
      level: 'L1-L4',
      color: 'from-red-600 to-red-700',
      highlights: [
        'Java desde cero',
        'POO avanzada en Java',
        'Collections Framework',
        'Streams y funcional',
        'Spring Boot framework',
        'Java Master',
        'Certificado de finalización'
      ],
      popular: false
    },
    {
      id: 'devops',
      name: 'DevOps & Cloud',
      icon: '🚀',
      description: 'Git, Linux, Docker, Kubernetes, CI/CD y AWS Cloud - Infraestructura moderna',
      price: 39.99,
      courses: 7,
      lessons: 49,
      duration: '12-16 semanas',
      level: 'L2-L5',
      color: 'from-teal-600 to-teal-700',
      highlights: [
        'Git & GitHub avanzado',
        'Linux y línea de comandos',
        'Docker y contenedores',
        'Kubernetes orquestación',
        'CI/CD pipelines',
        'AWS Cloud',
        'DevOps Master'
      ],
      popular: false
    },
    {
      id: 'security',
      name: 'Seguridad & Hacking Ético',
      icon: '🛡️',
      description: 'Ciberseguridad, pentesting, redes seguras y criptografía aplicada',
      price: 34.99,
      courses: 6,
      lessons: 36,
      duration: '10-14 semanas',
      level: 'L2-L5',
      color: 'from-red-700 to-orange-700',
      highlights: [
        'Fundamentos de seguridad',
        'Network Security',
        'Web Security (OWASP)',
        'Penetration Testing',
        'Criptografía aplicada',
        'Security Master',
        'Certificado de finalización'
      ],
      popular: false
    },
    {
      id: 'mobile',
      name: 'Desarrollo Mobile',
      icon: '📱',
      description: 'React Native para crear apps iOS y Android nativas desde JavaScript',
      price: 34.99,
      courses: 6,
      lessons: 40,
      duration: '10-14 semanas',
      level: 'L2-L4',
      color: 'from-pink-600 to-pink-700',
      highlights: [
        'React Native desde cero',
        'Navegación en apps móviles',
        'Integración con APIs',
        'Módulos nativos',
        'Publicación en stores',
        'Mobile Master',
        'Certificado de finalización'
      ],
      popular: false
    },
    {
      id: 'arduino',
      name: 'Arduino & IoT',
      icon: '🔌',
      description: 'Electrónica, sensores, actuadores y proyectos IoT con Arduino',
      price: 29.99,
      courses: 6,
      lessons: 36,
      duration: '10-14 semanas',
      level: 'L1-L3',
      color: 'from-cyan-600 to-cyan-700',
      highlights: [
        'Arduino desde cero',
        'Sensores y medición',
        'Actuadores y control',
        'Conectividad WiFi',
        'Proyectos IoT',
        'Arduino Master',
        'Certificado de finalización'
      ],
      popular: false
    },
    {
      id: 'raspberry',
      name: 'Raspberry Pi Server',
      icon: '🥧',
      description: 'Crea tu propio servidor casero: web hosting, NAS, media server, VPN, Pi-hole y más',
      price: 14.99,
      courses: 1,
      lessons: 10,
      duration: '4-6 semanas',
      level: 'L2-L3',
      color: 'from-orange-600 to-orange-700',
      highlights: [
        'Configuración de Raspberry Pi OS',
        'Servidor web (Apache/Nginx)',
        'NAS - Tu nube personal',
        'Plex Media Server',
        'Pi-hole: Bloquea anuncios',
        'VPN casera con PiVPN',
        'Docker y contenedores',
        'Proyecto servidor completo'
      ],
      popular: false
    },
    {
      id: '3d',
      name: 'Diseño y Modelado 3D',
      icon: '🎨',
      description: 'Blender, modelado 3D, diseño paramétrico y preparación para impresión 3D',
      price: 24.99,
      courses: 4,
      lessons: 24,
      duration: '8-10 semanas',
      level: 'L1-L3',
      color: 'from-violet-600 to-violet-700',
      highlights: [
        'Introducción a Blender',
        'Modelado 3D básico',
        'Diseño paramétrico',
        'Preparación para impresión 3D',
        'Proyectos reales',
        'Certificado de finalización'
      ],
      popular: false
    }
  ];

  return (
    <main className="min-h-screen bg-stone-900">
      <Navigation />
      
      <div className="pt-24 pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
              Catálogo de{' '}
              <span className="bg-gradient-to-r from-amber-500 to-orange-500 bg-clip-text text-transparent">
                Skill Trees
              </span>
            </h1>
            <p className="text-xl text-stone-400 max-w-3xl mx-auto">
              Compra acceso permanente a los árboles de habilidades. Pago único, sin suscripciones.
            </p>
          </div>

          {/* Skill Trees Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
            {skillTrees.map((tree) => (
              <div 
                key={tree.id}
                className={`bg-stone-800/50 backdrop-blur-sm rounded-2xl border-2 ${
                  tree.popular ? 'border-amber-600' : 'border-stone-700'
                } p-8 hover:border-amber-600/50 transition-all relative`}
              >
                {tree.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <div className="bg-gradient-to-r from-amber-600 to-orange-600 text-white text-sm font-bold px-4 py-1 rounded-full flex items-center space-x-1">
                      <Star className="w-4 h-4 fill-current" />
                      <span>MÁS POPULAR</span>
                    </div>
                  </div>
                )}

                {/* Icon & Title */}
                <div className="text-center mb-6">
                  <div className="text-6xl mb-4">{tree.icon}</div>
                  <h3 className="text-2xl font-bold text-white mb-2">{tree.name}</h3>
                  <p className="text-stone-400 text-sm">{tree.description}</p>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-4 mb-6 py-6 border-y border-stone-700">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-white">{tree.courses}</div>
                    <div className="text-xs text-stone-400">Cursos</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-white">{tree.lessons}</div>
                    <div className="text-xs text-stone-400">Lecciones</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-white">{tree.level}</div>
                    <div className="text-xs text-stone-400">Nivel</div>
                  </div>
                </div>

                {/* Highlights */}
                <ul className="space-y-2 mb-8">
                  {tree.highlights.map((highlight, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                      <span className="text-stone-300 text-sm">{highlight}</span>
                    </li>
                  ))}
                </ul>

                {/* Price & CTA */}
                <div className="border-t border-stone-700 pt-6">
                  <div className="flex items-baseline justify-between mb-4">
                    <div>
                      <span className="text-4xl font-bold text-white">€{tree.price}</span>
                      <span className="text-stone-400 text-sm ml-2">una vez</span>
                    </div>
                  </div>
                  <div className="text-stone-400 text-xs mb-4">
                    🕐 {tree.duration} de contenido
                  </div>
                  <Link
                    href={`/checkout?product=${tree.id}`}
                    className={`w-full py-4 px-6 rounded-full font-bold transition-all duration-200 flex items-center justify-center space-x-2 ${
                      tree.popular
                        ? 'bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 text-white shadow-lg'
                        : 'bg-stone-700 hover:bg-stone-600 text-white'
                    }`}
                  >
                    <span>Comprar Acceso</span>
                    <ArrowRight className="w-5 h-5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>

          {/* Bundle Offer */}
          <div className="bg-gradient-to-r from-amber-900/20 to-orange-900/20 border-2 border-amber-600/50 rounded-2xl p-8 text-center">
            <h3 className="text-3xl font-bold text-white mb-4">
              💎 Pack Completo: Todos los Skill Trees
            </h3>
            <p className="text-stone-300 mb-6">
              Ahorra comprando los 10 árboles juntos - Acceso total y permanente
            </p>
            <div className="flex items-center justify-center gap-4 mb-6">
              <span className="text-2xl text-stone-400 line-through">€337.89</span>
              <span className="text-5xl font-bold text-white">€249.99</span>
              <span className="bg-green-600 text-white px-3 py-1 rounded-full text-sm font-bold">
                Ahorra €87
              </span>
            </div>
                        <Link
              href="/checkout?product=pack"
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-4 px-8 rounded-xl transition-all shadow-lg flex items-center space-x-2"
            >
              <span>Comprar Pack Completo</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <p className="text-stone-400 text-sm mt-4">
              O suscríbete al Plan Pro por €9.99/mes y accede a todo + futuras actualizaciones
            </p>
          </div>

          {/* FAQ */}
          <div className="mt-16 text-center">
            <h3 className="text-2xl font-bold text-white mb-6">Preguntas Frecuentes</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
              <div className="bg-stone-800/50 rounded-xl p-6 text-left">
                <h4 className="font-bold text-white mb-2">¿Es pago único?</h4>
                <p className="text-stone-400 text-sm">
                  Sí, pagas una sola vez y tienes acceso de por vida al contenido.
                </p>
              </div>
              <div className="bg-stone-800/50 rounded-xl p-6 text-left">
                <h4 className="font-bold text-white mb-2">¿Puedo cambiar al plan Pro después?</h4>
                <p className="text-stone-400 text-sm">
                  Sí, y te descontaremos el valor de los árboles que ya compraste.
                </p>
              </div>
              <div className="bg-stone-800/50 rounded-xl p-6 text-left">
                <h4 className="font-bold text-white mb-2">¿Hay actualizaciones incluidas?</h4>
                <p className="text-stone-400 text-sm">
                  Sí, todas las actualizaciones futuras del árbol están incluidas.
                </p>
              </div>
              <div className="bg-stone-800/50 rounded-xl p-6 text-left">
                <h4 className="font-bold text-white mb-2">¿Necesito suscripción Pro?</h4>
                <p className="text-stone-400 text-sm">
                  No, los árboles individuales no requieren suscripción mensual.
                </p>
              </div>
            </div>
          </div>

          {/* CTA Alternative */}
          <div className="mt-16 text-center">
            <p className="text-stone-400 mb-4">
              ¿Prefieres acceso completo con suscripción?
            </p>
            <Link
              href="/#pricing"
              className="inline-flex items-center space-x-2 text-amber-500 hover:text-amber-400 font-semibold"
            >
              <span>Ver planes de suscripción</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>

      <Footer />
    </main>
  );
}
