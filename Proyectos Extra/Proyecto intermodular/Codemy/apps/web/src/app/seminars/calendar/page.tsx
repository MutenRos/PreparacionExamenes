'use client';

import { useState } from 'react';
import { Navigation } from '@/components/Navigation';
import { Footer } from '@/components/Footer';
import { Calendar as CalendarIcon, ChevronLeft, ChevronRight, Video, Clock, Users, Coins, Filter, Star } from 'lucide-react';
import Link from 'next/link';

type SeminarEvent = {
  id: number;
  title: string;
  instructor: string;
  instructorAvatar: number;
  duration: number;
  entryCost: number;
  date: string;
  time: string;
  attendees: number;
  maxAttendees: number;
  category: string;
  level: string;
};

export default function CalendarPage() {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDay, setSelectedDay] = useState<Date | null>(null);
  const [filterCategory, setFilterCategory] = useState<string>('all');

    // Los seminarios se cargarán desde Supabase cuando estén disponibles
  const seminars: SeminarEvent[] = [];

  const categories = ['all', 'Web Development', 'IA & Data Science', 'Hardware', 'DevOps'];

  const filteredSeminars = filterCategory === 'all' 
    ? seminars 
    : seminars.filter(s => s.category === filterCategory);

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    return { daysInMonth, startingDayOfWeek, year, month };
  };

  const { daysInMonth, startingDayOfWeek, year, month } = getDaysInMonth(currentDate);

  const getSeminarsForDay = (day: number) => {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return filteredSeminars.filter(s => s.date === dateStr);
  };

  const previousMonth = () => {
    setCurrentDate(new Date(year, month - 1, 1));
  };

  const nextMonth = () => {
    setCurrentDate(new Date(year, month + 1, 1));
  };

  const monthNames = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ];

  const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];

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

  const selectedDaySeminars = selectedDay ? getSeminarsForDay(selectedDay.getDate()) : [];

  return (
    <main className="min-h-screen bg-stone-900">
      <Navigation />
      
      <div className="pt-24 pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">
              Calendario de Seminarios
            </h1>
            <p className="text-stone-400">
              Explora y asiste a seminarios programados por la comunidad
            </p>
          </div>

          {/* Filter */}
          <div className="mb-6 flex items-center space-x-4">
            <Filter className="w-5 h-5 text-stone-400" />
            <div className="flex flex-wrap gap-2">
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setFilterCategory(cat)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    filterCategory === cat
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                      : 'bg-stone-800 text-stone-400 hover:bg-stone-700'
                  }`}
                >
                  {cat === 'all' ? 'Todos' : cat}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Calendar */}
            <div className="lg:col-span-2">
              <div className="bg-stone-800/50 rounded-xl border border-stone-700 p-6">
                {/* Calendar Header */}
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-white">
                    {monthNames[month]} {year}
                  </h2>
                  <div className="flex space-x-2">
                    <button
                      onClick={previousMonth}
                      className="p-2 bg-stone-700 hover:bg-stone-600 rounded-lg transition-colors"
                    >
                      <ChevronLeft className="w-5 h-5 text-white" />
                    </button>
                    <button
                      onClick={nextMonth}
                      className="p-2 bg-stone-700 hover:bg-stone-600 rounded-lg transition-colors"
                    >
                      <ChevronRight className="w-5 h-5 text-white" />
                    </button>
                  </div>
                </div>

                {/* Day Names */}
                <div className="grid grid-cols-7 gap-2 mb-2">
                  {dayNames.map((day) => (
                    <div key={day} className="text-center text-stone-400 font-semibold text-sm py-2">
                      {day}
                    </div>
                  ))}
                </div>

                {/* Calendar Grid */}
                <div className="grid grid-cols-7 gap-2">
                  {/* Empty cells for days before month starts */}
                  {Array.from({ length: startingDayOfWeek }).map((_, i) => (
                    <div key={`empty-${i}`} className="aspect-square" />
                  ))}

                  {/* Days of the month */}
                  {Array.from({ length: daysInMonth }).map((_, i) => {
                    const day = i + 1;
                    const daySeminars = getSeminarsForDay(day);
                    const isToday = new Date().getDate() === day && 
                                   new Date().getMonth() === month && 
                                   new Date().getFullYear() === year;
                    const isSelected = selectedDay?.getDate() === day;

                    return (
                      <button
                        key={day}
                        onClick={() => setSelectedDay(new Date(year, month, day))}
                        className={`aspect-square p-2 rounded-lg border-2 transition-all ${
                          isSelected
                            ? 'border-blue-600 bg-blue-600/20'
                            : isToday
                            ? 'border-amber-600 bg-amber-600/10'
                            : daySeminars.length > 0
                            ? 'border-stone-600 bg-stone-700/50 hover:border-stone-500'
                            : 'border-stone-700 hover:bg-stone-700/30'
                        }`}
                      >
                        <div className="h-full flex flex-col">
                          <span className={`text-sm font-semibold ${
                            isSelected || isToday ? 'text-white' : 'text-stone-300'
                          }`}>
                            {day}
                          </span>
                          {daySeminars.length > 0 && (
                            <div className="flex-1 flex items-center justify-center">
                              <div className="flex flex-col items-center space-y-1">
                                {daySeminars.slice(0, 3).map((seminar, idx) => (
                                  <div
                                    key={idx}
                                    className="w-1.5 h-1.5 rounded-full bg-blue-500"
                                  />
                                ))}
                                {daySeminars.length > 3 && (
                                  <span className="text-xs text-blue-400">+{daySeminars.length - 3}</span>
                                )}
                              </div>
                            </div>
                          )}
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Selected Day Seminars / Upcoming */}
            <div className="lg:col-span-1">
              <div className="bg-stone-800/50 rounded-xl border border-stone-700 p-6 sticky top-24">
                <h3 className="text-xl font-bold text-white mb-4">
                  {selectedDay ? `${selectedDay.getDate()} ${monthNames[selectedDay.getMonth()]}` : 'Próximos Seminarios'}
                </h3>

                {selectedDay && selectedDaySeminars.length === 0 ? (
                  <div className="text-center py-8">
                    <CalendarIcon className="w-12 h-12 text-stone-600 mx-auto mb-3" />
                    <p className="text-stone-400">No hay seminarios este día</p>
                  </div>
                ) : (
                  <div className="space-y-4 max-h-[600px] overflow-y-auto">
                    {(selectedDay ? selectedDaySeminars : filteredSeminars.slice(0, 5)).map((seminar) => (
                      <div
                        key={seminar.id}
                        className="bg-stone-700/50 rounded-lg p-4 border border-stone-600 hover:border-blue-600/50 transition-all"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <div className={`w-8 h-8 rounded-full bg-gradient-to-r ${getAvatarColor(seminar.instructorAvatar)} flex items-center justify-center text-white font-bold text-sm`}>
                              {seminar.instructor[0]}
                            </div>
                            <div>
                              <div className="text-white font-semibold text-sm">{seminar.instructor}</div>
                              <div className="text-stone-400 text-xs">{seminar.category}</div>
                            </div>
                          </div>
                          <span className="text-xs bg-amber-600/20 text-amber-400 px-2 py-1 rounded">
                            {seminar.level}
                          </span>
                        </div>

                        <h4 className="text-white font-bold mb-2">{seminar.title}</h4>

                        <div className="space-y-1 mb-3 text-xs text-stone-400">
                          <div className="flex items-center space-x-2">
                            <CalendarIcon className="w-3 h-3" />
                            <span>{seminar.date} - {seminar.time}</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Clock className="w-3 h-3" />
                            <span>{seminar.duration} minutos</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Users className="w-3 h-3" />
                            <span>{seminar.attendees}/{seminar.maxAttendees}</span>
                          </div>
                        </div>

                        <div className="flex items-center justify-between pt-3 border-t border-stone-600">
                          <div className="flex items-center space-x-1">
                            <Coins className="w-4 h-4 text-amber-500" />
                            <span className="text-white font-bold">{seminar.entryCost}</span>
                          </div>
                          <Link
                            href={`/seminars`}
                            className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg transition-colors"
                          >
                            Ver detalles
                          </Link>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                <Link
                  href="/seminars"
                  className="mt-4 w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 rounded-lg transition-all flex items-center justify-center space-x-2"
                >
                  <Video className="w-4 h-4" />
                  <span>Ver todos los seminarios</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </main>
  );
}
