'use client';

import { useEffect, useState } from 'react';
import { Calendar, TrendingUp, Clock, Target } from 'lucide-react';

interface WeekActivity {
  day: string;
  date: string;
  lessonsCompleted: number;
  xpEarned: number;
  active: boolean;
}

export default function ActivityStats() {
  const [weekActivity, setWeekActivity] = useState<WeekActivity[]>([]);
  const [monthlyStats, setMonthlyStats] = useState({
    totalLessons: 0,
    totalXP: 0,
    averagePerDay: 0,
    mostProductiveDay: '',
  });

  useEffect(() => {
    if (typeof window !== 'undefined') {
      loadActivityData();
    }
  }, []);

  const loadActivityData = () => {
    const days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    const today = new Date();
    const weekData: WeekActivity[] = [];

    // Generar datos de la última semana
    for (let i = 6; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      
      const dayKey = `activity_${date.toDateString()}`;
      const storedData = localStorage.getItem(dayKey);
      const dayData = storedData ? JSON.parse(storedData) : { lessons: 0, xp: 0 };

      weekData.push({
        day: days[date.getDay()],
        date: date.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' }),
        lessonsCompleted: dayData.lessons || 0,
        xpEarned: dayData.xp || 0,
        active: dayData.lessons > 0,
      });
    }

    setWeekActivity(weekData);

    // Calcular estadísticas mensuales
    const totalLessons = weekData.reduce((sum, day) => sum + day.lessonsCompleted, 0);
    const totalXP = weekData.reduce((sum, day) => sum + day.xpEarned, 0);
    const activeDays = weekData.filter(d => d.active).length;
    const averagePerDay = activeDays > 0 ? Math.round(totalLessons / activeDays) : 0;
    
    const mostProductive = weekData.reduce((max, day) => 
      day.lessonsCompleted > max.lessonsCompleted ? day : max
    , weekData[0]);

    setMonthlyStats({
      totalLessons,
      totalXP,
      averagePerDay,
      mostProductiveDay: mostProductive.lessonsCompleted > 0 ? mostProductive.day : 'N/A',
    });
  };

  const maxLessons = Math.max(...weekActivity.map(d => d.lessonsCompleted), 1);

  return (
    <div className="space-y-6">
      {/* Resumen mensual */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-2xl p-4 border-2 border-stone-500/30">
          <div className="flex items-center gap-2 mb-2">
            <Target className="w-5 h-5 text-stone-400" />
            <h3 className="text-sm font-medium text-stone-200">Esta Semana</h3>
          </div>
          <p className="text-2xl font-bold text-stone-400">{monthlyStats.totalLessons}</p>
          <p className="text-xs text-stone-300">lecciones</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-2xl p-4 border-2 border-stone-500/30">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-5 h-5 text-stone-400" />
            <h3 className="text-sm font-medium text-stone-200">XP Ganado</h3>
          </div>
          <p className="text-2xl font-bold text-stone-400">{monthlyStats.totalXP}</p>
          <p className="text-xs text-stone-300">puntos</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-2xl p-4 border-2 border-green-500/30">
          <div className="flex items-center gap-2 mb-2">
            <Clock className="w-5 h-5 text-green-400" />
            <h3 className="text-sm font-medium text-green-200">Promedio/Día</h3>
          </div>
          <p className="text-2xl font-bold text-green-400">{monthlyStats.averagePerDay}</p>
          <p className="text-xs text-green-300">lecciones</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-2xl p-4 border-2 border-orange-500/30">
          <div className="flex items-center gap-2 mb-2">
            <Calendar className="w-5 h-5 text-orange-400" />
            <h3 className="text-sm font-medium text-orange-200">Mejor Día</h3>
          </div>
          <p className="text-2xl font-bold text-orange-400">{monthlyStats.mostProductiveDay}</p>
          <p className="text-xs text-orange-300">más activo</p>
        </div>
      </div>

      {/* Gráfico de actividad semanal */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-2xl p-6 border border-stone-500/20">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-white">Actividad Semanal</h2>
          <div className="flex items-center gap-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-stone-500"></div>
              <span className="text-stone-200">Lecciones</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-amber-500"></div>
              <span className="text-stone-200">XP</span>
            </div>
          </div>
        </div>

        {/* Gráfico de barras */}
        <div className="flex items-end justify-between gap-2 h-48 mb-4">
          {weekActivity.map((day, index) => (
            <div key={index} className="flex-1 flex flex-col items-center gap-2">
              {/* Barra de lecciones */}
              <div className="w-full relative" style={{ height: '100%' }}>
                <div className="absolute bottom-0 w-full flex flex-col gap-1">
                  {/* Barra de lecciones */}
                  {day.lessonsCompleted > 0 && (
                    <div
                      className="w-full bg-gradient-to-t from-stone-500 to-stone-400 rounded-t-lg transition-all duration-500 hover:from-stone-600 hover:to-stone-500 relative group"
                      style={{ height: `${(day.lessonsCompleted / maxLessons) * 100}%` }}
                    >
                      {/* Tooltip */}
                      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block">
                        <div className="bg-gray-900 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
                          {day.lessonsCompleted} lecciones
                          <br />
                          {day.xpEarned} XP
                        </div>
                        <div className="w-2 h-2 bg-gray-900 transform rotate-45 mx-auto -mt-1"></div>
                      </div>
                    </div>
                  )}
                  
                  {/* Indicador de día activo */}
                  {day.active && (
                    <div className="h-1 w-full bg-green-400 rounded-full"></div>
                  )}
                </div>
              </div>

              {/* Etiquetas */}
              <div className="text-center">
                <div className={`text-xs font-medium ${day.active ? 'text-white' : 'text-stone-400'}`}>
                  {day.day}
                </div>
                <div className="text-xs text-stone-300">{day.date}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Leyenda con totales */}
        <div className="flex items-center justify-center gap-8 pt-4 border-t border-stone-500/20">
          <div className="text-center">
            <p className="text-sm text-stone-200">Lecciones Completadas</p>
            <p className="text-2xl font-bold text-stone-400">{monthlyStats.totalLessons}</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-stone-200">XP Ganado</p>
            <p className="text-2xl font-bold text-stone-400">{monthlyStats.totalXP}</p>
          </div>
        </div>
      </div>

      {/* Consejos y motivación */}
      <div className="bg-gradient-to-r from-stone-600 to-amber-600 rounded-xl p-6 text-white shadow-2xl border border-stone-400/30">
        <h3 className="text-lg font-bold mb-2">💡 Consejo del día</h3>
        <p className="text-white/90">
          {monthlyStats.totalLessons === 0 
            ? '¡Comienza hoy tu viaje de aprendizaje! Completa tu primera lección para empezar a acumular XP.'
            : monthlyStats.totalLessons < 5
            ? '¡Excelente inicio! Sigue practicando todos los días para mejorar tus habilidades.'
            : monthlyStats.totalLessons < 10
            ? '¡Vas muy bien! Mantén el ritmo para dominar todos los conceptos.'
            : '¡Eres imparable! Tu dedicación está dando frutos. ¡Sigue así!'
          }
        </p>
      </div>
    </div>
  );
}
