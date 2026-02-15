import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

/**
 * POST /api/auth/assign-pioneer
 * Asigna status de pionero a un usuario recién registrado si hay slots disponibles
 */
export async function POST(request: Request) {
  try {
    const { userId } = await request.json();

    if (!userId) {
      return NextResponse.json(
        { error: 'User ID is required' },
        { status: 400 }
      );
    }

    const supabase = await createClient();

    // Llamar a la función de Supabase para asignar status de pionero
    const { data, error } = await supabase.rpc('assign_pioneer_status', {
      p_user_id: userId
    });

    if (error) {
      console.error('Error assigning pioneer status:', error);
      // No fallar si no se puede asignar pionero (puede que ya no haya slots)
      return NextResponse.json({
        success: false,
        isPioneer: false,
        error: error.message
      });
    }

    return NextResponse.json({
      success: true,
      isPioneer: data?.pioneer_number !== null,
      pioneerNumber: data?.pioneer_number,
      message: data?.pioneer_number 
        ? `¡Felicidades! Eres el usuario pionero #${data.pioneer_number}` 
        : 'Usuario registrado correctamente'
    });

  } catch (error) {
    console.error('Error in assign-pioneer endpoint:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
