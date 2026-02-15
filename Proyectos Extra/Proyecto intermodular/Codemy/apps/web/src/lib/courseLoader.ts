// Helper to load course data from modules or fallback
import { courseModules } from '@/data/courses';
import { getCourseStats } from './course-db';

// Type for course data
export interface CourseData {
  id: string;
  title: string;
  description: string;
  icon?: string;
  xp?: number;
  level?: string;
  duration?: string;
  category?: string;
  objectives?: string[];
  lessons: Array<{
    id?: string | number;
    title: string;
    content?: string;
    duration?: string;
    status?: 'available' | 'locked';
    xp?: number;
  }>;
  progress?: number;
  studentsEnrolled?: number;
}

// Load course by ID - tries module first, then returns null if not found
export async function getCourseData(courseId: string, userId?: string): Promise<CourseData | null> {
  console.log('🔍 getCourseData called with:', courseId);
  
  // Try to load from course modules
  const moduleData = courseModules[courseId as keyof typeof courseModules];
  
  console.log('📦 Module data found:', !!moduleData, moduleData ? (moduleData as any).title : 'none');
  
  if (moduleData) {
    // Get real stats from database (or use defaults if it fails)
    let stats = { studentsEnrolled: 0, progressPercentage: 0, lessonsCompleted: 0, totalLessons: 0 };
    try {
      stats = await getCourseStats(courseId, userId);
      console.log('📊 Stats loaded from DB:', stats);
    } catch (error) {
      console.warn('⚠️ Could not load stats from DB, using defaults:', error);
    }
    
    // Adapt module format to expected format
    const lessons = (moduleData as any).lessons || [];
    
    console.log('📚 Lessons count:', lessons.length);
    
    return {
      id: (moduleData as any).id || courseId,
      title: (moduleData as any).title || 'Curso',
      description: (moduleData as any).description || '',
      icon: '📚',
      xp: 300,
      level: 'Intermedio',
      duration: '2 horas',
      category: 'Programación',
      objectives: ['Objetivo 1', 'Objetivo 2', 'Objetivo 3'],
      lessons: lessons.map((lesson: any, index: number) => ({
        id: lesson.id || String(index + 1),
        title: lesson.title,
        content: lesson.content,
        duration: lesson.duration || '30 min',
        status: index === 0 ? 'available' : 'locked',
        xp: lesson.xp || 50,
      })),
      progress: stats.progressPercentage,
      studentsEnrolled: stats.studentsEnrolled,
    };
  }
  
  return null;
}

// Check if course exists in modules
export function courseExistsInModules(courseId: string): boolean {
  return courseId in courseModules;
}

// Get a specific lesson content from a course
export function getLessonContent(courseId: string, lessonId: string): { title: string; content: string } | null {
  const moduleData = courseModules[courseId as keyof typeof courseModules];
  
  if (!moduleData) {
    return null;
  }
  
  const lessons = (moduleData as any).lessons || [];
  // lessonId puede ser un índice (1, 2, 3...) o un id real
  const lessonIndex = parseInt(lessonId) - 1;
  const lesson = lessons[lessonIndex];
  
  if (!lesson) {
    return null;
  }
  
  return {
    title: lesson.title,
    content: lesson.content || '',
  };
}
