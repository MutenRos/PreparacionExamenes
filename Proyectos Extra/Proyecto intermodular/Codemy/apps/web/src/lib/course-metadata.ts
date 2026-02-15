/**
 * Dynamic course data loader
 * This file loads course metadata dynamically from the course modules
 * Replaces hardcoded coursesData object in course pages
 */

import { courseModules } from '@/data/courses';
import { DEFAULTS, COURSE_LEVELS, type CourseLevel } from '@/lib/constants';

export interface CourseMetadata {
  id: string;
  title: string;
  description: string;
  icon: string;
  xp: number;
  level: CourseLevel;
  duration: string;
  category: string;
  objectives: string[];
  lessonsCount: number;
  studentsEnrolled: number;
  progress?: number;
}

export interface LessonMetadata {
  id: string;
  title: string;
  duration: string;
  status: 'locked' | 'available' | 'in-progress' | 'completed';
  xp: number;
}

export interface CourseWithLessons extends CourseMetadata {
  lessons: LessonMetadata[];
}

/**
 * Get course metadata by ID from course modules
 */
export function getCourseMetadata(courseId: string): CourseMetadata | null {
  const course = courseModules[courseId as keyof typeof courseModules] as any;
  
  if (!course) {
    return null;
  }

  return {
    id: course.id,
    title: course.title,
    description: course.description || 'Curso de programación',
    icon: course.icon || '📚',
    xp: course.xp || (course.lessons?.length ?? 0) * DEFAULTS.LESSON_XP,
    level: (course.level || COURSE_LEVELS.FOUNDATION) as CourseLevel,
    duration: course.duration || DEFAULTS.COURSE_DURATION,
    category: course.category || 'Programación',
    objectives: course.objectives || [],
    lessonsCount: course.lessons?.length ?? 0,
    studentsEnrolled: DEFAULTS.STUDENTS_ENROLLED,
    progress: DEFAULTS.COURSE_PROGRESS,
  };
}

/**
 * Get course with lessons metadata
 */
export function getCourseWithLessons(courseId: string): CourseWithLessons | null {
  const course = courseModules[courseId as keyof typeof courseModules] as any;
  
  // CRITICAL DEBUG - Check what's actually loaded
  if (courseId === 'ofimatica-intro') {
    console.error('🔍 CRITICAL DEBUG - courseModules keys:', Object.keys(courseModules).filter(k => k.includes('ofimat')));
    console.error('🔍 Module loaded for ofimatica-intro:', {
      title: course?.title,
      id: course?.id,
      lessonsCount: course?.lessons?.length,
      firstLesson: course?.lessons?.[0],
      lastLesson: course?.lessons?.[course?.lessons?.length - 1]
    });
  }
  
  console.error('🔍 getCourseWithLessons DEBUG:', {
    courseId,
    courseExists: !!course,
    courseLessons: course?.lessons,
    courseLessonsLength: course?.lessons?.length
  });
  
  if (!course) {
    return null;
  }

  const metadata = getCourseMetadata(courseId);
  if (!metadata) {
    return null;
  }

  const lessons: LessonMetadata[] = (course.lessons || []).map((lesson: any, index: number) => ({
    id: lesson.id,
    title: lesson.title,
    duration: lesson.duration || DEFAULTS.LESSON_DURATION,
    status: index === 0 ? 'available' : 'locked',
    xp: lesson.xp || DEFAULTS.LESSON_XP,
  }));

  console.error('🔍 Lessons mapped:', lessons.length);

  return {
    ...metadata,
    lessons,
  };
}

/**
 * Get all available courses
 */
export function getAllCourses(): CourseMetadata[] {
  const courses: CourseMetadata[] = [];
  
  for (const courseId in courseModules) {
    const metadata = getCourseMetadata(courseId);
    if (metadata) {
      courses.push(metadata);
    }
  }
  
  return courses;
}

/**
 * Get courses by category
 */
export function getCoursesByCategory(category: string): CourseMetadata[] {
  return getAllCourses().filter(course => course.category === category);
}

/**
 * Get courses by level
 */
export function getCoursesByLevel(level: CourseLevel): CourseMetadata[] {
  return getAllCourses().filter(course => course.level === level);
}

/**
 * Search courses by title or description
 */
export function searchCourses(query: string): CourseMetadata[] {
  const lowerQuery = query.toLowerCase();
  return getAllCourses().filter(
    course =>
      course.title.toLowerCase().includes(lowerQuery) ||
      course.description.toLowerCase().includes(lowerQuery)
  );
}

/**
 * Get recommended courses based on current course
 */
export function getRecommendedCourses(
  currentCourseId: string,
  limit: number = 3
): CourseMetadata[] {
  const currentCourse = getCourseMetadata(currentCourseId);
  if (!currentCourse) {
    return [];
  }

  // Get courses from the same category
  const sameCategoryCourses = getCoursesByCategory(currentCourse.category).filter(
    course => course.id !== currentCourseId
  );

  // Return limited results
  return sameCategoryCourses.slice(0, limit);
}

/**
 * Get course categories
 */
export function getCourseCategories(): string[] {
  const categories = new Set<string>();
  
  for (const courseId in courseModules) {
    const course = courseModules[courseId as keyof typeof courseModules] as any;
    if (course?.category) {
      categories.add(course.category);
    }
  }
  
  return Array.from(categories).sort();
}

/**
 * Get course count by category
 */
export function getCourseCountByCategory(): Record<string, number> {
  const counts: Record<string, number> = {};
  
  for (const courseId in courseModules) {
    const course = courseModules[courseId as keyof typeof courseModules] as any;
    const category = course?.category || 'Otros';
    counts[category] = (counts[category] || 0) + 1;
  }
  
  return counts;
}

/**
 * Validate if a course exists
 */
export function courseExists(courseId: string): boolean {
  return courseId in courseModules;
}

/**
 * Get total number of courses
 */
export function getTotalCoursesCount(): number {
  return Object.keys(courseModules).length;
}

/**
 * Get total number of lessons across all courses
 */
export function getTotalLessonsCount(): number {
  let total = 0;
  
  for (const courseId in courseModules) {
    const course = courseModules[courseId as keyof typeof courseModules] as any;
    total += course?.lessons?.length ?? 0;
  }
  
  return total;
}
