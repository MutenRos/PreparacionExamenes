import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import { getSafeUser } from '@/lib/auth-helpers';

// Obtener suscripciones
export async function GET(req: NextRequest) {
  try {
    const supabase = await createClient();
    const { user, error: authError, isDeleted } = await getSafeUser();
    
    if (authError || !user || isDeleted || user.email !== 'admin@codedungeon.es') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
    }

    const { searchParams } = new URL(req.url);
    const userId = searchParams.get('userId');

    let query = supabase
      .from('subscriptions')
      .select('*')
      .order('created_at', { ascending: false });

    if (userId) {
      query = query.eq('user_id', userId);
    }

    const { data, error } = await query;

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ subscriptions: data });
  } catch (error: any) {
    console.error('Error fetching subscriptions:', error);
    return NextResponse.json(
      { error: error.message || 'Error fetching subscriptions' },
      { status: 500 }
    );
  }
}

// Crear o actualizar suscripción
export async function POST(req: NextRequest) {
  try {
    const supabase = await createClient();
    const { user, error: authError, isDeleted } = await getSafeUser();
    
    if (authError || !user || user.email !== 'admin@codedungeon.es') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
    }

    const body = await req.json();
    const { userId, planType, action } = body;

    if (action === 'create') {
      // Crear nueva suscripción manual
      const { data, error } = await supabase
        .from('subscriptions')
        .insert({
          user_id: userId,
          plan_type: planType,
          status: 'active',
          current_period_start: new Date().toISOString(),
          current_period_end: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(), // 30 días
          payment_method: 'manual',
        })
        .select()
        .single();

      if (error) {
        return NextResponse.json({ error: error.message }, { status: 500 });
      }

      return NextResponse.json({ success: true, subscription: data });
    }

    if (action === 'cancel') {
      // Cancelar suscripción
      const { error } = await supabase
        .from('subscriptions')
        .update({ status: 'canceled', canceled_at: new Date().toISOString() })
        .eq('user_id', userId);

      if (error) {
        return NextResponse.json({ error: error.message }, { status: 500 });
      }

      return NextResponse.json({ success: true });
    }

    if (action === 'reactivate') {
      // Reactivar suscripción
      const { error } = await supabase
        .from('subscriptions')
        .update({ 
          status: 'active',
          current_period_end: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
        })
        .eq('user_id', userId);

      if (error) {
        return NextResponse.json({ error: error.message }, { status: 500 });
      }

      return NextResponse.json({ success: true });
    }

    return NextResponse.json({ error: 'Invalid action' }, { status: 400 });
  } catch (error: any) {
    console.error('Error managing subscription:', error);
    return NextResponse.json(
      { error: error.message || 'Error managing subscription' },
      { status: 500 }
    );
  }
}
