import { STORAGE_KEYS, NOTIFICATION_LIMITS, NOTIFICATION_TYPES, type NotificationType } from './constants';

type AppNotificationType = typeof NOTIFICATION_TYPES[keyof typeof NOTIFICATION_TYPES];

interface AppNotification {
  id: string;
  type: AppNotificationType;
  title: string;
  message: string;
  timestamp: string; // ISO
  read: boolean;
  icon?: string;
}

export function getNotifications(): AppNotification[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.NOTIFICATIONS);
    if (!raw) return [];
    return JSON.parse(raw) as AppNotification[];
  } catch (e) {
    console.error('getNotifications error', e);
    return [];
  }
}

export function saveNotifications(list: AppNotification[]) {
  localStorage.setItem(STORAGE_KEYS.NOTIFICATIONS, JSON.stringify(list));
  // dispatch event to notify UI
  window.dispatchEvent(new CustomEvent('notifications-updated'));
}

export function pushNotification(payload: Omit<AppNotification, 'id' | 'timestamp' | 'read'>) {
  const existing = getNotifications();
  const n: AppNotification = {
    id: `${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
    title: payload.title,
    message: payload.message,
    type: payload.type,
    icon: payload.icon || '',
    timestamp: new Date().toISOString(),
    read: false,
  };
  const next = [n, ...existing].slice(0, NOTIFICATION_LIMITS.MAX_STORED);
  saveNotifications(next);
  return n;
}

// XP / achievements helpers
interface CourseDef { id: string; lessons: number; xpPerLesson?: number }
const COURSES: CourseDef[] = [
  { id: 'py-intro', lessons: 4, xpPerLesson: 50 },
  { id: 'py-variables', lessons: 5, xpPerLesson: 50 },
  { id: 'py-control', lessons: 6, xpPerLesson: 50 },
  { id: 'py-functions', lessons: 6, xpPerLesson: 50 },
  { id: 'py-classes', lessons: 6, xpPerLesson: 50 },
  { id: 'py-files', lessons: 6, xpPerLesson: 50 },
];

export function computeXP() {
  let totalXP = 0;
  let completedLessons = 0;
  let completedCourses = 0;

  COURSES.forEach(course => {
    let courseCompleted = 0;
    for (let i = 1; i <= course.lessons; i++) {
      const key = `lesson_${course.id}_${i}`;
      if (localStorage.getItem(key) === 'completed') {
        totalXP += course.xpPerLesson || 50;
        completedLessons++;
        courseCompleted++;
      }
    }
    if (courseCompleted === course.lessons) {
      totalXP += 100; // course bonus
      completedCourses++;
    }
  });

  const level = Math.floor(totalXP / 100) + 1;
  return { totalXP, level, completedLessons, completedCourses };
}

export function checkLevelUpAndNotify() {
  try {
    const prevLevel = Number(localStorage.getItem('user_level') || '1');
    const { totalXP, level } = computeXP();
    if (level > prevLevel) {
      // notify
      pushNotification({
        type: 'achievement',
        title: `¡Subiste al nivel ${level}!`,
        message: `Has ganado ${totalXP} XP en total. Sigue así.`,
        icon: '⭐',
      });
      localStorage.setItem('user_level', String(level));
    }
    // always store latest XP
    localStorage.setItem('user_total_xp', String(totalXP));
    return { level, prevLevel };
  } catch (e) {
    console.error('checkLevelUp error', e);
    return null;
  }
}

export function checkCourseCompletionAndNotify(courseId: string) {
  const course = COURSES.find(c => c.id === courseId);
  if (!course) return;
  let completed = 0;
  for (let i = 1; i <= course.lessons; i++) {
    const key = `lesson_${courseId}_${i}`;
    if (localStorage.getItem(key) === 'completed') completed++;
  }
  const alreadyNotified = localStorage.getItem(`course_completed_notified_${courseId}`);
  if (completed === course.lessons && !alreadyNotified) {
    pushNotification({
      type: NOTIFICATION_TYPES.COURSE_COMPLETE,
      title: `Curso completado: ${courseId}`,
      message: `¡Felicidades! Has completado todas las lecciones del curso. Bonus XP otorgado.`,
      icon: '🏆',
    });
    localStorage.setItem(`course_completed_notified_${courseId}`, '1');
  }
}
