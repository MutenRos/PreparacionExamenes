'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from '@/lib/supabase/client';
import { Hero } from '@/components/landing/Hero'
import { Features } from '@/components/landing/Features'
import { Curriculum } from '@/components/landing/Curriculum'
import { Pricing } from '@/components/landing/Pricing'
import { CTA } from '@/components/landing/CTA'
import { Navigation } from '@/components/Navigation'
import { Footer } from '@/components/Footer'
import { PioneerCounter } from '@/components/PioneerCounter'

export default function HomePage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const supabase = createClient();
        const { data: { session }, error } = await supabase.auth.getSession();
        
        if (!error && session?.user) {
          // Si está logueado, redirigir al dashboard
          router.push('/dashboard');
          return;
        }
      } catch (error) {
        // Si hay error de conexión con Supabase, mostrar landing
        console.warn('Auth check failed:', error);
      }
      
      setIsLoading(false);
    };
    
    // Timeout de seguridad para evitar loading infinito
    const timeout = setTimeout(() => {
      setIsLoading(false);
    }, 3000);
    
    checkAuth();
    
    return () => clearTimeout(timeout);
  }, [router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-stone-900 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="relative w-12 h-12">
            <div className="absolute inset-0 border-4 border-amber-700/30 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-amber-600 border-t-transparent rounded-full animate-spin"></div>
          </div>
          <div className="text-stone-400 text-sm">Cargando...</div>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-stone-900">
      <Navigation />
      <Hero />
      <PioneerCounter />
      <Features />
      <Curriculum />
      <Pricing />
      <CTA />
      <Footer />
    </main>
  )
}
