'use client';

import { useEffect, useState } from 'react';
import { Trophy, Lock, Star, Zap } from 'lucide-react';
import { Achievement, achievements, checkAchievements, getRarityColor, getRarityBorder } from '@/data/achievements';

export default function AchievementsDisplay() {
  const [unlockedAchievements, setUnlockedAchievements] = useState<Achievement[]>([]);
  const [stats, setStats] = useState({
    lessonsCompleted: 0,
    coursesCompleted: 0,
    totalXP: 0,
    streakDays: 0,
    perfectLessons: 0,
    lessonsToday: 0,
  });

  useEffect(() => {
    if (typeof window !== 'undefined') {
      calculateStats();
    }
  }, []);

  const calculateStats = () => {
    let totalXP = 0;
    let lessonsCompleted = 0;
    let coursesCompleted = 0;

    const courses = [
      { id: 'py-intro', lessons: 4, xpPerLesson: 50 },
      { id: 'py-variables', lessons: 5, xpPerLesson: 50 },
      { id: 'py-control', lessons: 6, xpPerLesson: 50 },
    ];

    courses.forEach(course => {
      let courseLessonsCompleted = 0;
      
      for (let i = 1; i <= course.lessons; i++) {
        const key = `lesson_${course.id}_${i}`;
        if (localStorage.getItem(key) === 'completed') {
          totalXP += course.xpPerLesson;
          lessonsCompleted++;
          courseLessonsCompleted++;
        }
      }

      if (courseLessonsCompleted === course.lessons) {
        totalXP += 100;
        coursesCompleted++;
      }
    });

    // Calcular racha (simulado por ahora)
    const lastVisit = localStorage.getItem('last_visit_date');
    const today = new Date().toDateString();
    let streakDays = parseInt(localStorage.getItem('streak_days') || '0');
    
    if (lastVisit !== today && lessonsCompleted > 0) {
      streakDays += 1;
      localStorage.setItem('streak_days', streakDays.toString());
      localStorage.setItem('last_visit_date', today);
    }

    const newStats = {
      lessonsCompleted,
      coursesCompleted,
      totalXP,
      streakDays,
      perfectLessons: 0, // TODO: implementar tracking de puntajes perfectos
      lessonsToday: 0, // TODO: implementar tracking diario
    };

    setStats(newStats);
    
    const unlocked = checkAchievements(newStats);
    setUnlockedAchievements(unlocked);

    // Guardar logros desbloqueados en localStorage
    localStorage.setItem('unlocked_achievements', JSON.stringify(unlocked.map(a => a.id)));
  };

  const progress = (unlockedAchievements.length / achievements.length) * 100;

  return (
    <div className="space-y-6">
      {/* Header con progreso */}
      <div className="bg-gradient-to-r from-stone-600 to-stone-600 rounded-2xl p-6 text-white">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold mb-1">Logros</h2>
            <p className="text-stone-100">
              {unlockedAchievements.length} de {achievements.length} desbloqueados
            </p>
          </div>
          <div className="bg-white/20 backdrop-blur-sm rounded-full p-4">
            <Trophy className="w-8 h-8" />
          </div>
        </div>

        {/* Barra de progreso */}
        <div className="w-full bg-white/20 rounded-full h-3 overflow-hidden">
          <div
            className="bg-gradient-to-r from-yellow-400 to-orange-400 h-full transition-all duration-500 flex items-center justify-end pr-1"
            style={{ width: `${progress}%` }}
          >
            {progress > 5 && (
              <Star className="w-2.5 h-2.5 text-white" fill="white" />
            )}
          </div>
        </div>
        <p className="text-sm text-stone-100 mt-2">{Math.round(progress)}% completado</p>
      </div>

      {/* Grid de logros */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {achievements.map((achievement) => {
          const isUnlocked = unlockedAchievements.some(a => a.id === achievement.id);
          
          return (
            <div
              key={achievement.id}
              className={`relative rounded-xl p-5 border-2 transition-all ${
                isUnlocked
                  ? `bg-gradient-to-br ${getRarityColor(achievement.rarity)} ${getRarityBorder(achievement.rarity)} shadow-lg transform hover:scale-105`
                  : 'bg-gray-100 border-gray-300 opacity-60'
              }`}
            >
              {/* Badge de rareza */}
              <div className="absolute top-2 right-2">
                <span className={`text-xs font-bold px-2 py-1 rounded-full ${
                  isUnlocked
                    ? achievement.rarity === 'legendary'
                      ? 'bg-yellow-200 text-yellow-900'
                      : achievement.rarity === 'epic'
                      ? 'bg-amber-200 text-stone-900'
                      : achievement.rarity === 'rare'
                      ? 'bg-stone-200 text-stone-900'
                      : 'bg-gray-200 text-gray-900'
                    : 'bg-gray-300 text-gray-600'
                }`}>
                  {achievement.rarity}
                </span>
              </div>

              {/* Icono */}
              <div className={`text-5xl mb-3 ${!isUnlocked && 'filter grayscale'}`}>
                {isUnlocked ? achievement.icon : <Lock className="w-12 h-12 text-gray-400" />}
              </div>

              {/* Título y descripción */}
              <h3 className={`font-bold text-lg mb-2 ${isUnlocked ? 'text-white' : 'text-gray-700'}`}>
                {achievement.title}
              </h3>
              <p className={`text-sm mb-3 ${isUnlocked ? 'text-white/90' : 'text-gray-600'}`}>
                {achievement.description}
              </p>

              {/* Recompensa XP */}
              <div className={`flex items-center gap-1 text-sm font-semibold ${
                isUnlocked ? 'text-yellow-300' : 'text-gray-500'
              }`}>
                <Zap className="w-4 h-4" />
                +{achievement.xpReward} XP
              </div>

              {/* Progreso para logros no desbloqueados */}
              {!isUnlocked && (
                <div className="mt-3 pt-3 border-t border-gray-300">
                  <div className="flex justify-between text-xs text-gray-600 mb-1">
                    <span>Progreso</span>
                    <span>
                      {achievement.requirement.type === 'lessons_completed' && `${stats.lessonsCompleted}/${achievement.requirement.value}`}
                      {achievement.requirement.type === 'courses_completed' && `${stats.coursesCompleted}/${achievement.requirement.value}`}
                      {achievement.requirement.type === 'xp_earned' && `${stats.totalXP}/${achievement.requirement.value} XP`}
                      {achievement.requirement.type === 'streak_days' && `${stats.streakDays}/${achievement.requirement.value} días`}
                    </span>
                  </div>
                  <div className="w-full bg-gray-300 rounded-full h-2">
                    <div
                      className="bg-stone-500 h-2 rounded-full transition-all"
                      style={{ 
                        width: `${Math.min(100, (
                          achievement.requirement.type === 'lessons_completed' ? (stats.lessonsCompleted / achievement.requirement.value) * 100 :
                          achievement.requirement.type === 'courses_completed' ? (stats.coursesCompleted / achievement.requirement.value) * 100 :
                          achievement.requirement.type === 'xp_earned' ? (stats.totalXP / achievement.requirement.value) * 100 :
                          achievement.requirement.type === 'streak_days' ? (stats.streakDays / achievement.requirement.value) * 100 :
                          0
                        ))}%` 
                      }}
                    />
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Logros recientes */}
      {unlockedAchievements.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Star className="w-6 h-6 text-yellow-500" />
            Logros Recientes
          </h3>
          <div className="space-y-3">
            {unlockedAchievements.slice(-3).reverse().map((achievement) => (
              <div key={achievement.id} className="flex items-center gap-4 p-3 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg border border-yellow-200">
                <span className="text-3xl">{achievement.icon}</span>
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900">{achievement.title}</h4>
                  <p className="text-sm text-gray-600">{achievement.description}</p>
                </div>
                <div className="text-right">
                  <div className="text-yellow-600 font-bold">+{achievement.xpReward} XP</div>
                  <div className="text-xs text-gray-500">{achievement.rarity}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
