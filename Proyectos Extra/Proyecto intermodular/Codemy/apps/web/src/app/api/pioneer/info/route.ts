import { createClient } from '@/lib/supabase/server';
import { getSafeUser } from '@/lib/auth-helpers';
import { NextResponse } from 'next/server';

/**
 * GET /api/pioneer/info
 * Obtiene información del status de pionero del usuario actual o de un usuario específico
 */
export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get('userId');

    const supabase = await createClient();
    
    // Si no se proporciona userId, usar el usuario actual
    let targetUserId = userId;
    
    if (!targetUserId) {
      const { user, isDeleted } = await getSafeUser();
      if (!user) {
        return NextResponse.json({ isPioneer: false });
      }
      targetUserId = user.id;
    }

    // Obtener información del pionero
    const { data, error } = await supabase
      .rpc('get_pioneer_info', { p_user_id: targetUserId });

    if (error) {
      console.error('Error getting pioneer info:', error);
      return NextResponse.json({ isPioneer: false });
    }

    if (!data || data.length === 0) {
      return NextResponse.json({ isPioneer: false });
    }

    const pioneerData = data[0];

    return NextResponse.json({
      isPioneer: true,
      pioneerNumber: pioneerData.pioneer_number,
      grantedAt: pioneerData.granted_at,
      isActive: pioneerData.is_active
    });

  } catch (error) {
    console.error('Error in pioneer info endpoint:', error);
    return NextResponse.json({ isPioneer: false });
  }
}
