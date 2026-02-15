import { NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';

/**
 * GET /api/pioneer/slots
 * Obtiene cuántos slots pioneros quedan disponibles
 */
export async function GET() {
  try {
    const supabase = await createClient();

    const { data, error } = await supabase.rpc('get_pioneer_slots_remaining');

    if (error) {
      console.error('Error obteniendo slots pioneros:', error);
      return NextResponse.json(
        { error: 'Error obteniendo slots', slotsRemaining: 0 },
        { status: 500 }
      );
    }

    return NextResponse.json({
      slotsRemaining: data || 0,
      totalSlots: 100,
      percentage: ((data || 0) / 100) * 100
    });

  } catch (error) {
    console.error('Error en API pioneer/slots:', error);
    return NextResponse.json(
      { error: 'Internal server error', slotsRemaining: 0 },
      { status: 500 }
    );
  }
}
