/**
 * Page: Lección del Curso Gratuito
 * Vista de una lección individual con video, quiz y labs
 */

import { LessonVideo } from '@/components/course/LessonVideo';
import { LessonQuiz } from '@/components/course/LessonQuiz';
import { CodeLab } from '@/components/course/CodeLab';
import { LessonNav } from '@/components/course/LessonNav';
import { FREE_COURSE } from '@/data/free-course';

interface LessonPageProps {
  params: {
    lessonSlug: string;
  };
}

export default function LessonPage({ params }: LessonPageProps) {
  const lesson = FREE_COURSE.lessons.find(l => l.slug === params.lessonSlug);

  if (!lesson) {
    return <div>Lección no encontrada</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="border-b border-gray-200 bg-white">
        <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">
                Lección {lesson.order} de {FREE_COURSE.lessons.length}
              </p>
              <h1 className="text-2xl font-bold text-gray-900">
                {lesson.title}
              </h1>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                ⏱️ {lesson.duration_minutes} min
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-3">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Video */}
            {lesson.content.video_url && (
              <LessonVideo
                url={lesson.content.video_url}
                duration={lesson.content.video_duration || 0}
                transcript={(lesson.content as any).transcript}
              />
            )}

            {/* Lab */}
            {(lesson.content as any).lab && (
              <CodeLab
                lab={(lesson.content as any).lab}
                lessonId={String(lesson.id)}
              />
            )}

            {/* Quiz */}
            {(lesson.content as any).quiz && (
              <LessonQuiz
                quiz={(lesson.content as any).quiz}
                lessonId={String(lesson.id)}
              />
            )}

            {/* Project */}
            {(lesson.content as any).project && (
              <div className="rounded-lg border border-gray-200 bg-white p-8">
                <h2 className="text-2xl font-bold text-gray-900">
                  {(lesson.content as any).project.title}
                </h2>
                <div className="prose mt-4 max-w-none">
                  {(lesson.content as any).project.description}
                </div>
                
                <div className="mt-6">
                  <h3 className="font-semibold text-gray-900">Requisitos:</h3>
                  <ul className="mt-2 space-y-2">
                    {(lesson.content as any).project.requirements.map((req: string, i: number) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-green-500">✓</span>
                        <span className="text-gray-700">{req}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <CodeLab
                  lab={{
                    title: (lesson.content as any).project.title,
                    description: 'Proyecto final',
                    exercises: [{
                      id: 'project',
                      language: 'python',
                      title: (lesson.content as any).project.title,
                      instructions: (lesson.content as any).project.description,
                      starter_code: (lesson.content as any).project.starter_code,
                      solution: (lesson.content as any).project.solution,
                      tests: [],
                    }],
                  }}
                  lessonId={String(lesson.id)}
                />
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <LessonNav
              currentSlug={lesson.slug}
              lessons={FREE_COURSE.lessons.map(l => ({ slug: l.slug, title: l.title }))}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export async function generateStaticParams() {
  return FREE_COURSE.lessons.map((lesson) => ({
    lessonSlug: lesson.slug,
  }));
}
