import { NextRequest, NextResponse } from 'next/server';

const PAYPAL_API_BASE = process.env.NEXT_PUBLIC_PAYPAL_ENVIRONMENT === 'production'
  ? 'https://api-m.paypal.com'
  : 'https://api-m.sandbox.paypal.com';

/**
 * Obtiene access token de PayPal para autenticar requests
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
 * POST /api/paypal/create-order
 * Crea una orden de pago en PayPal
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { type, planId, billing, productId, amount, userId } = body;

    if (!amount || !userId) {
      return NextResponse.json(
        { error: 'Missing required fields: amount, userId' },
        { status: 400 }
      );
    }

    // Obtener access token
    const accessToken = await getPayPalAccessToken();

    // Preparar metadata para la orden
    const customId = JSON.stringify({
      userId,
      type,
      planId,
      billing,
      productId,
      timestamp: new Date().toISOString()
    });

    // Crear orden en PayPal
    const orderResponse = await fetch(`${PAYPAL_API_BASE}/v2/checkout/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        intent: 'CAPTURE',
        purchase_units: [{
          amount: {
            currency_code: 'EUR',
            value: amount.toFixed(2),
          },
          custom_id: customId,
          description: type === 'subscription'
            ? `Suscripción ${planId} - ${billing}`
            : `Producto ${productId}`,
        }],
        application_context: {
          brand_name: 'CodeAcademy',
          landing_page: 'NO_PREFERENCE',
          user_action: 'PAY_NOW',
          return_url: `${process.env.NEXT_PUBLIC_APP_URL}/payment/success`,
          cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/checkout?plan=${planId || ''}&product=${productId || ''}`,
        },
      }),
    });

    const orderData = await orderResponse.json();

    if (!orderResponse.ok) {
      console.error('PayPal order creation failed:', orderData);
      return NextResponse.json(
        { error: 'Failed to create PayPal order', details: orderData },
        { status: 500 }
      );
    }

    return NextResponse.json({
      orderID: orderData.id,
      status: orderData.status,
    });

  } catch (error) {
    console.error('Error creating PayPal order:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
