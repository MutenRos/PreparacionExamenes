/**
 * Helper functions for XP and level calculations
 */

import { XP_CONSTANTS } from './constants';

export interface LevelInfo {
  currentLevel: number;
  currentXP: number;
  xpForNextLevel: number;
  xpProgress: number;
  totalXP: number;
}

/**
 * Calculate level from total XP
 */
export function calculateLevel(totalXP: number): number {
  return Math.floor(totalXP / XP_CONSTANTS.PER_LEVEL) + 1;
}

/**
 * Get detailed level information
 */
export function getLevelInfo(totalXP: number): LevelInfo {
  const currentLevel = calculateLevel(totalXP);
  const xpForCurrentLevel = (currentLevel - 1) * XP_CONSTANTS.PER_LEVEL;
  const xpForNextLevel = currentLevel * XP_CONSTANTS.PER_LEVEL;
  const currentXP = totalXP - xpForCurrentLevel;
  const xpProgress = (currentXP / XP_CONSTANTS.PER_LEVEL) * 100;

  return {
    currentLevel,
    currentXP,
    xpForNextLevel,
    xpProgress,
    totalXP,
  };
}

/**
 * Calculate total XP from completed lessons
 */
export function calculateTotalXP(): number {
  let totalXP = 0;
  const completedLessons: string[] = [];

  // Get all completed lessons from localStorage
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key?.startsWith('lesson_') && localStorage.getItem(key) === 'completed') {
      completedLessons.push(key);
      totalXP += XP_CONSTANTS.PER_LESSON;
    }
  }

  return totalXP;
}

/**
 * Check if user leveled up after gaining XP
 */
export function checkLevelUp(oldXP: number, newXP: number): { leveledUp: boolean; newLevel?: number } {
  const oldLevel = calculateLevel(oldXP);
  const newLevel = calculateLevel(newXP);

  if (newLevel > oldLevel) {
    return { leveledUp: true, newLevel };
  }

  return { leveledUp: false };
}

/**
 * Get XP for specific action
 */
export function getXPForAction(action: 'lesson' | 'course'): number {
  switch (action) {
    case 'lesson':
      return XP_CONSTANTS.PER_LESSON;
    case 'course':
      return XP_CONSTANTS.COURSE_BONUS;
    default:
      return 0;
  }
}
