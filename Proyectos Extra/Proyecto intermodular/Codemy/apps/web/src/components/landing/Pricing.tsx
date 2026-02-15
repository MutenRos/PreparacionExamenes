'use client'

import { useState } from 'react'
import { Check, Star, Users, Crown, ArrowRight, Sparkles } from 'lucide-react'
import Link from 'next/link'

export function Pricing() {
  const [isYearly, setIsYearly] = useState(false)

  const plans = [
    {
      id: 'starter',
      name: 'Starter',
      description: 'Perfecto para empezar tu aventura en programación',
      priceMonthly: 4.99,
      priceYearly: 49,
      icon: Star,
      color: 'from-stone-600 to-stone-700',
      features: [
        'Acceso a 1 track (Web, Datos o Juegos)',
        'Retos semanales',
        'Sistema XP y ranking básico',
        'Certificados internos por módulo',
        'Soporte por email',
        'Progreso detallado',
        'Autocorrección básica'
      ],
      popular: false
    },
    {
      id: 'pro',
      name: 'Pro',
      description: 'Para estudiantes serios que quieren dominar la programación',
      priceMonthly: 9.99,
      priceYearly: 99,
      icon: Crown,
      color: 'from-stone-600 to-stone-700',
      features: [
        'Acceso a TODOS los tracks',
        'Proyectos guiados avanzados',
        'Autocorrección avanzada con IA',
        'Ranking global y competencias',
        'Plantillas y boilerplates',
        'Mentoría grupal (2 sesiones/mes)',
        'Certificados oficiales verificables',
        'Soporte prioritario',
        'API para integraciones'
      ],
      popular: true
    },
    {
      id: 'family',
      name: 'Pro Familia',
      description: 'Ideal para familias con múltiples estudiantes',
      priceMonthly: 19.99,
      priceYearly: 199,
      icon: Users,
      color: 'from-green-600 to-green-700',
      features: [
        'Hasta 3 perfiles (infantiles/teens)',
        'Panel parental completo',
        'Control de tiempo de sesión',
        'Reportes automáticos',
        'Alertas de progreso',
        'Todos los beneficios Pro',
        'Gestión familiar centralizada',
        'Descuentos en eventos'
      ],
      popular: false
    }
  ]

  const addOns = [
    {
      name: 'Python & IA',
      description: '15 cursos completos: desde básico hasta LLMs (81 lecciones)',
      price: 49.99,
      icon: '🐍',
      lessons: 81,
      courses: 15
    },
    {
      name: 'C++ Completo',
      description: '6 cursos: fundamentos hasta programación avanzada (42 lecciones)',
      price: 29.99,
      icon: '⚙️',
      lessons: 42,
      courses: 6
    },
    {
      name: 'Raspberry Pi Server',
      description: 'Monta tu propio servidor casero: NAS, VPN, media server (10 lecciones)',
      price: 14.99,
      icon: '🥧',
      lessons: 10,
      courses: 1
    }
  ]

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Precios{' '}
            <span className="bg-gradient-to-r from-stone-600 to-amber-600 bg-clip-text text-transparent">
              Transparentes
            </span>
          </h2>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto leading-relaxed mb-8">
            Desde curso gratuito hasta mentorías 1:1. Sin permanencia, cancela cuando quieras.
          </p>

          {/* Toggle */}
          <div className="inline-flex items-center bg-gray-100 rounded-full p-1 mb-8">
            <button
              onClick={() => setIsYearly(false)}
              className={`px-6 py-2 rounded-full font-medium transition-all duration-200 ${
                !isYearly
                  ? 'bg-slate-800/50 backdrop-blur-sm text-white shadow-sm'
                  : 'text-stone-300 hover:text-white'
              }`}
            >
              Mensual
            </button>
            <button
              onClick={() => setIsYearly(true)}
              className={`px-6 py-2 rounded-full font-medium transition-all duration-200 relative ${
                isYearly
                  ? 'bg-slate-800/50 backdrop-blur-sm text-white shadow-sm'
                  : 'text-stone-300 hover:text-white'
              }`}
            >
              Anual
              <span className="absolute -top-2 -right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full">
                -25%
              </span>
            </button>
          </div>
        </div>

        {/* Free Tier */}
        <div className="mb-12">
          <div className="bg-gradient-to-br from-stone-50 to-stone-50 rounded-2xl border-2 border-stone-200/20 p-8 text-center">
            <div className="flex items-center justify-center mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-stone-600 to-amber-600 rounded-full flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">Curso Gratuito</h3>
            <p className="text-lg text-stone-300 mb-6">
              Introducción completa: prepara tu equipo, prueba 3 lenguajes y elige tu especialización
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-4">
                <div className="text-2xl font-bold text-stone-600">6</div>
                <div className="text-sm text-stone-300">Lecciones completas</div>
              </div>
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-4">
                <div className="text-2xl font-bold text-stone-600">3</div>
                <div className="text-sm text-stone-300">Lenguajes (Python, JS, C#)</div>
              </div>
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-4">
                <div className="text-2xl font-bold text-green-600">∞</div>
                <div className="text-sm text-stone-300">Tiempo sin límites</div>
              </div>
            </div>
            <button className="bg-gradient-to-r from-stone-600 to-amber-600 text-white px-8 py-3 rounded-full hover:from-stone-700 hover:to-stone-700 transition-all duration-200 font-semibold">
              Empezar Gratis
            </button>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
          {plans.map((plan) => {
            const IconComponent = plan.icon
            const price = isYearly ? plan.priceYearly : plan.priceMonthly
            const monthlyPrice = isYearly ? (plan.priceYearly / 12) : plan.priceMonthly

            return (
              <div
                key={plan.id}
                className={`relative bg-slate-800/50 backdrop-blur-sm rounded-2xl border-2 p-8 transition-all duration-300 hover:shadow-xl ${
                  plan.popular
                    ? 'border-stone-200 shadow-lg scale-105'
                    : 'border-stone-500/30 hover:border-gray-300'
                }`}
              >
                {/* Popular Badge */}
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <div className="bg-gradient-to-r from-stone-600 to-amber-600 text-white px-6 py-2 rounded-full text-sm font-bold">
                      MÁS POPULAR
                    </div>
                  </div>
                )}

                {/* Icon */}
                <div className={`inline-flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-r ${plan.color} mb-6`}>
                  <IconComponent className="w-7 h-7 text-white" />
                </div>

                {/* Plan Details */}
                <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                <p className="text-stone-300 mb-6">{plan.description}</p>

                {/* Price */}
                <div className="mb-6">
                  <div className="flex items-baseline space-x-1">
                    <span className="text-4xl font-bold text-white">€{monthlyPrice.toFixed(0)}</span>
                    <span className="text-stone-300">/mes</span>
                  </div>
                  {isYearly && (
                    <div className="text-sm text-stone-400 mt-1">
                      €{price} facturados anualmente
                    </div>
                  )}
                </div>

                {/* Features */}
                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-start space-x-3">
                      <Check className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                      <span className="text-stone-200">{feature}</span>
                    </li>
                  ))}
                </ul>

                {/* CTA Button */}
                <Link
                  href={`/checkout?plan=${plan.id}&billing=${isYearly ? 'yearly' : 'monthly'}`}
                  className={`w-full py-3 px-6 rounded-full font-semibold transition-all duration-200 flex items-center justify-center ${
                    plan.popular
                      ? 'bg-gradient-to-r from-stone-600 to-amber-600 text-white hover:from-stone-700 hover:to-amber-700 shadow-lg'
                      : 'bg-gray-900 text-white hover:bg-gray-800'
                  }`}
                >
                  {plan.popular ? 'Empezar Pro' : `Elegir ${plan.name}`}
                </Link>
              </div>
            )
          })}
        </div>

        {/* Add-ons */}
        <div className="bg-gradient-to-br from-gray-50 to-white rounded-2xl border border-stone-500/30 p-8">
          <h3 className="text-2xl font-bold text-white mb-2 text-center">
            O compra árboles individuales
          </h3>
          <p className="text-stone-300 text-center mb-8">
            Acceso de por vida al contenido. Pago único, sin suscripciones.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {addOns.map((addon, index) => (
              <div key={index} className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-stone-500/30 hover:border-amber-600/50 hover:shadow-lg transition-all">
                <div className="text-4xl mb-3">{addon.icon}</div>
                <h4 className="text-xl font-bold text-white mb-2">{addon.name}</h4>
                <p className="text-stone-300 text-sm mb-4">{addon.description}</p>
                
                <div className="flex items-center gap-4 mb-4 text-sm text-stone-400">
                  <span>📚 {addon.courses} {addon.courses === 1 ? 'curso' : 'cursos'}</span>
                  <span>🎓 {addon.lessons} lecciones</span>
                </div>
                
                <div className="border-t border-stone-500/30 pt-4 mt-4">
                  <div className="flex items-baseline justify-between mb-4">
                    <span className="text-3xl font-bold text-white">€{addon.price}</span>
                    <span className="text-stone-400 text-sm">pago único</span>
                  </div>
                  <button className="w-full bg-gradient-to-r from-stone-600 to-amber-600 hover:from-stone-700 hover:to-amber-700 text-white font-semibold py-3 px-6 rounded-full transition-all duration-200 shadow-lg flex items-center justify-center space-x-2">
                    <span>Comprar Árbol</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-8 text-center space-y-4">
            <Link 
              href="/shop"
              className="inline-flex items-center space-x-2 bg-white hover:bg-gray-50 text-stone-800 font-semibold py-3 px-8 rounded-full border-2 border-stone-200 transition-all duration-200 shadow-sm hover:shadow-md"
            >
              <span>Ver todos los árboles disponibles</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <p className="text-stone-400 text-sm">
              💡 <strong className="text-white">Tip:</strong> El plan Pro incluye todos los árboles + actualizaciones futuras por solo €9.99/mes
            </p>
          </div>
        </div>

        {/* FAQ Link */}
        <div className="text-center mt-12">
          <p className="text-stone-300 mb-4">
            ¿Tienes dudas sobre los planes? 
          </p>
          <button className="text-stone-600 hover:text-stone-700 font-medium flex items-center space-x-2 mx-auto">
            <span>Ver preguntas frecuentes</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </section>
  )
}