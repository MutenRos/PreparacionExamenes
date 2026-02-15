'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Users, TrendingUp, Award, DollarSign, Shield, Database, Settings, Activity } from 'lucide-react';
import DatabaseViewer from '@/components/admin/DatabaseViewer';
import UsersManager from '@/components/admin/UsersManager';
import TicketsManager from '@/components/admin/TicketsManager';

export default function AdminDashboard() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'database' | 'users' | 'tickets'>('overview');
  const [stats, setStats] = useState({
    totalUsers: 0,
    pioneersUsed: 0,
    pioneersRemaining: 100,
    activeSubscriptions: 0,
    totalRevenue: 0,
    coursesCompleted: 0,
  });

  // Lista de tablas disponibles en Supabase
  const availableTables = [
    'profiles',
    'pioneer_users',
    'pioneer_config',
    'purchases',
    'subscriptions',
  ];

  useEffect(() => {
    async function checkAdminAccess() {
      try {
        // Verificar autenticación
        const sessionResponse = await fetch('/api/auth/session');
        const sessionData = await sessionResponse.json();
        
        if (!sessionData.user) {
          router.push('/auth/login?redirectTo=/admin');
          return;
        }

        // Verificar que sea admin
        if (sessionData.user.email !== 'admin@codedungeon.es') {
          router.push('/dashboard');
          return;
        }

        setIsAdmin(true);

        // Cargar estadísticas
        await loadStats();
        
        setLoading(false);
      } catch (error) {
        console.error('Error checking admin access:', error);
        router.push('/dashboard');
      }
    }

    checkAdminAccess();
  }, [router]);

  async function loadStats() {
    try {
      // Obtener información del programa pionero
      const pioneerResponse = await fetch('/api/pioneer/slots');
      const pioneerData = await pioneerResponse.json();
      
      // Obtener usuarios
      const usersResponse = await fetch('/api/admin/users');
      const usersData = await usersResponse.json();
      
      const totalUsers = usersData.total || 0;
      const pioneersUsed = 100 - (pioneerData.slotsRemaining || 0);
      
      // Contar suscripciones activas
      const activeSubscriptions = usersData.users?.filter(
        (u: any) => u.subscription?.status === 'active'
      ).length || 0;
      
      setStats({
        totalUsers,
        pioneersUsed,
        pioneersRemaining: pioneerData.slotsRemaining || 0,
        activeSubscriptions,
        totalRevenue: 0, // TODO: Calcular desde Stripe
        coursesCompleted: 0, // TODO: Implementar cuando tengas datos de progreso
      });
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-stone-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-amber-700 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-stone-200">Verificando acceso...</p>
        </div>
      </div>
    );
  }

  if (!isAdmin) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-stone-950 via-stone-900 to-stone-950">
      {/* Header */}
      <div className="border-b border-stone-800 bg-stone-900/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Shield className="w-8 h-8 text-amber-600" />
              <div>
                <h1 className="text-2xl font-bold text-white">Panel de Administración</h1>
                <p className="text-sm text-stone-400">Code Dungeon</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              {/* Tabs */}
              <div className="flex gap-2">
                <button
                  onClick={() => setActiveTab('overview')}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    activeTab === 'overview'
                      ? 'bg-amber-600 text-white'
                      : 'bg-stone-800 text-stone-300 hover:bg-stone-700'
                  }`}
                >
                  Resumen
                </button>
                <button
                  onClick={() => setActiveTab('users')}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    activeTab === 'users'
                      ? 'bg-amber-600 text-white'
                      : 'bg-stone-800 text-stone-300 hover:bg-stone-700'
                  }`}
                >
                  Usuarios
                </button>
                <button
                  onClick={() => setActiveTab('tickets')}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    activeTab === 'tickets'
                      ? 'bg-amber-600 text-white'
                      : 'bg-stone-800 text-stone-300 hover:bg-stone-700'
                  }`}
                >
                  Tickets
                </button>
                <button
                  onClick={() => setActiveTab('database')}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    activeTab === 'database'
                      ? 'bg-amber-600 text-white'
                      : 'bg-stone-800 text-stone-300 hover:bg-stone-700'
                  }`}
                >
                  Base de Datos
                </button>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => window.open('https://supabase.com/dashboard', '_blank')}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
                >
                  <Database className="w-4 h-4" />
                  Supabase
                </button>
                <button
                  onClick={() => router.push('/dashboard')}
                  className="px-4 py-2 bg-stone-800 text-stone-200 rounded-lg hover:bg-stone-700 transition-colors border border-stone-700"
                >
                  Volver al Dashboard
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && (
          <>
            {/* Estadísticas principales */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Total Usuarios */}
          <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <Users className="w-8 h-8 text-blue-400" />
              <span className="text-xs text-stone-400 bg-stone-900 px-2 py-1 rounded">Total</span>
            </div>
            <div className="text-3xl font-bold text-white mb-1">{stats.totalUsers}</div>
            <p className="text-sm text-stone-400">Usuarios registrados</p>
          </div>

          {/* Pioneros */}
          <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <Award className="w-8 h-8 text-purple-400" />
              <span className="text-xs text-stone-400 bg-stone-900 px-2 py-1 rounded">Pioneros</span>
            </div>
            <div className="text-3xl font-bold text-white mb-1">{stats.pioneersUsed}/100</div>
            <p className="text-sm text-stone-400">{stats.pioneersRemaining} slots restantes</p>
          </div>

          {/* Suscripciones */}
          <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <TrendingUp className="w-8 h-8 text-green-400" />
              <span className="text-xs text-stone-400 bg-stone-900 px-2 py-1 rounded">Activas</span>
            </div>
            <div className="text-3xl font-bold text-white mb-1">{stats.activeSubscriptions}</div>
            <p className="text-sm text-stone-400">Suscripciones activas</p>
          </div>

          {/* Ingresos */}
          <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <DollarSign className="w-8 h-8 text-amber-400" />
              <span className="text-xs text-stone-400 bg-stone-900 px-2 py-1 rounded">MRR</span>
            </div>
            <div className="text-3xl font-bold text-white mb-1">${stats.totalRevenue}</div>
            <p className="text-sm text-stone-400">Ingresos mensuales</p>
          </div>
        </div>

        {/* Secciones de gestión */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Gestión de usuarios */}
          <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
            <div className="flex items-center space-x-3 mb-4">
              <Users className="w-6 h-6 text-blue-400" />
              <h2 className="text-xl font-bold text-white">Gestión de Usuarios</h2>
            </div>
            <p className="text-stone-400 mb-4">
              Administra usuarios, pioneros y permisos
            </p>
            <button 
              onClick={() => setActiveTab('users')}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Ver Usuarios
            </button>
          </div>

          {/* Programa Pionero */}
          <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
            <div className="flex items-center space-x-3 mb-4">
              <Award className="w-6 h-6 text-purple-400" />
              <h2 className="text-xl font-bold text-white">Programa Pionero</h2>
            </div>
            <p className="text-stone-400 mb-4">
              {stats.pioneersUsed} de 100 slots utilizados
            </p>
            <div className="mb-4">
              <div className="h-2 bg-stone-700 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-purple-600 transition-all duration-500"
                  style={{ width: `${(stats.pioneersUsed / 100) * 100}%` }}
                ></div>
              </div>
            </div>
            <button 
              onClick={() => setActiveTab('users')}
              className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
            >
              Ver Pioneros
            </button>
          </div>

          {/* Contenido */}
          <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
            <div className="flex items-center space-x-3 mb-4">
              <Database className="w-6 h-6 text-green-400" />
              <h2 className="text-xl font-bold text-white">Gestión de Contenido</h2>
            </div>
            <p className="text-stone-400 mb-4">
              Administra cursos, lecciones y recursos
            </p>
            <button 
              onClick={() => setActiveTab('database')}
              className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              Ver Base de Datos
            </button>
          </div>

          {/* Analíticas */}
          <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
            <div className="flex items-center space-x-3 mb-4">
              <Activity className="w-6 h-6 text-amber-400" />
              <h2 className="text-xl font-bold text-white">Analíticas</h2>
            </div>
            <p className="text-stone-400 mb-4">
              Estadísticas detalladas y métricas
            </p>
            <button 
              onClick={() => setActiveTab('database')}
              className="w-full px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-colors"
            >
              Ver Base de Datos
            </button>
          </div>
        </div>

        {/* Acciones rápidas */}
        <div className="mt-8 bg-stone-800 border border-stone-700 rounded-lg p-6">
          <div className="flex items-center space-x-3 mb-4">
            <Settings className="w-6 h-6 text-stone-400" />
            <h2 className="text-xl font-bold text-white">Configuración del Sistema</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button 
              onClick={() => setActiveTab('database')}
              className="px-4 py-3 bg-stone-700 text-stone-200 rounded-lg hover:bg-stone-600 transition-colors text-left"
            >
              <div className="font-semibold mb-1">Base de datos</div>
              <div className="text-xs text-stone-400">Ver tablas y datos</div>
            </button>
            <button 
              onClick={() => setActiveTab('users')}
              className="px-4 py-3 bg-stone-700 text-stone-200 rounded-lg hover:bg-stone-600 transition-colors text-left"
            >
              <div className="font-semibold mb-1">Gestión de usuarios</div>
              <div className="text-xs text-stone-400">Administrar cuentas</div>
            </button>
            <button 
              onClick={() => window.open('https://supabase.com/dashboard', '_blank')}
              className="px-4 py-3 bg-stone-700 text-stone-200 rounded-lg hover:bg-stone-600 transition-colors text-left"
            >
              <div className="font-semibold mb-1">Panel Supabase</div>
              <div className="text-xs text-stone-400">Abrir dashboard externo</div>
            </button>
          </div>
        </div>
          </>
        )}

        {activeTab === 'users' && (
          <UsersManager />
        )}

        {activeTab === 'tickets' && (
          <TicketsManager />
        )}

        {activeTab === 'database' && (
          <DatabaseViewer tables={availableTables} />
        )}
      </div>
    </div>
  );
}
