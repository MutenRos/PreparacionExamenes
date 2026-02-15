/**
 * Component: ParentalControls
 * Configuración de controles parentales
 */

'use client';

import { useState } from 'react';
import { 
  Clock, 
  Shield, 
  Bell, 
  Calendar,
  Lock,
  Eye,
  Save
} from 'lucide-react';

interface ParentalControlsProps {
  parentId: string;
}

interface ControlSettings {
  max_daily_minutes: number;
  allowed_days: string[];
  content_filter: 'all' | 'age_appropriate' | 'custom';
  notifications: {
    daily_report: boolean;
    achievement_alerts: boolean;
    time_limit_warning: boolean;
  };
  quiet_hours: {
    enabled: boolean;
    start: string;
    end: string;
  };
}

export function ParentalControls({ parentId }: ParentalControlsProps) {
  const [settings, setSettings] = useState<ControlSettings>({
    max_daily_minutes: 120,
    allowed_days: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
    content_filter: 'age_appropriate',
    notifications: {
      daily_report: true,
      achievement_alerts: true,
      time_limit_warning: true,
    },
    quiet_hours: {
      enabled: true,
      start: '20:00',
      end: '08:00',
    },
  });
  const [saving, setSaving] = useState(false);

  const days = [
    { id: 'monday', name: 'Lun' },
    { id: 'tuesday', name: 'Mar' },
    { id: 'wednesday', name: 'Mié' },
    { id: 'thursday', name: 'Jue' },
    { id: 'friday', name: 'Vie' },
    { id: 'saturday', name: 'Sáb' },
    { id: 'sunday', name: 'Dom' },
  ];

  const handleSave = async () => {
    setSaving(true);
    try {
      // TODO: Implement API call
      // await fetch('/api/parent/controls', {
      //   method: 'PUT',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ parentId, settings }),
      // });
      
      console.log('Saving settings:', settings);
      await new Promise(resolve => setTimeout(resolve, 1000));
      
    } catch (error) {
      console.error('Error saving settings:', error);
    } finally {
      setSaving(false);
    }
  };

  const toggleDay = (dayId: string) => {
    setSettings(prev => ({
      ...prev,
      allowed_days: prev.allowed_days.includes(dayId)
        ? prev.allowed_days.filter(d => d !== dayId)
        : [...prev.allowed_days, dayId],
    }));
  };

  return (
    <div className="rounded-lg border border-gray-200 bg-white">
      <div className="border-b border-gray-200 p-6">
        <div className="flex items-center gap-3">
          <Shield className="h-6 w-6 text-stone-600" />
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              Controles Parentales
            </h2>
            <p className="mt-1 text-sm text-gray-600">
              Configura límites y restricciones
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-6 p-6">
        {/* Tiempo Diario */}
        <div>
          <div className="flex items-center gap-2 text-gray-900">
            <Clock className="h-5 w-5" />
            <label className="font-medium">Tiempo Máximo Diario</label>
          </div>
          <div className="mt-3 flex items-center gap-4">
            <input
              type="range"
              min="30"
              max="300"
              step="30"
              value={settings.max_daily_minutes}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                max_daily_minutes: parseInt(e.target.value),
              }))}
              className="flex-1"
            />
            <div className="flex items-center gap-2 rounded-lg bg-stone-50 px-4 py-2 text-stone-600">
              <span className="text-2xl font-bold">
                {Math.floor(settings.max_daily_minutes / 60)}
              </span>
              <span className="text-sm">
                h {settings.max_daily_minutes % 60}m
              </span>
            </div>
          </div>
        </div>

        {/* Días Permitidos */}
        <div>
          <div className="flex items-center gap-2 text-gray-900">
            <Calendar className="h-5 w-5" />
            <label className="font-medium">Días Permitidos</label>
          </div>
          <div className="mt-3 flex gap-2">
            {days.map(day => (
              <button
                key={day.id}
                onClick={() => toggleDay(day.id)}
                className={`flex-1 rounded-lg border-2 px-3 py-2 text-sm font-medium transition-colors ${
                  settings.allowed_days.includes(day.id)
                    ? 'border-stone-500 bg-stone-50 text-stone-700'
                    : 'border-gray-200 bg-white text-gray-500 hover:border-gray-300'
                }`}
              >
                {day.name}
              </button>
            ))}
          </div>
        </div>

        {/* Horario de Descanso */}
        <div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-gray-900">
              <Lock className="h-5 w-5" />
              <label className="font-medium">Horario de Descanso</label>
            </div>
            <button
              onClick={() => setSettings(prev => ({
                ...prev,
                quiet_hours: {
                  ...prev.quiet_hours,
                  enabled: !prev.quiet_hours.enabled,
                },
              }))}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                settings.quiet_hours.enabled ? 'bg-stone-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  settings.quiet_hours.enabled ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          
          {settings.quiet_hours.enabled && (
            <div className="mt-3 flex items-center gap-4">
              <div className="flex-1">
                <label className="block text-xs text-gray-600">Inicio</label>
                <input
                  type="time"
                  value={settings.quiet_hours.start}
                  onChange={(e) => setSettings(prev => ({
                    ...prev,
                    quiet_hours: {
                      ...prev.quiet_hours,
                      start: e.target.value,
                    },
                  }))}
                  className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2"
                />
              </div>
              <div className="flex-1">
                <label className="block text-xs text-gray-600">Fin</label>
                <input
                  type="time"
                  value={settings.quiet_hours.end}
                  onChange={(e) => setSettings(prev => ({
                    ...prev,
                    quiet_hours: {
                      ...prev.quiet_hours,
                      end: e.target.value,
                    },
                  }))}
                  className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2"
                />
              </div>
            </div>
          )}
        </div>

        {/* Filtro de Contenido */}
        <div>
          <div className="flex items-center gap-2 text-gray-900">
            <Eye className="h-5 w-5" />
            <label className="font-medium">Filtro de Contenido</label>
          </div>
          <div className="mt-3 space-y-2">
            {[
              { value: 'all', label: 'Todo el contenido', desc: 'Sin restricciones' },
              { value: 'age_appropriate', label: 'Apropiado para la edad', desc: 'Contenido adaptado automáticamente' },
              { value: 'custom', label: 'Personalizado', desc: 'Selección manual de cursos' },
            ].map(option => (
              <button
                key={option.value}
                onClick={() => setSettings(prev => ({
                  ...prev,
                  content_filter: option.value as any,
                }))}
                className={`w-full rounded-lg border-2 p-4 text-left transition-colors ${
                  settings.content_filter === option.value
                    ? 'border-stone-500 bg-stone-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <p className="font-medium text-gray-900">{option.label}</p>
                <p className="mt-1 text-sm text-gray-600">{option.desc}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Notificaciones */}
        <div>
          <div className="flex items-center gap-2 text-gray-900">
            <Bell className="h-5 w-5" />
            <label className="font-medium">Notificaciones</label>
          </div>
          <div className="mt-3 space-y-3">
            {[
              { key: 'daily_report', label: 'Informe diario de actividad' },
              { key: 'achievement_alerts', label: 'Alertas de logros conseguidos' },
              { key: 'time_limit_warning', label: 'Avisos de límite de tiempo' },
            ].map(notif => (
              <label
                key={notif.key}
                className="flex cursor-pointer items-center justify-between rounded-lg border border-gray-200 p-4"
              >
                <span className="text-gray-700">{notif.label}</span>
                <input
                  type="checkbox"
                  checked={settings.notifications[notif.key as keyof typeof settings.notifications]}
                  onChange={(e) => setSettings(prev => ({
                    ...prev,
                    notifications: {
                      ...prev.notifications,
                      [notif.key]: e.target.checked,
                    },
                  }))}
                  className="h-4 w-4 rounded border-gray-300 text-stone-600 focus:ring-blue-500"
                />
              </label>
            ))}
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="border-t border-gray-200 p-6">
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-stone-600 px-6 py-3 font-semibold text-white hover:bg-stone-700 disabled:opacity-50"
        >
          <Save className="h-5 w-5" />
          {saving ? 'Guardando...' : 'Guardar Cambios'}
        </button>
      </div>
    </div>
  );
}
