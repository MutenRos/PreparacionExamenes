/**
 * Component: SubscriptionManager
 * Panel de gestión de suscripción en el dashboard
 */

'use client';

import { useEffect, useState } from 'react';
import { useStripe } from '@/hooks/useStripe';
import { 
  CreditCard, 
  Calendar, 
  AlertCircle, 
  CheckCircle,
  XCircle 
} from 'lucide-react';

interface Subscription {
  id: string;
  plan_type: string;
  billing_interval: string;
  status: string;
  current_period_end: string;
  cancel_at_period_end: boolean;
  stripe_details?: {
    current_period_end: Date;
    cancel_at_period_end: boolean;
    canceled_at: Date | null;
  };
}

interface SubscriptionManagerProps {
  userId: string;
}

export function SubscriptionManager({ userId }: SubscriptionManagerProps) {
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [loading, setLoading] = useState(true);
  const { openBillingPortal, cancelSubscription, loading: actionLoading } = useStripe();

  useEffect(() => {
    fetchSubscription();
  }, [userId]);

  const fetchSubscription = async () => {
    try {
      const response = await fetch(`/api/subscription?userId=${userId}`);
      const data = await response.json();
      setSubscription(data.subscription);
    } catch (error) {
      console.error('Error fetching subscription:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleManageBilling = async () => {
    await openBillingPortal(userId);
  };

  const handleCancelSubscription = async () => {
    if (!confirm('¿Estás seguro de que quieres cancelar tu suscripción?')) {
      return;
    }

    try {
      await cancelSubscription(userId, false);
      await fetchSubscription();
    } catch (error) {
      console.error('Error canceling subscription:', error);
    }
  };

  if (loading) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <div className="animate-pulse">
          <div className="h-6 w-32 rounded bg-gray-200" />
          <div className="mt-4 h-4 w-full rounded bg-gray-200" />
        </div>
      </div>
    );
  }

  if (!subscription) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <div className="flex items-start gap-4">
          <AlertCircle className="h-6 w-6 text-yellow-500" />
          <div>
            <h3 className="font-semibold text-gray-900">Sin suscripción activa</h3>
            <p className="mt-1 text-sm text-gray-600">
              Suscríbete para acceder a todo el contenido de CodeAcademy
            </p>
            <a
              href="/pricing"
              className="mt-4 inline-block rounded-lg bg-stone-600 px-4 py-2 text-sm font-semibold text-white hover:bg-stone-700"
            >
              Ver Planes
            </a>
          </div>
        </div>
      </div>
    );
  }

  const getStatusBadge = (status: string) => {
    const badges: Record<string, { text: string; color: string; icon: any }> = {
      active: { text: 'Activa', color: 'bg-green-100 text-green-800', icon: CheckCircle },
      trialing: { text: 'En Prueba', color: 'bg-stone-100 text-stone-800', icon: CheckCircle },
      past_due: { text: 'Pago Pendiente', color: 'bg-yellow-100 text-yellow-800', icon: AlertCircle },
      canceled: { text: 'Cancelada', color: 'bg-gray-100 text-gray-800', icon: XCircle },
      incomplete: { text: 'Incompleta', color: 'bg-red-100 text-red-800', icon: AlertCircle },
    };

    const badge = badges[status] || badges.active;
    const Icon = badge.icon;

    return (
      <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium ${badge.color}`}>
        <Icon className="h-4 w-4" />
        {badge.text}
      </span>
    );
  };

  const getPlanName = (planType: string) => {
    const plans: Record<string, string> = {
      starter: 'Plan Starter',
      pro: 'Plan Pro',
      familia: 'Plan Familia',
    };
    return plans[planType] || planType;
  };

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Suscripción Actual</h3>
          <p className="mt-1 text-sm text-gray-600">
            Gestiona tu plan y métodos de pago
          </p>
        </div>
        {getStatusBadge(subscription.status)}
      </div>

      <div className="mt-6 space-y-4">
        {/* Plan Info */}
        <div className="flex items-center gap-3 rounded-lg bg-gray-50 p-4">
          <CreditCard className="h-5 w-5 text-gray-600" />
          <div>
            <p className="font-medium text-gray-900">
              {getPlanName(subscription.plan_type)}
            </p>
            <p className="text-sm text-gray-600 capitalize">
              Facturación {subscription.billing_interval === 'monthly' ? 'mensual' : 'anual'}
            </p>
          </div>
        </div>

        {/* Renewal Date */}
        <div className="flex items-center gap-3 rounded-lg bg-gray-50 p-4">
          <Calendar className="h-5 w-5 text-gray-600" />
          <div>
            <p className="font-medium text-gray-900">
              {subscription.stripe_details?.cancel_at_period_end
                ? 'Termina el'
                : 'Próxima renovación'}
            </p>
            <p className="text-sm text-gray-600">
              {new Date(subscription.current_period_end).toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </p>
          </div>
        </div>

        {/* Cancelation Notice */}
        {subscription.stripe_details?.cancel_at_period_end && (
          <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-4">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-5 w-5 shrink-0 text-yellow-600" />
              <div>
                <p className="font-medium text-yellow-900">
                  Suscripción programada para cancelación
                </p>
                <p className="mt-1 text-sm text-yellow-700">
                  Tu plan terminará el{' '}
                  {new Date(subscription.current_period_end).toLocaleDateString('es-ES')}
                  . Puedes reactivarlo en cualquier momento.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="mt-6 flex gap-3">
        <button
          onClick={handleManageBilling}
          disabled={actionLoading}
          className="flex-1 rounded-lg border border-gray-300 bg-white px-4 py-2 font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          Gestionar Facturación
        </button>
        
        {!subscription.stripe_details?.cancel_at_period_end && (
          <button
            onClick={handleCancelSubscription}
            disabled={actionLoading}
            className="rounded-lg border border-red-300 bg-white px-4 py-2 font-medium text-red-600 hover:bg-red-50 disabled:opacity-50"
          >
            Cancelar Plan
          </button>
        )}
      </div>
    </div>
  );
}
