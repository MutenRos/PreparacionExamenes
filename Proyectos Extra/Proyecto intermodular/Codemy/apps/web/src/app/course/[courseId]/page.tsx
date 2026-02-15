'use client';

import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { 
  ArrowLeft, 
  BookOpen, 
  Clock, 
  Trophy, 
  Target, 
  CheckCircle, 
  Circle, 
  Lock, 
  Play, 
  Star, 
  MessageSquare 
} from 'lucide-react';
import Forum from '@/components/Forum';
import { getCourseWithLessons } from '@/lib/course-metadata';
import type { CourseWithLessons } from '@/lib/course-metadata';
import { getSafeUserClient } from '@/lib/auth-helpers-client';
import { courseModules } from '@/data/courses';

export default function CoursePage() {
  const params = useParams();
  const router = useRouter();
  const courseId = params.courseId as string;
  
  console.error('🚀 COMPONENT MOUNTING - courseId:', courseId);
  
  // IMMEDIATE DIRECT MODULE CHECK
  const directMod = (courseModules as any)[courseId];
  console.error('📦 DIRECT MODULE CHECK:', {
    id: courseId,
    exists: !!directMod,
    title: directMod?.title,
    lessonsCount: directMod?.lessons?.length,
    lessons: directMod?.lessons
  });
  
  const [course, setCourse] = useState<CourseWithLessons | null>(null);
  const [lessonStatuses, setLessonStatuses] = useState<{[key: string]: string}>({});
  const [activeTab, setActiveTab] = useState<'lessons' | 'forum'>('lessons');
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);

  // Check if user is admin
  useEffect(() => {
    async function checkAdmin() {
      try {
        const { user } = await getSafeUserClient();
        const isAdminUser = user?.email === 'admin@codedungeon.es';
        setIsAdmin(isAdminUser);
      } catch (error) {
        console.error('Error checking admin:', error);
      }
    }
    checkAdmin();
  }, []);
  
  // Load course data
  useEffect(() => {
    try {
      console.error('🔍 STARTING getCourseWithLessons for:', courseId);
      
      // DIRECT MODULE INSPECTION
      const directModule = (courseModules as any)[courseId];
      console.error('🔍 DIRECT MODULE INSPECTION:', {
        courseId,
        moduleExists: !!directModule,
        moduleTitle: directModule?.title,
        moduleLessons: directModule?.lessons?.length,
        firstLesson: directModule?.lessons?.[0],
        allLessonIds: directModule?.lessons?.map((l: any) => l.id)
      });
      
      const courseData = getCourseWithLessons(courseId);
      console.error('🔍 DEBUG courseId:', courseId);
      console.error('🔍 DEBUG courseData:', courseData);
      console.error('🔍 DEBUG lessons array:', courseData?.lessons);
      console.error('🔍 DEBUG lessons count:', courseData?.lessons?.length);
      if (!courseData) {
        // Course not found, redirect to dashboard
        console.error('❌ NO COURSE DATA - redirecting');
        router.push('/dashboard');
        return;
      }
      setCourse(courseData);
      setLoading(false);
    } catch (error) {
      console.error('❌ ERROR in getCourseWithLessons:', error);
      alert(`ERROR: ${error}`);
    }
  }, [courseId, router]);

  // Load lesson statuses from localStorage
  useEffect(() => {
    if (typeof window !== 'undefined' && course) {
      const statuses: {[key: string]: string} = {};
      course.lessons.forEach(lesson => {
        const key = `${courseId}_lesson_${lesson.id}_status`;
        const status = localStorage.getItem(key);
        // If admin, unlock all lessons
        if (isAdmin) {
          statuses[lesson.id] = 'available';
        } else {
          statuses[lesson.id] = status || lesson.status;
        }
      });
      setLessonStatuses(statuses);
    }
  }, [course, courseId, isAdmin]);

  // Update lesson status when completed
  const handleLessonComplete = (lessonId: string) => {
    if (typeof window !== 'undefined') {
      const key = `${courseId}_lesson_${lessonId}_status`;
      localStorage.setItem(key, 'completed');
      setLessonStatuses(prev => ({ ...prev, [lessonId]: 'completed' }));
      
      // Unlock next lesson
      const lessonIndex = course?.lessons.findIndex(l => l.id === lessonId);
      if (lessonIndex !== undefined && lessonIndex !== -1 && course) {
        const nextLesson = course.lessons[lessonIndex + 1];
        if (nextLesson) {
          const nextKey = `${courseId}_lesson_${nextLesson.id}_status`;
          localStorage.setItem(nextKey, 'available');
          setLessonStatuses(prev => ({ ...prev, [nextLesson.id]: 'available' }));
        }
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-stone-900 flex items-center justify-center">
        <div className="animate-pulse text-stone-400">Cargando curso...</div>
      </div>
    );
  }

  if (!course) {
    return (
      <div className="min-h-screen bg-stone-900 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-stone-100 mb-4">Curso no encontrado</h1>
          <Link 
            href="/dashboard"
            className="text-amber-600 hover:text-amber-700 underline"
          >
            Volver al dashboard
          </Link>
        </div>
      </div>
    );
  }

  // Calculate progress
  const completedLessons = Object.values(lessonStatuses).filter(s => s === 'completed').length;
  const totalLessons = course.lessons.length;
  const progress = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0;

  return (
    <div className="min-h-screen bg-stone-900">
      {/* Header */}
      <div className="bg-stone-800/50 backdrop-blur-sm border-b-2 border-stone-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Link 
            href="/dashboard"
            className="inline-flex items-center gap-2 text-stone-100 hover:text-amber-600 mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Volver al Dashboard
          </Link>
          
          <div className="flex items-start gap-6">
            <div className="text-6xl">{course.icon}</div>
            <div className="flex-1">
              <h1 className="text-4xl font-bold text-stone-100 mb-2">{course.title}</h1>
              <p className="text-lg text-stone-300 mb-4">{course.description}</p>
              
              <div className="flex flex-wrap gap-4">
                <div className="flex items-center gap-2 text-stone-100">
                  <Clock className="w-5 h-5 text-amber-600" />
                  <span>{course.duration}</span>
                </div>
                <div className="flex items-center gap-2 text-stone-100">
                  <Trophy className="w-5 h-5 text-amber-600" />
                  <span>{course.xp} XP</span>
                </div>
                <div className="flex items-center gap-2 text-stone-100">
                  <BookOpen className="w-5 h-5 text-amber-600" />
                  <span>{totalLessons} lecciones</span>
                </div>
                <div className="px-3 py-1 rounded-full bg-amber-700/30 border border-amber-600/50 text-amber-600 text-sm font-semibold">
                  {course.level}
                </div>
              </div>
            </div>
          </div>
          
          {/* Progress Bar */}
          <div className="mt-6">
            <div className="flex justify-between text-sm text-stone-300 mb-2">
              <span>Progreso del curso</span>
              <span className="font-bold">{progress}%</span>
            </div>
            <div className="w-full h-3 bg-stone-700 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-amber-600 to-amber-700 transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-xs text-stone-400 mt-1">
              {completedLessons} de {totalLessons} lecciones completadas
            </p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tabs */}
        <div className="flex gap-4 mb-6 border-b-2 border-stone-700">
          <button
            onClick={() => setActiveTab('lessons')}
            className={`px-6 py-3 font-semibold transition-colors border-b-2 ${
              activeTab === 'lessons'
                ? 'border-amber-600 text-amber-600'
                : 'border-transparent text-stone-400 hover:text-stone-100'
            }`}
          >
            <BookOpen className="w-5 h-5 inline-block mr-2" />
            Lecciones
          </button>
          <button
            onClick={() => setActiveTab('forum')}
            className={`px-6 py-3 font-semibold transition-colors border-b-2 ${
              activeTab === 'forum'
                ? 'border-amber-600 text-amber-600'
                : 'border-transparent text-stone-400 hover:text-stone-100'
            }`}
          >
            <MessageSquare className="w-5 h-5 inline-block mr-2" />
            Foro
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {activeTab === 'lessons' ? (
              <>
                {/* Objectives */}
                <div className="bg-stone-800 rounded-lg p-6 mb-6 border-2 border-stone-700">
                  <h2 className="text-2xl font-bold text-stone-100 mb-4 flex items-center gap-2">
                    <Target className="w-6 h-6 text-amber-600" />
                    Objetivos del Curso
                  </h2>
                  <ul className="space-y-3">
                    {course.objectives.map((objective, index) => (
                      <li key={index} className="flex items-start gap-3 text-stone-300">
                        <CheckCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                        <span>{objective}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Lessons List */}
                <div className="space-y-4">
                  <h2 className="text-2xl font-bold text-stone-100 mb-4">Lecciones</h2>
                  {course.lessons.map((lesson, index) => {
                    const status = lessonStatuses[lesson.id] || lesson.status;
                    // Admin nunca tiene lecciones bloqueadas
                    const isLocked = isAdmin ? false : status === 'locked';
                    const isCompleted = status === 'completed';
                    const isAvailable = status === 'available' || status === 'in-progress';

                    return (
                      <div
                        key={lesson.id}
                        className={`bg-stone-800 rounded-lg p-4 border-2 transition-all ${
                          isCompleted
                            ? 'border-green-600/50 bg-green-900/20'
                            : isLocked
                            ? 'border-stone-700 opacity-50'
                            : 'border-stone-700 hover:border-amber-600/50'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-4 flex-1">
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                              isCompleted
                                ? 'bg-green-600'
                                : isLocked
                                ? 'bg-stone-700'
                                : 'bg-amber-700'
                            }`}>
                              {isCompleted ? (
                                <CheckCircle className="w-6 h-6 text-white" />
                              ) : isLocked ? (
                                <Lock className="w-6 h-6 text-stone-400" />
                              ) : (
                                <Play className="w-6 h-6 text-white" />
                              )}
                            </div>
                            <div className="flex-1">
                              <h3 className="text-lg font-semibold text-stone-100">
                                {index + 1}. {lesson.title}
                              </h3>
                              <div className="flex items-center gap-4 text-sm text-stone-400 mt-1">
                                <span className="flex items-center gap-1">
                                  <Clock className="w-4 h-4" />
                                  {lesson.duration}
                                </span>
                                <span className="flex items-center gap-1">
                                  <Trophy className="w-4 h-4" />
                                  {lesson.xp} XP
                                </span>
                              </div>
                            </div>
                          </div>
                          
                          {!isLocked && (
                            <Link
                              href={`/course/${courseId}/lesson/${lesson.id}`}
                              className="px-4 py-2 bg-amber-700 hover:bg-amber-600 text-white rounded-lg font-semibold transition-colors"
                            >
                              {isCompleted ? 'Repasar' : 'Comenzar'}
                            </Link>
                          )}
                          {isLocked && (
                            <div className="px-4 py-2 bg-stone-700 text-stone-400 rounded-lg font-semibold cursor-not-allowed">
                              Bloqueado
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </>
            ) : (
              <Forum courseId={courseId} />
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Progress Card */}
            <div className="bg-stone-800 rounded-lg p-6 border-2 border-stone-700">
              <h3 className="text-xl font-bold text-stone-100 mb-4">Tu Progreso</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-white/70">Completado</span>
                  <span className="text-white font-bold">{progress}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-white/70">Lecciones</span>
                  <span className="text-white font-bold">{completedLessons}/{totalLessons}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-white/70">Duración</span>
                  <span className="text-white font-bold">{course.duration}</span>
                </div>
              </div>
            </div>

            {/* Achievements Preview */}
            <div className="bg-stone-800 rounded-lg p-6 border-2 border-stone-700">
              <h3 className="text-xl font-bold text-stone-100 mb-3 flex items-center gap-2">
                <Trophy className="w-6 h-6 text-amber-600" />
                Logros Desbloqueables
              </h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 rounded-full ${
                    progress >= 50 ? 'bg-amber-700' : 'bg-stone-700'
                  } flex items-center justify-center`}>
                    <Star className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <p className="text-stone-100 font-semibold text-sm">Medio Camino</p>
                    <p className="text-stone-400 text-xs">Completa el 50% del curso</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 rounded-full ${
                    progress >= 100 ? 'bg-amber-700' : 'bg-stone-700'
                  } flex items-center justify-center`}>
                    <Trophy className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <p className="text-stone-100 font-semibold text-sm">Maestro {course.category}</p>
                    <p className="text-stone-400 text-xs">Completa el 100% del curso</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Community Stats */}
            <div className="bg-stone-800 rounded-lg p-6 border-2 border-stone-700">
              <h3 className="text-xl font-bold text-stone-100 mb-4">Comunidad</h3>
              <div className="text-center">
                <p className="text-4xl font-bold text-amber-600 mb-2">
                  {course.studentsEnrolled.toLocaleString()}
                </p>
                <p className="text-stone-400">estudiantes inscritos</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
