'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Mail, ArrowLeft, CheckCircle } from 'lucide-react';
import { createClient } from '@supabase/supabase-js';

// Crear cliente de Supabase
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

export default function ResendVerificationPage() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState('');

  const handleResend = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const supabase = getSupabaseClient();
      
      const { error: resendError } = await supabase.auth.resend({
        type: 'signup',
        email: email,
        options: {
          emailRedirectTo: `${window.location.origin}/auth/callback`
        }
      });
      
      if (resendError) {
        console.error('Error al reenviar email:', resendError);
        throw resendError;
      }
      
      console.log('Email de verificación reenviado exitosamente');
      setSent(true);
    } catch (err) {
      console.error('Error completo:', err);
      const errorMessage = err instanceof Error ? err.message : 'Error al enviar el email. Por favor, intenta de nuevo.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-stone-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-amber-600 to-amber-500 bg-clip-text text-transparent">
              Code Dungeon
            </h1>
          </Link>
          <h2 className="mt-6 text-3xl font-bold text-stone-100">
            Reenviar verificación
          </h2>
          <p className="mt-2 text-sm text-stone-300">
            Ingresa tu email para recibir un nuevo enlace de verificación
          </p>
        </div>

        {/* Card */}
        <div className="bg-stone-800 backdrop-blur-sm rounded-lg shadow-2xl p-8 border-2 border-stone-700">
          {!sent ? (
            <>
              {error && (
                <div className="mb-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
                  <p className="text-sm text-red-200">{error}</p>
                </div>
              )}

              <form onSubmit={handleResend} className="space-y-4">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-stone-300 mb-2">
                    Email
                  </label>
                  <input
                    id="email"
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-4 py-3 bg-stone-950 border-2 border-stone-700 rounded-lg focus:ring-2 focus:ring-amber-700 focus:border-amber-700 text-stone-100 placeholder-stone-500 transition-all"
                    placeholder="tu@email.com"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3 px-4 bg-amber-700 border-2 border-amber-800 text-stone-100 rounded-lg font-medium hover:bg-amber-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
                >
                  {loading ? 'Enviando...' : 'Reenviar email'}
                </button>
              </form>

              <div className="mt-6 text-center">
                <Link
                  href="/auth/login"
                  className="inline-flex items-center text-sm text-stone-400 hover:text-stone-200 transition-colors"
                >
                  <ArrowLeft className="w-4 h-4 mr-1" />
                  Volver al login
                </Link>
              </div>
            </>
          ) : (
            <div className="text-center">
              <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-green-400" />
              </div>
              <h3 className="text-xl font-bold text-stone-100 mb-2">
                ¡Email enviado!
              </h3>
              <p className="text-stone-300 mb-6">
                Hemos enviado un nuevo enlace de verificación a{' '}
                <span className="font-semibold text-stone-100">{email}</span>
              </p>
              <div className="bg-amber-700/20 border-2 border-stone-700 rounded-lg p-4 mb-6">
                <div className="flex items-start space-x-2">
                  <Mail className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
                  <div className="text-sm text-stone-300 text-left">
                    <p className="mb-2">
                      Revisa tu bandeja de entrada y haz clic en el enlace de verificación.
                    </p>
                    <p className="text-stone-400">
                      Si no ves el email, revisa tu carpeta de spam.
                    </p>
                  </div>
                </div>
              </div>
              <Link
                href="/auth/login"
                className="block w-full py-3 px-4 bg-amber-700 border-2 border-amber-800 text-stone-100 rounded-lg font-medium hover:bg-amber-800 transition-all shadow-lg"
              >
                Ir al login
              </Link>
            </div>
          )}
        </div>

        {/* Back to home */}
        <p className="mt-8 text-center text-sm text-stone-400">
          <Link href="/" className="font-medium text-stone-100 hover:text-stone-300 transition-colors">
            ← Volver al inicio
          </Link>
        </p>
      </div>
    </div>
  );
}
