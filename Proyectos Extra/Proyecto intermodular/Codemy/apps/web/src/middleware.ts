import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { createServerClient } from '@supabase/ssr';

export async function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // Rutas públicas que no requieren autenticación
  const publicPaths = [
    '/',
    '/auth/login',
    '/auth/register',
    '/auth/callback',
    '/api/auth/login',
    '/api/auth/logout',
    '/api/auth/callback'
  ];

  // Rutas de assets estáticos que siempre son accesibles
  const isStaticAsset = 
    request.nextUrl.pathname.startsWith('/_next') ||
    request.nextUrl.pathname.startsWith('/images/') ||
    request.nextUrl.pathname.startsWith('/fonts/') ||
    request.nextUrl.pathname === '/favicon.ico';

  // Agregar headers de caché para assets estáticos
  if (isStaticAsset) {
    response.headers.set(
      'Cache-Control',
      'public, max-age=31536000, immutable'
    );
    return response;
  }

  // Security headers
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');

  // CORS para API
  if (request.nextUrl.pathname.startsWith('/api/')) {
    response.headers.set('Access-Control-Allow-Credentials', 'true');
    response.headers.set('Access-Control-Allow-Origin', '*');
    response.headers.set(
      'Access-Control-Allow-Methods',
      'GET,DELETE,PATCH,POST,PUT,OPTIONS'
    );
    response.headers.set(
      'Access-Control-Allow-Headers',
      'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
    );
  }

  // Verificar si la ruta es pública
  const isPublicPath = publicPaths.some(path => 
    request.nextUrl.pathname === path || 
    request.nextUrl.pathname.startsWith(path + '/')
  );

  // Permitir acceso a rutas públicas sin verificar autenticación
  if (isPublicPath) {
    return response;
  }

  // TODO: Verificación de autenticación deshabilitada temporalmente
  // La protección se maneja en el cliente con SessionProvider
  return response;

  /* Verificación de autenticación comentada - causa problemas con persistencia
  // Verificar autenticación para rutas protegidas
  try {
    let supabaseResponse = NextResponse.next({
      request,
    });

    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          get(name: string) {
            return request.cookies.get(name)?.value;
          },
          set(name: string, value: string, options: any) {
            // Respetar las opciones que vienen de Supabase
            supabaseResponse.cookies.set({
              name,
              value,
              ...options,
            });
          },
          remove(name: string, options: any) {
            supabaseResponse.cookies.set({
              name,
              value: '',
              ...options,
            });
          },
        },
      }
    );

    // Refrescar la sesión si está a punto de expirar
    const { data: { user }, error } = await supabase.auth.getUser();

    if (error) {
      console.error('Error al obtener usuario:', error);
      return NextResponse.redirect(new URL('/auth/login', request.url));
    }

    // Si no hay usuario autenticado, redirigir a login
    if (!user) {
      return NextResponse.redirect(new URL('/auth/login', request.url));
    }

    // Verificar acceso a rutas de admin
    if (request.nextUrl.pathname.startsWith('/admin')) {
      if (user.email !== 'admin@codedungeon.es') {
        return NextResponse.redirect(new URL('/dashboard', request.url));
      }
    }

    // Retornar respuesta con cookies actualizadas
    return supabaseResponse;

  } catch (error) {
    console.error('Error en middleware de autenticación:', error);
    return NextResponse.redirect(new URL('/auth/login', request.url));
  }
  */
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for webpack HMR
     */
    '/((?!_next/webpack-hmr).*)',
  ],
};
