'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Trophy, Medal, Award, Crown, TrendingUp, Users, Zap } from 'lucide-react';
import { createClient } from '@supabase/supabase-js';

interface LeaderboardEntry {
  id: string;
  name: string;
  avatar: string;
  xp: number;
  level: number;
  streak: number;
  rank: number;
  avatarColor?: number;
}

// Crear cliente de Supabase
const getSupabaseClient = () => {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  
  if (!supabaseUrl || !supabaseAnonKey) {
    return null;
  }
  
  return createClient(supabaseUrl, supabaseAnonKey);
};

export default function LeaderboardPage() {
  const [timeframe, setTimeframe] = useState<'daily' | 'weekly' | 'monthly' | 'alltime'>('alltime');
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [currentUser, setCurrentUser] = useState<LeaderboardEntry | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeaderboard();
  }, [timeframe]);

  const loadLeaderboard = async () => {
    setLoading(true);
    
    try {
      const supabase = getSupabaseClient();
      
      if (supabase) {
        // Intentar cargar desde Supabase
        const { data: users, error } = await supabase
          .from('profiles')
          .select('id, name, avatar_color, total_xp, level, streak_days')
          .order('total_xp', { ascending: false })
          .limit(50);

        if (!error && users && users.length > 0) {
          const formattedLeaderboard = users.map((user, index) => ({
            id: user.id,
            name: user.name || 'Usuario',
            avatar: (user.name || 'U').substring(0, 2).toUpperCase(),
            xp: user.total_xp || 0,
            level: user.level || 1,
            streak: user.streak_days || 0,
            rank: index + 1,
            avatarColor: user.avatar_color || 0
          }));
          
          setLeaderboard(formattedLeaderboard);
          
          // Encontrar usuario actual
          const { data: { session } } = await supabase.auth.getSession();
          if (session) {
            const current = formattedLeaderboard.find(u => u.id === session.user.id);
            if (current) {
              setCurrentUser(current);
            }
          }
          
          setLoading(false);
          return;
        }
      }
      
      // Si no hay datos de Supabase, usar datos locales
      loadLocalLeaderboard();
    } catch (error) {
      console.error('Error cargando leaderboard:', error);
      loadLocalLeaderboard();
    }
  };

  const loadLocalLeaderboard = () => {
    // Generar leaderboard basado en datos locales del usuario actual
    const localUserName = localStorage.getItem('user_name') || 'Estudiante';
    const localUserEmail = localStorage.getItem('user_email') || 'estudiante@ejemplo.com';
    
    // Calcular XP total del usuario actual
    let totalXP = 0;
    let completedLessons = 0;
    
    const courses = [
      { id: 'py-intro', lessons: 4 },
      { id: 'py-variables', lessons: 5 },
      { id: 'py-control', lessons: 6 },
      { id: 'py-functions', lessons: 6 },
      { id: 'py-classes', lessons: 6 },
      { id: 'py-files', lessons: 6 },
    ];

    courses.forEach(course => {
      for (let i = 1; i <= course.lessons; i++) {
        const key = `lesson_${course.id}_${i}`;
        if (localStorage.getItem(key) === 'completed') {
          totalXP += 50;
          completedLessons++;
        }
      }
    });

    const level = Math.floor(totalXP / 100) + 1;
    const streak = parseInt(localStorage.getItem('streak_days') || '0');
    const avatarColor = parseInt(localStorage.getItem('user_avatar_color') || '0');

    // Solo el usuario actual
    const currentUserData: LeaderboardEntry = {
      id: localUserEmail,
      name: localUserName,
      avatar: localUserName.substring(0, 2).toUpperCase(),
      xp: totalXP,
      level: level,
      streak: streak,
      rank: 1,
      avatarColor: avatarColor
    };

    setLeaderboard([currentUserData]);
    setCurrentUser(currentUserData);
    setLoading(false);
  };

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <Crown className="w-6 h-6 text-yellow-500" />;
      case 2:
        return <Medal className="w-6 h-6 text-gray-400" />;
      case 3:
        return <Medal className="w-6 h-6 text-amber-600" />;
      default:
        return <span className="text-lg font-bold text-gray-400">#{rank}</span>;
    }
  };

  const getRankBadgeColor = (rank: number) => {
    switch (rank) {
      case 1:
        return 'from-yellow-400 to-yellow-600';
      case 2:
        return 'from-gray-300 to-gray-500';
      case 3:
        return 'from-amber-400 to-amber-600';
      default:
        return 'from-stone-400 to-stone-500';
    }
  };

  return (
    <div className="min-h-screen bg-stone-900">
      {/* Header */}
      <div className="bg-stone-800 backdrop-blur-sm shadow-sm border-b-2 border-stone-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-amber-600 to-amber-500 bg-clip-text text-transparent">
              Code Dungeon
            </Link>
            <Link href="/dashboard" className="text-sm text-stone-300 hover:text-stone-100 font-medium">
              ← Volver al dashboard
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Title */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Trophy className="w-12 h-12 text-yellow-500" />
            <h1 className="text-4xl font-bold text-stone-100">Tabla de Líderes</h1>
          </div>
          <p className="text-stone-400">Compite con otros estudiantes y sube en el ranking</p>
        </div>

        {/* Timeframe Selector */}
        <div className="flex justify-center mb-8">
          <div className="bg-stone-800 backdrop-blur-sm rounded-lg shadow-md p-1 inline-flex border-2 border-stone-700">
            {(['daily', 'weekly', 'monthly', 'alltime'] as const).map((period) => (
              <button
                key={period}
                onClick={() => setTimeframe(period)}
                className={`px-6 py-2 rounded-md text-sm font-medium transition-colors ${
                  timeframe === period
                    ? 'bg-amber-700 border-2 border-amber-800 text-stone-100'
                    : 'text-stone-400 hover:text-stone-100'
                }`}
              >
                {period === 'daily' && 'Diario'}
                {period === 'weekly' && 'Semanal'}
                {period === 'monthly' && 'Mensual'}
                {period === 'alltime' && 'Todo el tiempo'}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Leaderboard */}
          <div className="lg:col-span-2">
            {/* Top 3 Podium */}
            <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-8 mb-6 border-2 border-stone-700">
              <div className="flex items-end justify-center gap-4">
                {/* 2nd Place */}
                {leaderboard[1] && (
                  <div className="flex-1 text-center">
                    <div className="relative inline-block mb-3">
                      <div className="w-20 h-20 bg-gradient-to-br from-gray-300 to-gray-500 rounded-full flex items-center justify-center text-white font-bold text-xl mb-2">
                        {leaderboard[1].avatar}
                      </div>
                      <div className="absolute -top-2 -right-2 bg-slate-800/50 backdrop-blur-sm rounded-full p-1 shadow-md">
                        <Medal className="w-6 h-6 text-gray-400" />
                      </div>
                    </div>
                    <h3 className="font-bold text-stone-100">{leaderboard[1].name}</h3>
                    <p className="text-sm text-stone-400">Nivel {leaderboard[1].level}</p>
                    <p className="text-lg font-bold text-stone-100 mt-2">{leaderboard[1].xp} XP</p>
                    <div className="mt-3 h-24 bg-gradient-to-t from-gray-300 to-gray-400 rounded-t-lg flex items-end justify-center pb-2">
                      <span className="text-white font-bold text-2xl">2</span>
                    </div>
                  </div>
                )}

                {/* 1st Place */}
                {leaderboard[0] && (
                  <div className="flex-1 text-center">
                    <div className="relative inline-block mb-3">
                      <div className="w-24 h-24 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center text-white font-bold text-2xl mb-2 ring-4 ring-yellow-200">
                        {leaderboard[0].avatar}
                      </div>
                      <div className="absolute -top-2 -right-2 bg-slate-800/50 backdrop-blur-sm rounded-full p-1 shadow-md">
                        <Crown className="w-8 h-8 text-yellow-500" />
                      </div>
                    </div>
                    <h3 className="font-bold text-stone-100 text-lg">{leaderboard[0].name}</h3>
                    <p className="text-sm text-stone-400">Nivel {leaderboard[0].level}</p>
                    <p className="text-xl font-bold text-yellow-600 mt-2">{leaderboard[0].xp} XP</p>
                    <div className="mt-3 h-32 bg-gradient-to-t from-yellow-400 to-yellow-500 rounded-t-lg flex items-end justify-center pb-2">
                      <span className="text-white font-bold text-3xl">1</span>
                    </div>
                  </div>
                )}

                {/* 3rd Place */}
                {leaderboard[2] && (
                  <div className="flex-1 text-center">
                    <div className="relative inline-block mb-3">
                      <div className="w-20 h-20 bg-gradient-to-br from-amber-400 to-amber-600 rounded-full flex items-center justify-center text-white font-bold text-xl mb-2">
                        {leaderboard[2].avatar}
                      </div>
                      <div className="absolute -top-2 -right-2 bg-slate-800/50 backdrop-blur-sm rounded-full p-1 shadow-md">
                        <Medal className="w-6 h-6 text-amber-600" />
                      </div>
                    </div>
                    <h3 className="font-bold text-stone-100">{leaderboard[2].name}</h3>
                    <p className="text-sm text-stone-400">Nivel {leaderboard[2].level}</p>
                    <p className="text-lg font-bold text-amber-700 mt-2">{leaderboard[2].xp} XP</p>
                    <div className="mt-3 h-20 bg-gradient-to-t from-amber-400 to-amber-500 rounded-t-lg flex items-end justify-center pb-2">
                      <span className="text-white font-bold text-2xl">3</span>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Rest of Leaderboard */}
            <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg overflow-hidden border-2 border-stone-700">
              <div className="divide-y divide-stone-700">
                {leaderboard.slice(3).map((entry) => (
                  <div key={entry.id} className="p-4 hover:bg-stone-700 transition-colors">
                    <div className="flex items-center gap-4">
                      <div className="w-12 text-center">
                        {getRankIcon(entry.rank)}
                      </div>
                      <div className={`w-12 h-12 bg-gradient-to-br ${getRankBadgeColor(entry.rank)} rounded-full flex items-center justify-center text-white font-bold`}>
                        {entry.avatar}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-stone-100">{entry.name}</h3>
                        <p className="text-sm text-stone-400">Nivel {entry.level}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-stone-100">{entry.xp} XP</p>
                        <div className="flex items-center gap-1 text-sm text-orange-600">
                          <Zap className="w-4 h-4" />
                          <span>{entry.streak}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Current User Position */}
            {currentUser && (
              <div className="bg-amber-700 border-2 border-amber-800 rounded-xl shadow-lg p-6 mt-6">
                <div className="flex items-center gap-4 text-white">
                  <div className="w-12 text-center">
                    <span className="text-lg font-bold">#{currentUser.rank}</span>
                  </div>
                  <div className="w-12 h-12 bg-stone-900/20 backdrop-blur rounded-full flex items-center justify-center font-bold">
                    {currentUser.avatar}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold">{currentUser.name} (Tú)</h3>
                    <p className="text-sm text-white/80">Nivel {currentUser.level}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold">{currentUser.xp} XP</p>
                    <div className="flex items-center gap-1 text-sm">
                      <Zap className="w-4 h-4" />
                      <span>{currentUser.streak}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Stats */}
            <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-stone-700">
              <h2 className="text-xl font-bold text-stone-100 mb-4 flex items-center gap-2">
                <TrendingUp className="w-6 h-6 text-amber-600" />
                Estadísticas
              </h2>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-stone-400">Total de participantes</span>
                    <span className="font-bold text-stone-100">156</span>
                  </div>
                  <div className="w-full bg-stone-700 rounded-full h-2">
                    <div className="bg-gradient-to-r from-amber-600 to-amber-500 h-2 rounded-full w-3/4" />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-stone-400">XP promedio</span>
                    <span className="font-bold text-stone-100">2,450</span>
                  </div>
                  <div className="w-full bg-stone-700 rounded-full h-2">
                    <div className="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full w-1/2" />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-stone-400">Mayor racha</span>
                    <span className="font-bold text-stone-100">28 días</span>
                  </div>
                  <div className="w-full bg-stone-700 rounded-full h-2">
                    <div className="bg-gradient-to-r from-orange-500 to-red-500 h-2 rounded-full w-full" />
                  </div>
                </div>
              </div>
            </div>

            {/* Achievements */}
            <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-stone-700">
              <h2 className="text-xl font-bold text-stone-100 mb-4 flex items-center gap-2">
                <Award className="w-6 h-6 text-amber-600" />
                Premios semanales
              </h2>
              <div className="space-y-3">
                <div className="p-3 bg-yellow-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-1">
                    <Crown className="w-5 h-5 text-yellow-600" />
                    <span className="font-semibold text-yellow-900">1er Lugar</span>
                  </div>
                  <p className="text-sm text-yellow-800">Badge exclusivo + 500 XP</p>
                </div>

                <div className="p-3 bg-stone-950 rounded-lg border-2 border-stone-700">
                  <div className="flex items-center gap-2 mb-1">
                    <Medal className="w-5 h-5 text-stone-300" />
                    <span className="font-semibold text-stone-100">2do Lugar</span>
                  </div>
                  <p className="text-sm text-stone-400">Badge de plata + 300 XP</p>
                </div>

                <div className="p-3 bg-amber-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-1">
                    <Medal className="w-5 h-5 text-amber-600" />
                    <span className="font-semibold text-amber-900">3er Lugar</span>
                  </div>
                  <p className="text-sm text-amber-800">Badge de bronce + 200 XP</p>
                </div>
              </div>
            </div>

            {/* Tips */}
            <div className="bg-amber-700 border-2 border-amber-800 rounded-xl shadow-lg p-6 text-white">
              <h2 className="text-xl font-bold mb-4">💡 Consejo</h2>
              <p className="text-sm text-white/90">
                Completa lecciones diariamente para mantener tu racha y ganar más XP.
                ¡Las rachas largas te dan bonificaciones!
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
