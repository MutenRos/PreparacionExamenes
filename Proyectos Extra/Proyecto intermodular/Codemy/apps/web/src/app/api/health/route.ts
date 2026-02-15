/**
 * API Route: Health Check
 * GET /api/health
 * Verifica el estado de la aplicación y servicios
 */

import { NextResponse } from 'next/server';
import { createClient } from '@codeacademy/database/client';
import { stripe } from '@/lib/stripe';

export async function GET() {
  const checks = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    services: {
      database: 'unknown',
      stripe: 'unknown',
    },
    version: process.env.npm_package_version || '1.0.0',
    environment: process.env.NODE_ENV,
  };

  try {
    // Check Supabase
    const supabase = createClient();
    const { error: dbError } = await supabase.from('users').select('count').limit(1);
    checks.services.database = dbError ? 'error' : 'ok';
  } catch (error) {
    checks.services.database = 'error';
    checks.status = 'degraded';
  }

  try {
    // Check Stripe
    await stripe.products.list({ limit: 1 });
    checks.services.stripe = 'ok';
  } catch (error) {
    checks.services.stripe = 'error';
    checks.status = 'degraded';
  }

  // Overall status
  if (checks.services.database === 'error' || checks.services.stripe === 'error') {
    checks.status = 'degraded';
  }

  const statusCode = checks.status === 'ok' ? 200 : 503;

  return NextResponse.json(checks, { status: statusCode });
}
