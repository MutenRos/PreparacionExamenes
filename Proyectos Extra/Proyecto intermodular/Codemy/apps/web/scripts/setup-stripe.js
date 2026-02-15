#!/usr/bin/env node

/**
 * Script: Setup de Productos Stripe
 * Crea productos y precios en Stripe para CodeAcademy
 * 
 * Uso: node scripts/setup-stripe.js
 */

import { stripe, setupStripeProducts, setupStripePrices } from '../src/lib/stripe.ts';

async function main() {
  console.log('🚀 Configurando productos de Stripe para CodeAcademy...\n');

  try {
    // 1. Crear productos
    console.log('📦 Creando productos...');
    const productIds = await setupStripeProducts();
    console.log(`✅ ${Object.keys(productIds).length} productos configurados\n`);

    // 2. Crear precios
    console.log('💰 Creando precios...');
    const priceIds = await setupStripePrices(productIds);
    console.log(`✅ ${Object.keys(priceIds).length} precios configurados\n`);

    // 3. Mostrar IDs para variables de entorno
    console.log('📋 IDs de Precios (agregar a .env.local):');
    console.log('─'.repeat(60));
    
    Object.entries(priceIds).forEach(([key, id]) => {
      const envKey = `NEXT_PUBLIC_PRICE_${key.toUpperCase()}`;
      console.log(`${envKey}=${id}`);
    });

    console.log('\n✨ Configuración completada exitosamente!');
    
  } catch (error) {
    console.error('❌ Error durante la configuración:', error);
    process.exit(1);
  }
}

main();
