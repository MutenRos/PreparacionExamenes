'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Navigation } from '@/components/Navigation';
import { Footer } from '@/components/Footer';
import { CheckCircle, AlertCircle, ArrowRight, Clock } from 'lucide-react';

export default function PaymentSuccessPage() {
  const router = useRouter();
  const [orderStatus, setOrderStatus] = useState<'pending' | 'verified' | 'error'>('pending');
  const [orderData, setOrderData] = useState<any>(null);

  useEffect(() => {
    // Recuperar datos del pedido de localStorage
    const pendingOrder = localStorage.getItem('pending_order');
    
    if (!pendingOrder) {
      setOrderStatus('error');
      return;
    }

    try {
      const order = JSON.parse(pendingOrder);
      setOrderData(order);
      
      // Simular verificación (en producción, esto vendría del webhook)
      setTimeout(() => {
        setOrderStatus('verified');
        // Limpiar pedido pendiente después de confirmación
        localStorage.removeItem('pending_order');
      }, 2000);
      
    } catch (error) {
      console.error('Error parseando order data:', error);
      setOrderStatus('error');
    }
  }, []);

  if (orderStatus === 'error' || !orderData) {
    return (
      <>
        <Navigation />
        <div className="min-h-screen bg-gradient-to-br from-stone-950 via-stone-900 to-stone-950 pt-20">
          <div className="max-w-2xl mx-auto px-4 py-16">
            
            <div className="bg-stone-900/50 backdrop-blur-sm rounded-2xl border border-stone-800 p-12 text-center">
              <div className="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <AlertCircle className="w-10 h-10 text-red-500" />
              </div>
              
              <h1 className="text-3xl font-bold text-white mb-4">
                No se encontró información del pago
              </h1>
              
              <p className="text-stone-400 mb-8">
                No pudimos verificar tu pedido. Si completaste el pago en PayPal, 
                por favor contacta con soporte enviando tu ID de transacción.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button
                  onClick={() => router.push('/')}
                  className="px-6 py-3 bg-stone-700 hover:bg-stone-600 text-white rounded-xl font-semibold transition-all"
                >
                  Volver al Inicio
                </button>
                <button
                  onClick={() => router.push('/support')}
                  className="px-6 py-3 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 text-white rounded-xl font-semibold transition-all"
                >
                  Contactar Soporte
                </button>
              </div>
            </div>
            
          </div>
        </div>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-gradient-to-br from-stone-950 via-stone-900 to-stone-950 pt-20">
        <div className="max-w-3xl mx-auto px-4 py-16">
          
          {/* Estado: Verificando */}
          {orderStatus === 'pending' && (
            <div className="bg-stone-900/50 backdrop-blur-sm rounded-2xl border border-stone-800 p-12 text-center">
              <div className="w-20 h-20 bg-amber-500/10 rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse">
                <Clock className="w-10 h-10 text-amber-500" />
              </div>
              
              <h1 className="text-3xl font-bold text-white mb-4">
                Verificando tu pago...
              </h1>
              
              <p className="text-stone-400 mb-4">
                Estamos procesando tu pago de PayPal. Esto puede tardar unos segundos.
              </p>
              
              <div className="max-w-md mx-auto">
                <div className="h-2 bg-stone-800 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-amber-600 to-orange-600 animate-pulse w-2/3 transition-all duration-1000"></div>
                </div>
              </div>
            </div>
          )}

          {/* Estado: Verificado */}
          {orderStatus === 'verified' && (
            <div className="space-y-8">
              
              {/* Confirmación */}
              <div className="bg-stone-900/50 backdrop-blur-sm rounded-2xl border border-stone-800 p-12 text-center">
                <div className="w-20 h-20 bg-green-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
                  <CheckCircle className="w-10 h-10 text-green-500" />
                </div>
                
                <h1 className="text-4xl font-bold text-white mb-4">
                  ¡Pago Recibido!
                </h1>
                
                <p className="text-xl text-stone-300 mb-8">
                  Tu pago se ha procesado correctamente.
                </p>
                
                <div className="inline-flex items-center space-x-2 px-4 py-2 bg-stone-800 rounded-lg">
                  <span className="text-stone-400 text-sm">ID de Orden:</span>
                  <span className="text-white font-mono text-sm">
                    {orderData.timestamp.slice(0, 19).replace('T', ' ')}
                  </span>
                </div>
              </div>

              {/* Resumen del Pedido */}
              <div className="bg-stone-900/50 backdrop-blur-sm rounded-2xl border border-stone-800 p-8">
                <h2 className="text-2xl font-bold text-white mb-6">
                  Resumen de tu compra
                </h2>
                
                <div className="space-y-4">
                  <div className="flex justify-between items-center py-3 border-b border-stone-800">
                    <span className="text-stone-400">Tipo</span>
                    <span className="text-white font-semibold capitalize">
                      {orderData.type === 'subscription' ? 'Suscripción' : 'Producto'}
                    </span>
                  </div>
                  
                  {orderData.plan && (
                    <>
                      <div className="flex justify-between items-center py-3 border-b border-stone-800">
                        <span className="text-stone-400">Plan</span>
                        <span className="text-white font-semibold capitalize">
                          {orderData.plan}
                        </span>
                      </div>
                      <div className="flex justify-between items-center py-3 border-b border-stone-800">
                        <span className="text-stone-400">Facturación</span>
                        <span className="text-white font-semibold capitalize">
                          {orderData.billing === 'monthly' ? 'Mensual' : 'Anual'}
                        </span>
                      </div>
                    </>
                  )}
                  
                  {orderData.product && (
                    <div className="flex justify-between items-center py-3 border-b border-stone-800">
                      <span className="text-stone-400">Producto</span>
                      <span className="text-white font-semibold capitalize">
                        {orderData.product}
                      </span>
                    </div>
                  )}
                  
                  <div className="flex justify-between items-center py-4 bg-gradient-to-r from-stone-800/50 to-transparent rounded-lg px-4">
                    <span className="text-white font-bold text-lg">Total Pagado</span>
                    <span className="text-2xl font-bold text-gradient bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-transparent">
                      €{orderData.price.toFixed(2)}
                    </span>
                  </div>
                </div>
              </div>

              {/* Próximos pasos */}
              <div className="bg-gradient-to-br from-amber-900/20 to-orange-900/20 backdrop-blur-sm rounded-2xl border border-amber-800/30 p-8">
                <h2 className="text-2xl font-bold text-white mb-4">
                  Próximos pasos
                </h2>
                
                <div className="space-y-4 text-stone-300">
                  <div className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-amber-600 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-white text-sm font-bold">1</span>
                    </div>
                    <p>
                      <strong className="text-white">Activación automática:</strong> Tu acceso se activará en los próximos minutos.
                    </p>
                  </div>
                  
                  <div className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-amber-600 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-white text-sm font-bold">2</span>
                    </div>
                    <p>
                      <strong className="text-white">Email de confirmación:</strong> Recibirás un correo con los detalles de tu compra.
                    </p>
                  </div>
                  
                  <div className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-amber-600 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-white text-sm font-bold">3</span>
                    </div>
                    <p>
                      <strong className="text-white">Comienza a aprender:</strong> Accede al contenido desde tu panel de usuario.
                    </p>
                  </div>
                </div>
              </div>

              {/* Acciones */}
              <div className="flex flex-col sm:flex-row gap-4">
                <button
                  onClick={() => router.push('/dashboard')}
                  className="flex-1 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 text-white font-bold py-4 px-8 rounded-xl transition-all shadow-lg flex items-center justify-center space-x-2"
                >
                  <span>Ir a mi Dashboard</span>
                  <ArrowRight className="w-5 h-5" />
                </button>
                
                <button
                  onClick={() => router.push('/shop')}
                  className="flex-1 bg-stone-700 hover:bg-stone-600 text-white font-bold py-4 px-8 rounded-xl transition-all flex items-center justify-center space-x-2"
                >
                  <span>Ver más cursos</span>
                </button>
              </div>

            </div>
          )}

        </div>
      </div>
      <Footer />
    </>
  );
}
