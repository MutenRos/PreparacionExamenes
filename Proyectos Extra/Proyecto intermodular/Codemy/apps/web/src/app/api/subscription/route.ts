/**
 * API Route: Gestión de Suscripciones
 * GET /api/subscription - Obtener suscripción actual
 * DELETE /api/subscription - Cancelar suscripción
 */

import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@codeacademy/database/client';
import { stripe } from '@/lib/stripe';

// GET - Obtener suscripción actual
export async function GET(req: NextRequest) {
  try {
    const userId = req.nextUrl.searchParams.get('userId');

    if (!userId) {
      return NextResponse.json(
        { error: 'Missing userId' },
        { status: 400 }
      );
    }

    const supabase = createClient();
    const { data: subscription, error } = await supabase
      .from('subscriptions')
      .select('*')
      .eq('user_id', userId)
      .eq('status', 'active')
      .order('created_at', { ascending: false })
      .limit(1)
      .single();

    if (error && error.code !== 'PGRST116') {
      throw error;
    }

    if (!subscription) {
      return NextResponse.json({ subscription: null });
    }

    // Obtener detalles adicionales de Stripe
    const stripeSubscription = await stripe.subscriptions.retrieve(
      (subscription as any).stripe_subscription_id
    );

    return NextResponse.json({
      subscription: {
        ...(subscription as any),
        stripe_details: {
          current_period_end: new Date((stripeSubscription as any).current_period_end * 1000),
          cancel_at_period_end: (stripeSubscription as any).cancel_at_period_end,
          canceled_at: stripeSubscription.canceled_at 
            ? new Date(stripeSubscription.canceled_at * 1000) 
            : null,
        },
      },
    });

  } catch (error: any) {
    console.error('Error fetching subscription:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}

// DELETE - Cancelar suscripción
export async function DELETE(req: NextRequest) {
  try {
    const { userId, immediately } = await req.json();

    if (!userId) {
      return NextResponse.json(
        { error: 'Missing userId' },
        { status: 400 }
      );
    }

    const supabase = createClient();
    const { data: subscription } = await supabase
      .from('subscriptions')
      .select('stripe_subscription_id')
      .eq('user_id', userId)
      .eq('status', 'active')
      .single();

    if (!subscription) {
      return NextResponse.json(
        { error: 'No active subscription found' },
        { status: 404 }
      );
    }

    // Cancelar en Stripe
    if (immediately) {
      await stripe.subscriptions.cancel((subscription as any).stripe_subscription_id);
    } else {
      await stripe.subscriptions.update((subscription as any).stripe_subscription_id, {
        cancel_at_period_end: true,
      });
    }

    return NextResponse.json({ 
      success: true,
      message: immediately 
        ? 'Subscription canceled immediately' 
        : 'Subscription will be canceled at period end'
    });

  } catch (error: any) {
    console.error('Error canceling subscription:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
