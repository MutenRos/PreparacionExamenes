import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';

/**
 * PayPal Webhook Handler - Instant Payment Notification (IPN)
 * 
 * Este endpoint recibe notificaciones de PayPal cuando se completan pagos.
 * 
 * CONFIGURACIÓN NECESARIA EN PAYPAL:
 * 1. Ir a https://developer.paypal.com/dashboard/
 * 2. Tu App → Webhooks
 * 3. Añadir webhook URL: https://tudominio.com/api/webhooks/paypal
 * 4. Seleccionar eventos: "Payment capture completed", "Payment sale completed"
 * 
 * NOTA: paypal.me no envía webhooks automáticamente. Opciones:
 * - Usar PayPal Buttons SDK (recomendado para webhooks automáticos)
 * - Usar IPN manual verificando transacciones periódicamente
 * - Implementar página de retorno donde usuario confirma pago
 */

interface PayPalWebhookEvent {
  event_type: string;
  resource: {
    id: string; // Transaction ID
    amount: {
      total: string;
      currency: string;
    };
    custom?: string; // Aquí enviaremos user_id, plan_id, product_id
    payer: {
      email_address?: string;
      payer_id?: string;
    };
    status: string;
    create_time: string;
  };
}

export async function POST(request: NextRequest) {
  try {
    const body: PayPalWebhookEvent = await request.json();
    
    console.log('PayPal Webhook recibido:', body.event_type);

    // Verificar que es un evento de pago completado
    if (!['PAYMENT.CAPTURE.COMPLETED', 'PAYMENT.SALE.COMPLETED'].includes(body.event_type)) {
      return NextResponse.json({ message: 'Event type not handled' }, { status: 200 });
    }

    // Extraer datos del pago
    const { resource } = body;
    const transactionId = resource.id;
    const amount = parseFloat(resource.amount.total);
    const currency = resource.amount.currency;
    
    // Parsear metadata custom (formato: "userId:planId:billing" o "userId:productId")
    const customData = resource.custom ? JSON.parse(resource.custom) : {};
    const { userId, type, planId, billing, productId } = customData;

    if (!userId) {
      console.error('No userId en webhook PayPal');
      return NextResponse.json({ error: 'Missing userId' }, { status: 400 });
    }

    // Crear cliente Supabase
    const supabase = await createClient();

    // Verificar si ya existe esta transacción (prevenir duplicados)
    const { data: existing } = await supabase
      .from('purchases')
      .select('id')
      .eq('paypal_transaction_id', transactionId)
      .single();

    if (existing) {
      console.log('Transacción ya procesada:', transactionId);
      return NextResponse.json({ message: 'Already processed' }, { status: 200 });
    }

    // Calcular fecha de expiración para suscripciones
    let expiresAt = null;
    if (type === 'subscription') {
      const now = new Date();
      if (billing === 'monthly') {
        expiresAt = new Date(now.setMonth(now.getMonth() + 1)).toISOString();
      } else if (billing === 'yearly') {
        expiresAt = new Date(now.setFullYear(now.getFullYear() + 1)).toISOString();
      }
    }

    // Insertar compra en base de datos
    const { error: insertError } = await supabase
      .from('purchases')
      .insert({
        user_id: userId,
        type: type,
        plan_id: planId || null,
        billing_period: billing || null,
        product_id: productId || null,
        paypal_transaction_id: transactionId,
        paypal_payer_email: resource.payer.email_address,
        paypal_payer_id: resource.payer.payer_id,
        amount: amount,
        currency: currency,
        status: 'completed',
        completed_at: resource.create_time,
        expires_at: expiresAt,
        metadata: {
          event_type: body.event_type,
          payment_status: resource.status
        }
      });

    if (insertError) {
      console.error('Error insertando purchase:', insertError);
      return NextResponse.json({ error: 'Database error' }, { status: 500 });
    }

    console.log(`✅ Pago procesado: ${transactionId} - User: ${userId} - Amount: ${amount} ${currency}`);

    return NextResponse.json({ 
      success: true, 
      message: 'Payment processed successfully' 
    });

  } catch (error) {
    console.error('Error procesando webhook PayPal:', error);
    return NextResponse.json({ 
      error: 'Internal server error' 
    }, { status: 500 });
  }
}

// Endpoint GET para verificación de health
export async function GET() {
  return NextResponse.json({ 
    status: 'active',
    endpoint: 'paypal-webhook',
    note: 'Configure this URL in PayPal Developer Dashboard'
  });
}
