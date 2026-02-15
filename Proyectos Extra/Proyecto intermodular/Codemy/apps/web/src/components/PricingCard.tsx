/**
 * Component: PricingCard
 * Tarjeta de plan con integración Stripe
 */

'use client';

import { Check } from 'lucide-react';
import { useStripe } from '@/hooks/useStripe';
import { useState } from 'react';

interface PricingCardProps {
  name: string;
  description: string;
  price: {
    monthly: number;
    yearly: number;
  };
  priceIds: {
    monthly: string;
    yearly: string;
  };
  features: string[];
  popular?: boolean;
  planType: 'starter' | 'pro' | 'familia';
  userId?: string;
}

export function PricingCard({
  name,
  description,
  price,
  priceIds,
  features,
  popular = false,
  planType,
  userId,
}: PricingCardProps) {
  const [billingInterval, setBillingInterval] = useState<'monthly' | 'yearly'>('monthly');
  const { createCheckoutSession, loading } = useStripe();

  const currentPrice = billingInterval === 'monthly' ? price.monthly : price.yearly;
  const currentPriceId = billingInterval === 'monthly' ? priceIds.monthly : priceIds.yearly;

  const handleSubscribe = async () => {
    if (!userId) {
      // Redirigir a login/registro
      window.location.href = '/auth/signup';
      return;
    }

    await createCheckoutSession({
      priceId: currentPriceId,
      userId,
      planType,
      billingInterval,
    });
  };

  return (
    <div
      className={`relative rounded-2xl border-2 p-8 ${
        popular
          ? 'border-stone-500 bg-gradient-to-br from-stone-50 to-white shadow-xl scale-105'
          : 'border-gray-200 bg-white'
      }`}
    >
      {popular && (
        <div className="absolute -top-4 left-1/2 -translate-x-1/2 rounded-full bg-white text-black px-4 py-1 text-sm font-semibold">
          Más Popular
        </div>
      )}

      <div className="mb-6">
        <h3 className="text-2xl font-bold text-gray-900">{name}</h3>
        <p className="mt-2 text-gray-600">{description}</p>
      </div>

      {/* Selector de intervalo */}
      <div className="mb-6 flex gap-2 rounded-lg bg-gray-100 p-1">
        <button
          onClick={() => setBillingInterval('monthly')}
          className={`flex-1 rounded-md px-4 py-2 text-sm font-medium transition-colors ${
            billingInterval === 'monthly'
              ? 'bg-white text-gray-900 shadow'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Mensual
        </button>
        <button
          onClick={() => setBillingInterval('yearly')}
          className={`flex-1 rounded-md px-4 py-2 text-sm font-medium transition-colors ${
            billingInterval === 'yearly'
              ? 'bg-white text-gray-900 shadow'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Anual
          <span className="ml-1 text-xs text-green-600">-16%</span>
        </button>
      </div>

      {/* Precio */}
      <div className="mb-6">
        <div className="flex items-baseline gap-2">
          <span className="text-4xl font-bold text-gray-900">
            €{currentPrice}
          </span>
          <span className="text-gray-600">
            /{billingInterval === 'monthly' ? 'mes' : 'año'}
          </span>
        </div>
        {billingInterval === 'yearly' && (
          <p className="mt-1 text-sm text-green-600">
            €{price.monthly} al mes, facturado anualmente
          </p>
        )}
        <p className="mt-2 text-sm text-gray-500">
          14 días de prueba gratuita
        </p>
      </div>

      {/* Features */}
      <ul className="mb-8 space-y-3">
        {features.map((feature, index) => (
          <li key={index} className="flex items-start gap-3">
            <Check className="h-5 w-5 shrink-0 text-green-500" />
            <span className="text-gray-700">{feature}</span>
          </li>
        ))}
      </ul>

      {/* CTA Button */}
      <button
        onClick={handleSubscribe}
        disabled={loading}
        className={`w-full rounded-lg px-6 py-3 font-semibold transition-all ${
          popular
            ? 'bg-white text-black hover:bg-white/90 shadow-lg hover:shadow-xl'
            : 'bg-gray-900 text-white hover:bg-gray-800'
        } disabled:opacity-50 disabled:cursor-not-allowed`}
      >
        {loading ? 'Procesando...' : 'Comenzar Prueba Gratuita'}
      </button>
    </div>
  );
}
