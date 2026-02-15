'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { Menu, X, Code2, Zap, Users, Star, User, LogOut, Target, Video } from 'lucide-react'

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false)
  const [userName, setUserName] = useState<string | null>(null)
  const [userEmail, setUserEmail] = useState<string | null>(null)

  useEffect(() => {
    // Verificar sesión del usuario
    async function checkSession() {
      try {
        const response = await fetch('/api/auth/session')
        const data = await response.json()
        
        if (data.user) {
          setUserEmail(data.user.email)
          setUserName(data.user.email?.split('@')[0] || 'Usuario')
        }
      } catch (error) {
        console.error('Error checking session:', error)
      }
    }
    
    checkSession()
  }, [])

  const handleLogout = async () => {
    if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
      // Llamar a logout en el servidor
      await fetch('/api/auth/logout', { method: 'POST' })
      
      // Limpiar localStorage
      localStorage.clear()
      
      // Redirigir
      window.location.href = '/auth/login'
    }
  }

  return (
    <nav className="fixed top-0 w-full bg-stone-900/95 backdrop-blur-md border-b-2 border-stone-800 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-amber-700 border-2 border-amber-800 flex items-center justify-center">
              <Code2 className="w-5 h-5 text-stone-100" />
            </div>
            <span className="text-xl font-bold text-stone-100">
              Code Dungeon
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/courses" className="text-stone-300 hover:text-stone-100 transition-colors">
              Cursos
            </Link>
            <Link href="/challenges" className="text-stone-300 hover:text-stone-100 transition-colors flex items-center gap-2">
              <Target className="w-4 h-4" />
              Retos
            </Link>
            <Link href="/seminars" className="text-stone-300 hover:text-stone-100 transition-colors flex items-center gap-2">
              <Video className="w-4 h-4" />
              Seminarios
            </Link>
            <Link href="/social" className="text-stone-300 hover:text-stone-100 transition-colors flex items-center gap-2">
              <Users className="w-4 h-4" />
              Social
            </Link>
            <Link href="/playground" className="text-stone-300 hover:text-stone-100 transition-colors">
              Playground
            </Link>
            <Link href="/leaderboard" className="text-stone-300 hover:text-stone-100 transition-colors">
              Ranking
            </Link>
            {userEmail === 'admin@codedungeon.es' && (
              <Link href="/admin" className="text-amber-400 hover:text-amber-300 transition-colors font-semibold">
                Admin
              </Link>
            )}
            <Link href="#pricing" className="text-stone-200 hover:text-stone-400 transition-colors">
              Precios
            </Link>
          </div>

          {/* CTA Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {userName ? (
              <>
                <Link 
                  href="/profile" 
                  className="flex items-center gap-2 text-stone-200 hover:text-stone-400 transition-colors font-medium"
                >
                  <User className="w-4 h-4" />
                  <span>{userName}</span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-2 text-stone-200 hover:text-red-400 transition-colors font-medium"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </>
            ) : (
              <>
                <Link 
                  href="/auth/login" 
                  className="text-stone-200 hover:text-stone-400 transition-colors font-medium"
                >
                  Iniciar Sesión
                </Link>
                <Link 
                  href="/auth/register" 
                  className="bg-gradient-to-r from-stone-600 to-amber-600 text-white px-6 py-2 rounded-full hover:from-stone-700 hover:to-amber-700 transition-all duration-200 font-medium shadow-lg"
                >
                  Empezar Gratis
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-slate-800 transition-colors"
          >
            {isOpen ? (
              <X className="w-6 h-6 text-stone-200" />
            ) : (
              <Menu className="w-6 h-6 text-stone-200" />
            )}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden py-4 border-t border-stone-500/20">
            <div className="flex flex-col space-y-4">
              <Link href="/courses" className="text-stone-200 hover:text-stone-400 transition-colors py-2">
                Cursos
              </Link>
              <Link href="/social" className="text-stone-200 hover:text-stone-400 transition-colors py-2 flex items-center gap-2">
                <Users className="w-4 h-4" />
                Social
              </Link>
              <Link href="/challenges" className="text-stone-200 hover:text-stone-400 transition-colors py-2 flex items-center gap-2">
                <Target className="w-4 h-4" />
                Retos
              </Link>
              <Link href="/seminars" className="text-stone-200 hover:text-stone-400 transition-colors py-2 flex items-center gap-2">
                <Video className="w-4 h-4" />
                Seminarios
              </Link>
              <Link href="/social" className="text-stone-200 hover:text-stone-400 transition-colors py-2 flex items-center gap-2">
                <Users className="w-4 h-4" />
                Social
              </Link>
              <Link href="/playground" className="text-stone-200 hover:text-stone-400 transition-colors py-2">
                Playground
              </Link>
              <Link href="/leaderboard" className="text-stone-200 hover:text-stone-400 transition-colors py-2">
                Ranking
              </Link>
              <Link href="#pricing" className="text-stone-200 hover:text-stone-400 transition-colors py-2">
                Precios
              </Link>
              <div className="flex flex-col space-y-2 pt-4 border-t border-stone-500/20">
                {userName ? (
                  <>
                    <Link 
                      href="/profile" 
                      className="flex items-center gap-2 text-stone-200 hover:text-stone-400 transition-colors py-2"
                    >
                      <User className="w-4 h-4" />
                      <span>{userName}</span>
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="flex items-center gap-2 text-stone-200 hover:text-red-400 transition-colors py-2 text-left"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Cerrar Sesión</span>
                    </button>
                  </>
                ) : (
                  <>
                    <Link 
                      href="/auth/login" 
                      className="text-stone-200 hover:text-stone-400 transition-colors py-2"
                    >
                      Iniciar Sesión
                    </Link>
                    <Link 
                      href="/auth/register" 
                      className="bg-gradient-to-r from-stone-600 to-amber-600 text-white px-6 py-3 rounded-full hover:from-stone-700 hover:to-amber-700 transition-all duration-200 font-medium text-center shadow-lg"
                    >
                      Empezar Gratis
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}