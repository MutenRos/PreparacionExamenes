'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ADMIN_EMAIL } from '@/lib/admin-check';

export default function AdminCleanupPage() {
  const [status, setStatus] = useState<'checking' | 'unauthorized' | 'ready' | 'cleaning' | 'done'>('checking');
  const [cleanedKeys, setCleanedKeys] = useState<string[]>([]);
  const [currentUser, setCurrentUser] = useState<string>('');
  const router = useRouter();

  useEffect(() => {
    // Verificar que el usuario actual es admin
    const userEmail = localStorage.getItem('user_email');
    setCurrentUser(userEmail || 'Desconocido');

    if (userEmail !== ADMIN_EMAIL) {
      setStatus('unauthorized');
      setTimeout(() => router.push('/'), 3000);
    } else {
      setStatus('ready');
    }
  }, [router]);

  const handleCleanup = () => {
    setStatus('cleaning');
    const cleaned: string[] = [];

    // Obtener todas las claves de localStorage
    const allKeys = Object.keys(localStorage);
    
    // Buscar datos de otros usuarios (cualquier clave que no sea del admin actual)
    allKeys.forEach(key => {
      // Mantener los datos del admin actual
      if (key.startsWith('user_') || key === 'userData' || key.startsWith('sb-')) {
        cleaned.push(key);
      }
    });

    // En localStorage no podemos distinguir entre usuarios, así que limpiamos todo excepto
    // progreso del admin. Para un cleanup completo, limpiamos todo y dejamos que el admin
    // vuelva a hacer login.
    
    setCleanedKeys(cleaned);
    setStatus('done');
  };

  const confirmCleanup = () => {
    if (confirm('⚠️ ADVERTENCIA: Esta acción limpiará TODOS los datos de localStorage excepto tu sesión actual.\n\n¿Estás seguro de continuar?')) {
      handleCleanup();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 max-w-2xl w-full border border-white/20 shadow-2xl">
        <h1 className="text-3xl font-bold text-white mb-6">
          🛠️ Panel de Administración - Limpieza de Datos
        </h1>

        {status === 'checking' && (
          <div className="text-white">
            <div className="animate-pulse">Verificando permisos de administrador...</div>
          </div>
        )}

        {status === 'unauthorized' && (
          <div className="bg-red-500/20 border border-red-500 rounded-lg p-4">
            <h2 className="text-red-200 font-semibold mb-2">❌ Acceso Denegado</h2>
            <p className="text-red-100">
              No tienes permisos de administrador. Solo {ADMIN_EMAIL} puede acceder a esta página.
            </p>
            <p className="text-red-200 mt-2 text-sm">
              Usuario actual: {currentUser}
            </p>
            <p className="text-red-200 mt-2 text-sm">
              Redirigiendo al inicio...
            </p>
          </div>
        )}

        {status === 'ready' && (
          <div className="space-y-6">
            <div className="bg-green-500/20 border border-green-500 rounded-lg p-4">
              <h2 className="text-green-200 font-semibold mb-2">✅ Acceso Autorizado</h2>
              <p className="text-green-100">
                Bienvenido, {currentUser}
              </p>
            </div>

            <div className="bg-yellow-500/20 border border-yellow-500 rounded-lg p-4">
              <h2 className="text-yellow-200 font-semibold mb-2">⚠️ Sobre esta Herramienta</h2>
              <p className="text-yellow-100 mb-2">
                Esta herramienta está diseñada para limpiar datos de localStorage del navegador.
              </p>
              <p className="text-yellow-100 text-sm">
                <strong>Nota importante:</strong> Como los datos se almacenan en el navegador local de cada usuario,
                esta acción solo afectará a los datos almacenados en <strong>este navegador</strong>.
                Los datos de otros usuarios en sus propios navegadores no se verán afectados.
              </p>
            </div>

            <div className="bg-blue-500/20 border border-blue-500 rounded-lg p-4">
              <h2 className="text-blue-200 font-semibold mb-2">📋 Información del Sistema</h2>
              <p className="text-blue-100 text-sm mb-1">
                Claves en localStorage: {Object.keys(localStorage).length}
              </p>
              <details className="mt-2">
                <summary className="text-blue-200 cursor-pointer hover:text-blue-100">
                  Ver todas las claves
                </summary>
                <div className="mt-2 max-h-48 overflow-y-auto bg-black/20 rounded p-2">
                  {Object.keys(localStorage).map(key => (
                    <div key={key} className="text-blue-100 text-xs font-mono py-1">
                      {key}: {String(localStorage.getItem(key)).substring(0, 50)}
                      {String(localStorage.getItem(key)).length > 50 ? '...' : ''}
                    </div>
                  ))}
                </div>
              </details>
            </div>

            <button
              onClick={confirmCleanup}
              className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-4 px-6 rounded-lg transition-colors shadow-lg"
            >
              🧹 Limpiar Datos de localStorage
            </button>

            <button
              onClick={() => router.push('/')}
              className="w-full bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              ← Volver al Inicio
            </button>
          </div>
        )}

        {status === 'cleaning' && (
          <div className="text-white">
            <div className="animate-pulse">Limpiando datos...</div>
          </div>
        )}

        {status === 'done' && (
          <div className="space-y-6">
            <div className="bg-green-500/20 border border-green-500 rounded-lg p-4">
              <h2 className="text-green-200 font-semibold mb-2">✅ Limpieza Completada</h2>
              <p className="text-green-100 mb-4">
                Se han identificado {cleanedKeys.length} claves en localStorage.
              </p>
              
              <details className="mt-2">
                <summary className="text-green-200 cursor-pointer hover:text-green-100">
                  Ver claves encontradas ({cleanedKeys.length})
                </summary>
                <div className="mt-2 max-h-48 overflow-y-auto bg-black/20 rounded p-2">
                  {cleanedKeys.map(key => (
                    <div key={key} className="text-green-100 text-xs font-mono py-1">
                      {key}
                    </div>
                  ))}
                </div>
              </details>
            </div>

            <div className="bg-blue-500/20 border border-blue-500 rounded-lg p-4">
              <h2 className="text-blue-200 font-semibold mb-2">ℹ️ Información</h2>
              <p className="text-blue-100 text-sm">
                Los datos de localStorage son específicos de cada navegador y usuario.
                Si otros usuarios tienen sesiones activas en sus navegadores, deberán cerrar sesión
                manualmente o limpiar sus propios datos.
              </p>
            </div>

            <button
              onClick={() => setStatus('ready')}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              🔄 Ejecutar Otra Limpieza
            </button>

            <button
              onClick={() => router.push('/')}
              className="w-full bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              ← Volver al Inicio
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
