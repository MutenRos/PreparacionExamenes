'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Mail, CheckCircle } from 'lucide-react';
import { createClient } from '@supabase/supabase-js';

// Crear cliente de Supabase en el lado del cliente
const getSupabaseClient = () => {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  
  if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error('Las credenciales de Supabase no están configuradas. Verifica tu archivo .env.local');
  }
  
  return createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: true
    }
  });
};

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'student', // student, parent, teacher
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [registered, setRegistered] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

    const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    if (formData.password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const supabase = getSupabaseClient();
      
      const { data, error: signUpError } = await supabase.auth.signUp({
        email: formData.email,
        password: formData.password,
        options: {
          data: {
            name: formData.name,
            role: formData.role
          },
          emailRedirectTo: `${window.location.origin}/auth/callback`
        }
      });
      
      if (signUpError) {
        console.error('Supabase signUp error:', signUpError);
        throw signUpError;
      }
      
      console.log('Usuario registrado exitosamente:', data);

      // Intentar asignar status de pionero si hay slots disponibles
      if (data.user) {
        try {
          const pioneerResponse = await fetch('/api/auth/assign-pioneer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId: data.user.id })
          });

          const pioneerData = await pioneerResponse.json();
          
          if (pioneerData.isPioneer) {
            console.log(`🎉 ¡Usuario pionero #${pioneerData.pioneerNumber} asignado!`);
          }
        } catch (pioneerError) {
          // No fallar el registro si la asignación de pionero falla
          console.warn('No se pudo verificar status de pionero:', pioneerError);
        }
      }
      
      setRegistered(true);
    } catch (err) {
      console.error('Error completo:', err);
      const errorMessage = err instanceof Error ? err.message : 'Error al crear la cuenta. Por favor, intenta de nuevo.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleRegister = async () => {
    // TODO: Implementar registro con Google
    console.log('Google register');
  };

  const handleGithubRegister = async () => {
    // TODO: Implementar registro con GitHub
    console.log('GitHub register');
  };

  return (
    <div className="min-h-screen bg-stone-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        {/* Logo y título */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-stone-400 to-amber-400 bg-clip-text text-transparent">
              Code Dungeon
            </h1>
          </Link>
          <h2 className="mt-6 text-3xl font-bold text-stone-100">
            Crea tu cuenta
          </h2>
          <p className="mt-2 text-sm text-stone-300">
            O{' '}
            <Link href="/auth/login" className="font-medium text-amber-600 hover:text-amber-500 transition-colors">
              inicia sesión si ya tienes cuenta
            </Link>
          </p>
        </div>

        {/* Formulario */}
        <div className="bg-stone-800 py-8 px-6 shadow-2xl rounded-lg border-2 border-stone-700">
          {registered ? (
            <div className="text-center">
              <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-green-400" />
              </div>
              <h3 className="text-xl font-bold text-stone-100 mb-2">
                ¡Cuenta creada!
              </h3>
              <p className="text-stone-200 mb-6">
                Hemos enviado un email de verificación a{' '}
                <span className="font-semibold text-stone-100">{formData.email}</span>
              </p>
              <div className="bg-amber-500/20 border-2 border-stone-700 rounded-lg p-4 mb-6">
                <div className="flex items-start space-x-2">
                  <Mail className="w-5 h-5 text-stone-400 mt-0.5 flex-shrink-0" />
                  <div className="text-sm text-stone-200 text-left">
                    <p className="mb-2">
                      Por favor, revisa tu bandeja de entrada y haz clic en el enlace de verificación para activar tu cuenta.
                    </p>
                    <p className="text-stone-300">
                      Si no ves el email, revisa tu carpeta de spam.
                    </p>
                  </div>
                </div>
              </div>
              <Link
                href="/auth/login"
                className="block w-full py-3 px-4 bg-gradient-to-r from-stone-600 to-amber-600 text-stone-100 rounded-lg font-medium hover:from-stone-700 hover:to-amber-700 transition-all shadow-lg mb-3"
              >
                Ir al login
              </Link>
              <Link
                href="/auth/resend-verification"
                className="block w-full text-sm text-stone-400 hover:text-stone-300 transition-colors"
              >
                ¿No recibiste el email? Reenviar
              </Link>
            </div>
          ) : (
            <>
              {error && (
                <div className="mb-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
                  <p className="text-sm text-red-200">{error}</p>
                </div>
              )}

          {/* Social Login */}
          <div className="space-y-3 mb-6">
            <button
              onClick={handleGoogleRegister}
              className="w-full flex items-center justify-center gap-3 px-4 py-3 border-2 border-stone-700 bg-stone-900/30 rounded-lg hover:bg-stone-900/50 transition-colors"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              <span className="text-sm font-medium text-stone-100">Continuar con Google</span>
            </button>

            <button
              onClick={handleGithubRegister}
              className="w-full flex items-center justify-center gap-3 px-4 py-3 bg-stone-900 text-stone-100 rounded-lg hover:bg-stone-700 transition-colors border-2 border-stone-700"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path
                  fillRule="evenodd"
                  d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="text-sm font-medium">Continuar con GitHub</span>
            </button>
          </div>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-stone-500/30" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-stone-800/50 text-stone-300">O con email</span>
            </div>
          </div>

          {/* Registration Form */}
          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-stone-200 mb-2">
                Nombre completo
              </label>
              <input
                id="name"
                name="name"
                type="text"
                required
                value={formData.name}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-stone-900/50 border-2 border-stone-700 rounded-lg focus:ring-2 focus:ring-amber-700 focus:border-amber-700 text-stone-100 placeholder-stone-500 transition-all"
                placeholder="Juan Pérez"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-stone-200 mb-2">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-stone-900/50 border-2 border-stone-700 rounded-lg focus:ring-2 focus:ring-amber-700 focus:border-amber-700 text-stone-100 placeholder-stone-500 transition-all"
                placeholder="tu@email.com"
              />
            </div>

            <div>
              <label htmlFor="role" className="block text-sm font-medium text-stone-200 mb-2">
                Tipo de cuenta
              </label>
              <select
                id="role"
                name="role"
                value={formData.role}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-stone-900/50 border-2 border-stone-700 rounded-lg focus:ring-2 focus:ring-amber-700 focus:border-amber-700 text-stone-100 transition-all"
              >
                <option value="student">Estudiante</option>
                <option value="parent">Padre/Madre</option>
                <option value="teacher">Profesor</option>
              </select>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-stone-200 mb-2">
                Contraseña
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-stone-900/50 border-2 border-stone-700 rounded-lg focus:ring-2 focus:ring-amber-700 focus:border-amber-700 text-stone-100 placeholder-stone-500 transition-all"
                placeholder="Mínimo 6 caracteres"
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-stone-200 mb-2">
                Confirmar contraseña
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-stone-900/50 border-2 border-stone-700 rounded-lg focus:ring-2 focus:ring-amber-700 focus:border-amber-700 text-stone-100 placeholder-stone-500 transition-all"
                placeholder="Repite tu contraseña"
              />
            </div>

            <div className="flex items-start">
              <input
                id="terms"
                type="checkbox"
                required
                className="mt-1 rounded border-stone-500/30 bg-stone-900/50 text-stone-500 focus:ring-amber-700"
              />
              <label htmlFor="terms" className="ml-2 text-sm text-stone-200">
                Acepto los{' '}
                <Link href="/terms" className="text-amber-600 hover:text-amber-500 transition-colors">
                  términos y condiciones
                </Link>{' '}
                y la{' '}
                <Link href="/privacy" className="text-amber-600 hover:text-amber-500 transition-colors">
                  política de privacidad
                </Link>
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-amber-700 text-white rounded-lg font-medium hover:bg-amber-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg border-2 border-amber-800"
            >
              {loading ? 'Creando cuenta...' : 'Crear cuenta'}
            </button>
          </form>

          {/* Footer */}
          <p className="mt-6 text-center text-sm text-stone-300">
            ¿Ya tienes cuenta?{' '}
            <Link href="/auth/login" className="font-medium text-amber-600 hover:text-amber-500 transition-colors">
              Inicia sesión
            </Link>
          </p>
          </>
          )}
        </div>

        {/* Link a inicio */}
        <p className="mt-8 text-center text-sm text-stone-300">
          <Link href="/" className="font-medium text-amber-600 hover:text-amber-500 transition-colors">
            ← Volver al inicio
          </Link>
        </p>
      </div>
    </div>
  );
}
