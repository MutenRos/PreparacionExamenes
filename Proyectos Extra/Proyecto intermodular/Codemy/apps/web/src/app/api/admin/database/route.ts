import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import { getSafeUser } from '@/lib/auth-helpers';

export async function GET(req: NextRequest) {
  try {
    // Verificar que sea admin
    const supabase = await createClient();
    const { user, error: authError, isDeleted } = await getSafeUser();
    
    if (authError || !user || user.email !== 'admin@codedungeon.es') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 403 });
    }

    const { searchParams } = new URL(req.url);
    const table = searchParams.get('table');
    const limit = parseInt(searchParams.get('limit') || '50');
    const offset = parseInt(searchParams.get('offset') || '0');

    if (!table) {
      return NextResponse.json({ error: 'Table name required' }, { status: 400 });
    }

    // Obtener datos de la tabla
    const { data, error, count } = await supabase
      .from(table)
      .select('*', { count: 'exact' })
      .range(offset, offset + limit - 1);

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({
      data,
      count,
      limit,
      offset,
    });
  } catch (error: any) {
    console.error('Error fetching database data:', error);
    return NextResponse.json(
      { error: error.message || 'Error fetching data' },
      { status: 500 }
    );
  }
}
