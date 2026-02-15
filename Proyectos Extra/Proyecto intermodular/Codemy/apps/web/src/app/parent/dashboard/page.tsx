/**
 * Page: Dashboard Parental
 * Panel de control para padres/tutores
 */

import { ParentDashboard } from '@/components/parent/ParentDashboard';
import { ParentStats } from '@/components/parent/ParentStats';
import { ChildrenList } from '@/components/parent/ChildrenList';
import { ActivityTimeline } from '@/components/parent/ActivityTimeline';
import { ParentalControls } from '@/components/parent/ParentalControls';

export default function ParentDashboardPage() {
  // TODO: Get from auth session
  const parentId = 'parent_123';

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="border-b border-gray-200 bg-white">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Panel Parental
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            Monitorea el progreso y gestiona el tiempo de pantalla de tus hijos
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="space-y-8">
          {/* Estadísticas generales */}
          <ParentStats parentId={parentId} />

          {/* Lista de estudiantes */}
          <ChildrenList parentId={parentId} />

          {/* Timeline de actividad */}
          <div className="grid gap-8 lg:grid-cols-2">
            <ActivityTimeline parentId={parentId} />
            <ParentalControls parentId={parentId} />
          </div>
        </div>
      </div>
    </div>
  );
}
