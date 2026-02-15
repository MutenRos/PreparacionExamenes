/**
 * Configuración de Stripe para CodeAcademy
 * Gestión de suscripciones, pagos y billing
 */

import Stripe from 'stripe';

// Cliente de Stripe (servidor)
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || '', {
  apiVersion: '2025-10-29.clover',
  typescript: true,
});

// Configuración de productos y precios
export const STRIPE_CONFIG = {
  products: {
    starter: {
      name: 'Plan Starter',
      description: '1 estudiante - Acceso completo a la plataforma',
      metadata: {
        plan_type: 'starter',
        max_students: '1',
      },
    },
    pro: {
      name: 'Plan Pro',
      description: '1 estudiante - Acceso premium con talleres en vivo',
      metadata: {
        plan_type: 'pro',
        max_students: '1',
        includes_workshops: 'true',
      },
    },
    familia: {
      name: 'Plan Familia',
      description: 'Hasta 4 estudiantes - Acceso completo + panel parental',
      metadata: {
        plan_type: 'familia',
        max_students: '4',
        includes_workshops: 'true',
        parent_dashboard: 'true',
      },
    },
  },
  prices: {
    starter_monthly: {
      unit_amount: 1990, // €19.90
      currency: 'eur',
      recurring: { interval: 'month' },
      product: 'starter',
    },
    starter_yearly: {
      unit_amount: 19900, // €199/año (ahorro 16%)
      currency: 'eur',
      recurring: { interval: 'year' },
      product: 'starter',
    },
    pro_monthly: {
      unit_amount: 3990, // €39.90
      currency: 'eur',
      recurring: { interval: 'month' },
      product: 'pro',
    },
    pro_yearly: {
      unit_amount: 39900, // €399/año (ahorro 16%)
      currency: 'eur',
      recurring: { interval: 'year' },
      product: 'pro',
    },
    familia_monthly: {
      unit_amount: 7990, // €79.90
      currency: 'eur',
      recurring: { interval: 'month' },
      product: 'familia',
    },
    familia_yearly: {
      unit_amount: 79900, // €799/año (ahorro 16%)
      currency: 'eur',
      recurring: { interval: 'year' },
      product: 'familia',
    },
  },
  // Complementos (add-ons)
  addons: {
    extra_student: {
      name: 'Estudiante Adicional',
      description: 'Añade un estudiante extra a tu plan Familia',
      unit_amount: 1500, // €15/mes
      currency: 'eur',
      recurring: { interval: 'month' },
    },
    tutoring_hours: {
      name: 'Horas de Tutoría',
      description: 'Pack de 4 horas de tutoría personalizada',
      unit_amount: 9900, // €99 (one-time)
      currency: 'eur',
    },
    certificate: {
      name: 'Certificado Oficial',
      description: 'Certificado de finalización verificado',
      unit_amount: 2900, // €29 (one-time)
      currency: 'eur',
    },
  },
} as const;

// Trial configuration
export const TRIAL_DAYS = 14;

/**
 * Crea o actualiza productos en Stripe
 */
export async function setupStripeProducts() {
  const products = STRIPE_CONFIG.products;
  const createdProducts: Record<string, string> = {};

  for (const [key, productData] of Object.entries(products)) {
    const existingProducts = await stripe.products.list({
      limit: 100,
    });

    const existing = existingProducts.data.find(
      (p) => p.metadata.plan_type === productData.metadata.plan_type
    );

    if (existing) {
      createdProducts[key] = existing.id;
      console.log(`✓ Producto existente: ${productData.name} (${existing.id})`);
    } else {
      const product = await stripe.products.create({
        name: productData.name,
        description: productData.description,
        metadata: productData.metadata,
      });
      createdProducts[key] = product.id;
      console.log(`✓ Producto creado: ${productData.name} (${product.id})`);
    }
  }

  return createdProducts;
}

/**
 * Crea precios para los productos
 */
export async function setupStripePrices(productIds: Record<string, string>) {
  const prices = STRIPE_CONFIG.prices;
  const createdPrices: Record<string, string> = {};

  for (const [key, priceData] of Object.entries(prices)) {
    const productKey = priceData.product as keyof typeof productIds;
    const productId = productIds[productKey];

    if (!productId) {
      console.error(`❌ Producto no encontrado para: ${key}`);
      continue;
    }

    const price = await stripe.prices.create({
      product: productId,
      unit_amount: priceData.unit_amount,
      currency: priceData.currency,
      recurring: priceData.recurring,
      metadata: {
        price_type: key,
      },
    });

    createdPrices[key] = price.id;
    console.log(`✓ Precio creado: ${key} (${price.id})`);
  }

  return createdPrices;
}

/**
 * Formatea precio para mostrar
 */
export function formatPrice(amount: number, currency: string = 'eur'): string {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: currency.toUpperCase(),
    minimumFractionDigits: 0,
  }).format(amount / 100);
}

/**
 * Calcula ahorro anual
 */
export function calculateYearlySavings(monthlyPrice: number, yearlyPrice: number): number {
  const monthlyTotal = monthlyPrice * 12;
  const savings = monthlyTotal - yearlyPrice;
  return Math.round((savings / monthlyTotal) * 100);
}
