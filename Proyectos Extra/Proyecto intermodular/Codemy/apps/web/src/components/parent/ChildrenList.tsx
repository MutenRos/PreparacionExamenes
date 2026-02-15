/**
 * Component: ChildrenList
 * Lista de estudiantes con su progreso
 */

'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { User, TrendingUp, Clock, Award, ChevronRight } from 'lucide-react';

interface Child {
  id: string;
  name: string;
  age: number;
  avatar_url: string | null;
  current_track: string;
  weekly_time: number; // minutos
  progress_percentage: number;
  achievements_count: number;
  last_activity: string;
}

interface ChildrenListProps {
  parentId: string;
}

export function ChildrenList({ parentId }: ChildrenListProps) {
  const [children, setChildren] = useState<Child[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchChildren();
  }, [parentId]);

  const fetchChildren = async () => {
    try {
      // TODO: Implement API call
      // const response = await fetch(`/api/parent/children?parentId=${parentId}`);
      // const data = await response.json();
      
      // Mock data
      setChildren([
        {
          id: '1',
          name: 'María García',
          age: 12,
          avatar_url: null,
          current_track: 'Python para Principiantes',
          weekly_time: 420, // 7h
          progress_percentage: 75,
          achievements_count: 23,
          last_activity: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        },
        {
          id: '2',
          name: 'Carlos García',
          age: 15,
          avatar_url: null,
          current_track: 'JavaScript Avanzado',
          weekly_time: 540, // 9h
          progress_percentage: 62,
          achievements_count: 18,
          last_activity: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        },
        {
          id: '3',
          name: 'Ana García',
          age: 9,
          avatar_url: null,
          current_track: 'Scratch Junior',
          weekly_time: 280, // 4h 40min
          progress_percentage: 85,
          achievements_count: 6,
          last_activity: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
        },
      ]);
    } catch (error) {
      console.error('Error fetching children:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  const getTimeAgo = (dateString: string) => {
    const diff = Date.now() - new Date(dateString).getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `Hace ${days}d`;
    if (hours > 0) return `Hace ${hours}h`;
    if (minutes > 0) return `Hace ${minutes}m`;
    return 'Ahora';
  };

  if (loading) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <div className="animate-pulse space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="flex items-center gap-4">
              <div className="h-16 w-16 rounded-full bg-gray-200" />
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
          Estudiantes
        </h2>
        <p className="mt-1 text-sm text-gray-600">
          {children.length} estudiante{children.length !== 1 ? 's' : ''} activo{children.length !== 1 ? 's' : ''}
        </p>
      </div>

      <div className="divide-y divide-gray-200">
        {children.map((child) => (
          <Link
            key={child.id}
            href={`/parent/student/${child.id}`}
            className="block p-6 transition-colors hover:bg-gray-50"
          >
            <div className="flex items-start gap-4">
              {/* Avatar */}
              <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-stone-500 to-stone-600 text-white">
                {child.avatar_url ? (
                  <img
                    src={child.avatar_url}
                    alt={child.name}
                    className="h-full w-full rounded-full object-cover"
                  />
                ) : (
                  <User className="h-8 w-8" />
                )}
              </div>

              {/* Info */}
              <div className="flex-1">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      {child.name}
                    </h3>
                    <p className="mt-1 text-sm text-gray-600">
                      {child.age} años · {child.current_track}
                    </p>
                  </div>
                  <ChevronRight className="h-5 w-5 text-gray-400" />
                </div>

                {/* Progress bar */}
                <div className="mt-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Progreso del curso</span>
                    <span className="font-medium text-gray-900">
                      {child.progress_percentage}%
                    </span>
                  </div>
                  <div className="mt-2 h-2 overflow-hidden rounded-full bg-gray-100">
                    <div
                      className="h-full bg-gradient-to-r from-stone-500 to-stone-600 transition-all duration-500"
                      style={{ width: `${child.progress_percentage}%` }}
                    />
                  </div>
                </div>

                {/* Stats */}
                <div className="mt-4 flex flex-wrap gap-4 text-sm">
                  <div className="flex items-center gap-1.5 text-gray-600">
                    <Clock className="h-4 w-4" />
                    <span>{formatTime(child.weekly_time)} esta semana</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-gray-600">
                    <Award className="h-4 w-4" />
                    <span>{child.achievements_count} logros</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-gray-600">
                    <TrendingUp className="h-4 w-4" />
                    <span>Última actividad: {getTimeAgo(child.last_activity)}</span>
                  </div>
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {children.length === 0 && (
        <div className="p-12 text-center">
          <User className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-4 font-medium text-gray-900">
            No hay estudiantes
          </h3>
          <p className="mt-1 text-sm text-gray-600">
            Añade estudiantes a tu plan familiar
          </p>
          <button className="mt-4 rounded-lg bg-stone-600 px-4 py-2 text-sm font-semibold text-white hover:bg-stone-700">
            Añadir Estudiante
          </button>
        </div>
      )}
    </div>
  );
}
