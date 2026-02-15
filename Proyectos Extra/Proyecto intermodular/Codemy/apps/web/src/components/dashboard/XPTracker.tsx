'use client';

import { useEffect, useState } from 'react';
import { Trophy, Star, Zap, TrendingUp } from 'lucide-react';

interface XPData {
  totalXP: number;
  level: number;
  xpToNextLevel: number;
  currentLevelXP: number;
  completedLessons: number;
  completedCourses: number;
}

export default function XPTracker() {
  const [xpData, setXpData] = useState<XPData>({
    totalXP: 0,
    level: 1,
    xpToNextLevel: 100,
    currentLevelXP: 0,
    completedLessons: 0,
    completedCourses: 0,
  });

  useEffect(() => {
    if (typeof window !== 'undefined') {
      calculateXP();
    }
  }, []);

  const calculateXP = () => {
    let totalXP = 0;
    let completedLessons = 0;
    let completedCourses = 0;

    // Definir cursos y XP por lección
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
        if (localStorage.getItem(key) === 'completed') {
          // La última lección (proyecto final) de py-functions, py-classes, py-files da 100 XP
          const isProjectLesson = course.bonusLastLesson && i === course.lessons;
          const lessonXP = isProjectLesson ? course.xpPerLesson + course.bonusLastLesson : course.xpPerLesson;
          
          totalXP += lessonXP;
          completedLessons++;
          courseLessonsCompleted++;
        }
      }

      // Bonus por completar curso completo
      if (courseLessonsCompleted === course.lessons) {
        totalXP += 100; // Bonus XP
        completedCourses++;
      }
    });

    // Calcular nivel (cada 100 XP = 1 nivel)
    const level = Math.floor(totalXP / 100) + 1;
    const currentLevelXP = totalXP % 100;
    const xpToNextLevel = 100 - currentLevelXP;

    setXpData({
      totalXP,
      level,
      xpToNextLevel,
      currentLevelXP,
      completedLessons,
      completedCourses,
    });

    console.log('XP Data:', {
      totalXP,
      level,
      completedLessons,
      completedCourses,
    });
  };

  const progressPercentage = (xpData.currentLevelXP / 100) * 100;

  return (
    <div className="bg-gradient-to-br from-stone-600 to-stone-600 rounded-2xl p-6 text-white shadow-xl">
      {/* Header con nivel */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-3xl font-bold mb-1">Nivel {xpData.level}</h2>
          <p className="text-stone-100">
            {xpData.xpToNextLevel} XP para siguiente nivel
          </p>
        </div>
        <div className="bg-white/20 backdrop-blur-sm rounded-full p-4">
          <Trophy className="w-8 h-8" />
        </div>
      </div>

      {/* Barra de progreso */}
      <div className="mb-6">
        <div className="flex justify-between text-sm mb-2">
          <span>{xpData.currentLevelXP} XP</span>
          <span>100 XP</span>
        </div>
        <div className="w-full bg-white/20 rounded-full h-4 overflow-hidden">
          <div
            className="bg-gradient-to-r from-yellow-400 to-orange-400 h-full transition-all duration-500 rounded-full flex items-center justify-end pr-1"
            style={{ width: `${progressPercentage}%` }}
          >
            {progressPercentage > 10 && (
              <Star className="w-3 h-3 text-white" fill="white" />
            )}
          </div>
        </div>
      </div>

      {/* Estadísticas */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 text-center">
          <div className="flex justify-center mb-2">
            <Zap className="w-6 h-6 text-yellow-300" />
          </div>
          <p className="text-2xl font-bold">{xpData.totalXP}</p>
          <p className="text-sm text-stone-100">XP Total</p>
        </div>

        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 text-center">
          <div className="flex justify-center mb-2">
            <Star className="w-6 h-6 text-stone-300" />
          </div>
          <p className="text-2xl font-bold">{xpData.completedLessons}</p>
          <p className="text-sm text-stone-100">Lecciones</p>
        </div>

        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 text-center">
          <div className="flex justify-center mb-2">
            <TrendingUp className="w-6 h-6 text-green-300" />
          </div>
          <p className="text-2xl font-bold">{xpData.completedCourses}</p>
          <p className="text-sm text-stone-100">Cursos</p>
        </div>
      </div>

      {/* Mensaje motivacional */}
      {xpData.completedLessons === 0 && (
        <div className="mt-6 bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
          <p className="text-sm">
            🚀 ¡Completa tu primera lección para ganar XP!
          </p>
        </div>
      )}

      {xpData.completedLessons > 0 && xpData.completedLessons < 5 && (
        <div className="mt-6 bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
          <p className="text-sm">
            🔥 ¡Buen comienzo! Sigue así para subir de nivel
          </p>
        </div>
      )}

      {xpData.completedCourses > 0 && (
        <div className="mt-6 bg-gradient-to-r from-yellow-400/20 to-orange-400/20 backdrop-blur-sm rounded-lg p-4 text-center border border-yellow-400/30">
          <p className="text-sm font-semibold">
            ⭐ ¡Completaste {xpData.completedCourses} curso{xpData.completedCourses > 1 ? 's' : ''}!
          </p>
        </div>
      )}
    </div>
  );
}
