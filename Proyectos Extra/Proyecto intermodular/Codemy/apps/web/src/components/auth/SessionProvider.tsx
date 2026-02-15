'use client';

import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { createClient } from '@/lib/supabase/client';

export function SessionProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const supabase = createClient();

    // Verificar sesión inicial
    const checkSession = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      
      // Si no hay sesión y no estamos en ruta pública, redirigir a login
      const publicPaths = ['/', '/auth/login', '/auth/register', '/auth/callback'];
      const isPublicPath = publicPaths.some(path => pathname === path || pathname.startsWith(path + '/'));
      
      if (!session && !isPublicPath) {
        router.push('/auth/login');
      }
    };

    checkSession();

    // Escuchar cambios de autenticación
    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      if (event === 'SIGNED_OUT') {
        router.push('/auth/login');
      } else if (event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') {
        router.refresh();
      }
    });

    return () => {
      subscription.unsubscribe();
    };
  }, [router, pathname]);

  return <>{children}</>;
}
