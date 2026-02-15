/**
 * Component: ActivityTimeline
 * Timeline de actividades recientes
 */

'use client';

import { useEffect, useState } from 'react';
import { 
  Trophy, 
  BookOpen, 
  Code, 
  CheckCircle,
  Clock 
} from 'lucide-react';

interface Activity {
  id: string;
  student_name: string;
  type: 'achievement' | 'lesson_completed' | 'code_submitted' | 'course_started';
  title: string;
  description: string;
  created_at: string;
  metadata?: {
    course_name?: string;
    lesson_title?: string;
    xp_earned?: number;
  };
}

interface ActivityTimelineProps {
  parentId: string;
}

export function ActivityTimeline({ parentId }: ActivityTimelineProps) {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchActivities();
  }, [parentId]);

  const fetchActivities = async () => {
    try {
      // TODO: Implement API call
      // const response = await fetch(`/api/parent/activities?parentId=${parentId}`);
      // const data = await response.json();
      
      // Mock data
      setActivities([
        {
          id: '1',
          student_name: 'Carlos',
          type: 'achievement',
          title: 'Nuevo logro desbloqueado',
          description: 'Racha de 7 días consecutivos',
          created_at: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
          metadata: { xp_earned: 100 },
        },
        {
          id: '2',
          student_name: 'María',
          type: 'lesson_completed',
          title: 'Lección completada',
          description: 'Variables y Tipos de Datos',
          created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          metadata: { 
            course_name: 'Python para Principiantes',
            xp_earned: 50 
          },
        },
        {
          id: '3',
          student_name: 'Ana',
          type: 'code_submitted',
          title: 'Ejercicio enviado',
          description: 'Mi primer programa en Scratch',
          created_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
        },
        {
          id: '4',
          student_name: 'Carlos',
          type: 'course_started',
          title: 'Curso iniciado',
          description: 'JavaScript Avanzado',
          created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
        },
        {
          id: '5',
          student_name: 'María',
          type: 'achievement',
          title: 'Nuevo logro desbloqueado',
          description: 'Primera línea de código',
          created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
          metadata: { xp_earned: 25 },
        },
      ]);
    } catch (error) {
      console.error('Error fetching activities:', error);
    } finally {
      setLoading(false);
    }
  };

  const getActivityIcon = (type: Activity['type']) => {
    switch (type) {
      case 'achievement':
        return { icon: Trophy, color: 'text-yellow-500', bg: 'bg-yellow-100' };
      case 'lesson_completed':
        return { icon: CheckCircle, color: 'text-green-500', bg: 'bg-green-100' };
      case 'code_submitted':
        return { icon: Code, color: 'text-stone-500', bg: 'bg-stone-100' };
      case 'course_started':
        return { icon: BookOpen, color: 'text-stone-500', bg: 'bg-amber-100' };
      default:
        return { icon: Clock, color: 'text-gray-500', bg: 'bg-gray-100' };
    }
  };

  const getTimeAgo = (dateString: string) => {
    const diff = Date.now() - new Date(dateString).getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `Hace ${days} día${days > 1 ? 's' : ''}`;
    if (hours > 0) return `Hace ${hours} hora${hours > 1 ? 's' : ''}`;
    if (minutes > 0) return `Hace ${minutes} minuto${minutes > 1 ? 's' : ''}`;
    return 'Justo ahora';
  };

  if (loading) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <div className="animate-pulse space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="flex gap-4">
              <div className="h-10 w-10 rounded-full bg-gray-200" />
              <div className="flex-1 space-y-2">
                <div className="h-4 w-32 rounded bg-gray-200" />
                <div className="h-3 w-48 rounded bg-gray-200" />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-gray-200 bg-white">
      <div className="border-b border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900">
          Actividad Reciente
        </h2>
        <p className="mt-1 text-sm text-gray-600">
          Últimas acciones de tus estudiantes
        </p>
      </div>

      <div className="p-6">
        <div className="relative space-y-6">
          {/* Timeline line */}
          <div className="absolute left-5 top-0 bottom-0 w-0.5 bg-gray-200" />

          {activities.map((activity, index) => {
            const { icon: Icon, color, bg } = getActivityIcon(activity.type);
            
            return (
              <div key={activity.id} className="relative flex gap-4">
                {/* Icon */}
                <div className={`relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full ${bg}`}>
                  <Icon className={`h-5 w-5 ${color}`} />
                </div>

                {/* Content */}
                <div className="flex-1 pb-6">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-medium text-gray-900">
                        {activity.student_name}
                      </p>
                      <p className="text-sm text-gray-600">
                        {activity.title}
                      </p>
                      <p className="mt-1 text-sm text-gray-500">
                        {activity.description}
                      </p>
                      
                      {/* Metadata */}
                      {activity.metadata && (
                        <div className="mt-2 flex flex-wrap gap-3 text-xs">
                          {activity.metadata.course_name && (
                            <span className="rounded bg-gray-100 px-2 py-1 text-gray-600">
                              {activity.metadata.course_name}
                            </span>
                          )}
                          {activity.metadata.xp_earned && (
                            <span className="rounded bg-stone-100 px-2 py-1 text-stone-600">
                              +{activity.metadata.xp_earned} XP
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                    
                    <span className="shrink-0 text-xs text-gray-500">
                      {getTimeAgo(activity.created_at)}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {activities.length === 0 && (
          <div className="py-12 text-center">
            <Clock className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-4 font-medium text-gray-900">
              No hay actividades aún
            </h3>
            <p className="mt-1 text-sm text-gray-600">
              Las actividades de tus estudiantes aparecerán aquí
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
