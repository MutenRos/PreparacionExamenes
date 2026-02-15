import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import { getSafeUser } from '@/lib/auth-helpers';

// Obtener todos los tickets (admin)
export async function GET(req: NextRequest) {
  try {
    const supabase = await createClient();
    const { user, error: authError, isDeleted } = await getSafeUser();
    
    if (authError || !user || user.email !== 'admin@codedungeon.es') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
    }

    const { searchParams } = new URL(req.url);
    const status = searchParams.get('status');

    let query = supabase
      .from('tickets')
      .select(`
        *,
        ticket_messages(count)
      `)
      .order('created_at', { ascending: false });

    if (status) {
      query = query.eq('status', status);
    }

    const { data: tickets, error } = await query;

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ tickets });
  } catch (error: any) {
    console.error('Error fetching tickets:', error);
    return NextResponse.json(
      { error: error.message || 'Error fetching tickets' },
      { status: 500 }
    );
  }
}

// Responder a ticket (admin)
export async function POST(req: NextRequest) {
  try {
    const supabase = await createClient();
    const { user, error: authError, isDeleted } = await getSafeUser();
    
    if (authError || !user || user.email !== 'admin@codedungeon.es') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
    }

    const body = await req.json();
    const { ticketId, message, updateStatus } = body;

    // Crear mensaje de admin
    const { error: messageError } = await supabase
      .from('ticket_messages')
      .insert({
        ticket_id: ticketId,
        user_id: user.id,
        message,
        is_admin: true,
      });

    if (messageError) {
      return NextResponse.json({ error: messageError.message }, { status: 500 });
    }

    // Actualizar estado si se especifica
    if (updateStatus) {
      await supabase
        .from('tickets')
        .update({ 
          status: updateStatus,
          assigned_to: user.id,
        })
        .eq('id', ticketId);
    }

    return NextResponse.json({ success: true });
  } catch (error: any) {
    console.error('Error responding to ticket:', error);
    return NextResponse.json(
      { error: error.message || 'Error responding to ticket' },
      { status: 500 }
    );
  }
}
