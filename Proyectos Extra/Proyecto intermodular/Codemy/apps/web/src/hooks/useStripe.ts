/**
 * Hook: useStripe
 * Manejo de checkout y billing de Stripe
 */

'use client';

import { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY || ''
);

export interface CheckoutParams {
  priceId: string;
  userId: string;
  planType: 'starter' | 'pro' | 'familia';
  billingInterval: 'monthly' | 'yearly';
}

export function useStripe() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createCheckoutSession = async (params: CheckoutParams) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/stripe/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Error creating checkout session');
      }

      const stripe = await stripePromise;
      
      if (!stripe) {
        throw new Error('Stripe not loaded');
      }

      // Redirigir a Stripe Checkout
      if (data.url) {
        window.location.href = data.url;
      }

    } catch (err: any) {
      setError(err.message);
      console.error('Checkout error:', err);
    } finally {
      setLoading(false);
    }
  };

  const openBillingPortal = async (userId: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/stripe/portal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Error opening billing portal');
      }

      if (data.url) {
        window.location.href = data.url;
      }

    } catch (err: any) {
      setError(err.message);
      console.error('Portal error:', err);
    } finally {
      setLoading(false);
    }
  };

  const cancelSubscription = async (userId: string, immediately: boolean = false) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/subscription', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, immediately }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Error canceling subscription');
      }

      return data;

    } catch (err: any) {
      setError(err.message);
      console.error('Cancel error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    createCheckoutSession,
    openBillingPortal,
    cancelSubscription,
    loading,
    error,
  };
}
