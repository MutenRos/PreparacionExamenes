'use client';

import React, { useState, useEffect } from 'react';
import SkillTreeRoadmap from '@/components/SkillTreeRoadmap';
import { getSafeUserClient } from '@/lib/auth-helpers-client';

export default function MobileSkillTree() {
  const [completedCourses, setCompletedCourses] = useState<string[]>([]);
  const [isAdmin, setIsAdmin] = useState(false);
  
  // Check if user is admin
  useEffect(() => {
    async function checkAdmin() {
      try {
        const { user } = await getSafeUserClient();
        const isAdminUser = user?.email === "admin@codedungeon.es";
        setIsAdmin(isAdminUser);
      } catch (error) {
        console.error("Error checking admin:", error);
      }
    }
    checkAdmin();
  }, []);
  const [courseProgress, setCourseProgress] = useState<{[key: string]: number}>({});

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const completed: string[] = [];
      const progress: {[key: string]: number} = {};
      
      const courses = [
        { id: 'react-native-intro', lessons: 6 },
        { id: 'react-native-navigation', lessons: 6 },
        { id: 'react-native-api', lessons: 6 },
        { id: 'react-native-native', lessons: 6 },
        { id: 'react-native-publish', lessons: 6 },
        { id: 'mobile-master', lessons: 10 },
      ];
      
      courses.forEach(course => {
        let completedLessons = 0;
        for (let i = 1; i <= course.lessons; i++) {
          const key = `lesson_${course.id}_${i}`;
          if (localStorage.getItem(key) === 'completed') {
            completedLessons++;
          }
        }
        
        progress[course.id] = completedLessons;
        
        if (completedLessons === course.lessons) {
          completed.push(course.id);
        }
      });
      
      setCompletedCourses(completed);
      setCourseProgress(progress);
    }
  }, []);

  const mobileNodes = [
    {
      id: 'react-native-intro',
      title: 'React Native: Intro',
      description: 'Fundamentos de RN',
      icon: '📱',
      status: 'available' as const,
      xp: 400,
      lessons: 6,
      progress: 0,
      category: 'foundation' as const,
      position: { x: 75, y: 30 },
      prerequisites: [],
      color: 'from-cyan-500 to-stone-500',
      language: 'Mobile',
    },
    {
      id: 'react-native-navigation',
      title: 'RN: Navegación',
      description: 'React Navigation',
      icon: '🧭',
      status: 'locked' as const,
      xp: 450,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 80 },
      prerequisites: ['react-native-intro'],
      color: 'from-stone-500 to-stone-500',
      language: 'Mobile',
    },
    {
      id: 'react-native-api',
      title: 'RN: APIs',
      description: 'Conectar con backend',
      icon: '🔌',
      status: 'locked' as const,
      xp: 500,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 130 },
      prerequisites: ['react-native-navigation'],
      color: 'from-stone-500 to-stone-500',
      language: 'Mobile',
    },
    {
      id: 'react-native-native',
      title: 'RN: Módulos Nativos',
      description: 'Cámara, GPS, sensores',
      icon: '📸',
      status: 'locked' as const,
      xp: 600,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 180 },
      prerequisites: ['react-native-api'],
      color: 'from-stone-500 to-amber-500',
      language: 'Mobile',
    },
    {
      id: 'react-native-publish',
      title: 'RN: Publicación',
      description: 'Deploy a tiendas',
      icon: '🚀',
      status: 'locked' as const,
      xp: 650,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 230 },
      prerequisites: ['react-native-native'],
      color: 'from-amber-500 to-red-500',
      language: 'Mobile',
    },
    {
      id: 'mobile-master',
      title: 'Mobile Master',
      description: 'Apps profesionales',
      icon: '🏆',
      status: 'locked' as const,
      xp: 1000,
      lessons: 10,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 290 },
      prerequisites: ['react-native-publish'],
      color: 'from-violet-600 to-stone-600',
      language: 'Mobile',
    },
  ];

  return (
    <SkillTreeRoadmap
      title="📱 Roadmap de Mobile Development"
      description="Acerca el ratón a los bordes para navegar • Haz clic en un nodo para empezar"
      nodes={mobileNodes}
      completedCourses={completedCourses}
      courseProgress={courseProgress}
      language="Mobile"
      backUrl="/skill-tree"
      isAdmin={isAdmin}
    />
  );
}
