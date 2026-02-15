/**
 * API Route: Crear Checkout Session
 * POST /api/stripe/checkout
 */

import { NextRequest, NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';
import { createClient } from '@codeacademy/database/client';

export async function POST(req: NextRequest) {
  try {
    const { priceId, userId, planType, billingInterval } = await req.json();

    if (!priceId || !userId) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // Verificar usuario en Supabase
    const supabase = createClient();
    const { data: user, error: userError } = await supabase
      .from('users')
      .select('email, stripe_customer_id')
      .eq('id', userId)
      .single();

    if (userError || !user) {
      return NextResponse.json(
        { error: 'User not found' },
        { status: 404 }
      );
    }

    // Crear o recuperar customer de Stripe
    let customerId = (user as any).stripe_customer_id;
    
    if (!customerId) {
      const customer = await stripe.customers.create({
        email: (user as any).email || '',
        metadata: {
          supabase_user_id: userId,
        },
      });
      customerId = customer.id;

      // Guardar customer ID en Supabase
      await (supabase
        .from('users') as any)
        .update({ stripe_customer_id: customerId })
        .eq('id', userId);
    }

    // Crear Checkout Session
    const session = await stripe.checkout.sessions.create({
      customer: customerId,
      mode: 'subscription',
      payment_method_types: ['card'],
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      subscription_data: {
        trial_period_days: 14, // 14 días de prueba
        metadata: {
          user_id: userId,
          plan_type: planType,
          billing_interval: billingInterval,
        },
      },
      success_url: `${req.nextUrl.origin}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${req.nextUrl.origin}/pricing`,
      metadata: {
        user_id: userId,
      },
    });

    return NextResponse.json({ 
      sessionId: session.id,
      url: session.url 
    });

  } catch (error: any) {
    console.error('Error creating checkout session:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}
