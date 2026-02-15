'use client'

import { ArrowRight, Rocket, Star, Users } from 'lucide-react'

export function CTA() {
  return (
    <section className="py-20 bg-stone-800 border-y-2 border-stone-700 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-stone-800" />
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-white/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-white/10 rounded-full blur-3xl" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center text-white">
          {/* Badge */}
          <div className="inline-flex items-center space-x-2 bg-white/20 backdrop-blur-sm border border-white/20 rounded-full px-6 py-3 mb-8">
            <Rocket className="w-5 h-5" />
            <span className="font-medium">Beta Exclusiva</span>
            <Star className="w-4 h-4 fill-current" />
          </div>

          {/* Main Headline */}
          <h2 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            Únete a la Revolución
            <br />
            <span className="text-yellow-300">Educativa</span>
          </h2>

          {/* Description */}
          <p className="text-xl md:text-2xl text-white/90 mb-12 max-w-4xl mx-auto leading-relaxed">
            Sé parte de los primeros 1,000 usuarios en experimentar la academia de programación 
            más avanzada del mundo. <strong>Acceso gratuito de por vida</strong> al curso de introducción.
          </p>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
              <div className="text-3xl font-bold text-yellow-300 mb-2">500+</div>
              <div className="text-white/80">Usuarios Beta</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
              <div className="text-3xl font-bold text-yellow-300 mb-2">15%</div>
              <div className="text-white/80">Conversión Free→Pro</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
              <div className="text-3xl font-bold text-yellow-300 mb-2">NPS 9.2</div>
              <div className="text-white/80">Satisfacción</div>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row justify-center items-center gap-6 mb-16">
            <button className="group bg-amber-700 text-stone-100 px-12 py-4 hover:bg-amber-600 transition-all duration-200 font-bold text-lg shadow-xl border-2 border-amber-800 flex items-center space-x-3">
              <span>Empezar Ahora</span>
              <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
            </button>
            
            <button className="flex items-center space-x-2 text-white/90 hover:text-white transition-colors px-8 py-4 font-semibold border border-white/20 rounded-full hover:bg-white/10">
              <Users className="w-5 h-5" />
              <span>Unirse a Discord</span>
            </button>
          </div>

          {/* Social Proof */}
          <div className="max-w-4xl mx-auto">
            <p className="text-white/70 text-lg mb-8">
              Únete a desarrolladores de empresas como:
            </p>
            
            <div className="flex flex-wrap justify-center items-center gap-8 opacity-70">
              {/* Mock company logos - replace with actual logos */}
              <div className="bg-white/20 rounded-lg px-6 py-3 font-bold text-white">
                Google
              </div>
              <div className="bg-white/20 rounded-lg px-6 py-3 font-bold text-white">
                Microsoft
              </div>
              <div className="bg-white/20 rounded-lg px-6 py-3 font-bold text-white">
                Meta
              </div>
              <div className="bg-white/20 rounded-lg px-6 py-3 font-bold text-white">
                Netflix
              </div>
              <div className="bg-white/20 rounded-lg px-6 py-3 font-bold text-white">
                Spotify
              </div>
            </div>
          </div>

          {/* Guarantee */}
          <div className="mt-16 max-w-2xl mx-auto">
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
              <h3 className="text-xl font-bold mb-4">Garantía de 30 días</h3>
              <p className="text-white/90 leading-relaxed">
                Si no estás 100% satisfecho con tu experiencia en los primeros 30 días, 
                te devolvemos todo tu dinero sin preguntas.
              </p>
            </div>
          </div>

          {/* Bottom text */}
          <p className="text-white/60 text-sm mt-8">
            No se requiere tarjeta de crédito • Cancela cuando quieras • Datos seguros
          </p>
        </div>
      </div>
    </section>
  )
}