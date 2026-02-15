'use client';

import { useState, useEffect } from 'react';
import { Users, Award, Mail, Calendar, Shield, Trash2, Key, RefreshCw, CheckCircle, XCircle } from 'lucide-react';

interface User {
  id: string;
  email: string;
  created_at: string;
  last_sign_in_at: string | null;
  confirmed_at: string | null;
  is_pioneer: boolean;
  pioneer_number?: number;
  subscription: {
    plan: string;
    status: string;
    expires_at: string;
  } | null;
}

export default function UsersManager() {
  const [users, setUsers] = useState<User[]>([]);
  const [totalUsers, setTotalUsers] = useState(0);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [modalAction, setModalAction] = useState<string>('');

  useEffect(() => {
    fetchUsers();
  }, []);

  async function fetchUsers() {
    setLoading(true);
    try {
      const response = await fetch('/api/admin/users');
      const data = await response.json();
      
      if (response.ok) {
        setUsers(data.users || []);
        setTotalUsers(data.total || 0);
        console.log(`Loaded ${data.users?.length || 0} users out of ${data.total || 0} total`);
      }
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleUserAction(userId: string, action: string, data?: any) {
    try {
      const response = await fetch('/api/admin/users', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, action, data }),
      });

      if (response.ok) {
        await fetchUsers();
        setShowModal(false);
        setSelectedUser(null);
      } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
      }
    } catch (error) {
      console.error('Error performing action:', error);
      alert('Error al realizar la acción');
    }
  }

  async function handleSubscriptionAction(userId: string, action: string, planType?: string) {
    try {
      const response = await fetch('/api/admin/subscriptions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, action, planType }),
      });

      if (response.ok) {
        await fetchUsers();
      } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
      }
    } catch (error) {
      console.error('Error managing subscription:', error);
      alert('Error al gestionar suscripción');
    }
  }

  function openModal(user: User, action: string) {
    setSelectedUser(user);
    setModalAction(action);
    setShowModal(true);
  }

  if (loading) {
    return (
      <div className="bg-stone-800 border border-stone-700 rounded-lg p-12">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Users className="w-6 h-6 text-blue-400" />
          <h2 className="text-xl font-bold text-white">Gestión de Usuarios</h2>
        </div>
        <button
          onClick={fetchUsers}
          className="flex items-center gap-2 px-4 py-2 bg-stone-700 text-stone-200 rounded-lg hover:bg-stone-600 transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Actualizar
        </button>
      </div>

      <div className="mb-4 flex items-center justify-between">
        <div className="text-sm text-stone-400">
          Mostrando <span className="text-white font-semibold">{users.length}</span> de{' '}
          <span className="text-white font-semibold">{totalUsers}</span> usuarios totales
          {users.length < totalUsers && (
            <span className="ml-2 text-amber-400">
              ⚠ No se muestran todos los usuarios
            </span>
          )}
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-stone-700">
              <th className="text-left py-3 px-4 text-stone-300 font-semibold">Email</th>
              <th className="text-left py-3 px-4 text-stone-300 font-semibold">Estado</th>
              <th className="text-left py-3 px-4 text-stone-300 font-semibold">Pionero</th>
              <th className="text-left py-3 px-4 text-stone-300 font-semibold">Suscripción</th>
              <th className="text-left py-3 px-4 text-stone-300 font-semibold">Registro</th>
              <th className="text-left py-3 px-4 text-stone-300 font-semibold">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-b border-stone-800 hover:bg-stone-700/50 transition-colors">
                <td className="py-3 px-4">
                  <div className="flex items-center gap-2">
                    <Mail className="w-4 h-4 text-stone-400" />
                    <span className="text-stone-200">{user.email}</span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  {user.confirmed_at ? (
                    <span className="flex items-center gap-1 text-green-400">
                      <CheckCircle className="w-4 h-4" />
                      Verificado
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-orange-400">
                      <XCircle className="w-4 h-4" />
                      Sin verificar
                    </span>
                  )}
                </td>
                <td className="py-3 px-4">
                  {user.is_pioneer ? (
                    <span className="flex items-center gap-1 text-purple-400 font-semibold">
                      <Award className="w-4 h-4" />
                      #{user.pioneer_number}
                    </span>
                  ) : (
                    <span className="text-stone-500">-</span>
                  )}
                </td>
                <td className="py-3 px-4">
                  {user.subscription ? (
                    <div>
                      <span className={`font-semibold ${
                        user.subscription.status === 'active' ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {user.subscription.plan}
                      </span>
                      <span className="text-xs text-stone-400 ml-2">
                        ({user.subscription.status})
                      </span>
                    </div>
                  ) : (
                    <span className="text-stone-500">Sin suscripción</span>
                  )}
                </td>
                <td className="py-3 px-4 text-stone-400">
                  {new Date(user.created_at).toLocaleDateString()}
                </td>
                <td className="py-3 px-4">
                  <div className="flex gap-2">
                    {!user.confirmed_at && (
                      <button
                        onClick={() => handleUserAction(user.id, 'confirm_email')}
                        className="p-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                        title="Confirmar email"
                      >
                        <CheckCircle className="w-4 h-4" />
                      </button>
                    )}
                    
                    {!user.is_pioneer && (
                      <button
                        onClick={() => handleUserAction(user.id, 'assign_pioneer')}
                        className="p-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors"
                        title="Asignar como pionero"
                      >
                        <Award className="w-4 h-4" />
                      </button>
                    )}

                    {user.is_pioneer && (
                      <button
                        onClick={() => openModal(user, 'remove_pioneer')}
                        className="p-2 bg-orange-600 text-white rounded hover:bg-orange-700 transition-colors"
                        title="Quitar pionero"
                      >
                        <XCircle className="w-4 h-4" />
                      </button>
                    )}

                    {!user.subscription && (
                      <button
                        onClick={() => openModal(user, 'add_subscription')}
                        className="p-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                        title="Agregar suscripción"
                      >
                        <Shield className="w-4 h-4" />
                      </button>
                    )}

                    {user.subscription && user.subscription.status === 'active' && (
                      <button
                        onClick={() => handleSubscriptionAction(user.id, 'cancel')}
                        className="p-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
                        title="Cancelar suscripción"
                      >
                        <XCircle className="w-4 h-4" />
                      </button>
                    )}

                    <button
                      onClick={() => openModal(user, 'delete')}
                      className="p-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
                      title="Eliminar usuario"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal de confirmación */}
      {showModal && selectedUser && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-stone-800 border border-stone-700 rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold text-white mb-4">
              {modalAction === 'delete' && 'Eliminar Usuario'}
              {modalAction === 'remove_pioneer' && 'Quitar Estado Pionero'}
              {modalAction === 'add_subscription' && 'Agregar Suscripción'}
            </h3>
            
            {modalAction === 'delete' && (
              <p className="text-stone-300 mb-6">
                ¿Estás seguro de que quieres eliminar a <strong>{selectedUser.email}</strong>? 
                Esta acción no se puede deshacer.
              </p>
            )}

            {modalAction === 'remove_pioneer' && (
              <p className="text-stone-300 mb-6">
                ¿Quitar el estado pionero de <strong>{selectedUser.email}</strong>?
              </p>
            )}

            {modalAction === 'add_subscription' && (
              <div className="mb-6">
                <p className="text-stone-300 mb-4">
                  Selecciona el plan para <strong>{selectedUser.email}</strong>:
                </p>
                <div className="space-y-2">
                  <button
                    onClick={() => handleSubscriptionAction(selectedUser.id, 'create', 'starter')}
                    className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                  >
                    Starter
                  </button>
                  <button
                    onClick={() => handleSubscriptionAction(selectedUser.id, 'create', 'pro')}
                    className="w-full px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
                  >
                    Pro
                  </button>
                  <button
                    onClick={() => handleSubscriptionAction(selectedUser.id, 'create', 'family')}
                    className="w-full px-4 py-2 bg-amber-600 text-white rounded hover:bg-amber-700"
                  >
                    Family
                  </button>
                </div>
              </div>
            )}

            <div className="flex gap-3">
              <button
                onClick={() => {
                  setShowModal(false);
                  setSelectedUser(null);
                }}
                className="flex-1 px-4 py-2 bg-stone-700 text-stone-200 rounded hover:bg-stone-600"
              >
                Cancelar
              </button>
              {modalAction !== 'add_subscription' && (
                <button
                  onClick={() => handleUserAction(selectedUser.id, modalAction === 'delete' ? 'delete_user' : 'remove_pioneer')}
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                >
                  Confirmar
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
