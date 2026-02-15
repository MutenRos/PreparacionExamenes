'use client';

import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { useState, useEffect, useCallback, useMemo } from 'react';
import { ArrowLeft, ArrowRight, CheckCircle, Code, BookOpen, Lightbulb, Play, RotateCcw, Trophy } from 'lucide-react';
import { useNotifications } from '@/contexts/NotificationContext';
import { getLevelInfo, checkLevelUp } from '@/lib/xp-helpers';
import { pushNotification, checkCourseCompletionAndNotify, checkLevelUpAndNotify } from '@/lib/achievements';
import { loadLessonContent, preloadNextLesson } from '@/lib/lesson-loader';

export default function LessonPage() {
  const params = useParams();
  const router = useRouter();
  const courseId = params.courseId as string;
  const lessonId = params.lessonId as string;
  const { showNotification } = useNotifications();

  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [showHints, setShowHints] = useState(false);
  const [lessonContent, setLessonContent] = useState<any>(null);
  const [isLoadingContent, setIsLoadingContent] = useState(true);
  const [currentHint, setCurrentHint] = useState(0);
  const [completed, setCompleted] = useState(false);

  // Cargar contenido dinámicamente
  useEffect(() => {
    let cancelled = false;
    
    async function loadContent() {
      setIsLoadingContent(true);
      
      try {
        const dynamicContent = await loadLessonContent(courseId);
        if (!cancelled && dynamicContent && (dynamicContent as any)[lessonId]) {
          setLessonContent((dynamicContent as any)[lessonId]);
        }
      } catch (error) {
        console.error('Error loading lesson content:', error);
      }
      
      if (!cancelled) {
        setIsLoadingContent(false);
      }
    }
    
    loadContent();
    
    return () => {
      cancelled = true;
    };
  }, [courseId, lessonId]);

  // Cargar el código inicial cuando la lección se carga
  useEffect(() => {
    if (lessonContent?.exercise?.initialCode) {
      setCode(lessonContent.exercise.initialCode);
    }
  }, [lessonContent]);
  
  // Precargar siguiente lección
  useEffect(() => {
    const nextLessonId = parseInt(lessonId) + 1;
    preloadNextLesson(courseId);
  }, [courseId, lessonId]);

  const lessonData = lessonContent;

  const runCode = useCallback(() => {
    if (!lessonData?.exercise) return;
    
    const exercise = lessonData.exercise;
    let isCorrect = false;
    
    // Verificar según el tipo de test
    if (exercise.test === 'output_contains' && exercise.expectedOutput) {
      isCorrect = exercise.expectedOutput.every((expected: string) => 
        code.toLowerCase().includes(expected.toLowerCase())
      );
    } else if (exercise.test === 'text_required') {
      isCorrect = code.trim().length >= (exercise.minLines || 1) * 5;
    } else if (exercise.test === 'code_structure') {
      isCorrect = exercise.expectedOutput?.every((expected: string) => 
        code.includes(expected)
      ) ?? false;
    } else {
      // Default: verificar que hay código
      isCorrect = code.trim().length > 10;
    }

    if (isCorrect) {
      setOutput('✅ ¡Correcto! Has completado el ejercicio.');
      if (!completed) {
        setCompleted(true);
        handleLessonComplete();
      }
    } else {
      setOutput('❌ No es correcto. Revisa las pistas e inténtalo de nuevo.');
    }
  }, [code, lessonData, completed]);

  const resetCode = useCallback(() => {
    if (lessonData?.exercise?.initialCode) {
      setCode(lessonData.exercise.initialCode);
    }
    setOutput('');
    setCompleted(false);
    setCurrentHint(0);
    setShowHints(false);
  }, [lessonData]);

  const nextHint = useCallback(() => {
    if (lessonData?.exercise?.hints && currentHint < lessonData.exercise.hints.length - 1) {
      setCurrentHint(prev => prev + 1);
    }
  }, [lessonData, currentHint]);

  const handleLessonComplete = useCallback(async () => {
    try {
      // Guardar progreso en localStorage
      const progress = JSON.parse(localStorage.getItem('lessonProgress') || '{}');
      if (!progress[courseId]) progress[courseId] = {};
      progress[courseId][lessonId] = { completed: true, xp: lessonData?.xp || 50 };
      localStorage.setItem('lessonProgress', JSON.stringify(progress));

      // Actualizar XP total
      const currentXP = parseInt(localStorage.getItem('totalXP') || '0');
      const newXP = currentXP + (lessonData?.xp || 50);
      localStorage.setItem('totalXP', newXP.toString());

      // Verificar level up
      const oldLevel = getLevelInfo(currentXP).currentLevel;
      const newLevel = getLevelInfo(newXP).currentLevel;
      if (newLevel > oldLevel) {
        await checkLevelUpAndNotify();
        showNotification('level-up', 'Nivel Up', `Has alcanzado el nivel ${newLevel}`);
      }

      // Verificar completar curso
      await checkCourseCompletionAndNotify(courseId);
      
      showNotification('xp', 'Completado', `Has ganado ${lessonData?.xp || 50} XP`);
    } catch (error) {
      console.error('Error saving progress:', error);
    }
  }, [courseId, lessonId, lessonData, showNotification]);

  // Memo para evitar recalcular en cada render
  const exerciseHints = useMemo(() => {
    return lessonData?.exercise?.hints || [];
  }, [lessonData]);

  if (isLoadingContent) {
    return (
      <div className="min-h-screen bg-stone-900 flex items-center justify-center">
        <div className="text-center">
          <div className="relative w-16 h-16 mx-auto mb-4">
            <div className="absolute inset-0 border-4 border-amber-700/30 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-amber-600 border-t-transparent rounded-full animate-spin"></div>
          </div>
          <p className="text-stone-100 text-xl">Cargando lección...</p>
        </div>
      </div>
    );
  }

  if (!lessonData) {
    return (
      <div className="min-h-screen bg-stone-900 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-stone-100 mb-4">Lección no encontrada</h1>
          <p className="text-stone-400 mb-6">El contenido de esta lección aún no está disponible.</p>
          <Link href={`/course/${courseId}`} className="text-amber-600 hover:text-amber-500 font-medium">
            ← Volver al curso
          </Link>
        </div>
      </div>
    );
  }

  // Si es una lección de contenido (sin ejercicio), renderizar vista de lectura
  if (lessonData.content && !lessonData.exercise) {
    return (
      <div className="min-h-screen bg-stone-900">
        <div className="bg-stone-800/50 backdrop-blur-sm border-b-2 border-stone-700 sticky top-0 z-10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <Link href={`/course/${courseId}`} className="text-stone-300 hover:text-stone-100 flex items-center gap-2 font-medium">
                <ArrowLeft className="w-5 h-5" />
                Volver al curso
              </Link>
              <div className="flex items-center gap-4">
                <div className="text-stone-400 text-sm">{lessonData.duration}</div>
                <div className="flex items-center gap-2 text-amber-600 font-semibold">
                  <Trophy className="w-5 h-5" />
                  +{lessonData.xp} XP
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-3xl font-bold text-stone-100 mb-8">{lessonData.title}</h1>
          <div className="prose prose-invert prose-stone max-w-none">
            <div className="text-stone-300 whitespace-pre-wrap leading-relaxed">
              {lessonData.content}
            </div>
          </div>
          
          <div className="mt-12 flex justify-between items-center">
            <Link
              href={`/course/${courseId}`}
              className="text-stone-400 hover:text-stone-100 flex items-center gap-2"
            >
              <ArrowLeft className="w-5 h-5" />
              Volver al curso
            </Link>
            <button
              onClick={() => {
                handleLessonComplete();
                setCompleted(true);
              }}
              disabled={completed}
              className={`px-6 py-3 rounded-lg font-bold flex items-center gap-2 transition-all ${
                completed 
                  ? 'bg-green-700 text-white cursor-default' 
                  : 'bg-amber-700 hover:bg-amber-600 text-white'
              }`}
            >
              {completed ? (
                <>
                  <CheckCircle className="w-5 h-5" />
                  Completado
                </>
              ) : (
                <>
                  Marcar como completado
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Lección con ejercicio interactivo
  return (
    <div className="min-h-screen bg-stone-900">
      {/* Header */}
      <div className="bg-stone-800/50 backdrop-blur-sm border-b-2 border-stone-700 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href={`/course/${courseId}`} className="text-stone-300 hover:text-stone-100 flex items-center gap-2 font-medium">
              <ArrowLeft className="w-5 h-5" />
              Volver al curso
            </Link>
            <div className="flex items-center gap-4">
              <div className="text-stone-400 text-sm">{lessonData.duration}</div>
              <div className="flex items-center gap-2 text-amber-600 font-semibold">
                <Trophy className="w-5 h-5" />
                +{lessonData.xp} XP
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-stone-100 mb-8">{lessonData.title}</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Teoría */}
          <div className="bg-stone-800 backdrop-blur-sm rounded-lg p-6 border-2 border-stone-700">
            <h2 className="text-2xl font-bold text-stone-100 mb-4 flex items-center gap-3">
              <BookOpen className="w-7 h-7 text-amber-600" />
              Teoría
            </h2>
            
            {lessonData.theory && (
              <div className="space-y-6">
                <p className="text-stone-300 leading-relaxed">{lessonData.theory.introduction}</p>
                
                {lessonData.theory.sections?.map((section: any, idx: number) => (
                  <div key={idx} className="space-y-3">
                    <h3 className="text-lg font-semibold text-stone-100">{section.title}</h3>
                    <p className="text-stone-300">{section.content}</p>
                    {section.points && (
                      <ul className="list-disc list-inside text-stone-400 space-y-1">
                        {section.points.map((point: string, pidx: number) => (
                          <li key={pidx}>{point}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}

                {lessonData.theory.example && (
                  <div className="bg-stone-950 rounded-lg p-4 border-2 border-stone-700">
                    <h4 className="text-amber-600 font-semibold mb-2">{lessonData.theory.example.title}</h4>
                    <pre className="text-sm text-amber-400 font-mono overflow-x-auto whitespace-pre-wrap">
                      {lessonData.theory.example.code}
                    </pre>
                    {lessonData.theory.example.explanation && (
                      <p className="text-stone-400 text-sm mt-3">{lessonData.theory.example.explanation}</p>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Ejercicio */}
          <div className="bg-stone-800 backdrop-blur-sm rounded-lg p-6 border-2 border-stone-700 sticky top-24">
            <h2 className="text-2xl font-bold text-stone-100 mb-2 flex items-center gap-3">
              <Code className="w-7 h-7 text-amber-600" />
              {lessonData.exercise?.title || 'Ejercicio'}
            </h2>
            <p className="text-stone-300 mb-6">{lessonData.exercise?.description}</p>

            {/* Code Editor */}
            <div className="mb-4">
              <div className="bg-stone-950 rounded-t-lg px-4 py-2 border-b-2 border-stone-700">
                <span className="text-stone-400 text-sm font-mono">editor.py</span>
              </div>
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="w-full bg-stone-950 text-amber-400 font-mono text-sm p-4 rounded-b-lg border-2 border-stone-700 focus:outline-none focus:ring-2 focus:ring-amber-700 min-h-[200px] resize-y"
                spellCheck={false}
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 mb-4">
              <button
                onClick={runCode}
                className="flex-1 bg-amber-700 text-white px-6 py-3 rounded-lg font-bold hover:bg-amber-600 transition-all flex items-center justify-center gap-2 border-2 border-amber-800"
              >
                <Play className="w-5 h-5" />
                Ejecutar Código
              </button>
              <button
                onClick={resetCode}
                className="bg-stone-700 hover:bg-stone-600 text-stone-100 px-4 py-3 rounded-lg transition-colors border-2 border-stone-700"
                title="Reiniciar código"
              >
                <RotateCcw className="w-5 h-5" />
              </button>
            </div>

            {/* Output */}
            {output && (
              <div className="bg-stone-950 rounded-lg p-4 mb-4 border-2 border-stone-700">
                <div className="text-stone-400 text-sm font-mono mb-2">Salida:</div>
                <pre className="text-sm text-stone-100 whitespace-pre-wrap font-mono">{output}</pre>
              </div>
            )}

            {/* Hints */}
            <div className="bg-amber-700/10 border-2 border-amber-800 rounded-lg p-4">
              <button
                onClick={() => setShowHints(!showHints)}
                className="flex items-center gap-2 text-amber-600 font-semibold mb-2"
              >
                <Lightbulb className="w-5 h-5" />
                {showHints ? 'Ocultar pistas' : 'Ver pistas'}
              </button>
              {showHints && exerciseHints.length > 0 && (
                <div className="space-y-3">
                  <p className="text-stone-300 text-sm">{exerciseHints[currentHint]}</p>
                  {currentHint < exerciseHints.length - 1 && (
                    <button
                      onClick={nextHint}
                      className="text-amber-600 text-sm hover:text-amber-500"
                    >
                      Ver siguiente pista →
                    </button>
                  )}
                </div>
              )}
            </div>

            {/* Completion */}
            {completed && (
              <div className="mt-6 bg-amber-700 rounded-lg p-6 text-center border-2 border-amber-800">
                <CheckCircle className="w-12 h-12 text-white mx-auto mb-3" />
                <h3 className="text-2xl font-bold text-white mb-2">¡Lección Completada!</h3>
                <p className="text-stone-100 mb-4">Has ganado {lessonData.xp} XP</p>
                <Link
                  href={`/course/${courseId}`}
                  className="inline-flex items-center gap-2 bg-stone-900 text-amber-600 px-6 py-3 rounded-lg font-bold hover:bg-stone-800 transition-colors border-2 border-stone-700"
                >
                  Ver Curso Completo
                  <ArrowRight className="w-5 h-5" />
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
