'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';

export default function SupportWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) return null;

  return (
    <>
      {/* Botón flotante */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 w-16 h-16 bg-amber-600 hover:bg-amber-700 text-white rounded-full shadow-lg flex items-center justify-center transition-all duration-200 z-50 text-2xl"
        aria-label="Soporte"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Panel de soporte */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-80 bg-stone-900 border border-stone-700 rounded-lg shadow-2xl z-50 overflow-hidden">
          <div className="bg-gradient-to-r from-amber-600 to-amber-700 p-4">
            <h3 className="text-white font-semibold text-lg">Centro de Soporte</h3>
            <p className="text-amber-100 text-sm">¿Necesitas ayuda?</p>
          </div>

          <div className="p-4 space-y-3">
            <Link
              href="/soporte"
              className="block w-full p-3 bg-stone-800 hover:bg-stone-700 rounded-lg transition-colors"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">📚</span>
                <div>
                  <p className="text-white font-medium">Centro de Ayuda</p>
                  <p className="text-stone-400 text-sm">Guías y tutoriales</p>
                </div>
              </div>
            </Link>

            <Link
              href="/contacto"
              className="block w-full p-3 bg-stone-800 hover:bg-stone-700 rounded-lg transition-colors"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">✉️</span>
                <div>
                  <p className="text-white font-medium">Contactar</p>
                  <p className="text-stone-400 text-sm">Envíanos un mensaje</p>
                </div>
              </div>
            </Link>

            <a
              href="mailto:soporte@codedungeon.es"
              className="block w-full p-3 bg-stone-800 hover:bg-stone-700 rounded-lg transition-colors"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">📧</span>
                <div>
                  <p className="text-white font-medium">Email Directo</p>
                  <p className="text-stone-400 text-sm">soporte@codedungeon.es</p>
                </div>
              </div>
            </a>
          </div>
        </div>
      )}
    </>
  );
}
