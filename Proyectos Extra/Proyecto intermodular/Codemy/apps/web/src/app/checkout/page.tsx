'use client';

import { useEffect, useState, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Navigation } from '@/components/Navigation';
import { Footer } from '@/components/Footer';
import { Check, ArrowRight, Shield, Lock } from 'lucide-react';
import { PayPalScriptProvider, PayPalButtons } from '@paypal/react-paypal-js';

function CheckoutContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  
  const planId = searchParams.get('plan');
  const billing = searchParams.get('billing') || 'monthly';
  const productId = searchParams.get('product');

  // Obtener usuario autenticado
  useEffect(() => {
    async function getUser() {
      // TODO: Implementar cuando se configure Supabase
      // Por ahora, asumimos que el usuario está logueado
      setUserId('temp-user-id');
    }
    getUser();
  }, []);

  const plans = {
    starter: {
      name: 'Starter',
      monthlyPrice: 4.99,
      yearlyPrice: 49,
      features: [
        'Acceso a 1 track (Web, Datos o Juegos)',
        'Retos semanales',
        'Sistema XP y ranking básico',
        'Certificados internos por módulo',
        'Soporte por email'
      ]
    },
    pro: {
      name: 'Pro',
      monthlyPrice: 9.99,
      yearlyPrice: 99,
      features: [
        'Acceso a TODOS los tracks',
        'Proyectos guiados avanzados',
        'Autocorrección avanzada con IA',
        'Ranking global y competencias',
        'Mentoría grupal (2 sesiones/mes)',
        'Certificados oficiales verificables'
      ]
    },
    family: {
      name: 'Pro Familia',
      monthlyPrice: 19.99,
      yearlyPrice: 199,
      features: [
        'Hasta 3 perfiles (infantiles/teens)',
        'Panel parental completo',
        'Control de tiempo de sesión',
        'Todos los beneficios Pro',
        'Gestión familiar centralizada'
      ]
    }
  };

  const products = {
    'python': { name: 'Python & IA', price: 49.99 },
    'cpp': { name: 'C++ Completo', price: 29.99 },
    'web': { name: 'Web Full-Stack', price: 44.99 },
    'java': { name: 'Java Completo', price: 34.99 },
    'devops': { name: 'DevOps Pro', price: 39.99 },
    'security': { name: 'Ciberseguridad', price: 34.99 },
    'mobile': { name: 'Mobile Development', price: 34.99 },
    'arduino': { name: 'Arduino & IoT', price: 29.99 },
    'raspberry': { name: 'Raspberry Pi Server', price: 14.99 },
    '3d': { name: 'Diseño 3D', price: 24.99 },
    'pack': { name: 'Pack Completo (10 Skill Trees)', price: 249.99 }
  };

  const selectedPlan = planId ? plans[planId as keyof typeof plans] : null;
  const selectedProduct = productId ? products[productId as keyof typeof products] : null;

  const isYearly = billing === 'yearly';
  const price = selectedPlan 
    ? (isYearly ? selectedPlan.yearlyPrice : selectedPlan.monthlyPrice)
    : (selectedProduct?.price || 0);

  const handlePayPalRedirect = () => {
    setLoading(true);
    
    // Si no hay usuario autenticado, guardar en localStorage y redirigir a login
    if (!userId) {
      const checkoutData = {
        plan: planId,
        billing: billing,
        product: productId,
        returnTo: '/checkout'
      };
      localStorage.setItem('checkout_pending', JSON.stringify(checkoutData));
      router.push('/auth/login?redirectTo=/checkout');
      return;
    }
    
    // Guardar información del pedido en localStorage (fallback)
    const orderData = {
      timestamp: new Date().toISOString(),
      type: selectedPlan ? 'subscription' : 'product',
      plan: planId,
      billing: billing,
      product: productId,
      price: price,
      status: 'pending',
      userId: userId
    };
    
    localStorage.setItem('pending_order', JSON.stringify(orderData));
    
    // NOTA: Este código se mantiene como fallback para paypal.me
    // Si no tienes credenciales de PayPal configuradas, redirige a paypal.me
    window.location.href = `https://paypal.me/mutenros/${price.toFixed(2)}`;
  };

  if (!selectedPlan && !selectedProduct) {
    return (
      <>
        <Navigation />
        <div className="min-h-screen bg-gradient-to-br from-stone-950 via-stone-900 to-stone-950 pt-20">
          <div className="max-w-2xl mx-auto px-4 py-16 text-center">
            <h1 className="text-3xl font-bold text-white mb-4">
              No se seleccionó ningún plan o producto
            </h1>
            <button
              onClick={() => router.push('/#pricing')}
              className="bg-gradient-to-r from-amber-600 to-orange-600 text-white px-8 py-3 rounded-xl font-bold hover:from-amber-700 hover:to-orange-700 transition-all"
            >
              Volver a Precios
            </button>
          </div>
        </div>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Navigation />
      <PayPalScriptProvider
        options={{
          clientId: process.env.NEXT_PUBLIC_PAYPAL_CLIENT_ID || 'sb',
          currency: 'EUR',
          intent: 'capture',
        }}
      >
        <div className="min-h-screen bg-gradient-to-br from-stone-950 via-stone-900 to-stone-950 pt-20">
          <div className="max-w-4xl mx-auto px-4 py-16">
            
            {/* Header */}
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold text-white mb-4">
                Completa tu compra
              </h1>
              <p className="text-stone-400 text-lg">
                Seguro y cifrado - Procesado por PayPal
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
            
            {/* Order Summary */}
            <div className="bg-stone-900/50 backdrop-blur-sm border border-stone-800 rounded-2xl p-8">
              <h2 className="text-2xl font-bold text-white mb-6">Resumen del pedido</h2>
              
              {selectedPlan && (
                <>
                  <div className="mb-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-bold text-white">{selectedPlan.name}</h3>
                        <p className="text-stone-400 text-sm">
                          {isYearly ? 'Suscripción Anual' : 'Suscripción Mensual'}
                        </p>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-white">€{price}</div>
                        <div className="text-stone-400 text-sm">
                          {isYearly ? '/año' : '/mes'}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="border-t border-stone-700 pt-6 mb-6">
                    <h4 className="text-sm font-bold text-stone-300 mb-3">Incluye:</h4>
                    <ul className="space-y-2">
                      {selectedPlan.features.map((feature, index) => (
                        <li key={index} className="flex items-start space-x-2 text-sm text-stone-400">
                          <Check className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                          <span>{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </>
              )}

              {selectedProduct && (
                <>
                  <div className="mb-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-bold text-white">{selectedProduct.name}</h3>
                        <p className="text-stone-400 text-sm">Pago único - Acceso de por vida</p>
                      </div>
                      <div className="text-2xl font-bold text-white">€{price}</div>
                    </div>
                  </div>
                </>
              )}

              <div className="border-t border-stone-700 pt-6">
                <div className="flex justify-between items-center text-lg">
                  <span className="font-bold text-white">Total a pagar:</span>
                  <span className="text-2xl font-bold text-white">€{price.toFixed(2)}</span>
                </div>
                {isYearly && selectedPlan && (
                  <p className="text-green-600 text-sm mt-2 text-right">
                    Ahorras €{((selectedPlan.monthlyPrice * 12) - selectedPlan.yearlyPrice).toFixed(2)} al año
                  </p>
                )}
              </div>
            </div>

            {/* Payment Method */}
            <div>
              <div className="bg-stone-900/50 backdrop-blur-sm border border-stone-800 rounded-2xl p-8 mb-6">
                <h2 className="text-2xl font-bold text-white mb-6">Método de pago</h2>
                
                <div className="bg-blue-900/20 border-2 border-blue-600/30 rounded-xl p-6 mb-6">
                  <div className="flex items-center space-x-4 mb-4">
                    <div className="bg-blue-600 rounded-lg p-3">
                      <svg className="w-8 h-8 text-white" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M7.076 21.337H2.47a.641.641 0 0 1-.633-.74L4.944.901C5.026.382 5.474 0 5.998 0h7.46c2.57 0 4.578.543 5.69 1.81 1.01 1.15 1.304 2.42 1.012 4.287-.023.143-.047.288-.077.437-.983 5.05-4.349 6.797-8.647 6.797h-2.19c-.524 0-.968.382-1.05.9l-1.12 7.106zm14.146-14.42a3.35 3.35 0 0 0-.607-.541c-.013.076-.026.175-.041.254-.93 4.778-4.005 7.201-9.138 7.201h-2.19a.563.563 0 0 0-.556.479l-1.187 7.527h-.506l-.24 1.516a.56.56 0 0 0 .554.647h3.882c.46 0 .85-.334.922-.788.06-.26.76-4.852.76-4.852a.932.932 0 0 1 .923-.788h.58c3.76 0 6.705-1.528 7.565-5.946.36-1.847.174-3.388-.746-4.46z"/>
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-white font-bold">PayPal</h3>
                      <p className="text-stone-400 text-sm">Pago seguro y rápido</p>
                    </div>
                  </div>
                  <p className="text-stone-300 text-sm mb-4">
                    Completa tu pago de forma segura con PayPal.
                  </p>
                </div>

                {/* PayPal Buttons */}
                {userId && process.env.NEXT_PUBLIC_PAYPAL_CLIENT_ID && (
                  <div className="mb-4">
                    <PayPalButtons
                      createOrder={async () => {
                        const response = await fetch('/api/paypal/create-order', {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({
                            type: selectedPlan ? 'subscription' : 'product',
                            planId,
                            billing,
                            productId,
                            amount: price,
                            userId,
                          }),
                        });
                        const data = await response.json();
                        return data.orderID;
                      }}
                      onApprove={async (data) => {
                        setLoading(true);
                        const response = await fetch('/api/paypal/capture-order', {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({ orderID: data.orderID }),
                        });
                        const result = await response.json();
                        
                        if (result.success) {
                          router.push('/payment/success');
                        } else {
                          alert('Error procesando el pago. Contacta con soporte.');
                          setLoading(false);
                        }
                      }}
                      onError={(err) => {
                        console.error('PayPal error:', err);
                        alert('Error con PayPal. Intenta de nuevo.');
                        setLoading(false);
                      }}
                      style={{
                        layout: 'vertical',
                        color: 'gold',
                        shape: 'rect',
                        label: 'paypal',
                      }}
                    />
                  </div>
                )}

                {/* Fallback button for paypal.me */}
                {(!process.env.NEXT_PUBLIC_PAYPAL_CLIENT_ID) && (
                  <button
                    onClick={handlePayPalRedirect}
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-amber-600 to-orange-600 text-white px-8 py-4 rounded-xl font-bold hover:from-amber-700 hover:to-orange-700 transition-all shadow-lg flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? (
                      <span>Redirigiendo...</span>
                    ) : (
                      <>
                        <span>Pagar con PayPal</span>
                        <ArrowRight className="w-5 h-5" />
                      </>
                    )}
                  </button>
                )}
              </div>

              {/* Security Info */}
              <div className="space-y-3">
                <div className="flex items-center space-x-3 text-stone-400 text-sm">
                  <Shield className="w-5 h-5 text-green-600" />
                  <span>Pago 100% seguro y encriptado</span>
                </div>
                <div className="flex items-center space-x-3 text-stone-400 text-sm">
                  <Lock className="w-5 h-5 text-green-600" />
                  <span>Protección del comprador de PayPal</span>
                </div>
                <div className="flex items-center space-x-3 text-stone-400 text-sm">
                  <Check className="w-5 h-5 text-green-600" />
                  <span>Garantía de devolución de 30 días</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </PayPalScriptProvider>
      <Footer />
    </>
  );
}

export default function CheckoutPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-stone-900 flex items-center justify-center"><div className="animate-spin h-8 w-8 border-4 border-amber-500 border-t-transparent rounded-full"></div></div>}>
      <CheckoutContent />
    </Suspense>
  );
}
