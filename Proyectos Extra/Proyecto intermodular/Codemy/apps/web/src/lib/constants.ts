/**
 * Central configuration file for all application constants
 * This file contains all hardcoded values that were previously scattered across the codebase
 */

// ============================================================================
// XP AND GAMIFICATION CONSTANTS
// ============================================================================

export const XP_CONSTANTS = {
  /** XP required per level (100 XP = 1 level) */
  PER_LEVEL: 100,
  /** XP awarded per lesson completion */
  PER_LESSON: 50,
  /** Bonus XP awarded for completing an entire course */
  COURSE_BONUS: 100,
} as const;

// ============================================================================
// ADMIN CONFIGURATION
// ============================================================================

export const ADMIN_CONFIG = {
  /** Email address of the main admin user */
  EMAIL: 'admin@codedungeon.es',
} as const;

// ============================================================================
// APPLICATION URLS AND ENDPOINTS
// ============================================================================

export const APP_URLS = {
  /** Base URL for the application */
  BASE: process.env.NEXT_PUBLIC_APP_URL || 'https://codedungeon.es',
  /** PayPal donation link */
  PAYPAL_DONATION: 'https://paypal.me/mutenros',
  /** GitHub repository link */
  GITHUB_REPO: 'https://github.com/jocarsa/dam2526',
} as const;

// ============================================================================
// PAYPAL API CONFIGURATION
// ============================================================================

export const PAYPAL_CONFIG = {
  /** PayPal API base URL for production */
  PRODUCTION_URL: 'https://api-m.paypal.com',
  /** PayPal API base URL for sandbox/testing */
  SANDBOX_URL: 'https://api-m.sandbox.paypal.com',
  /** Get the appropriate PayPal API URL based on environment */
  getApiUrl: () =>
    process.env.NODE_ENV === 'production'
      ? PAYPAL_CONFIG.PRODUCTION_URL
      : PAYPAL_CONFIG.SANDBOX_URL,
} as const;

// ============================================================================
// LOCALSTORAGE KEYS
// ============================================================================

export const STORAGE_KEYS = {
  /** Key for storing notifications in localStorage */
  NOTIFICATIONS: 'app_notifications_v1',
  /** Prefix for Supabase auth tokens */
  SUPABASE_AUTH_PREFIX: 'sb-',
} as const;

// ============================================================================
// NOTIFICATION LIMITS
// ============================================================================

export const NOTIFICATION_LIMITS = {
  /** Maximum number of notifications to store in localStorage */
  MAX_STORED: 100,
} as const;

// ============================================================================
// UI CONSTANTS
// ============================================================================

export const UI_CONSTANTS = {
  /** Default animation duration in milliseconds */
  ANIMATION_DURATION: 300,
  /** Loading text for pages */
  LOADING_TEXT: 'Cargando...',
} as const;

// ============================================================================
// SKILL TREE CONFIGURATION
// ============================================================================

export const SKILL_TREE_CONFIG = {
  /** Available skill tree categories */
  CATEGORIES: [
    'Python',
    'Web Development',
    '3D Modeling',
    'Security',
    'Arduino',
    'DevOps',
    'Java',
    'Mobile',
  ] as const,
} as const;

// ============================================================================
// COURSE LEVELS
// ============================================================================

export const COURSE_LEVELS = {
  FOUNDATION: 'Principiante',
  INTERMEDIATE: 'Intermedio',
  ADVANCED: 'Avanzado',
  EXPERT: 'Experto',
} as const;

export type CourseLevel = typeof COURSE_LEVELS[keyof typeof COURSE_LEVELS];

// ============================================================================
// LESSON STATUS
// ============================================================================

export const LESSON_STATUS = {
  LOCKED: 'locked',
  AVAILABLE: 'available',
  IN_PROGRESS: 'in-progress',
  COMPLETED: 'completed',
} as const;

export type LessonStatus = typeof LESSON_STATUS[keyof typeof LESSON_STATUS];

// ============================================================================
// ACHIEVEMENT RARITY
// ============================================================================

export const ACHIEVEMENT_RARITY = {
  COMMON: 'common',
  RARE: 'rare',
  EPIC: 'epic',
  LEGENDARY: 'legendary',
} as const;

export type AchievementRarity = typeof ACHIEVEMENT_RARITY[keyof typeof ACHIEVEMENT_RARITY];

// ============================================================================
// NOTIFICATION TYPES
// ============================================================================

export const NOTIFICATION_TYPES = {
  ACHIEVEMENT: 'achievement',
  LEVEL_UP: 'level_up',
  COURSE_COMPLETE: 'course_complete',
  INFO: 'info',
  ERROR: 'error',
} as const;

export type NotificationType = typeof NOTIFICATION_TYPES[keyof typeof NOTIFICATION_TYPES];

// ============================================================================
// DEFAULT VALUES
// ============================================================================

export const DEFAULTS = {
  /** Default course duration when not specified */
  COURSE_DURATION: '30 min',
  /** Default lesson duration when not specified */
  LESSON_DURATION: '30 min',
  /** Default lesson XP when not specified */
  LESSON_XP: 50,
  /** Default starting students enrolled count */
  STUDENTS_ENROLLED: 0,
  /** Default course progress percentage */
  COURSE_PROGRESS: 0,
} as const;

// ============================================================================
// PAGINATION AND LIMITS
// ============================================================================

export const LIMITS = {
  /** Maximum number of courses to display per page */
  COURSES_PER_PAGE: 12,
  /** Maximum number of lessons to display per page */
  LESSONS_PER_PAGE: 20,
  /** Maximum number of forum posts per page */
  FORUM_POSTS_PER_PAGE: 10,
  /** Maximum number of leaderboard entries to display */
  LEADERBOARD_ENTRIES: 50,
} as const;

// ============================================================================
// API ENDPOINTS (External)
// ============================================================================

export const EXTERNAL_APIS = {
  /** JSONPlaceholder API for testing */
  JSON_PLACEHOLDER: 'https://jsonplaceholder.typicode.com',
  /** OpenWeatherMap API */
  OPEN_WEATHER_MAP: 'https://api.openweathermap.org/data/2.5/weather',
  /** GitHub API */
  GITHUB_API: 'https://api.github.com',
} as const;

// ============================================================================
// SUBSCRIPTION PLANS
// ============================================================================

export const SUBSCRIPTION_PLANS = {
  FREE: {
    id: 'free',
    name: 'Gratuito',
    price: 0,
    features: ['Acceso a cursos básicos', 'Foro de la comunidad'],
  },
  PREMIUM: {
    id: 'premium',
    name: 'Premium',
    price: 9.99,
    features: [
      'Acceso a todos los cursos',
      'Certificados verificados',
      'Soporte prioritario',
      'Sin anuncios',
    ],
  },
  PIONEER: {
    id: 'pioneer',
    name: 'Pionero',
    price: 4.99,
    features: [
      'Acceso completo de por vida',
      'Todos los beneficios Premium',
      'Insignia especial de pionero',
      'Acceso anticipado a nuevos cursos',
    ],
    maxSlots: 100,
  },
} as const;

// ============================================================================
// EXAMPLE/TESTING URLS
// ============================================================================

export const EXAMPLE_URLS = {
  /** Example YouTube video URL for testing */
  YOUTUBE: 'https://youtube.com/watch?v=example',
  /** Example website URL for testing */
  WEBSITE: 'https://www.example.com',
  /** Example database connection string */
  DATABASE: 'mongodb://localhost:27017',
} as const;

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Check if a user is an admin
 */
export function isAdmin(email: string | null | undefined): boolean {
  return email === ADMIN_CONFIG.EMAIL;
}

/**
 * Get PayPal donation URL with amount
 */
export function getPayPalDonationUrl(amount: number): string {
  return `${APP_URLS.PAYPAL_DONATION}/${amount.toFixed(2)}`;
}

/**
 * Calculate level from total XP
 */
export function calculateLevel(totalXP: number): number {
  return Math.floor(totalXP / XP_CONSTANTS.PER_LEVEL) + 1;
}

/**
 * Calculate XP needed for next level
 */
export function getXPForNextLevel(currentLevel: number): number {
  return currentLevel * XP_CONSTANTS.PER_LEVEL;
}

/**
 * Get notification storage key
 */
export function getNotificationStorageKey(): string {
  return STORAGE_KEYS.NOTIFICATIONS;
}
