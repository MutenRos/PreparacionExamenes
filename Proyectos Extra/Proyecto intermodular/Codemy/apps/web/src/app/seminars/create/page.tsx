'use client';

import { useState } from 'react';
import { Navigation } from '@/components/Navigation';
import { Footer } from '@/components/Footer';
import { Video, Calendar, Clock, Coins, Users, Tag, FileText, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function CreateSeminarPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    level: 'principiante',
    duration: 30,
    date: '',
    time: '',
    maxAttendees: 50,
    requirements: '',
    topics: ''
  });

  const durations = [
    { minutes: 15, coins: 500, entryCost: 50, label: 'Express', description: 'Sesión rápida y enfocada' },
    { minutes: 30, coins: 1000, entryCost: 100, label: 'Standard', description: 'Tiempo perfecto para la mayoría de temas' },
    { minutes: 60, coins: 2000, entryCost: 200, label: 'Master Class', description: 'Profundiza en temas complejos' }
  ];

  const categories = [
    { id: 'web', name: 'Desarrollo Web', icon: '🌐' },
    { id: 'python', name: 'Python & IA', icon: '🐍' },
    { id: 'mobile', name: 'Desarrollo Mobile', icon: '📱' },
    { id: 'hardware', name: 'Hardware & IoT', icon: '🔌' },
    { id: 'security', name: 'Seguridad', icon: '🛡️' },
    { id: 'devops', name: 'DevOps', icon: '🚀' },
    { id: 'design', name: 'Diseño', icon: '🎨' },
    { id: 'other', name: 'Otro', icon: '📚' }
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Aquí se procesaría la creación del seminario
    console.log('Seminario creado:', formData);
    router.push('/seminars');
  };

  const selectedDuration = durations.find(d => d.minutes === formData.duration);

  return (
    <main className="min-h-screen bg-stone-900">
      <Navigation />
      
      <div className="pt-24 pb-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <Link
              href="/seminars"
              className="inline-flex items-center text-stone-400 hover:text-white mb-4 transition-colors"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Volver a seminarios
            </Link>
            <h1 className="text-4xl font-bold text-white mb-2">
              Crear Nuevo Seminario
            </h1>
            <p className="text-stone-400">
              Comparte tu conocimiento y gana coins enseñando a la comunidad
            </p>
          </div>

          {/* Progress Steps */}
          <div className="mb-12">
            <div className="flex items-center justify-between">
              {[1, 2, 3].map((s) => (
                <div key={s} className="flex items-center">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold transition-all ${
                    step >= s
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                      : 'bg-stone-700 text-stone-400'
                  }`}>
                    {s}
                  </div>
                  {s < 3 && (
                    <div className={`w-full h-1 mx-4 ${
                      step > s ? 'bg-gradient-to-r from-blue-600 to-purple-600' : 'bg-stone-700'
                    }`} />
                  )}
                </div>
              ))}
            </div>
            <div className="flex justify-between mt-2">
              <span className="text-sm text-stone-400">Información básica</span>
              <span className="text-sm text-stone-400">Detalles</span>
              <span className="text-sm text-stone-400">Confirmación</span>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            {/* Step 1: Basic Info */}
            {step === 1 && (
              <div className="space-y-6">
                <div className="bg-stone-800/50 rounded-xl border border-stone-700 p-6">
                  <h2 className="text-2xl font-bold text-white mb-6">Información Básica</h2>

                  {/* Title */}
                  <div className="mb-6">
                    <label className="block text-white font-semibold mb-2">
                      Título del seminario
                    </label>
                    <input
                      type="text"
                      value={formData.title}
                      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                      placeholder="ej: Introducción a React Hooks"
                      className="w-full bg-stone-900 border border-stone-700 text-white px-4 py-3 rounded-lg focus:border-blue-600 focus:outline-none"
                      required
                    />
                  </div>

                  {/* Description */}
                  <div className="mb-6">
                    <label className="block text-white font-semibold mb-2">
                      Descripción
                    </label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      placeholder="Describe de qué tratará tu seminario..."
                      rows={4}
                      className="w-full bg-stone-900 border border-stone-700 text-white px-4 py-3 rounded-lg focus:border-blue-600 focus:outline-none resize-none"
                      required
                    />
                  </div>

                  {/* Category */}
                  <div className="mb-6">
                    <label className="block text-white font-semibold mb-2">
                      Categoría
                    </label>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {categories.map((cat) => (
                        <button
                          key={cat.id}
                          type="button"
                          onClick={() => setFormData({ ...formData, category: cat.id })}
                          className={`p-4 rounded-lg border-2 transition-all ${
                            formData.category === cat.id
                              ? 'border-blue-600 bg-blue-600/20'
                              : 'border-stone-700 bg-stone-900 hover:border-stone-600'
                          }`}
                        >
                          <div className="text-3xl mb-2">{cat.icon}</div>
                          <div className="text-white text-sm font-semibold">{cat.name}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Level */}
                  <div>
                    <label className="block text-white font-semibold mb-2">
                      Nivel
                    </label>
                    <div className="grid grid-cols-3 gap-3">
                      {['principiante', 'intermedio', 'avanzado'].map((level) => (
                        <button
                          key={level}
                          type="button"
                          onClick={() => setFormData({ ...formData, level })}
                          className={`py-3 px-4 rounded-lg border-2 transition-all capitalize ${
                            formData.level === level
                              ? 'border-blue-600 bg-blue-600/20 text-white'
                              : 'border-stone-700 bg-stone-900 text-stone-400 hover:border-stone-600'
                          }`}
                        >
                          {level}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => setStep(2)}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 rounded-xl transition-all"
                >
                  Continuar
                </button>
              </div>
            )}

            {/* Step 2: Details */}
            {step === 2 && (
              <div className="space-y-6">
                <div className="bg-stone-800/50 rounded-xl border border-stone-700 p-6">
                  <h2 className="text-2xl font-bold text-white mb-6">Detalles del Seminario</h2>

                  {/* Duration */}
                  <div className="mb-6">
                    <label className="block text-white font-semibold mb-2">
                      Duración
                    </label>
                    <div className="grid grid-cols-3 gap-4">
                      {durations.map((dur) => (
                        <button
                          key={dur.minutes}
                          type="button"
                          onClick={() => setFormData({ ...formData, duration: dur.minutes })}
                          className={`p-4 rounded-lg border-2 transition-all ${
                            formData.duration === dur.minutes
                              ? 'border-blue-600 bg-blue-600/20'
                              : 'border-stone-700 bg-stone-900 hover:border-stone-600'
                          }`}
                        >
                          <div className="text-white font-bold text-xl mb-1">{dur.minutes} min</div>
                          <div className="text-stone-400 text-sm mb-2">{dur.label}</div>
                          <div className="flex items-center justify-center space-x-1 text-amber-500">
                            <Coins className="w-4 h-4" />
                            <span className="font-bold">{dur.coins}</span>
                          </div>
                          <div className="text-stone-500 text-xs mt-2">{dur.description}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Date & Time */}
                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div>
                      <label className="block text-white font-semibold mb-2">
                        <Calendar className="w-4 h-4 inline mr-2" />
                        Fecha
                      </label>
                      <input
                        type="date"
                        value={formData.date}
                        onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                        className="w-full bg-stone-900 border border-stone-700 text-white px-4 py-3 rounded-lg focus:border-blue-600 focus:outline-none"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-white font-semibold mb-2">
                        <Clock className="w-4 h-4 inline mr-2" />
                        Hora
                      </label>
                      <input
                        type="time"
                        value={formData.time}
                        onChange={(e) => setFormData({ ...formData, time: e.target.value })}
                        className="w-full bg-stone-900 border border-stone-700 text-white px-4 py-3 rounded-lg focus:border-blue-600 focus:outline-none"
                        required
                      />
                    </div>
                  </div>

                  {/* Max Attendees */}
                  <div className="mb-6">
                    <label className="block text-white font-semibold mb-2">
                      <Users className="w-4 h-4 inline mr-2" />
                      Máximo de asistentes
                    </label>
                    <input
                      type="number"
                      value={formData.maxAttendees}
                      onChange={(e) => setFormData({ ...formData, maxAttendees: parseInt(e.target.value) })}
                      min="5"
                      max="500"
                      className="w-full bg-stone-900 border border-stone-700 text-white px-4 py-3 rounded-lg focus:border-blue-600 focus:outline-none"
                    />
                    <p className="text-stone-400 text-sm mt-2">Recomendado: 30-100 asistentes</p>
                  </div>

                  {/* Topics */}
                  <div className="mb-6">
                    <label className="block text-white font-semibold mb-2">
                      <Tag className="w-4 h-4 inline mr-2" />
                      Temas que cubrirás
                    </label>
                    <textarea
                      value={formData.topics}
                      onChange={(e) => setFormData({ ...formData, topics: e.target.value })}
                      placeholder="Separa cada tema con una coma (ej: Hooks, useState, useEffect, Custom Hooks)"
                      rows={3}
                      className="w-full bg-stone-900 border border-stone-700 text-white px-4 py-3 rounded-lg focus:border-blue-600 focus:outline-none resize-none"
                    />
                  </div>

                  {/* Requirements */}
                  <div>
                    <label className="block text-white font-semibold mb-2">
                      <FileText className="w-4 h-4 inline mr-2" />
                      Requisitos previos (opcional)
                    </label>
                    <textarea
                      value={formData.requirements}
                      onChange={(e) => setFormData({ ...formData, requirements: e.target.value })}
                      placeholder="¿Qué deben saber los asistentes antes del seminario?"
                      rows={3}
                      className="w-full bg-stone-900 border border-stone-700 text-white px-4 py-3 rounded-lg focus:border-blue-600 focus:outline-none resize-none"
                    />
                  </div>
                </div>

                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={() => setStep(1)}
                    className="flex-1 bg-stone-700 hover:bg-stone-600 text-white font-bold py-4 rounded-xl transition-all"
                  >
                    Atrás
                  </button>
                  <button
                    type="button"
                    onClick={() => setStep(3)}
                    className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 rounded-xl transition-all"
                  >
                    Continuar
                  </button>
                </div>
              </div>
            )}

            {/* Step 3: Confirmation */}
            {step === 3 && (
              <div className="space-y-6">
                <div className="bg-stone-800/50 rounded-xl border border-stone-700 p-6">
                  <h2 className="text-2xl font-bold text-white mb-6">Confirmación</h2>

                  <div className="space-y-4 mb-6">
                    <div className="flex justify-between items-center py-3 border-b border-stone-700">
                      <span className="text-stone-400">Título:</span>
                      <span className="text-white font-semibold">{formData.title}</span>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-stone-700">
                      <span className="text-stone-400">Categoría:</span>
                      <span className="text-white font-semibold capitalize">{formData.category}</span>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-stone-700">
                      <span className="text-stone-400">Nivel:</span>
                      <span className="text-white font-semibold capitalize">{formData.level}</span>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-stone-700">
                      <span className="text-stone-400">Duración:</span>
                      <span className="text-white font-semibold">{formData.duration} minutos</span>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-stone-700">
                      <span className="text-stone-400">Fecha y hora:</span>
                      <span className="text-white font-semibold">{formData.date} a las {formData.time}</span>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-stone-700">
                      <span className="text-stone-400">Máx. asistentes:</span>
                      <span className="text-white font-semibold">{formData.maxAttendees}</span>
                    </div>
                    <div className="flex justify-between items-center py-3">
                      <span className="text-stone-400">Ganarás:</span>
                      <div className="flex items-center space-x-2">
                        <Coins className="w-5 h-5 text-amber-500" />
                        <span className="text-white font-bold text-xl">{selectedDuration?.coins || 0}</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-900/20 border border-blue-600/30 rounded-lg p-4 mb-6">
                    <h4 className="text-white font-semibold mb-2">📹 Información sobre la grabación</h4>
                    <ul className="text-stone-300 text-sm space-y-1">
                      <li>• El seminario se grabará automáticamente</li>
                      <li>• Se subirá a YouTube en tu canal de Codemy</li>
                      <li>• Aparecerá en tu perfil y en la sección de grabaciones</li>
                      <li>• Los asistentes podrán valorar el seminario después</li>
                    </ul>
                  </div>
                </div>

                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={() => setStep(2)}
                    className="flex-1 bg-stone-700 hover:bg-stone-600 text-white font-bold py-4 rounded-xl transition-all"
                  >
                    Atrás
                  </button>
                  <button
                    type="submit"
                    className="flex-1 bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white font-bold py-4 rounded-xl transition-all shadow-lg"
                  >
                    Crear Seminario
                  </button>
                </div>
              </div>
            )}
          </form>
        </div>
      </div>

      <Footer />
    </main>
  );
}
