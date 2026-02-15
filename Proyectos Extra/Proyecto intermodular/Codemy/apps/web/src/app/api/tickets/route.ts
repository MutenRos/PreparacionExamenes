import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import { getSafeUser } from '@/lib/auth-helpers';

// Obtener tickets del usuario
export async function GET(req: NextRequest) {
  try {
    const supabase = await createClient();
    const { user, error: authError, isDeleted } = await getSafeUser();
    
    if (authError || !user || isDeleted) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(req.url);
    const ticketId = searchParams.get('id');

    if (ticketId) {
      // Obtener un ticket específico con sus mensajes
      const { data: ticket, error: ticketError } = await supabase
        .from('tickets')
        .select('*')
        .eq('id', ticketId)
        .eq('user_id', user.id)
        .single();

      if (ticketError) {
        return NextResponse.json({ error: ticketError.message }, { status: 500 });
      }

      const { data: messages, error: messagesError } = await supabase
        .from('ticket_messages')
        .select('*')
        .eq('ticket_id', ticketId)
        .order('created_at', { ascending: true });

      if (messagesError) {
        return NextResponse.json({ error: messagesError.message }, { status: 500 });
      }

      return NextResponse.json({ ticket, messages });
    }

    // Obtener todos los tickets del usuario
    const { data: tickets, error } = await supabase
      .from('tickets')
      .select('*, ticket_messages(count)')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false });

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

// Crear nuevo ticket
export async function POST(req: NextRequest) {
  try {
    const supabase = await createClient();
    const { user, error: authError, isDeleted } = await getSafeUser();
    
    if (authError || !user || isDeleted) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await req.json();
    const { subject, description, priority, category } = body;

    if (!subject || !description) {
      return NextResponse.json(
        { error: 'Subject and description are required' },
        { status: 400 }
      );
    }

    const { data: ticket, error } = await supabase
      .from('tickets')
      .insert({
        user_id: user.id,
        subject,
        description,
        priority: priority || 'medium',
        category: category || 'general',
        status: 'open',
      })
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    // Crear primer mensaje con la descripción
    await supabase
      .from('ticket_messages')
      .insert({
        ticket_id: ticket.id,
        user_id: user.id,
        message: description,
        is_admin: false,
      });

    return NextResponse.json({ ticket });
  } catch (error: any) {
    console.error('Error creating ticket:', error);
    return NextResponse.json(
      { error: error.message || 'Error creating ticket' },
      { status: 500 }
    );
  }
}

// Actualizar ticket (cerrar, cambiar prioridad, etc.)
export async function PATCH(req: NextRequest) {
  try {
    const supabase = await createClient();
    const { user, error: authError, isDeleted } = await getSafeUser();
    
    if (authError || !user || isDeleted) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await req.json();
    const { ticketId, status, priority } = body;

    const updates: any = {};
    if (status) updates.status = status;
    if (priority) updates.priority = priority;
    if (status === 'resolved' || status === 'closed') {
      updates.resolved_at = new Date().toISOString();
    }

    const { data: ticket, error } = await supabase
      .from('tickets')
      .update(updates)
      .eq('id', ticketId)
      .eq('user_id', user.id)
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ ticket });
  } catch (error: any) {
    console.error('Error updating ticket:', error);
    return NextResponse.json(
      { error: error.message || 'Error updating ticket' },
      { status: 500 }
    );
  }
}
