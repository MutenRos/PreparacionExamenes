import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');

  if (code) {
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
    const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
    
    const supabase = createClient(supabaseUrl, supabaseAnonKey, {
      auth: {
        autoRefreshToken: true,
        persistSession: true,
      },
    });

    try {
      // Intercambiar el código por una sesión
      const { error } = await supabase.auth.exchangeCodeForSession(code);
      
      if (!error) {
        // Redirigir al dashboard después de verificación exitosa
        return NextResponse.redirect(new URL('/dashboard', request.url));
      }
    } catch (error) {
      console.error('Error en callback:', error);
    }
  }

  // Si algo falla, redirigir a verify-email
  return NextResponse.redirect(new URL('/auth/verify-email', request.url));
}
