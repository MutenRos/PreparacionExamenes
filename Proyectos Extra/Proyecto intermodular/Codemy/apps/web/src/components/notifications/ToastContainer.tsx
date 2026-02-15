'use client';

import React from 'react';
import { X } from 'lucide-react';
import { useNotifications } from '@/contexts/NotificationContext';
import type { Notification } from '@/contexts/NotificationContext';

export function ToastContainer() {
  const { notifications, removeNotification } = useNotifications();

  // Get notification icon based on type
  const getIcon = (type: string) => {
    switch (type) {
      case 'achievement': return '🏆';
      case 'level-up': return '⬆️';
      case 'course-complete': return '🎓';
      case 'xp': return '⭐';
      case 'streak': return '🔥';
      default: return '🔔';
    }
  };

  const visibleNotifications = notifications.slice(0, 5); // Show max 5

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2 w-96 max-w-[90vw] pointer-events-none">
      {visibleNotifications.map((notification) => (
        <div
          key={notification.id}
          className="bg-gray-800 border border-gray-700 rounded-lg p-4 shadow-xl animate-slide-in-right pointer-events-auto"
        >
          <div className="flex items-start gap-3">
            <span className="text-2xl flex-shrink-0">{getIcon(notification.type)}</span>
            <div className="flex-1 min-w-0">
              <h4 className="font-semibold text-white text-sm mb-1">
                {notification.title}
              </h4>
              <p className="text-gray-300 text-xs line-clamp-2">
                {notification.message}
              </p>
            </div>
            <button
              onClick={() => removeNotification(notification.id)}
              className="flex-shrink-0 text-gray-400 hover:text-white transition-colors"
              aria-label="Close notification"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
