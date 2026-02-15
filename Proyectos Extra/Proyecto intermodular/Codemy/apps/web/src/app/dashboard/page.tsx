'use client';

import { useState, useEffect, useMemo, useCallback, memo } from 'react';
import Link from 'next/link';
import { Trophy, Target, Flame, BookOpen, Award, TrendingUp, Clock, Star, User, Users, MessageCircle, Gift, Video } from 'lucide-react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import { checkAchievements } from '@/data/achievements';
import { optimizedLocalStorage } from '@/lib/performance';
import { AccessGuard } from '@/components/AccessGuard';

// Lazy load de componentes pesados
const XPTracker = dynamic(() => import('@/components/dashboard/XPTracker'), {
  loading: () => <div className="animate-pulse bg-stone-800 h-32 rounded-lg border-2 border-stone-700" />,
});

const ActivityStats = dynamic(() => import('@/components/dashboard/ActivityStats'), {
  loading: () => <div className="animate-pulse bg-stone-800 h-48 rounded-lg border-2 border-stone-700" />,
});

export default function StudentDashboard() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState<any>(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [stats, setStats] = useState({
    xp: 0,
    level: 1,
    streak: 0,
    coursesInProgress: 0,
    coursesCompleted: 0,
    achievements: 0,
  });
  const [recentAchievements, setRecentAchievements] = useState<any[]>([]);

  useEffect(() => {
    // Cargar datos del usuario autenticado
    const loadUserData = async () => {
      try {
        // Obtener sesión del usuario
        const sessionResponse = await fetch('/api/auth/session');
        const sessionData = await sessionResponse.json();
        
        if (!sessionData.user) {
          router.push('/auth/login');
          return;
        }
        
        // Establecer datos del usuario
        const mockUser = {
          name: sessionData.user.email?.split('@')[0] || 'Usuario',
          email: sessionData.user.email,
          avatar: null,
        };
        
        setUserData(mockUser);
        
        // Verificar si es admin
        const isAdminUser = sessionData.user.email === 'admin@codedungeon.es';
        setIsAdmin(isAdminUser);
        
        // Calcular stats basados en localStorage (optimizado)
        let totalXP = 0;
        let completedLessons = 0;
        let completedCoursesCount = 0;
        let inProgressCoursesCount = 0;

        // Usar caché optimizado de localStorage (30 segundos para actualización rápida)
        const cachedStats = optimizedLocalStorage.getItem('dashboard_stats_cache');
        const cacheTimestamp = optimizedLocalStorage.getItem('dashboard_stats_timestamp');
        const now = Date.now();
        
        // Si el caché es reciente (menos de 30 segundos), usarlo
        if (cachedStats && cacheTimestamp && (now - parseInt(cacheTimestamp)) < 30 * 1000) {
          const stats = JSON.parse(cachedStats);
          totalXP = stats.totalXP;
          completedLessons = stats.completedLessons;
          completedCoursesCount = stats.completedCoursesCount;
          inProgressCoursesCount = stats.inProgressCoursesCount;
        } else {
          // Calcular stats (solo si no hay caché válido)
          const courses = [
            { id: 'py-intro', lessons: 4, xpPerLesson: 50 },
            { id: 'py-variables', lessons: 5, xpPerLesson: 50 },
            { id: 'py-control', lessons: 6, xpPerLesson: 50 },
            { id: 'py-functions', lessons: 6, xpPerLesson: 50, bonusLastLesson: 50 },
            { id: 'py-classes', lessons: 6, xpPerLesson: 50, bonusLastLesson: 50 },
            { id: 'py-files', lessons: 6, xpPerLesson: 50, bonusLastLesson: 50 },
          ];

          courses.forEach(course => {
            let courseLessonsCompleted = 0;
            
            for (let i = 1; i <= course.lessons; i++) {
              const key = `lesson_${course.id}_${i}`;
              if (optimizedLocalStorage.getItem(key) === 'completed') {
                const isProjectLesson = course.bonusLastLesson && i === course.lessons;
                const lessonXP = isProjectLesson ? course.xpPerLesson + course.bonusLastLesson : course.xpPerLesson;
                
                totalXP += lessonXP;
                completedLessons++;
                courseLessonsCompleted++;
              }
            }

            if (courseLessonsCompleted === course.lessons) {
              totalXP += 100; // Bonus por completar curso
              completedCoursesCount++;
            } else if (courseLessonsCompleted > 0) {
              inProgressCoursesCount++;
            }
          });
          
          // Guardar en caché
          optimizedLocalStorage.setItem('dashboard_stats_cache', JSON.stringify({
            totalXP,
            completedLessons,
            completedCoursesCount,
            inProgressCoursesCount
          }));
          optimizedLocalStorage.setItem('dashboard_stats_timestamp', now.toString());
        }

        const level = Math.floor(totalXP / 100) + 1;
        const streak = parseInt(optimizedLocalStorage.getItem('streak_days') || '0');
        
        const unlockedAchievements = checkAchievements({
          lessonsCompleted: completedLessons,
          coursesCompleted: completedCoursesCount,
          totalXP,
          streakDays: streak,
          perfectLessons: 0,
          lessonsToday: 0,
        });
        
        setStats({
          xp: totalXP,
          level,
          streak,
          coursesInProgress: inProgressCoursesCount,
          coursesCompleted: completedCoursesCount,
          achievements: unlockedAchievements.length,
        });
        
        // Guardar logros recientes
        setRecentAchievements(unlockedAchievements.slice(-3).reverse());
        
        setLoading(false);
      } catch (error) {
        console.error('Error loading user data:', error);
        setLoading(false);
      }
    };
    
    loadUserData();
  }, [router]);

  const [activeCourses, setActiveCourses] = useState<any[]>([]);

  const [weeklyActivity, setWeeklyActivity] = useState([
    { day: 'L', xp: 0, active: false },
    { day: 'M', xp: 0, active: false },
    { day: 'X', xp: 0, active: false },
    { day: 'J', xp: 0, active: false },
    { day: 'V', xp: 0, active: false },
    { day: 'S', xp: 0, active: false },
    { day: 'D', xp: 0, active: false },
  ]);

  const nextLevel = stats.level * 500;
  const progressToNext = stats.xp > 0 ? ((stats.xp % 500) / 500) * 100 : 0;

  if (loading) {
    return (
      <div className="min-h-screen bg-stone-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-amber-700 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-stone-200">Cargando tu dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <AccessGuard requiresAuth={true} requiresSubscription={false}>
      <div className="min-h-screen bg-stone-900">
        {/* Header */}
        <div className="bg-stone-800/50 backdrop-blur-sm shadow-lg border-b-2 border-stone-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div>
                <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-stone-400 to-amber-400 bg-clip-text text-transparent">
                  Code Dungeon
                </Link>
                <p className="text-sm text-stone-300 mt-1">¡Bienvenido de nuevo, <span className="font-semibold text-stone-200">{userData?.name || 'Estudiante'}</span>!</p>
              </div>
              <div className="flex items-center gap-4">
                {isAdmin && (
                  <Link 
                    href="/admin" 
                    className="px-4 py-2 bg-amber-700 hover:bg-amber-600 text-white rounded-lg transition-colors text-sm font-medium shadow-lg"
                  >
                    Panel Admin
                  </Link>
                )}
                <Link href="/profile" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
                  <div className="text-right">
                    <p className="text-sm font-medium text-stone-200">{userData?.name || 'Estudiante'}</p>
                    <p className="text-xs text-stone-400">Nivel {stats.level}</p>
                  </div>
                  <div className="w-10 h-10 bg-gradient-to-br from-stone-500 to-amber-500 rounded-full flex items-center justify-center text-white font-bold shadow-lg">
                    {userData?.name ? userData.name.charAt(0).toUpperCase() : <User className="w-5 h-5" />}
                  </div>
                </Link>
              </div>
            </div>
          </div>
        </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* XP Card */}
          <div className="bg-stone-800 rounded-lg shadow-2xl p-6 border-2 border-stone-700 hover:border-amber-700 transition-all">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-amber-700/20 rounded-lg">
                <Star className="w-6 h-6 text-amber-600" />
              </div>
              <span className="text-2xl font-bold text-amber-600">{stats.xp} XP</span>
            </div>
            <h3 className="text-sm font-medium text-stone-200 mb-2">Experiencia Total</h3>
            <div className="w-full bg-stone-700 rounded-full h-2">
              <div
                className="bg-amber-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${progressToNext}%` }}
              />
            </div>
            <p className="text-xs text-stone-300 mt-2">{500 - (stats.xp % 500)} XP para nivel {stats.level + 1}</p>
          </div>

          {/* Streak Card */}
          <div className="bg-stone-800 rounded-lg shadow-2xl p-6 border-2 border-stone-700 hover:border-amber-700 transition-all">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-amber-700/20 rounded-lg">
                <Flame className="w-6 h-6 text-amber-600" />
              </div>
              <span className="text-2xl font-bold text-amber-600">{stats.streak} días</span>
            </div>
            <h3 className="text-sm font-medium text-stone-200">Racha actual</h3>
            <p className="text-xs text-stone-300 mt-2">¡Sigue así! 🔥</p>
          </div>

          {/* Courses Card */}
          <div className="bg-stone-800 rounded-lg shadow-2xl p-6 border-2 border-stone-700 hover:border-amber-700 transition-all">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-amber-700/20 rounded-lg">
                <BookOpen className="w-6 h-6 text-amber-600" />
              </div>
              <span className="text-2xl font-bold text-amber-600">{stats.coursesInProgress}</span>
            </div>
            <h3 className="text-sm font-medium text-stone-200">Cursos activos</h3>
            <p className="text-xs text-stone-300 mt-2">{stats.coursesCompleted} completados</p>
          </div>

          {/* Achievements Card */}
          <div className="bg-stone-800 rounded-lg shadow-2xl p-6 border-2 border-stone-700 hover:border-amber-700 transition-all">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-amber-700/20 rounded-lg">
                <Trophy className="w-6 h-6 text-amber-600" />
              </div>
              <span className="text-2xl font-bold text-amber-600">{stats.achievements}</span>
            </div>
            <h3 className="text-sm font-medium text-stone-200">Logros desbloqueados</h3>
            <p className="text-xs text-stone-300 mt-2">¡Sigue coleccionando!</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Activity Stats */}
            <ActivityStats />

            {/* Active Courses */}
            <div className="bg-stone-800 rounded-lg shadow-2xl p-6 border-2 border-stone-700">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-stone-100">Cursos en progreso</h2>
                <Link href="/skill-tree-general" className="text-sm text-amber-600 hover:text-amber-500 font-medium transition-colors">
                  Ver árbol de habilidades completo 🌟
                </Link>
              </div>

              {activeCourses.length === 0 ? (
                <div className="text-center py-12">
                  <div className="w-20 h-20 bg-amber-700/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <BookOpen className="w-10 h-10 text-amber-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-stone-100 mb-2">
                    ¡Comienza tu viaje de aprendizaje!
                  </h3>
                  <p className="text-stone-300 mb-6">
                    Explora el árbol de habilidades y comienza a aprender.
                  </p>
                  <Link
                    href="/skill-tree-general"
                    className="inline-flex items-center gap-2 px-6 py-3 bg-amber-700 text-white rounded-lg hover:bg-amber-600 transition-all font-medium shadow-lg border-2 border-amber-800"
                  >
                    Ver Árbol Completo 🌟
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {activeCourses.map((course) => (
                    <div key={course.id} className="border-2 border-stone-700 bg-stone-900/30 rounded-lg p-4 hover:border-amber-700 transition-all">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="font-semibold text-stone-100">{course.title}</h3>
                          <p className="text-sm text-stone-300 mt-1">{course.nextLesson}</p>
                        </div>
                        <span className="text-sm font-medium text-amber-600">{course.progress}%</span>
                      </div>

                      <div className="w-full bg-stone-700 rounded-full h-2 mb-3">
                        <div
                          className="bg-amber-600 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${course.progress}%` }}
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 text-xs text-stone-300">
                          <Clock className="w-4 h-4" />
                          <span>{course.timeSpent}</span>
                        </div>
                        <Link
                          href={`/course/${course.slug}`}
                          className="text-sm font-medium text-amber-600 hover:text-amber-500 transition-colors"
                        >
                          Continuar →
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Weekly Activity */}
            <div className="bg-stone-800 rounded-lg shadow-2xl p-6 border-2 border-stone-700">
              <h2 className="text-xl font-bold text-stone-100 mb-6">Actividad semanal</h2>
              <div className="flex items-end justify-between gap-2 h-40">
                {weeklyActivity.map((day, index) => (
                  <div key={index} className="flex-1 flex flex-col items-center gap-2">
                    <div className="w-full bg-stone-700/50 rounded-t-lg relative" style={{ height: '100%' }}>
                      <div
                        className={`absolute bottom-0 w-full rounded-t-lg transition-all duration-500 ${
                          day.active
                            ? 'bg-amber-600'
                            : 'bg-stone-600/50'
                        }`}
                        style={{ height: `${(day.xp / 250) * 100}%` }}
                      />
                    </div>
                    <span className="text-xs font-medium text-stone-200">{day.day}</span>
                    <span className="text-xs text-stone-300">{day.xp}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* XP Tracker */}
            <XPTracker />

            {/* Recent Achievements */}
            <div className="bg-stone-800 rounded-lg shadow-2xl p-6 border-2 border-stone-700">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-stone-100">Logros recientes</h2>
                <Link href="/achievements" className="text-sm text-amber-600 hover:text-amber-500 font-medium transition-colors">
                  Ver todos
                </Link>
              </div>
              {recentAchievements.length === 0 ? (
                <div className="text-center py-8">
                  <div className="w-16 h-16 bg-amber-700/20 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Trophy className="w-8 h-8 text-amber-600" />
                  </div>
                  <p className="text-sm text-stone-300">
                    Completa lecciones para desbloquear logros
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {recentAchievements.map((achievement) => (
                    <div key={achievement.id} className="flex items-start gap-3 p-3 bg-amber-700/20 rounded-lg border-2 border-amber-800">
                      <span className="text-2xl">{achievement.icon}</span>
                      <div className="flex-1">
                        <h3 className="font-semibold text-sm text-stone-100">{achievement.title}</h3>
                        <p className="text-xs text-stone-300">{achievement.description}</p>
                        <p className="text-xs text-amber-600 font-semibold mt-1">+{achievement.xpReward} XP</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="bg-stone-800 rounded-lg shadow-2xl p-6 border-2 border-stone-700">
              <h2 className="text-xl font-bold text-stone-100 mb-4">Acciones rápidas</h2>
              <div className="space-y-2">
                <Link
                  href="/skill-tree"
                  className="flex items-center gap-3 p-3 bg-amber-700/20 hover:bg-amber-700/30 rounded-lg transition-all border-2 border-stone-700 hover:border-amber-700"
                >
                  <Target className="w-5 h-5 text-amber-600" />
                  <div className="flex-1">
                    <span className="text-sm font-bold text-stone-100 block">Árbol de Habilidades</span>
                    <span className="text-xs text-stone-300">Desbloquea nuevos cursos</span>
                  </div>
                  <Star className="w-4 h-4 text-amber-600" />
                </Link>
                <Link
                  href="/challenges"
                  className="flex items-center gap-3 p-3 bg-amber-700/20 hover:bg-amber-700/30 rounded-lg transition-all border-2 border-stone-700 hover:border-amber-700"
                >
                  <Trophy className="w-5 h-5 text-amber-600" />
                  <div className="flex-1">
                    <span className="text-sm font-bold text-stone-100 block">Retos & Recompensas</span>
                    <span className="text-xs text-stone-300">Completa desafíos diarios</span>
                  </div>
                  <Gift className="w-4 h-4 text-amber-600" />
                </Link>
                <Link
                  href="/social"
                  className="flex items-center gap-3 p-3 bg-amber-700/20 hover:bg-amber-700/30 rounded-lg transition-all border-2 border-stone-700 hover:border-amber-700"
                >
                  <Users className="w-5 h-5 text-amber-600" />
                  <div className="flex-1">
                    <span className="text-sm font-bold text-stone-100 block">Social Hub</span>
                    <span className="text-xs text-stone-300">Conéctate con amigos</span>
                  </div>
                  <MessageCircle className="w-4 h-4 text-amber-600" />
                </Link>
                <Link
                  href="/seminars"
                  className="flex items-center gap-3 p-3 bg-purple-700/20 hover:bg-purple-700/30 rounded-lg transition-all border-2 border-stone-700 hover:border-purple-600"
                >
                  <Video className="w-5 h-5 text-purple-400" />
                  <div className="flex-1">
                    <span className="text-sm font-bold text-stone-100 block">Seminarios en Vivo</span>
                    <span className="text-xs text-stone-300">Aprende de la comunidad</span>
                  </div>
                  <Star className="w-4 h-4 text-purple-400" />
                </Link>
                <Link
                  href="/community"
                  className="flex items-center gap-3 p-3 bg-amber-700/20 hover:bg-amber-700/30 rounded-lg transition-all border-2 border-stone-700 hover:border-amber-700"
                >
                  <MessageCircle className="w-5 h-5 text-amber-600" />
                  <div className="flex-1">
                    <span className="text-sm font-bold text-stone-100 block">Foro de la Comunidad</span>
                    <span className="text-xs text-stone-300">Comparte y pregunta</span>
                  </div>
                  <Users className="w-4 h-4 text-amber-600" />
                </Link>
                <Link
                  href="/courses"
                  className="flex items-center gap-3 p-3 bg-stone-700/20 hover:bg-stone-700/30 rounded-lg transition-all border-2 border-stone-700 hover:border-amber-700"
                >
                  <BookOpen className="w-5 h-5 text-amber-600" />
                  <span className="text-sm font-medium text-stone-100">Explorar cursos</span>
                </Link>
                <Link
                  href="/leaderboard"
                  className="flex items-center gap-3 p-3 bg-stone-700/20 hover:bg-stone-700/30 rounded-lg transition-all border-2 border-stone-700 hover:border-amber-700"
                >
                  <Trophy className="w-5 h-5 text-amber-600" />
                  <span className="text-sm font-medium text-stone-100">Tabla de líderes</span>
                </Link>
                <Link
                  href="/profile"
                  className="flex items-center gap-3 p-3 bg-stone-700/20 hover:bg-stone-700/30 rounded-lg transition-all border-2 border-stone-700 hover:border-amber-700"
                >
                  <Award className="w-5 h-5 text-amber-600" />
                  <span className="text-sm font-medium text-stone-100">Mi perfil</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
    </AccessGuard>
  );
}
