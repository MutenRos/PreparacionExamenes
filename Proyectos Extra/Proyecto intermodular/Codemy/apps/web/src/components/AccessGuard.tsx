'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Lock } from 'lucide-react';

interface AccessGuardProps {
  children: React.ReactNode;
  requiresAuth?: boolean;
  requiresSubscription?: boolean;
  requiredPlan?: 'starter' | 'pro' | 'family';
  requiresProduct?: string;
  fallbackUrl?: string;
}

/**
 * Componente para proteger contenido premium
 * Verifica autenticación, suscripción activa o status pionero
 */
export function AccessGuard({
  children,
  requiresAuth = true,
  requiresSubscription = false,
  requiredPlan,
  requiresProduct,
  fallbackUrl = '/#pricing'
}: AccessGuardProps) {
  const router = useRouter();
  const [hasAccess, setHasAccess] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function checkAccess() {
      try {
        // Verificar autenticación
        if (requiresAuth) {
          const authResponse = await fetch('/api/auth/session');
          const authData = await authResponse.json();
          
          if (!authData.user) {
            router.push(`/auth/login?redirectTo=${window.location.pathname}`);
            return;
          }
        }

        // Si solo requiere autenticación
        if (!requiresSubscription && !requiredPlan && !requiresProduct) {
          setHasAccess(true);
          setLoading(false);
          return;
        }

        // Verificar acceso premium
        const accessResponse = await fetch('/api/access/check', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            requiresSubscription,
            requiredPlan,
            requiresProduct
          })
        });

        const accessData = await accessResponse.json();

        if (!accessData.hasAccess) {
          router.push(fallbackUrl);
          return;
        }

        setHasAccess(true);
      } catch (error) {
        console.error('Error verificando acceso:', error);
        router.push(fallbackUrl);
      } finally {
        setLoading(false);
      }
    }

    checkAccess();
  }, [requiresAuth, requiresSubscription, requiredPlan, requiresProduct, fallbackUrl, router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-stone-950 via-stone-900 to-stone-950 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-amber-600 mx-auto mb-4"></div>
          <p className="text-stone-400">Verificando acceso...</p>
        </div>
      </div>
    );
  }

  if (hasAccess === false) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-stone-950 via-stone-900 to-stone-950 flex items-center justify-center p-4">
        <div className="max-w-md text-center">
          <div className="bg-red-900/20 border-2 border-red-600/30 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6">
            <Lock className="w-10 h-10 text-red-500" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-4">
            Acceso Restringido
          </h1>
          <p className="text-stone-400 mb-8">
            Este contenido requiere una suscripción activa o ser usuario pionero.
          </p>
          <button
            onClick={() => router.push(fallbackUrl)}
            className="bg-gradient-to-r from-amber-600 to-orange-600 text-white px-8 py-3 rounded-xl font-bold hover:from-amber-700 hover:to-orange-700 transition-all"
          >
            Ver Planes
          </button>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
