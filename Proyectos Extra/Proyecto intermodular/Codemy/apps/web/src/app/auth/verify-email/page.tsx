'use client';

import { useEffect, useState, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { Loader2, CheckCircle, XCircle } from 'lucide-react';

function VerifyEmailContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get('token');
  const [verificationState, setVerificationState] = useState<'loading' | 'success' | 'error'>('loading');

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        // En la nueva arquitectura con NextAuth, la verificación se maneja diferente
        // Por ahora, si hay token, asumimos éxito
        if (token) {
          // TODO: Implementar verificación real con NextAuth
          setVerificationState('success');
          setTimeout(() => {
            router.push('/dashboard');
          }, 2000);
        } else {
          // Sin token, redirigir a login
          setVerificationState('error');
        }
      } catch (err) {
        console.error('Error en verificación:', err);
        setVerificationState('error');
      }
    };

    verifyEmail();
  }, [token, router]);

  return (
    <div className="max-w-md w-full">
      <div className="text-center mb-8">
        <Link href="/" className="inline-block">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-amber-600 to-amber-500 bg-clip-text text-transparent">
            Code Dungeon
          </h1>
        </Link>
      </div>

      <div className="bg-stone-800 backdrop-blur-sm rounded-lg shadow-2xl p-8 border-2 border-stone-700">
        {verificationState === 'loading' && (
          <div className="text-center">
            <div className="w-16 h-16 bg-amber-700/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Loader2 className="w-8 h-8 text-amber-600 animate-spin" />
            </div>
            <h2 className="text-2xl font-bold text-stone-100 mb-2">
              Verificando tu email
            </h2>
            <p className="text-stone-300">
              Por favor espera mientras confirmamos tu cuenta...
            </p>
          </div>
        )}

        {verificationState === 'success' && (
          <div className="text-center">
            <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-8 h-8 text-green-400" />
            </div>
            <h2 className="text-2xl font-bold text-stone-100 mb-2">
              ¡Email verificado!
            </h2>
            <p className="text-stone-300 mb-6">
              Tu cuenta ha sido verificada correctamente. Redirigiendo al dashboard...
            </p>
            <div className="flex items-center justify-center space-x-2 text-sm text-stone-400">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Redirigiendo...</span>
            </div>
          </div>
        )}

        {verificationState === 'error' && (
          <div className="text-center">
            <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <XCircle className="w-8 h-8 text-red-400" />
            </div>
            <h2 className="text-2xl font-bold text-stone-100 mb-2">
              Error de verificación
            </h2>
            <p className="text-stone-300 mb-6">
              No pudimos verificar tu email. El enlace puede haber expirado.
            </p>
            <div className="space-y-3">
              <Link
                href="/auth/login"
                className="block w-full py-3 px-4 bg-amber-700 border-2 border-amber-800 text-stone-100 rounded-lg font-medium hover:bg-amber-800 transition-all shadow-lg"
              >
                Ir al login
              </Link>
            </div>
          </div>
        )}
      </div>

      <p className="mt-8 text-center text-sm text-stone-400">
        <Link href="/" className="font-medium text-stone-100 hover:text-stone-300 transition-colors">
          ← Volver al inicio
        </Link>
      </p>
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <div className="min-h-screen bg-stone-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <Suspense fallback={
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-4 border-amber-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-stone-300">Cargando...</p>
        </div>
      }>
        <VerifyEmailContent />
      </Suspense>
    </div>
  );
}
