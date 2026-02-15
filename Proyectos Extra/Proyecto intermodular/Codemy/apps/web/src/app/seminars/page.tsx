'use client';

import { useState, useEffect } from 'react';
import { Navigation } from '@/components/Navigation';
import { Footer } from '@/components/Footer';
import { Video, Calendar, Clock, Users, Coins, Star, Play, Eye, MessageSquare } from 'lucide-react';
import Link from 'next/link';

export default function SeminarsPage() {
  const [userCoins, setUserCoins] = useState(0);
  const [activeTab, setActiveTab] = useState<'upcoming' | 'past' | 'my-seminars'>('upcoming');

  useEffect(() => {
    const coins = parseInt(localStorage.getItem('user_coins') || '250');
    setUserCoins(coins);
  }, []);

  const seminarPrices = [
    { duration: 15, coins: 500, entryCost: 50, icon: '⚡', label: 'Express' },
    { duration: 30, coins: 1000, entryCost: 100, icon: '🎯', label: 'Standard' },
    { duration: 60, coins: 2000, entryCost: 200, icon: '🚀', label: 'Master Class' }
  ];

  const upcomingSeminars = [
    {
      id: 1,
      title: 'Introducción a React Hooks',
      instructor: 'María García',
      instructorAvatar: 2,
      duration: 30,
      cost: 100,
      creatorReward: 1000,
      date: '2025-11-18',
      time: '18:00',
      attendees: 23,
      maxAttendees: 50,
      category: 'Web Development',
      level: 'Intermedio',
      thumbnail: '🎨'
    },
    {
      id: 2,
      title: 'Machine Learning con Python',
      instructor: 'Carlos Ruiz',
      instructorAvatar: 5,
      duration: 60,
      cost: 200,
      creatorReward: 2000,
      date: '2025-11-19',
      time: '19:00',
      attendees: 45,
      maxAttendees: 100,
      category: 'IA & Data Science',
      level: 'Avanzado',
      thumbnail: '🤖'
    },
    {
      id: 3,
      title: 'Arduino para Principiantes',
      instructor: 'Ana López',
      instructorAvatar: 3,
      duration: 45,
      cost: 150,
      creatorReward: 1500,
      date: '2025-11-20',
      time: '17:30',
      attendees: 12,
      maxAttendees: 30,
      category: 'Hardware',
      level: 'Principiante',
      thumbnail: '🔌'
    }
  ];

  const pastSeminars = [
    {
      id: 10,
      title: 'Fundamentos de TypeScript',
      instructor: 'Pedro Martínez',
      instructorAvatar: 1,
      duration: 30,
      date: '2025-11-15',
      views: 156,
      rating: 4.8,
      thumbnail: '📘',
      videoUrl: 'https://youtube.com/watch?v=example'
    },
    {
      id: 11,
      title: 'CSS Grid y Flexbox',
      instructor: 'Laura Sánchez',
      instructorAvatar: 4,
      duration: 60,
      date: '2025-11-14',
      views: 234,
      rating: 4.9,
      thumbnail: '🎨',
      videoUrl: 'https://youtube.com/watch?v=example'
    }
  ];

  const getAvatarColor = (index: number) => {
    const colors = [
      'from-blue-500 to-blue-700',
      'from-green-500 to-green-700',
      'from-purple-500 to-purple-700',
      'from-pink-500 to-pink-700',
      'from-orange-500 to-orange-700',
      'from-red-500 to-red-700'
    ];
    return colors[index % colors.length];
  };

  return (
    <main className="min-h-screen bg-stone-900">
      <Navigation />
      
      <div className="pt-24 pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-4xl font-bold text-white mb-2">
                  Seminarios en Vivo
                </h1>
                <p className="text-stone-400">
                  Aprende de la comunidad en sesiones interactivas en directo
                </p>
              </div>
              <div className="flex items-center space-x-4">
                <Link
                  href="/seminars/calendar"
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-3 px-6 rounded-xl transition-all shadow-lg flex items-center space-x-2"
                >
                  <Calendar className="w-5 h-5" />
                  <span>Ver Calendario</span>
                </Link>
                <div className="text-right">
                  <div className="bg-gradient-to-r from-amber-600 to-orange-600 rounded-xl px-6 py-3 inline-flex items-center space-x-2">
                    <Coins className="w-6 h-6 text-white" />
                    <span className="text-2xl font-bold text-white">{userCoins}</span>
                  </div>
                  <p className="text-stone-400 text-sm mt-2">Tus coins</p>
                </div>
              </div>
            </div>

            {/* Create Seminar CTA */}
            <div className="bg-gradient-to-r from-blue-900/20 to-purple-900/20 border-2 border-blue-600/30 rounded-2xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2 flex items-center space-x-2">
                    <Video className="w-6 h-6 text-blue-400" />
                    <span>¿Quieres dar un seminario?</span>
                  </h3>
                  <p className="text-stone-300 mb-4">
                    Comparte tu conocimiento y gana coins mientras enseñas a la comunidad
                  </p>
                  <div className="flex items-center space-x-4">
                    {seminarPrices.map((price) => (
                      <div key={price.duration} className="bg-stone-800/50 rounded-lg px-4 py-2 border border-stone-700">
                        <div className="text-2xl mb-1">{price.icon}</div>
                        <div className="text-white font-bold">{price.duration} min</div>
                        <div className="text-amber-500 text-sm flex items-center space-x-1">
                          <Coins className="w-3 h-3" />
                          <span>{price.coins}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <Link
                  href="/seminars/create"
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl transition-all shadow-lg"
                >
                  Crear Seminario
                </Link>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex items-center space-x-2 mb-8 border-b border-stone-700">
            <button
              onClick={() => setActiveTab('upcoming')}
              className={`px-6 py-3 font-semibold transition-all ${
                activeTab === 'upcoming'
                  ? 'text-white border-b-2 border-amber-600'
                  : 'text-stone-400 hover:text-white'
              }`}
            >
              <Calendar className="w-4 h-4 inline mr-2" />
              Próximos
            </button>
            <button
              onClick={() => setActiveTab('past')}
              className={`px-6 py-3 font-semibold transition-all ${
                activeTab === 'past'
                  ? 'text-white border-b-2 border-amber-600'
                  : 'text-stone-400 hover:text-white'
              }`}
            >
              <Play className="w-4 h-4 inline mr-2" />
              Grabaciones
            </button>
            <button
              onClick={() => setActiveTab('my-seminars')}
              className={`px-6 py-3 font-semibold transition-all ${
                activeTab === 'my-seminars'
                  ? 'text-white border-b-2 border-amber-600'
                  : 'text-stone-400 hover:text-white'
              }`}
            >
              <Video className="w-4 h-4 inline mr-2" />
              Mis Seminarios
            </button>
          </div>

          {/* Upcoming Seminars */}
          {activeTab === 'upcoming' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {upcomingSeminars.map((seminar) => (
                <div
                  key={seminar.id}
                  className="bg-stone-800/50 rounded-xl border border-stone-700 hover:border-amber-600/50 transition-all overflow-hidden"
                >
                  {/* Thumbnail */}
                  <div className="bg-gradient-to-br from-stone-700 to-stone-800 h-40 flex items-center justify-center text-6xl">
                    {seminar.thumbnail}
                  </div>

                  <div className="p-6">
                    {/* Category & Level */}
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs bg-blue-600/20 text-blue-400 px-2 py-1 rounded">
                        {seminar.category}
                      </span>
                      <span className="text-xs bg-amber-600/20 text-amber-400 px-2 py-1 rounded">
                        {seminar.level}
                      </span>
                    </div>

                    {/* Title */}
                    <h3 className="text-xl font-bold text-white mb-3">
                      {seminar.title}
                    </h3>

                    {/* Instructor */}
                    <div className="flex items-center space-x-2 mb-4">
                      <div className={`w-8 h-8 rounded-full bg-gradient-to-r ${getAvatarColor(seminar.instructorAvatar)} flex items-center justify-center text-white font-bold text-sm`}>
                        {seminar.instructor[0]}
                      </div>
                      <span className="text-stone-300 text-sm">{seminar.instructor}</span>
                    </div>

                    {/* Info */}
                    <div className="space-y-2 mb-4 text-sm">
                      <div className="flex items-center text-stone-400">
                        <Calendar className="w-4 h-4 mr-2" />
                        <span>{seminar.date} a las {seminar.time}</span>
                      </div>
                      <div className="flex items-center text-stone-400">
                        <Clock className="w-4 h-4 mr-2" />
                        <span>{seminar.duration} minutos</span>
                      </div>
                      <div className="flex items-center text-stone-400">
                        <Users className="w-4 h-4 mr-2" />
                        <span>{seminar.attendees}/{seminar.maxAttendees} asistentes</span>
                      </div>
                    </div>

                    {/* Price & CTA */}
                    <div className="border-t border-stone-700 pt-4 flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Coins className="w-5 h-5 text-amber-500" />
                        <span className="text-2xl font-bold text-white">{seminar.cost}</span>
                      </div>
                      <button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-2 px-6 rounded-lg transition-all">
                        Inscribirse
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Past Seminars */}
          {activeTab === 'past' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {pastSeminars.map((seminar) => (
                <div
                  key={seminar.id}
                  className="bg-stone-800/50 rounded-xl border border-stone-700 hover:border-amber-600/50 transition-all overflow-hidden"
                >
                  {/* Thumbnail */}
                  <div className="bg-gradient-to-br from-stone-700 to-stone-800 h-40 flex items-center justify-center text-6xl relative">
                    {seminar.thumbnail}
                    <div className="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                      <Play className="w-16 h-16 text-white" />
                    </div>
                  </div>

                  <div className="p-6">
                    <h3 className="text-xl font-bold text-white mb-3">
                      {seminar.title}
                    </h3>

                    {/* Instructor */}
                    <div className="flex items-center space-x-2 mb-4">
                      <div className={`w-8 h-8 rounded-full bg-gradient-to-r ${getAvatarColor(seminar.instructorAvatar)} flex items-center justify-center text-white font-bold text-sm`}>
                        {seminar.instructor[0]}
                      </div>
                      <span className="text-stone-300 text-sm">{seminar.instructor}</span>
                    </div>

                    {/* Stats */}
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-4 text-sm text-stone-400">
                        <div className="flex items-center space-x-1">
                          <Eye className="w-4 h-4" />
                          <span>{seminar.views}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Clock className="w-4 h-4" />
                          <span>{seminar.duration}min</span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Star className="w-4 h-4 text-yellow-500 fill-current" />
                        <span className="text-white font-semibold">{seminar.rating}</span>
                      </div>
                    </div>

                    {/* CTA */}
                    <button className="w-full bg-stone-700 hover:bg-stone-600 text-white font-semibold py-2 px-6 rounded-lg transition-all flex items-center justify-center space-x-2">
                      <Play className="w-4 h-4" />
                      <span>Ver Grabación</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* My Seminars */}
          {activeTab === 'my-seminars' && (
            <div className="text-center py-20">
              <Video className="w-20 h-20 text-stone-600 mx-auto mb-6" />
              <h3 className="text-2xl font-bold text-white mb-4">
                Aún no has creado ningún seminario
              </h3>
              <p className="text-stone-400 mb-8">
                Comparte tu conocimiento y gana coins enseñando a la comunidad
              </p>
              <Link
                href="/seminars/create"
                className="inline-flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-3 px-8 rounded-xl transition-all shadow-lg"
              >
                <Video className="w-5 h-5" />
                <span>Crear Mi Primer Seminario</span>
              </Link>
            </div>
          )}
        </div>
      </div>

      <Footer />
    </main>
  );
}
