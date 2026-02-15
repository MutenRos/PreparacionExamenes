import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';
import { getSafeUser } from '@/lib/auth-helpers';
import { ADMIN_EMAIL } from '@/lib/admin-check';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { requiredPlan, requiresProduct } = body;

    const supabase = await createClient();
    
    // Verificar autenticación
    const { user, error: authError, isDeleted } = await getSafeUser();
    
    if (authError || !user || isDeleted) {
      return NextResponse.json(
        { hasAccess: false, reason: 'not_authenticated' },
        { status: 401 }
      );
    }

    // ADMIN TIENE ACCESO A TODO
    if (user.email === ADMIN_EMAIL) {
      return NextResponse.json({
        hasAccess: true,
        reason: 'admin_user',
        isAdmin: true
      });
    }

    // Verificar si es usuario pionero
    const { data: pioneerData } = await supabase
      .rpc('is_pioneer_user', { p_user_id: user.id });

    if (pioneerData === true) {
      return NextResponse.json({
        hasAccess: true,
        reason: 'pioneer_user',
        isPioneer: true
      });
    }

    // Verificar suscripción activa
    const { data: subscriptions } = await supabase
      .from('subscriptions')
      .select('plan_type, status, current_period_end')
      .eq('user_id', user.id)
      .eq('status', 'active')
      .single();

    if (subscriptions) {
      // Si requiere un plan específico, verificar
      if (requiredPlan) {
        const planHierarchy = { starter: 1, pro: 2, family: 3 };
        const userPlanLevel = planHierarchy[subscriptions.plan_type as keyof typeof planHierarchy] || 0;
        const requiredPlanLevel = planHierarchy[requiredPlan as keyof typeof planHierarchy] || 0;

        if (userPlanLevel >= requiredPlanLevel) {
          return NextResponse.json({
            hasAccess: true,
            reason: 'subscription',
            plan: subscriptions.plan_type,
            expiresAt: subscriptions.current_period_end
          });
        } else {
          return NextResponse.json({
            hasAccess: false,
            reason: 'insufficient_plan',
            currentPlan: subscriptions.plan_type,
            requiredPlan
          });
        }
      }

      return NextResponse.json({
        hasAccess: true,
        reason: 'subscription',
        plan: subscriptions.plan_type,
        expiresAt: subscriptions.current_period_end
      });
    }

    // Verificar acceso a producto específico
    if (requiresProduct) {
      const { data: purchases } = await supabase
        .from('purchases')
        .select('product_id')
        .eq('user_id', user.id)
        .eq('product_id', requiresProduct)
        .eq('status', 'completed')
        .single();

      if (purchases) {
        return NextResponse.json({
          hasAccess: true,
          reason: 'product_purchase',
          product: requiresProduct
        });
      }
    }

    // Sin acceso
    return NextResponse.json({
      hasAccess: false,
      reason: 'no_subscription'
    });

  } catch (error) {
    console.error('Error checking access:', error);
    return NextResponse.json(
      { hasAccess: false, reason: 'error', error: 'Internal server error' },
      { status: 500 }
    );
  }
}
