/**
 * Auth Helpers - Manejo seguro de autenticación de Supabase
 * 
 * Este módulo proporciona funciones wrapper para operaciones de autenticación
 * que manejan correctamente casos edge como usuarios eliminados con sesiones activas.
 */

import { createClient } from '@/lib/supabase/server';
import type { User } from '@supabase/supabase-js';

export interface SafeUserResult {
  user: User | null;
  error: string | null;
  isDeleted: boolean; // True si el usuario fue eliminado pero tiene sesión activa
}

/**
 * Obtiene el usuario actual de forma segura
 * 
 * Maneja correctamente el caso donde un usuario fue eliminado desde Supabase
 * pero su sesión/token aún existe en localStorage.
 * 
 * @param userId - ID del usuario (opcional, usa el usuario actual si no se proporciona)
 * @returns SafeUserResult con información del usuario o error
 */
export async function getSafeUser(userId?: string): Promise<SafeUserResult> {
  try {
    const supabase = await createClient();
    
    const { data: { user }, error } = await supabase.auth.getUser();
    
    if (error) {
      // Si hay un error al obtener el usuario, podría ser que fue eliminado
      // pero aún tiene una sesión activa
      console.warn('Error al obtener usuario:', error.message);
      
      // Verificar si es un error de usuario no encontrado
      const isDeletedUser = 
        error.message.includes('User not found') ||
        error.message.includes('Invalid user') ||
        error.message.includes('JWT') ||
        error.code === 'PGRST116';
      
      if (isDeletedUser) {
        // Limpiar la sesión inválida
        try {
          await supabase.auth.signOut();
        } catch (signOutError) {
          console.error('Error al cerrar sesión inválida:', signOutError);
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
    
    // Si hay un userId específico y no coincide, retornar error
    if (userId && user && user.id !== userId) {
      return {
        user: null,
        error: 'Usuario no autorizado',
        isDeleted: false
      };
    }
    
    return {
      user,
      error: null,
      isDeleted: false
    };
    
  } catch (error: any) {
    console.error('Error en getSafeUser:', error);
    return {
      user: null,
      error: error.message || 'Error desconocido',
      isDeleted: false
    };
  }
}

/**
 * Verifica si hay un usuario autenticado de forma segura
 * 
 * @returns true si hay un usuario válido, false en caso contrario
 */
export async function hasAuthenticatedUser(): Promise<boolean> {
  const { user, isDeleted } = await getSafeUser();
  
  // Si el usuario fue eliminado, limpiar la sesión y retornar false
  if (isDeleted) {
    return false;
  }
  
  return user !== null;
}

/**
 * Obtiene el ID del usuario actual de forma segura
 * 
 * @returns ID del usuario o null si no está autenticado
 */
export async function getCurrentUserId(): Promise<string | null> {
  const { user } = await getSafeUser();
  return user?.id || null;
}

/**
 * Requiere que haya un usuario autenticado
 * Lanza un error si no hay usuario o si fue eliminado
 * 
 * @throws Error si no hay usuario autenticado
 * @returns User autenticado
 */
export async function requireAuth(): Promise<User> {
  const { user, error, isDeleted } = await getSafeUser();
  
  if (isDeleted) {
    throw new Error('Tu cuenta ha sido eliminada. Por favor, contacta al soporte.');
  }
  
  if (!user) {
    throw new Error(error || 'No autenticado');
  }
  
  return user;
}
