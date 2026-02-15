'use client'

import { Target, Gamepad2, Shield, Users, BookOpen, Trophy, ArrowRight } from 'lucide-react'

export function Features() {
  const features = [
    {
      icon: Target,
      title: 'Autocorrección Inteligente',
      description: 'Feedback inmediato y específico en cada ejercicio con análisis de errores comunes.',
      color: 'from-stone-600 to-stone-700'
    },
    {
      icon: Gamepad2,
      title: 'Gamificación Profunda',
      description: '30+ logros únicos, sistema XP/nivel, racha diaria, proyectos finales y perfil personalizado.',
      color: 'from-stone-600 to-stone-700'
    },
    {
      icon: Shield,
      title: 'Ejecución Segura',
      description: 'Sandboxing Docker con límites estrictos de tiempo, memoria y red.',
      color: 'from-green-600 to-green-700'
    },
    {
      icon: Users,
      title: 'Panel Parental',
      description: 'Control tiempo real, límites de sesión y reportes automáticos del progreso.',
      color: 'from-orange-600 to-orange-700'
    },
    {
      icon: BookOpen,
      title: '14+ Cursos Completos',
      description: '90+ lecciones interactivas con 300+ ejercicios autocorregibles. Desde Python hasta desarrollo web.',
      color: 'from-teal-600 to-teal-700'
    },
    {
      icon: Trophy,
      title: '30+ Proyectos Prácticos',
      description: 'Desde calculadoras hasta sistemas web completos. Cada curso termina con un proyecto real.',
      color: 'from-amber-600 to-amber-700'
    }
  ]

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Tecnología de{' '}
            <span className="bg-gradient-to-r from-stone-600 to-amber-600 bg-clip-text text-transparent">
              Última Generación
            </span>
          </h2>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto leading-relaxed">
            MVP AAA diseñado para escalar desde 100 a 100,000 usuarios con la misma arquitectura. 
            Cada característica está pensada para la excelencia educativa.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const IconComponent = feature.icon
            return (
              <div 
                key={index}
                className="group relative bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-gray-100 hover:border-stone-500/30 transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
              >
                {/* Icon */}
                <div className={`inline-flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-r ${feature.color} mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <IconComponent className="w-7 h-7 text-white" />
                </div>

                {/* Content */}
                <h3 className="text-xl font-bold text-white mb-3 group-hover:text-stone-600 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-stone-300 leading-relaxed mb-4">
                  {feature.description}
                </p>

                {/* Hover Arrow */}
                <div className="flex items-center text-stone-600 font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <span className="text-sm mr-2">Saber más</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </div>

                {/* Background decoration */}
                <div className={`absolute top-0 right-0 w-20 h-20 bg-gradient-to-br ${feature.color} opacity-5 rounded-full translate-x-10 -translate-y-10 group-hover:scale-150 transition-transform duration-500`} />
              </div>
            )
          })}
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-stone-50 to-stone-50 border border-stone-200/20 rounded-full px-6 py-3 mb-6">
            <div className="w-2 h-2 bg-stone-600 rounded-full animate-pulse" />
            <span className="text-sm font-medium text-stone-800">Arquitectura escalable desde el día 1</span>
          </div>
          
          <h3 className="text-2xl font-bold text-white mb-4">
            ¿Listo para revolucionar la educación en programación?
          </h3>
          <p className="text-lg text-stone-300 mb-8 max-w-2xl mx-auto">
            Únete a la beta y ayúdanos a construir el futuro de la programación educativa.
          </p>
          
          <button className="bg-gradient-to-r from-stone-600 to-amber-600 text-white px-8 py-4 rounded-full hover:from-stone-700 hover:to-stone-700 transition-all duration-200 font-semibold shadow-lg hover:shadow-xl flex items-center space-x-2 mx-auto">
            <span>Acceder a Beta</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </section>
  )
}