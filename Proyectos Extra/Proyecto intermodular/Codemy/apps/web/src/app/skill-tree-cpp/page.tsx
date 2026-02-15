'use client';

import React, { useState, useEffect } from 'react';
import SkillTreeRoadmap from '@/components/SkillTreeRoadmap';
import { getSafeUserClient } from '@/lib/auth-helpers-client';

export default function CppSkillTree() {
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
        { id: 'cpp-intro', lessons: 6 },
        { id: 'cpp-oop', lessons: 6 },
        { id: 'cpp-stl', lessons: 6 },
        { id: 'cpp-memory', lessons: 6 },
        { id: 'cpp-advanced', lessons: 8 },
        { id: 'cpp-master', lessons: 10 },
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

  const cppNodes = [
    {
      id: 'cpp-intro',
      title: 'C++: Introducción',
      description: 'Fundamentos de C++',
      icon: '⚙️',
      status: 'available' as const,
      xp: 350,
      lessons: 6,
      progress: 0,
      category: 'foundation' as const,
      position: { x: 75, y: 30 },
      prerequisites: [],
      color: 'from-stone-500 to-stone-500',
      language: 'C++',
    },
    {
      id: 'cpp-oop',
      title: 'C++: POO',
      description: 'Clases y objetos',
      icon: '🏗️',
      status: 'locked' as const,
      xp: 400,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 80 },
      prerequisites: ['cpp-intro'],
      color: 'from-stone-500 to-stone-500',
      language: 'C++',
    },
    {
      id: 'cpp-stl',
      title: 'C++: STL',
      description: 'Vectores, Maps, Sets',
      icon: '📦',
      status: 'locked' as const,
      xp: 450,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 130 },
      prerequisites: ['cpp-oop'],
      color: 'from-stone-500 to-stone-500',
      language: 'C++',
    },
    {
      id: 'cpp-memory',
      title: 'C++: Memoria',
      description: 'Punteros y gestión',
      icon: '🧠',
      status: 'locked' as const,
      xp: 500,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 180 },
      prerequisites: ['cpp-stl'],
      color: 'from-stone-500 to-stone-500',
      language: 'C++',
    },
    {
      id: 'cpp-advanced',
      title: 'C++: Avanzado',
      description: 'Templates y Lambdas',
      icon: '🚀',
      status: 'locked' as const,
      xp: 600,
      lessons: 8,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 230 },
      prerequisites: ['cpp-memory'],
      color: 'from-stone-500 to-stone-500',
      language: 'C++',
    },
    {
      id: 'cpp-master',
      title: 'C++ Master',
      description: 'Sistemas de alto rendimiento',
      icon: '🏆',
      status: 'locked' as const,
      xp: 1000,
      lessons: 10,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 290 },
      prerequisites: ['cpp-advanced'],
      color: 'from-stone-600 to-stone-600',
      language: 'C++',
    },
  ];

  return (
    <SkillTreeRoadmap
      title="⚙️ Roadmap de C++ & Systems"
      description="Acerca el ratón a los bordes para navegar • Haz clic en un nodo para empezar"
      nodes={cppNodes}
      completedCourses={completedCourses}
      courseProgress={courseProgress}
      language="C++"
      backUrl="/skill-tree"
      isAdmin={isAdmin}
    />
  );
}
