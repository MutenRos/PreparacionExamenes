import { createClient } from '@/lib/supabase/server';
import { getSafeUser, getCurrentUserId } from '@/lib/auth-helpers';

/**
 * Helpers para verificar acceso de usuarios a contenido premium
 * Incluye soporte para usuarios pioneros (primeras 100 cuentas)
 */

export interface UserSubscription {
  planId: string;
  billingPeriod: string;
  expiresAt: string | null;
  createdAt: string;
}

export interface UserProduct {
  productId: string;
  amount: number;
  createdAt: string;
}

export interface PioneerInfo {
  isPioneer: boolean;
  pioneerNumber: number | null;
  grantedAt: string | null;
}

/**
 * Verifica si un usuario es pionero (acceso de por vida)
 */
export async function isPioneerUser(userId?: string): Promise<boolean> {
  try {
    const supabase = await createClient();
    
    let userIdToCheck = userId;
    if (!userIdToCheck) {
      const { user } = await getSafeUser();
      if (!user) return false;
      userIdToCheck = user.id;
    }

    const { data, error } = await supabase.rpc('is_pioneer_user', {
      p_user_id: userIdToCheck
    });

    if (error) {
      console.error('Error verificando pioneer status:', error);
      return false;
    }

    return data || false;
  } catch (error) {
    console.error('Error en isPioneerUser:', error);
    return false;
  }
}

/**
 * Obtiene información del usuario pionero
 */
export async function getPioneerInfo(userId?: string): Promise<PioneerInfo> {
  try {
    const supabase = await createClient();
    
    let userIdToCheck = userId;
    if (!userIdToCheck) {
      const { user } = await getSafeUser();
      if (!user) return { isPioneer: false, pioneerNumber: null, grantedAt: null };
      userIdToCheck = user.id;
    }

    const { data, error } = await supabase.rpc('get_pioneer_info', {
      p_user_id: userIdToCheck
    });

    if (error) {
      console.error('Error obteniendo pioneer info:', error);
      return { isPioneer: false, pioneerNumber: null, grantedAt: null };
    }

    if (!data || data.length === 0) {
      return { isPioneer: false, pioneerNumber: null, grantedAt: null };
    }

    const info = data[0];
    return {
      isPioneer: info.is_pioneer,
      pioneerNumber: info.pioneer_number,
      grantedAt: info.granted_at
    };
  } catch (error) {
    console.error('Error en getPioneerInfo:', error);
    return { isPioneer: false, pioneerNumber: null, grantedAt: null };
  }
}

/**
 * Obtiene cuántos slots pioneros quedan disponibles
 */
export async function getPioneerSlotsRemaining(): Promise<number> {
  try {
    const supabase = await createClient();

    const { data, error } = await supabase.rpc('get_pioneer_slots_remaining');

    if (error) {
      console.error('Error obteniendo slots pioneros:', error);
      return 0;
    }

    return data || 0;
  } catch (error) {
    console.error('Error en getPioneerSlotsRemaining:', error);
    return 0;
  }
}

/**
 * Verifica si un usuario tiene una suscripción activa
 * INCLUYE usuarios pioneros (acceso de por vida)
 * @param userId - ID del usuario (opcional, usa el usuario autenticado por defecto)
 * @param planId - ID del plan específico (opcional, verifica cualquier plan)
 */
export async function hasActiveSubscription(
  userId?: string,
  planId?: string
): Promise<boolean> {
  try {
    const supabase = await createClient();
    
    // Si no se proporciona userId, usar el usuario autenticado
    let userIdToCheck = userId;
    if (!userIdToCheck) {
      const { user } = await getSafeUser();
      if (!user) return false;
      userIdToCheck = user.id;
    }

    const { data, error } = await supabase.rpc('has_active_subscription', {
      p_user_id: userIdToCheck,
      p_plan_id: planId || null
    });

    if (error) {
      console.error('Error verificando suscripción:', error);
      return false;
    }

    return data || false;
  } catch (error) {
    console.error('Error en hasActiveSubscription:', error);
    return false;
  }
}

/**
 * Verifica si un usuario tiene acceso a un producto específico
 * @param productId - ID del producto (skill tree)
 * @param userId - ID del usuario (opcional, usa el usuario autenticado por defecto)
 */
export async function hasProductAccess(
  productId: string,
  userId?: string
): Promise<boolean> {
  try {
    const supabase = await createClient();
    
    let userIdToCheck = userId;
    if (!userIdToCheck) {
      const { user } = await getSafeUser();
      if (!user) return false;
      userIdToCheck = user.id;
    }

    const { data, error } = await supabase.rpc('has_product_access', {
      p_user_id: userIdToCheck,
      p_product_id: productId
    });

    if (error) {
      console.error('Error verificando producto:', error);
      return false;
    }

    return data || false;
  } catch (error) {
    console.error('Error en hasProductAccess:', error);
    return false;
  }
}

/**
 * Obtiene la suscripción activa de un usuario
 * @param userId - ID del usuario (opcional, usa el usuario autenticado por defecto)
 */
export async function getActiveSubscription(
  userId?: string
): Promise<UserSubscription | null> {
  try {
    const supabase = await createClient();
    
    let userIdToCheck = userId;
    if (!userIdToCheck) {
      const { user } = await getSafeUser();
      if (!user) return null;
      userIdToCheck = user.id;
    }

    const { data, error } = await supabase.rpc('get_active_subscription', {
      p_user_id: userIdToCheck
    });

    if (error) {
      console.error('Error obteniendo suscripción:', error);
      return null;
    }

    if (!data || data.length === 0) return null;

    const sub = data[0];
    return {
      planId: sub.plan_id,
      billingPeriod: sub.billing_period,
      expiresAt: sub.expires_at,
      createdAt: sub.created_at
    };
  } catch (error) {
    console.error('Error en getActiveSubscription:', error);
    return null;
  }
}

/**
 * Obtiene todos los productos comprados por un usuario
 * @param userId - ID del usuario (opcional, usa el usuario autenticado por defecto)
 */
export async function getUserProducts(
  userId?: string
): Promise<UserProduct[]> {
  try {
    const supabase = await createClient();
    
    let userIdToCheck = userId;
    if (!userIdToCheck) {
      const { user } = await getSafeUser();
      if (!user) return [];
      userIdToCheck = user.id;
    }

    const { data, error } = await supabase.rpc('get_user_products', {
      p_user_id: userIdToCheck
    });

    if (error) {
      console.error('Error obteniendo productos:', error);
      return [];
    }

    if (!data) return [];

    return data.map((p: any) => ({
      productId: p.product_id,
      amount: p.amount,
      createdAt: p.created_at
    }));
  } catch (error) {
    console.error('Error en getUserProducts:', error);
    return [];
  }
}

/**
 * Verifica si un usuario tiene acceso premium (suscripción o producto comprado)
 * Útil para verificar acceso a contenido que puede estar en suscripción O compra individual
 * @param productId - ID del producto/skill tree
 * @param userId - ID del usuario (opcional)
 */
export async function hasPremiumAccess(
  productId: string,
  userId?: string
): Promise<boolean> {
  // Primero verifica si tiene suscripción activa (cualquier plan da acceso a todo)
  const hasSubscription = await hasActiveSubscription(userId);
  if (hasSubscription) return true;

  // Si no tiene suscripción, verifica si compró el producto individual
  return await hasProductAccess(productId, userId);
}

/**
 * Obtiene el nivel de plan del usuario (starter, pro, family)
 */
export async function getUserPlanLevel(
  userId?: string
): Promise<'free' | 'starter' | 'pro' | 'family'> {
  const subscription = await getActiveSubscription(userId);
  if (!subscription) return 'free';
  
  const planId = subscription.planId as 'starter' | 'pro' | 'family';
  return planId;
}

/**
 * Verifica si el usuario puede crear seminarios (requiere Pro o Family)
 */
export async function canCreateSeminars(userId?: string): Promise<boolean> {
  const planLevel = await getUserPlanLevel(userId);
  return planLevel === 'pro' || planLevel === 'family';
}

/**
 * Verifica si el usuario puede compartir cuenta (requiere Family)
 */
export async function canShareAccount(userId?: string): Promise<boolean> {
  const planLevel = await getUserPlanLevel(userId);
  return planLevel === 'family';
}
