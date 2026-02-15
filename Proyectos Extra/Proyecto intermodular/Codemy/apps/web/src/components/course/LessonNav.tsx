'use client';

import Link from 'next/link';

interface LessonNavProps {
  currentSlug: string;
  lessons: Array<{
    slug: string;
    title: string;
  }>;
}

export function LessonNav({ currentSlug, lessons }: LessonNavProps) {
  const currentIndex = lessons.findIndex(l => l.slug === currentSlug);
  const prevLesson = currentIndex > 0 ? lessons[currentIndex - 1] : null;
  const nextLesson = currentIndex < lessons.length - 1 ? lessons[currentIndex + 1] : null;

  return (
    <div className="flex justify-between items-center py-6 border-t border-gray-200">
      <div>
        {prevLesson ? (
          <Link
            href={`/course/free/${prevLesson.slug}`}
            className="inline-flex items-center space-x-2 text-stone-600 hover:text-stone-800"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            <div className="text-left">
              <div className="text-xs text-gray-500">Anterior</div>
              <div className="font-medium">{prevLesson.title}</div>
            </div>
          </Link>
        ) : (
          <div className="text-gray-400">
            <div className="text-xs">Primera lección</div>
          </div>
        )}
      </div>

      <div className="text-center">
        <Link
          href="/course/free"
          className="text-sm text-gray-600 hover:text-gray-900"
        >
          📚 Ver todas las lecciones
        </Link>
      </div>

      <div>
        {nextLesson ? (
          <Link
            href={`/course/free/${nextLesson.slug}`}
            className="inline-flex items-center space-x-2 text-stone-600 hover:text-stone-800"
          >
            <div className="text-right">
              <div className="text-xs text-gray-500">Siguiente</div>
              <div className="font-medium">{nextLesson.title}</div>
            </div>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        ) : (
          <div className="text-right text-gray-400">
            <div className="text-xs">Última lección</div>
            <div className="font-medium">¡Completado! 🎉</div>
          </div>
        )}
      </div>
    </div>
  );
}
