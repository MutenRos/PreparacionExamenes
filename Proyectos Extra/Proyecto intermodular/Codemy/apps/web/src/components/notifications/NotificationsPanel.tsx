'use client';

import { useState, useEffect } from 'react';
import { Bell, X, Check, Info, AlertCircle, Trophy, BookOpen, Star } from 'lucide-react';
import { getNotifications, saveNotifications } from '@/lib/achievements';

interface Notification {
  id: string;
  type: 'achievement' | 'course' | 'streak' | 'info';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  icon: string;
}

export default function NotificationsPanel() {
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>(() =>
    (getNotifications() || []).map((n: any) => ({ ...n, timestamp: new Date(n.timestamp), icon: n.icon || '' })) as Notification[]
  );

  const unreadCount = notifications.filter(n => !n.read).length;

  const markAsRead = (id: string) => {
    setNotifications(prev => {
      const next = prev.map(n => n.id === id ? { ...n, read: true } : n);
      saveNotifications(next as any);
      return next;
    });
  };

  const markAllAsRead = () => {
    setNotifications(prev => {
      const next = prev.map(n => ({ ...n, read: true }));
      saveNotifications(next as any);
      return next;
    });
  };

  const deleteNotification = (id: string) => {
    setNotifications(prev => {
      const next = prev.filter(n => n.id !== id);
      saveNotifications(next as any);
      return next;
    });
  };

  const clearAll = () => {
    setNotifications([]);
    saveNotifications([] as any);
  };

  const getTimeAgo = (date: Date) => {
    const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
    
    if (seconds < 60) return 'Hace un momento';
    if (seconds < 3600) return `Hace ${Math.floor(seconds / 60)} min`;
    if (seconds < 86400) return `Hace ${Math.floor(seconds / 3600)} h`;
    if (seconds < 604800) return `Hace ${Math.floor(seconds / 86400)} días`;
    return date.toLocaleDateString();
  };

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'achievement':
        return 'from-yellow-400 to-orange-500';
      case 'course':
        return 'from-stone-400 to-stone-500';
      case 'streak':
        return 'from-orange-400 to-red-500';
      default:
        return 'from-gray-400 to-gray-600';
    }
  };

  // Simular notificaciones en tiempo real
  useEffect(() => {
    // Escuchar cambios disparados por saveNotifications
    const handler = () => {
      const list = (getNotifications() || []).map((n: any) => ({ ...n, timestamp: new Date(n.timestamp) }));
      setNotifications(list as any);
    };
    window.addEventListener('notifications-updated', handler as EventListener);

    // TODO: Implementar con Supabase Realtime
    // const channel = supabase.channel('notifications')
    //   .on('postgres_changes', {
    //     event: 'INSERT',
    //     schema: 'public',
    //     table: 'notifications'
    //   }, (payload) => {
    //     setNotifications(prev => [payload.new as Notification, ...prev]);
    //   })
    //   .subscribe();
    
    return () => {
      window.removeEventListener('notifications-updated', handler as EventListener);
    };
  }, []);

  return (
    <div className="relative">
      {/* Bell Icon Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
        aria-label="Notificaciones"
      >
        <Bell className="w-6 h-6" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {/* Notifications Panel */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />

          {/* Panel */}
          <div className="absolute right-0 mt-2 w-96 max-h-[600px] bg-white rounded-xl shadow-2xl border border-gray-200 z-50 overflow-hidden">
            {/* Header */}
            <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-stone-500 to-stone-600">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold text-white">Notificaciones</h3>
                  {unreadCount > 0 && (
                    <p className="text-sm text-white/80">{unreadCount} sin leer</p>
                  )}
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-1 text-white/80 hover:text-white hover:bg-white/20 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Actions */}
              {notifications.length > 0 && (
                <div className="flex gap-2 mt-3">
                  {unreadCount > 0 && (
                    <button
                      onClick={markAllAsRead}
                      className="text-xs text-white/90 hover:text-white font-medium px-3 py-1 bg-white/20 hover:bg-white/30 rounded-md transition-colors"
                    >
                      Marcar todas como leídas
                    </button>
                  )}
                  <button
                    onClick={clearAll}
                    className="text-xs text-white/90 hover:text-white font-medium px-3 py-1 bg-white/20 hover:bg-white/30 rounded-md transition-colors"
                  >
                    Limpiar todo
                  </button>
                </div>
              )}
            </div>

            {/* Notifications List */}
            <div className="overflow-y-auto max-h-[500px]">
              {notifications.length === 0 ? (
                <div className="p-8 text-center">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Bell className="w-8 h-8 text-gray-400" />
                  </div>
                  <p className="text-gray-600 font-medium">No tienes notificaciones</p>
                  <p className="text-sm text-gray-500 mt-1">Te avisaremos cuando haya algo nuevo</p>
                </div>
              ) : (
                <div className="divide-y divide-gray-100">
                  {notifications.map((notification) => (
                    <div
                      key={notification.id}
                      className={`p-4 hover:bg-gray-50 transition-colors ${
                        !notification.read ? 'bg-stone-50/50' : ''
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        {/* Icon */}
                        <div className={`w-10 h-10 bg-gradient-to-br ${getNotificationColor(notification.type)} rounded-full flex items-center justify-center flex-shrink-0`}>
                          <span className="text-xl">{notification.icon}</span>
                        </div>

                        {/* Content */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-2">
                            <h4 className={`text-sm font-semibold ${!notification.read ? 'text-gray-900' : 'text-gray-700'}`}>
                              {notification.title}
                            </h4>
                            {!notification.read && (
                              <div className="w-2 h-2 bg-stone-500 rounded-full flex-shrink-0 mt-1" />
                            )}
                          </div>
                          <p className="text-sm text-gray-600 mt-1">
                            {notification.message}
                          </p>
                          <p className="text-xs text-gray-500 mt-2">
                            {getTimeAgo(notification.timestamp)}
                          </p>

                          {/* Actions */}
                          <div className="flex gap-2 mt-3">
                            {!notification.read && (
                              <button
                                onClick={() => markAsRead(notification.id)}
                                className="text-xs text-stone-600 hover:text-stone-700 font-medium flex items-center gap-1"
                              >
                                <Check className="w-3 h-3" />
                                Marcar como leída
                              </button>
                            )}
                            <button
                              onClick={() => deleteNotification(notification.id)}
                              className="text-xs text-gray-500 hover:text-gray-700 font-medium flex items-center gap-1"
                            >
                              <X className="w-3 h-3" />
                              Eliminar
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Footer */}
            {notifications.length > 0 && (
              <div className="p-3 border-t border-gray-200 bg-gray-50">
                <button className="w-full text-center text-sm text-stone-600 hover:text-stone-700 font-medium">
                  Ver todas las notificaciones
                </button>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
