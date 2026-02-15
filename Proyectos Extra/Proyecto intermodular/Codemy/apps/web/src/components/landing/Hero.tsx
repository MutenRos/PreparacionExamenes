'use client'

import { useState } from 'react'
import { ArrowRight, PlayCircle, Github, Star, Users, Code2 } from 'lucide-react'
import Link from 'next/link'

export function Hero() {
  const [email, setEmail] = useState('')

  return (
    <section className="relative pt-32 pb-20 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-stone-900" />
      <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-[800px] h-[800px] bg-amber-900/5 rounded-full blur-3xl" />
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Main Headline */}
          <h1 className="text-5xl md:text-7xl font-bold text-stone-100 mb-6 leading-tight">
            Aprende{' '}
            <span className="text-amber-500">
              Programación
            </span>
            <br />
            de forma divertida
          </h1>

          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-stone-400 mb-12 max-w-4xl mx-auto leading-relaxed">
            <strong className="text-white">22 cursos completos</strong> con <strong className="text-white">133+ lecciones</strong> en Python, C++ y Raspberry Pi.
            Desde <strong className="text-white">fundamentos</strong> hasta <strong className="text-white">IA Avanzada</strong> con PyTorch, TensorFlow y LLMs.
          </p>

          {/* Stats */}
          <div className="flex flex-wrap justify-center items-center gap-8 mb-12">
            <div className="flex items-center space-x-2">
              <Code2 className="w-5 h-5 text-amber-600" />
              <span className="text-sm font-medium text-stone-400">133+ lecciones</span>
            </div>
            <div className="flex items-center space-x-2">
              <Star className="w-5 h-5 text-amber-600" />
              <span className="text-sm font-medium text-stone-400">22 cursos</span>
            </div>
            <div className="flex items-center space-x-2">
              <Users className="w-5 h-5 text-amber-600" />
              <span className="text-sm font-medium text-stone-400">15 tracks IA</span>
            </div>
            <div className="flex items-center space-x-2">
              <Star className="w-5 h-5 text-amber-600 fill-current" />
              <span className="text-sm font-medium text-stone-400">100+ horas</span>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 mb-16">
            <Link
              href="/auth/register"
              className="group bg-amber-700 text-stone-100 px-8 py-4 hover:bg-amber-600 transition-all duration-200 font-semibold shadow-2xl border-2 border-amber-800 flex items-center space-x-2"
            >
              <span>Empezar Gratis</span>
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            
            <Link
              href="/auth/login"
              className="flex items-center space-x-2 text-stone-300 hover:text-stone-100 transition-colors px-8 py-4 font-semibold border-2 border-stone-700 hover:border-stone-600"
            >
              <span>Iniciar Sesión</span>
            </Link>
          </div>

          {/* Email Signup */}
          <div className="max-w-md mx-auto">
            <form className="flex flex-col sm:flex-row gap-2">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="tu@email.com"
                className="flex-1 px-4 py-3 bg-stone-800 border-2 border-stone-700 focus:border-amber-700 focus:ring-2 focus:ring-amber-900/20 outline-none transition-all text-stone-100 placeholder-stone-500"
              />
              <button
                type="submit"
                className="bg-stone-700 text-stone-100 px-6 py-3 hover:bg-stone-600 transition-colors font-semibold border-2 border-stone-600"
              >
                Notificarme
              </button>
            </form>
            <p className="text-sm text-stone-500 mt-2">
              Acceso anticipado al curso gratuito de introducción
            </p>
          </div>
        </div>

        {/* Hero Image/Demo */}
        <div className="mt-20">
          <div className="relative max-w-5xl mx-auto">
            <div className="bg-stone-800 shadow-2xl border-2 border-stone-700 overflow-hidden">
              {/* Browser Bar */}
              <div className="bg-stone-950 px-4 py-3 flex items-center space-x-2 border-b-2 border-stone-700">
                <div className="flex space-x-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                </div>
                <div className="flex-1 text-center">
                  <div className="bg-stone-800 px-3 py-1 text-sm text-stone-400">
                    codedungeon.es
                  </div>
                </div>
              </div>
              
              {/* Dashboard Preview */}
              <div className="bg-stone-900 p-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {/* Progress Card */}
                  <div className="bg-stone-800 p-6 shadow-lg border-2 border-stone-700">
                    <h3 className="font-semibold text-stone-100 mb-2">Tu Progreso</h3>
                    <div className="flex items-center space-x-2 mb-3">
                      <div className="flex-1 bg-stone-700 h-2">
                        <div className="bg-amber-600 h-2 w-3/4"></div>
                      </div>
                      <span className="text-sm font-medium text-stone-400">75%</span>
                    </div>
                    <p className="text-sm text-stone-500">Python Básico - Nivel 2</p>
                  </div>

                  {/* XP Card */}
                  <div className="bg-stone-800 p-6 shadow-lg border-2 border-stone-700">
                    <h3 className="font-semibold text-stone-100 mb-2">Experiencia</h3>
                    <div className="flex items-center space-x-2">
                      <Star className="w-5 h-5 text-amber-600 fill-current" />
                      <span className="text-2xl font-bold text-stone-100">1,250</span>
                      <span className="text-sm text-stone-400">XP</span>
                    </div>
                    <p className="text-sm text-stone-500 mt-1">Nivel 3 - Intermedio</p>
                  </div>

                  {/* Streak Card */}
                  <div className="bg-stone-800 p-6 shadow-lg border-2 border-stone-700">
                    <h3 className="font-semibold text-stone-100 mb-2">Racha</h3>
                    <div className="flex items-center space-x-2">
                      <div className="w-5 h-5 bg-amber-600"></div>
                      <span className="text-2xl font-bold text-stone-100">7</span>
                      <span className="text-sm text-stone-400">días</span>
                    </div>
                    <p className="text-sm text-stone-500 mt-1">¡Sigue así!</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Floating Elements */}
            <div className="absolute -top-4 -left-4 w-20 h-20 bg-white/10 rounded-full opacity-20 animate-pulse"></div>
            <div className="absolute -bottom-4 -right-4 w-16 h-16 bg-white/10 rounded-full opacity-20 animate-pulse delay-1000"></div>
          </div>
        </div>
      </div>
    </section>
  )
}