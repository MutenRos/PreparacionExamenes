'use client';

import React, { useState, useEffect } from 'react';
import SkillTreeRoadmap from '@/components/SkillTreeRoadmap';
import { getSafeUserClient } from '@/lib/auth-helpers-client';

export default function JavaSkillTree() {
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

  // Cargar progreso desde localStorage
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const completed: string[] = [];
      const progress: {[key: string]: number} = {};
      
      const courses = [
        { id: 'java-intro', lessons: 5 },
        { id: 'java-oop', lessons: 6 },
        { id: 'java-collections', lessons: 6 },
        { id: 'java-streams', lessons: 6 },
        { id: 'java-spring', lessons: 8 },
        { id: 'java-master', lessons: 10 },
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

  const javaNodes = [
    {
      id: 'java-intro',
      title: 'Java: Introducción',
      description: 'Sintaxis básica y POO',
      icon: '☕',
      status: 'available' as const,
      xp: 300,
      lessons: 5,
      progress: 0,
      category: 'foundation' as const,
      position: { x: 75, y: 30 },
      prerequisites: [],
      color: 'from-orange-500 to-red-500',
      language: 'Java',
    },
    {
      id: 'java-oop',
      title: 'Java: POO',
      description: 'Herencia y Polimorfismo',
      icon: '🏗️',
      status: 'locked' as const,
      xp: 400,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 80 },
      prerequisites: ['java-intro'],
      color: 'from-orange-500 to-red-500',
      language: 'Java',
    },
    {
      id: 'java-collections',
      title: 'Java: Collections',
      description: 'ArrayList, HashMap, Sets',
      icon: '📦',
      status: 'locked' as const,
      xp: 450,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 130 },
      prerequisites: ['java-oop'],
      color: 'from-orange-500 to-red-500',
      language: 'Java',
    },
    {
      id: 'java-streams',
      title: 'Java: Streams',
      description: 'Programación funcional',
      icon: '🌊',
      status: 'locked' as const,
      xp: 500,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 180 },
      prerequisites: ['java-collections'],
      color: 'from-orange-500 to-red-500',
      language: 'Java',
    },
    {
      id: 'java-spring',
      title: 'Spring Boot',
      description: 'Framework backend',
      icon: '🍃',
      status: 'locked' as const,
      xp: 700,
      lessons: 8,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 230 },
      prerequisites: ['java-streams'],
      color: 'from-green-500 to-emerald-500',
      language: 'Java',
    },
    {
      id: 'java-master',
      title: 'Java Master',
      description: 'Microservicios y arquitectura',
      icon: '🏆',
      status: 'locked' as const,
      xp: 1000,
      lessons: 10,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 290 },
      prerequisites: ['java-spring'],
      color: 'from-yellow-600 to-orange-600',
      language: 'Java',
    },
  ];

  return (
    <SkillTreeRoadmap
      title="☕ Roadmap de Java & Backend"
      description="Acerca el ratón a los bordes para navegar • Haz clic en un nodo para empezar"
      nodes={javaNodes}
      completedCourses={completedCourses}
      courseProgress={courseProgress}
      language="Java"
      backUrl="/skill-tree"
      isAdmin={isAdmin}
    />
  );
}
