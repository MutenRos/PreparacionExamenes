'use client';

import React, { useEffect, useState } from 'react';
import { X } from 'lucide-react';
import { useNotifications, getNotificationIcon, getNotificationColor } from '@/contexts/NotificationContext';

export default function NotificationToast() {
  const { notifications, removeNotification } = useNotifications();

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-3 max-w-md">
      {notifications.map((notification) => (
        <ToastItem
          key={notification.id}
          notification={notification}
          onClose={() => removeNotification(notification.id)}
        />
      ))}
    </div>
  );
}

interface ToastItemProps {
  notification: {
    id: string;
    type: 'achievement' | 'level-up' | 'streak' | 'xp' | 'course-complete';
    title: string;
    message: string;
    duration?: number;
  };
  onClose: () => void;
}

function ToastItem({ notification, onClose }: ToastItemProps) {
  const [isExiting, setIsExiting] = useState(false);
  const Icon = getNotificationIcon(notification.type);
  const colorClass = getNotificationColor(notification.type);

  useEffect(() => {
    if (notification.duration && notification.duration > 0) {
      const timer = setTimeout(() => {
        setIsExiting(true);
        setTimeout(onClose, 300); // Wait for exit animation
      }, notification.duration - 300);

      return () => clearTimeout(timer);
    }
  }, [notification.duration, onClose]);

  return (
    <div
      className={`
        transform transition-all duration-300 ease-out
        ${isExiting ? 'translate-x-full opacity-0' : 'translate-x-0 opacity-100'}
      `}
    >
      <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-2xl border border-gray-200 overflow-hidden">
        {/* Colored top border */}
        <div className={`h-1 bg-gradient-to-r ${colorClass}`} />

        <div className="p-4">
          <div className="flex items-start gap-3">
            {/* Icon */}
            <div className={`flex-shrink-0 w-10 h-10 rounded-lg bg-gradient-to-br ${colorClass} flex items-center justify-center`}>
              <Icon className="w-5 h-5 text-white" />
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0">
              <h4 className="text-sm font-semibold text-gray-900 mb-1">
                {notification.title}
              </h4>
              <p className="text-sm text-gray-600 leading-relaxed">
                {notification.message}
              </p>
            </div>

            {/* Close button */}
            <button
              onClick={() => {
                setIsExiting(true);
                setTimeout(onClose, 300);
              }}
              className="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Progress bar (optional) */}
          {notification.duration && notification.duration > 0 && (
            <div className="mt-3 h-1 bg-gray-100 rounded-full overflow-hidden">
              <div
                className={`h-full bg-gradient-to-r ${colorClass} animate-shrink`}
                style={{
                  animation: `shrink ${notification.duration}ms linear forwards`,
                }}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
