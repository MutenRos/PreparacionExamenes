/**
 * Funciones para interactuar con cursos y progreso en Supabase
 */

import { createClient } from '@/lib/supabase/client';

export interface CourseStats {
  studentsEnrolled: number;
  lessonsCompleted: number;
  totalLessons: number;
  progressPercentage: number;
}

/**
 * Obtiene estadísticas de un curso desde la base de datos
 */
export async function getCourseStats(courseId: string, userId?: string): Promise<CourseStats> {
  const supabase = createClient();
  
  try {
    // Contar estudiantes inscritos (usuarios que han iniciado el curso)
    const { count: enrolled } = await supabase
      .from('user_courses')
      .select('*', { count: 'exact', head: true })
      .eq('course_id', courseId);

    // Si hay usuario, obtener su progreso personal
    if (userId) {
      const { data: userCourse } = await supabase
        .from('user_courses')
        .select('progress_percentage, lessons_completed')
        .eq('user_id', userId)
        .eq('course_id', courseId)
        .single();

      // Obtener total de lecciones del curso
      const { data: course } = await supabase
        .from('courses')
        .select('total_lessons')
        .eq('id', courseId)
        .single();

      return {
        studentsEnrolled: enrolled || 0,
        lessonsCompleted: userCourse?.lessons_completed || 0,
        totalLessons: course?.total_lessons || 0,
        progressPercentage: userCourse?.progress_percentage || 0,
      };
    }

    return {
      studentsEnrolled: enrolled || 0,
      lessonsCompleted: 0,
      totalLessons: 0,
      progressPercentage: 0,
    };
  } catch (error) {
    console.error('Error getting course stats:', error);
    return {
      studentsEnrolled: 0,
      lessonsCompleted: 0,
      totalLessons: 0,
      progressPercentage: 0,
    };
  }
}

/**
 * Obtiene el progreso de lecciones del usuario en un curso
 */
export async function getUserLessonProgress(userId: string, courseId: string): Promise<Record<string, string>> {
  const supabase = createClient();
  
  try {
    const { data: progress } = await supabase
      .from('user_progress')
      .select('lesson_id, status')
      .eq('user_id', userId)
      .eq('course_id', courseId);

    const progressMap: Record<string, string> = {};
    progress?.forEach(p => {
      progressMap[p.lesson_id] = p.status;
    });

    return progressMap;
  } catch (error) {
    console.error('Error getting user lesson progress:', error);
    return {};
  }
}

/**
 * Actualiza el estado de una lección para un usuario
 */
export async function updateLessonProgress(
  userId: string,
  courseId: string,
  lessonId: string,
  status: 'available' | 'in-progress' | 'completed',
  xpEarned?: number
): Promise<boolean> {
  const supabase = createClient();
  
  try {
    const { error } = await supabase
      .from('user_progress')
      .upsert({
        user_id: userId,
        course_id: courseId,
        lesson_id: lessonId,
        status,
        xp_earned: xpEarned || 0,
        completed_at: status === 'completed' ? new Date().toISOString() : null,
        updated_at: new Date().toISOString(),
      }, {
        onConflict: 'user_id,lesson_id'
      });

    if (error) {
      console.error('Error updating lesson progress:', error);
      return false;
    }

    // Si se completó, actualizar el progreso del curso
    if (status === 'completed') {
      await updateCourseProgress(userId, courseId);
    }

    return true;
  } catch (error) {
    console.error('Error updating lesson progress:', error);
    return false;
  }
}

/**
 * Actualiza el progreso general del curso para un usuario
 */
async function updateCourseProgress(userId: string, courseId: string): Promise<void> {
  const supabase = createClient();
  
  try {
    // Contar lecciones completadas
    const { count: completed } = await supabase
      .from('user_progress')
      .select('*', { count: 'exact', head: true })
      .eq('user_id', userId)
      .eq('course_id', courseId)
      .eq('status', 'completed');

    // Obtener total de lecciones del curso
    const { data: course } = await supabase
      .from('courses')
      .select('total_lessons')
      .eq('id', courseId)
      .single();

    const totalLessons = course?.total_lessons || 1;
    const progressPercentage = Math.round(((completed || 0) / totalLessons) * 100);
    const courseStatus = progressPercentage === 100 ? 'completed' : 
                         progressPercentage > 0 ? 'in-progress' : 'available';

    // Actualizar o insertar progreso del curso
    await supabase
      .from('user_courses')
      .upsert({
        user_id: userId,
        course_id: courseId,
        progress_percentage: progressPercentage,
        lessons_completed: completed || 0,
        status: courseStatus,
        started_at: progressPercentage > 0 ? new Date().toISOString() : null,
        completed_at: progressPercentage === 100 ? new Date().toISOString() : null,
        updated_at: new Date().toISOString(),
      }, {
        onConflict: 'user_id,course_id'
      });

  } catch (error) {
    console.error('Error updating course progress:', error);
  }
}

/**
 * Inicializa el curso para un usuario (lo marca como disponible)
 */
export async function initializeCourse(userId: string, courseId: string): Promise<boolean> {
  const supabase = createClient();
  
  try {
    const { error } = await supabase
      .from('user_courses')
      .upsert({
        user_id: userId,
        course_id: courseId,
        status: 'available',
        progress_percentage: 0,
        lessons_completed: 0,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      }, {
        onConflict: 'user_id,course_id',
        ignoreDuplicates: true
      });

    return !error;
  } catch (error) {
    console.error('Error initializing course:', error);
    return false;
  }
}
