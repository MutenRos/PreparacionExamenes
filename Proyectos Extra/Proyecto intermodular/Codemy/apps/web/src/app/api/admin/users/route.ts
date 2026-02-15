import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import { getSafeUser } from '@/lib/auth-helpers';

// Obtener lista de usuarios
export async function GET(req: NextRequest) {
  try {
    const supabase = await createClient();
    const { user, error: authError, isDeleted } = await getSafeUser();
    
    if (authError || !user || isDeleted || user.email !== 'admin@codedungeon.es') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
    }

    const { searchParams } = new URL(req.url);
    const limit = parseInt(searchParams.get('limit') || '1000'); // Aumentado a 1000
    const offset = parseInt(searchParams.get('offset') || '0');

    // Obtener TODOS los usuarios de auth.users (usando admin API)
    // Nota: Si hay más de 1000 usuarios, necesitarás implementar paginación adecuada
    const { data: authData, error: usersError } = await supabase.auth.admin.listUsers({
      page: Math.floor(offset / limit) + 1,
      perPage: limit,
    });

    if (usersError) {
      console.error('Error listing users:', usersError);
      return NextResponse.json({ error: usersError.message }, { status: 500 });
    }

    const users = authData.users || [];
    const userIds = users.map(u => u.id);
    
    console.log(`Total users fetched: ${users.length}, Total in DB: ${authData.total}`);

    // Obtener información de pioneros
    const { data: pioneersData } = await supabase
      .from('pioneer_users')
      .select('user_id, pioneer_number, assigned_at')
      .in('user_id', userIds);

    // Obtener suscripciones
    const { data: subscriptionsData } = await supabase
      .from('subscriptions')
      .select('user_id, plan_type, status, current_period_end')
      .in('user_id', userIds);

    // Combinar datos
    const enrichedUsers = users.map(user => {
      const pioneer = pioneersData?.find(p => p.user_id === user.id);
      const subscription = subscriptionsData?.find(s => s.user_id === user.id);

      return {
        id: user.id,
        email: user.email,
        created_at: user.created_at,
        last_sign_in_at: user.last_sign_in_at,
        confirmed_at: user.confirmed_at,
        is_pioneer: !!pioneer,
        pioneer_number: pioneer?.pioneer_number,
        subscription: subscription ? {
          plan: subscription.plan_type,
          status: subscription.status,
          expires_at: subscription.current_period_end,
        } : null,
      };
    });

    return NextResponse.json({
      users: enrichedUsers,
      total: authData.total || users.length,
    });
  } catch (error: any) {
    console.error('Error fetching users:', error);
    return NextResponse.json(
      { error: error.message || 'Error fetching users' },
      { status: 500 }
    );
  }
}

// Actualizar usuario
export async function PATCH(req: NextRequest) {
  try {
    const supabase = await createClient();
    const { user, error: authError, isDeleted } = await getSafeUser();
    
    if (authError || !user || isDeleted || user.email !== 'admin@codedungeon.es') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
    }

    const body = await req.json();
    const { userId, action, data: updateData } = body;

    switch (action) {
      case 'confirm_email':
        await supabase.auth.admin.updateUserById(userId, {
          email_confirm: true,
        });
        break;

      case 'reset_password':
        await supabase.auth.admin.updateUserById(userId, {
          password: updateData.password,
        });
        break;

      case 'delete_user':
        await supabase.auth.admin.deleteUser(userId);
        break;

      case 'assign_pioneer':
        const { data: pioneerData } = await supabase.rpc('assign_pioneer_status', {
          p_user_id: userId,
        });
        return NextResponse.json({ success: true, pioneer_number: pioneerData });

      case 'remove_pioneer':
        await supabase
          .from('pioneer_users')
          .delete()
          .eq('user_id', userId);
        
        // Incrementar slots disponibles
        await supabase.rpc('increment', {
          table_name: 'pioneer_config',
          column_name: 'available_slots',
        });
        break;

      default:
        return NextResponse.json({ error: 'Invalid action' }, { status: 400 });
    }

    return NextResponse.json({ success: true });
  } catch (error: any) {
    console.error('Error updating user:', error);
    return NextResponse.json(
      { error: error.message || 'Error updating user' },
      { status: 500 }
    );
  }
}
