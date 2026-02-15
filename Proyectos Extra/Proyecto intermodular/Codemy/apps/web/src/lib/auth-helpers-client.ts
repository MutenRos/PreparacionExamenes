/**
 * Auth Helpers Client - Manejo seguro de autenticación en el cliente
 * 
 * Versión para componentes del cliente que usa createClient() de @/lib/supabase/client
 */

import { createClient } from '@/lib/supabase/client';
import type { User } from '@supabase/supabase-js';
import { useEffect, useState } from 'react';

export interface SafeUserResult {
  user: User | null;
  error: string | null;
  isDeleted: boolean;
}

/**
 * Obtiene el usuario actual de forma segura (versión cliente)
 * 
 * Maneja el caso donde un usuario fue eliminado pero su sesión aún existe
 */
export async function getSafeUserClient(): Promise<SafeUserResult> {
  try {
    const supabase = createClient();
    
    const { data: { user }, error } = await supabase.auth.getUser();
    
    if (error) {
      console.warn('[Auth] Error al obtener usuario:', error.message);
      
      // Verificar si es un error de usuario eliminado
      const isDeletedUser = 
        error.message.includes('User not found') ||
        error.message.includes('Invalid user') ||
        error.message.includes('JWT') ||
        error.code === 'PGRST116';
      
      if (isDeletedUser) {
        console.warn('[Auth] Usuario eliminado detectado, limpiando sesión...');
        // Limpiar sesión inválida
        try {
          await supabase.auth.signOut();
          // Limpiar localStorage manualmente también
          localStorage.removeItem('supabase.auth.token');
          localStorage.removeItem('supabase.auth.session');
        } catch (signOutError) {
          console.error('[Auth] Error al cerrar sesión inválida:', signOutError);
        }
        
        // Recargar la página para limpiar el estado
        if (typeof window !== 'undefined') {
          window.location.reload();
        }
        
        return {
          user: null,
          error: 'Usuario eliminado',
          isDeleted: true
        };
      }
      
      return {
        user: null,
        error: error.message,
        isDeleted: false
      };
    }
    
    return {
      user,
      error: null,
      isDeleted: false
    };
    
  } catch (error: any) {
    console.error('[Auth] Error en getSafeUserClient:', error);
    return {
      user: null,
      error: error.message || 'Error desconocido',
      isDeleted: false
    };
  }
}

/**
 * Hook para usar en componentes React
 */
export function useAuthClient() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getSafeUserClient().then(({ user, error, isDeleted }) => {
      if (isDeleted) {
        // El usuario fue eliminado, la página se recargará
        return;
      }
      setUser(user);
      setError(error);
      setLoading(false);
    });
  }, []);

  return { user, loading, error };
}
