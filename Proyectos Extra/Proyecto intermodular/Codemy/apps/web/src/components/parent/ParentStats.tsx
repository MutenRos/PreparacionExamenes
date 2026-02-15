/**
 * Component: ParentStats
 * Estadísticas generales del panel parental
 */

'use client';

import { useEffect, useState } from 'react';
import { Clock, Trophy, Target, TrendingUp } from 'lucide-react';

interface ParentStatsProps {
  parentId: string;
}

interface Stats {
  total_study_time: number; // minutos
  total_achievements: number;
  average_progress: number; // porcentaje
  active_students: number;
}

export function ParentStats({ parentId }: ParentStatsProps) {
  const [stats, setStats] = useState<Stats>({
    total_study_time: 0,
    total_achievements: 0,
    average_progress: 0,
    active_students: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, [parentId]);

  const fetchStats = async () => {
    try {
      // TODO: Implement API call
      // const response = await fetch(`/api/parent/stats?parentId=${parentId}`);
      // const data = await response.json();
      
      // Mock data
      setStats({
        total_study_time: 1240, // 20h 40min
        total_achievements: 47,
        average_progress: 68,
        active_students: 3,
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  const statCards = [
    {
      title: 'Tiempo Total',
      value: formatTime(stats.total_study_time),
      subtitle: 'Esta semana',
      icon: Clock,
      color: 'from-stone-500 to-cyan-500',
      bgColor: 'bg-stone-50',
      textColor: 'text-stone-600',
    },
    {
      title: 'Logros Conseguidos',
      value: stats.total_achievements,
      subtitle: 'Entre todos',
      icon: Trophy,
      color: 'from-yellow-500 to-orange-500',
      bgColor: 'bg-yellow-50',
      textColor: 'text-yellow-600',
    },
    {
      title: 'Progreso Promedio',
      value: `${stats.average_progress}%`,
      subtitle: 'Cursos activos',
      icon: Target,
      color: 'from-green-500 to-emerald-500',
      bgColor: 'bg-green-50',
      textColor: 'text-green-600',
    },
    {
      title: 'Estudiantes Activos',
      value: stats.active_students,
      subtitle: 'Últimos 7 días',
      icon: TrendingUp,
      color: 'from-stone-500 to-amber-500',
      bgColor: 'bg-amber-50',
      textColor: 'text-stone-600',
    },
  ];

  if (loading) {
    return (
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="animate-pulse rounded-lg border border-gray-200 bg-white p-6">
            <div className="h-10 w-10 rounded-lg bg-gray-200" />
            <div className="mt-4 h-8 w-20 rounded bg-gray-200" />
            <div className="mt-2 h-4 w-24 rounded bg-gray-200" />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      {statCards.map((stat, index) => {
        const Icon = stat.icon;
        
        return (
          <div
            key={index}
            className="rounded-lg border border-gray-200 bg-white p-6 transition-shadow hover:shadow-lg"
          >
            <div className={`inline-flex rounded-lg ${stat.bgColor} p-3`}>
              <Icon className={`h-6 w-6 ${stat.textColor}`} />
            </div>
            
            <div className="mt-4">
              <p className="text-sm font-medium text-gray-600">{stat.title}</p>
              <p className="mt-1 text-3xl font-bold text-gray-900">
                {stat.value}
              </p>
              <p className="mt-1 text-sm text-gray-500">{stat.subtitle}</p>
            </div>

            {/* Progress indicator */}
            <div className="mt-4">
              <div className="h-2 overflow-hidden rounded-full bg-gray-100">
                <div
                  className={`h-full bg-gradient-to-r ${stat.color} transition-all duration-500`}
                  style={{ 
                    width: stat.title === 'Progreso Promedio' 
                      ? `${stats.average_progress}%` 
                      : '100%' 
                  }}
                />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
