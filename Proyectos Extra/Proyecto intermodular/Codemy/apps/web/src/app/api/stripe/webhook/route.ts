/**
 * API Route: Stripe Webhooks
 * POST /api/stripe/webhook
 * Maneja eventos de Stripe (subscripciones, pagos, cancelaciones)
 */

import { NextRequest, NextResponse } from 'next/server';
import { headers } from 'next/headers';
import { stripe } from '@/lib/stripe';
import { createClient } from '@codeacademy/database/client';
import Stripe from 'stripe';

const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET || '';

export async function POST(req: NextRequest) {
  const body = await req.text();
  const signature = (await headers()).get('stripe-signature');

  if (!signature) {
    return NextResponse.json(
      { error: 'Missing stripe-signature header' },
      { status: 400 }
    );
  }

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err: any) {
    console.error('⚠️ Webhook signature verification failed:', err.message);
    return NextResponse.json(
      { error: `Webhook Error: ${err.message}` },
      { status: 400 }
    );
  }

  const supabase = createClient();

  // Manejar diferentes tipos de eventos
  try {
    switch (event.type) {
      // Checkout completado
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session;
        const userId = session.metadata?.user_id;
        
        if (userId && session.subscription) {
          await (supabase
            .from('users') as any)
            .update({
              stripe_subscription_id: session.subscription as string,
              subscription_status: 'trialing',
              trial_ends_at: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString(),
            })
            .eq('id', userId);

          console.log(`✓ Subscription created for user: ${userId}`);
        }
        break;
      }

      // Suscripción creada
      case 'customer.subscription.created': {
        const subscription = event.data.object as Stripe.Subscription;
        const userId = subscription.metadata?.user_id;

        if (userId) {
          await (supabase
            .from('subscriptions') as any)
            .insert({
              user_id: userId,
              stripe_subscription_id: subscription.id,
              stripe_customer_id: subscription.customer as string,
              status: subscription.status,
              plan_type: subscription.metadata?.plan_type || 'starter',
              billing_interval: subscription.metadata?.billing_interval || 'monthly',
              current_period_start: new Date((subscription as any).current_period_start * 1000).toISOString(),
              current_period_end: new Date((subscription as any).current_period_end * 1000).toISOString(),
              cancel_at_period_end: (subscription as any).cancel_at_period_end,
            });

          console.log(`✓ Subscription record created: ${subscription.id}`);
        }
        break;
      }

      // Suscripción actualizada
      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription;

        await (supabase
          .from('subscriptions') as any)
          .update({
            status: subscription.status,
            current_period_start: new Date((subscription as any).current_period_start * 1000).toISOString(),
            current_period_end: new Date((subscription as any).current_period_end * 1000).toISOString(),
            cancel_at_period_end: (subscription as any).cancel_at_period_end,
            canceled_at: (subscription as any).canceled_at 
              ? new Date((subscription as any).canceled_at * 1000).toISOString() 
              : null,
          })
          .eq('stripe_subscription_id', subscription.id);

        // Actualizar estado en users
        const { data: subData } = await supabase
          .from('subscriptions')
          .select('user_id')
          .eq('stripe_subscription_id', subscription.id)
          .single();

        if (subData) {
          await (supabase
            .from('users') as any)
            .update({
              subscription_status: subscription.status,
            })
            .eq('id', (subData as any).user_id);
        }

        console.log(`✓ Subscription updated: ${subscription.id} - ${subscription.status}`);
        break;
      }

      // Suscripción eliminada
      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;

        await (supabase
          .from('subscriptions') as any)
          .update({
            status: 'canceled',
            canceled_at: new Date().toISOString(),
          })
          .eq('stripe_subscription_id', subscription.id);

        // Actualizar usuario
        const { data: subData } = await supabase
          .from('subscriptions')
          .select('user_id')
          .eq('stripe_subscription_id', subscription.id)
          .single();

        if (subData) {
          await (supabase
            .from('users') as any)
            .update({
              subscription_status: 'canceled',
              stripe_subscription_id: null,
            })
            .eq('id', (subData as any).user_id);
        }

        console.log(`✓ Subscription canceled: ${subscription.id}`);
        break;
      }

      // Pago exitoso
      case 'invoice.paid': {
        const invoice = event.data.object as Stripe.Invoice;
        
        if ((invoice as any).subscription) {
          await (supabase
            .from('payments') as any)
            .insert({
              stripe_invoice_id: invoice.id,
              stripe_subscription_id: (invoice as any).subscription as string,
              amount: (invoice as any).amount_paid,
              currency: invoice.currency,
              status: 'succeeded',
              paid_at: new Date((invoice as any).status_transitions.paid_at! * 1000).toISOString(),
            });

          console.log(`✓ Payment recorded: ${invoice.id} - €${invoice.amount_paid / 100}`);
        }
        break;
      }

      // Pago fallido
      case 'invoice.payment_failed': {
        const invoice = event.data.object as Stripe.Invoice;

        if ((invoice as any).subscription) {
          await (supabase
            .from('payments') as any)
            .insert({
              stripe_invoice_id: invoice.id,
              stripe_subscription_id: (invoice as any).subscription as string,
              amount: (invoice as any).amount_due,
              currency: invoice.currency,
              status: 'failed',
            });

          // Notificar al usuario
          const { data: subData } = await supabase
            .from('subscriptions')
            .select('user_id')
            .eq('stripe_subscription_id', (invoice as any).subscription)
            .single();

          if (subData) {
            // TODO: Enviar email de notificación
            console.log(`⚠️ Payment failed for user: ${(subData as any).user_id}`);
          }
        }
        break;
      }

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    return NextResponse.json({ received: true });

  } catch (error: any) {
    console.error('Error processing webhook:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
