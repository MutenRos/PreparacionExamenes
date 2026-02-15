'use client';

import React, { createContext, useContext, useState, useCallback } from 'react';
import { Trophy, Star, Zap, Award, TrendingUp } from 'lucide-react';

export type NotificationType = 'achievement' | 'level-up' | 'streak' | 'xp' | 'course-complete';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  duration?: number;
  timestamp: number;
}

interface NotificationContextType {
  notifications: Notification[];
  showNotification: (
    type: NotificationType,
    title: string,
    message: string,
    duration?: number
  ) => void;
  removeNotification: (id: string) => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export function NotificationProvider({ children }: { children: React.ReactNode }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const showNotification = useCallback(
    (type: NotificationType, title: string, message: string, duration = 5000) => {
      const id = `${Date.now()}-${Math.random()}`;
      const notification: Notification = {
        id,
        type,
        title,
        message,
        duration,
        timestamp: Date.now(),
      };

      setNotifications((prev) => [...prev, notification]);

      // Auto-remove after duration
      if (duration > 0) {
        setTimeout(() => {
          setNotifications((prev) => prev.filter((n) => n.id !== id));
        }, duration);
      }
    },
    []
  );

  const removeNotification = useCallback((id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  }, []);

  return (
    <NotificationContext.Provider value={{ notifications, showNotification, removeNotification }}>
      {children}
    </NotificationContext.Provider>
  );
}

export function useNotifications() {
  const context = useContext(NotificationContext);
  if (context === undefined) {
    throw new Error('useNotifications must be used within a NotificationProvider');
  }
  return context;
}

// Icon mapper
export function getNotificationIcon(type: NotificationType) {
  switch (type) {
    case 'achievement':
      return Trophy;
    case 'level-up':
      return Star;
    case 'streak':
      return Zap;
    case 'xp':
      return Award;
    case 'course-complete':
      return TrendingUp;
    default:
      return Award;
  }
}

// Color mapper
export function getNotificationColor(type: NotificationType) {
  switch (type) {
    case 'achievement':
      return 'from-yellow-500 to-orange-500';
    case 'level-up':
      return 'from-stone-500 to-amber-500';
    case 'streak':
      return 'from-orange-500 to-red-500';
    case 'xp':
      return 'from-stone-500 to-cyan-500';
    case 'course-complete':
      return 'from-green-500 to-emerald-500';
    default:
      return 'from-gray-500 to-gray-600';
  }
}
