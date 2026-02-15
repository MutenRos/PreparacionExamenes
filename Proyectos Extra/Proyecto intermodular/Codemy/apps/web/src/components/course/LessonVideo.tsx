'use client';

interface LessonVideoProps {
  videoUrl?: string;
  url?: string;
  title?: string;
  duration?: number;
  transcript?: any;
}

export function LessonVideo({ videoUrl, url, title, duration, transcript }: LessonVideoProps) {
  const videoPath = videoUrl || url;
  
  return (
    <div className="aspect-video bg-gray-900 rounded-lg overflow-hidden">
      <div className="w-full h-full flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-stone-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
            </svg>
          </div>
          <p className="text-gray-400 text-sm">{title || 'Video de la lección'}</p>
          {duration && <p className="text-gray-500 text-xs mt-1">{duration} minutos</p>}
          <p className="text-gray-500 text-xs mt-2">Video player en desarrollo</p>
        </div>
      </div>
    </div>
  );
}
