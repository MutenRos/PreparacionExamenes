import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';

const PAYPAL_API_BASE = process.env.NEXT_PUBLIC_PAYPAL_ENVIRONMENT === 'production'
  ? 'https://api-m.paypal.com'
  : 'https://api-m.sandbox.paypal.com';

/**
 * Obtiene access token de PayPal
 */
async function getPayPalAccessToken(): Promise<string> {
  const clientId = process.env.NEXT_PUBLIC_PAYPAL_CLIENT_ID;
  const clientSecret = process.env.PAYPAL_CLIENT_SECRET;

  if (!clientId || !clientSecret) {
    throw new Error('PayPal credentials not configured');
  }

  const auth = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');

  const response = await fetch(`${PAYPAL_API_BASE}/v1/oauth2/token`, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${auth}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'grant_type=client_credentials',
  });

  const data = await response.json();
  return data.access_token;
}

/**
 * POST /api/paypal/capture-order
 * Captura el pago de una orden de PayPal y la registra en la base de datos
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { orderID } = body;

    if (!orderID) {
      return NextResponse.json(
        { error: 'Missing orderID' },
        { status: 400 }
      );
    }

    // Obtener access token
    const accessToken = await getPayPalAccessToken();

    // Capturar el pago en PayPal
    const captureResponse = await fetch(
      `${PAYPAL_API_BASE}/v2/checkout/orders/${orderID}/capture`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
      }
    );

    const captureData = await captureResponse.json();

    if (!captureResponse.ok) {
      console.error('PayPal capture failed:', captureData);
      return NextResponse.json(
        { error: 'Failed to capture PayPal payment', details: captureData },
        { status: 500 }
      );
    }

    // Verificar que el pago fue completado
    if (captureData.status !== 'COMPLETED') {
      return NextResponse.json(
        { error: 'Payment not completed', status: captureData.status },
        { status: 400 }
      );
    }

    // Extraer información del pago
    const purchaseUnit = captureData.purchase_units[0];
    const capture = purchaseUnit.payments.captures[0];
    const customData = JSON.parse(purchaseUnit.custom_id || '{}');

    const { userId, type, planId, billing, productId } = customData;
    const amount = parseFloat(capture.amount.value);
    const currency = capture.amount.currency_code;
    const transactionId = capture.id;

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

    // Guardar la compra en Supabase
    const supabase = await createClient();

    const { error: insertError } = await supabase
      .from('purchases')
      .insert({
        user_id: userId,
        type: type,
        plan_id: planId || null,
        billing_period: billing || null,
        product_id: productId || null,
        paypal_transaction_id: transactionId,
        paypal_payer_email: captureData.payer?.email_address,
        paypal_payer_id: captureData.payer?.payer_id,
        amount: amount,
        currency: currency,
        status: 'completed',
        completed_at: capture.create_time,
        expires_at: expiresAt,
        metadata: {
          order_id: orderID,
          capture_status: capture.status,
        }
      });

    if (insertError) {
      console.error('Error saving purchase to database:', insertError);
      // El pago fue capturado en PayPal pero no se guardó en DB
      // TODO: Implementar retry logic o notificación al admin
      return NextResponse.json(
        { 
          success: true,
          warning: 'Payment captured but database save failed',
          orderID,
          transactionId 
        },
        { status: 200 }
      );
    }

    console.log(`✅ Payment captured and saved: ${transactionId} - User: ${userId}`);

    return NextResponse.json({
      success: true,
      orderID,
      transactionId,
      status: 'completed',
      amount,
      currency,
    });

  } catch (error) {
    console.error('Error capturing PayPal payment:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
