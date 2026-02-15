/**
 * Utilidad para verificar permisos de administrador
 * Importa configuración desde constants.ts
 */

import { ADMIN_CONFIG, isAdmin as isAdminHelper } from './constants';

export const ADMIN_EMAIL = ADMIN_CONFIG.EMAIL;

/**
 * Verifica si un email tiene permisos de administrador
 */
export function isAdmin(email: string | null | undefined): boolean {
  return isAdminHelper(email);
}

/**
 * Verifica si el usuario actual es administrador
 */
export async function checkIsAdmin(): Promise<boolean> {
  if (typeof window === 'undefined') return false;
  
  try {
    const userEmail = localStorage.getItem('user_email');
    return isAdmin(userEmail);
  } catch {
    return false;
  }
}

/**
 * Hook para obtener el estado de admin del usuario actual
 */
export function useIsAdmin(): boolean {
  if (typeof window === 'undefined') return false;
  
  const userEmail = localStorage.getItem('user_email');
  return isAdmin(userEmail);
}

/**
 * Middleware para proteger rutas de admin
 */
export function requireAdmin(email: string | null | undefined): void {
  if (!isAdmin(email)) {
    throw new Error('Acceso denegado: Se requieren permisos de administrador');
  }
}
