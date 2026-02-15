'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { createClient } from '@/lib/supabase/client';
import { getSafeUserClient } from '@/lib/auth-helpers-client';

export default function SupportWidgetDirect() {
  const [isOpen, setIsOpen] = useState(false);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    console.log('🚀 SupportWidgetDirect montado');
    getSafeUserClient().then(({ user, isDeleted }) => {
      if (isDeleted) {
        // Usuario eliminado, la página se recargará
        return;
      }
      console.log('👤 Usuario en SupportWidgetDirect:', user?.email);
      setUser(user);
    });
  }, []);

  console.log('🔄 SupportWidgetDirect render - user:', user?.email, 'isOpen:', isOpen);

  if (!user) {
    console.log('❌ No user, retornando null');
    return null;
  }

  console.log('✅ Renderizando botón del widget');

  return (
    <>
      <button
        onClick={() => {
          console.log('🔵 CLICK en SupportWidget - isOpen:', isOpen, '→', !isOpen);
          setIsOpen(!isOpen);
        }}
        className="fixed bottom-6 right-6 w-20 h-20 bg-red-600 hover:bg-red-700 text-white rounded-full shadow-2xl flex items-center justify-center text-4xl"
        style={{ zIndex: 99999 }}
      >
        {isOpen ? '❌' : '💬'}
      </button>

      {isOpen && (
        <div 
          className="fixed right-6 w-80 bg-stone-800 rounded-lg shadow-2xl border-2 border-amber-600"
          style={{ 
            zIndex: 99999,
            bottom: '96px',
            position: 'fixed'
          }}
        >
          <div className="bg-amber-700 p-4 text-white">
            <h3 className="font-bold text-lg">Centro de Soporte</h3>
            <p className="text-sm">¿En qué podemos ayudarte?</p>
          </div>

          <div className="p-4 space-y-3">
            <Link
              href="/tickets/new"
              onClick={() => setIsOpen(false)}
              className="block w-full p-4 bg-amber-700 hover:bg-amber-600 text-white rounded-lg"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">🎫</span>
                <div className="flex-1">
                  <p className="font-semibold">Abrir un ticket</p>
                  <p className="text-sm">Te responderemos pronto</p>
                </div>
                <span className="text-xl">📤</span>
              </div>
            </Link>

            <Link
              href="/tickets"
              onClick={() => setIsOpen(false)}
              className="block w-full p-3 bg-stone-700 hover:bg-stone-600 text-white rounded-lg text-center"
            >
              Ver mis tickets
            </Link>
          </div>
        </div>
      )}
    </>
  );
}
