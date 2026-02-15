'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Send, AlertCircle } from 'lucide-react';
import { createClient } from '@/lib/supabase/client';

export default function NewTicketPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    subject: '',
    category: 'general',
    priority: 'medium',
    description: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const supabase = createClient();
      const { data: { user } } = await supabase.auth.getUser();

      if (!user) {
        setError('Debes iniciar sesión para crear un ticket');
        setLoading(false);
        return;
      }

      const { error: insertError } = await supabase
        .from('tickets')
        .insert({
          user_id: user.id,
          subject: formData.subject,
          category: formData.category,
          priority: formData.priority,
          description: formData.description,
          status: 'open',
        });

      if (insertError) throw insertError;

      // Redirigir a la lista de tickets
      router.push('/tickets?success=true');
    } catch (err: any) {
      console.error('Error creating ticket:', err);
      setError(err.message || 'Error al crear el ticket');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-stone-900">
      {/* Header */}
      <div className="bg-stone-800 shadow-lg border-b-2 border-stone-700">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Link
            href="/tickets"
            className="inline-flex items-center gap-2 text-stone-300 hover:text-amber-500 transition-colors mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            Volver a mis tickets
          </Link>
          <h1 className="text-3xl font-bold text-stone-100">Crear nuevo ticket</h1>
          <p className="text-stone-400 mt-2">Describe tu problema y te ayudaremos lo antes posible</p>
        </div>
      </div>

      {/* Formulario */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form onSubmit={handleSubmit} className="bg-stone-800 rounded-lg shadow-xl border-2 border-stone-700 p-6 space-y-6">
          {error && (
            <div className="bg-red-900/20 border-2 border-red-700 rounded-lg p-4 flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
              <p className="text-red-300">{error}</p>
            </div>
          )}

          {/* Asunto */}
          <div>
            <label htmlFor="subject" className="block text-sm font-medium text-stone-200 mb-2">
              Asunto <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="subject"
              required
              value={formData.subject}
              onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
              placeholder="Ej: No puedo acceder a mi curso"
              className="w-full px-4 py-3 bg-stone-700 border-2 border-stone-600 rounded-lg text-stone-100 placeholder-stone-400 focus:outline-none focus:border-amber-600 transition-colors"
            />
          </div>

          {/* Categoría y Prioridad */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-stone-200 mb-2">
                Categoría
              </label>
              <select
                id="category"
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full px-4 py-3 bg-stone-700 border-2 border-stone-600 rounded-lg text-stone-100 focus:outline-none focus:border-amber-600 transition-colors"
              >
                <option value="general">General</option>
                <option value="technical">Problema técnico</option>
                <option value="billing">Facturación</option>
                <option value="content">Contenido del curso</option>
                <option value="account">Mi cuenta</option>
              </select>
            </div>

            <div>
              <label htmlFor="priority" className="block text-sm font-medium text-stone-200 mb-2">
                Prioridad
              </label>
              <select
                id="priority"
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                className="w-full px-4 py-3 bg-stone-700 border-2 border-stone-600 rounded-lg text-stone-100 focus:outline-none focus:border-amber-600 transition-colors"
              >
                <option value="low">Baja</option>
                <option value="medium">Media</option>
                <option value="high">Alta</option>
                <option value="urgent">Urgente</option>
              </select>
            </div>
          </div>

          {/* Descripción */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-stone-200 mb-2">
              Descripción <span className="text-red-500">*</span>
            </label>
            <textarea
              id="description"
              required
              rows={8}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Describe tu problema con el mayor detalle posible..."
              className="w-full px-4 py-3 bg-stone-700 border-2 border-stone-600 rounded-lg text-stone-100 placeholder-stone-400 focus:outline-none focus:border-amber-600 transition-colors resize-none"
            />
            <p className="text-sm text-stone-400 mt-2">
              Incluye capturas de pantalla, mensajes de error, o cualquier información que nos ayude a entender el problema
            </p>
          </div>

          {/* Botones */}
          <div className="flex items-center gap-4 pt-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-amber-700 hover:bg-amber-600 disabled:bg-stone-600 disabled:cursor-not-allowed text-white py-3 px-6 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Creando ticket...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  Crear ticket
                </>
              )}
            </button>
            <Link
              href="/tickets"
              className="px-6 py-3 bg-stone-700 hover:bg-stone-600 text-stone-200 rounded-lg font-semibold transition-colors"
            >
              Cancelar
            </Link>
          </div>
        </form>

        {/* Información adicional */}
        <div className="mt-6 bg-stone-800 rounded-lg border-2 border-stone-700 p-6">
          <h3 className="font-semibold text-stone-200 mb-3">💡 Consejos para obtener ayuda rápida:</h3>
          <ul className="space-y-2 text-sm text-stone-300">
            <li className="flex items-start gap-2">
              <span className="text-amber-500 mt-1">•</span>
              <span>Describe el problema con el mayor detalle posible</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-500 mt-1">•</span>
              <span>Incluye los pasos para reproducir el problema</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-500 mt-1">•</span>
              <span>Menciona el navegador y sistema operativo que usas</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-500 mt-1">•</span>
              <span>Si tienes capturas de pantalla, adjúntalas en la descripción</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
