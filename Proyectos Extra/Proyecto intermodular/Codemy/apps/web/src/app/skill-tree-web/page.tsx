'use client';

import React, { useState, useEffect } from 'react';
import SkillTreeRoadmap from '@/components/SkillTreeRoadmap';
import { getSafeUserClient } from '@/lib/auth-helpers-client';

export default function WebSkillTree() {
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
        { id: 'web-html', lessons: 6 },
        { id: 'web-css', lessons: 6 },
        { id: 'web-flexbox', lessons: 5 },
        { id: 'web-responsive', lessons: 6 },
        { id: 'js-intro', lessons: 6 },
        { id: 'js-dom', lessons: 6 },
        { id: 'js-async', lessons: 6 },
        { id: 'js-advanced', lessons: 6 },
        { id: 'typescript', lessons: 6 },
        { id: 'react', lessons: 8 },
        { id: 'nextjs', lessons: 8 },
        { id: 'master-fullstack', lessons: 10 },
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

  const webNodes = [
    // HTML & CSS
    {
      id: 'web-html',
      title: 'HTML5',
      description: 'Estructura web',
      icon: '📄',
      status: 'available' as const,
      xp: 250,
      lessons: 6,
      progress: 0,
      category: 'foundation' as const,
      position: { x: 75, y: 30 },
      prerequisites: [],
      color: 'from-stone-500 to-amber-500',
      language: 'Web',
    },
    {
      id: 'web-css',
      title: 'CSS3',
      description: 'Estilos y diseño',
      icon: '🎨',
      status: 'locked' as const,
      xp: 300,
      lessons: 6,
      progress: 0,
      category: 'foundation' as const,
      position: { x: 75, y: 65 },
      prerequisites: ['web-html'],
      color: 'from-stone-500 to-amber-500',
      language: 'Web',
    },
    {
      id: 'web-flexbox',
      title: 'Flexbox & Grid',
      description: 'Layout moderno',
      icon: '📐',
      status: 'locked' as const,
      xp: 200,
      lessons: 4,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 100 },
      prerequisites: ['web-css'],
      color: 'from-stone-500 to-amber-500',
      language: 'Web',
    },
    {
      id: 'web-responsive',
      title: 'Responsive Design',
      description: 'Diseño adaptativo',
      icon: '📱',
      status: 'locked' as const,
      xp: 300,
      lessons: 5,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 130 },
      prerequisites: ['web-flexbox'],
      color: 'from-stone-500 to-amber-500',
      language: 'Web',
    },
    
    // JavaScript
    {
      id: 'js-intro',
      title: 'JavaScript: Introducción',
      description: 'Fundamentos de JS',
      icon: '⚡',
      status: 'locked' as const,
      xp: 300,
      lessons: 6,
      progress: 0,
      category: 'foundation' as const,
      position: { x: 75, y: 165 },
      prerequisites: ['web-html'],
      color: 'from-yellow-500 to-orange-500',
      language: 'JavaScript',
    },
    {
      id: 'js-dom',
      title: 'JavaScript: DOM',
      description: 'Manipulación del DOM',
      icon: '🎨',
      status: 'locked' as const,
      xp: 350,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 195 },
      prerequisites: ['js-intro'],
      color: 'from-yellow-500 to-orange-500',
      language: 'JavaScript',
    },
    {
      id: 'js-async',
      title: 'JavaScript: Async',
      description: 'Promesas y async/await',
      icon: '⏱️',
      status: 'locked' as const,
      xp: 400,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 225 },
      prerequisites: ['js-dom'],
      color: 'from-yellow-500 to-orange-500',
      language: 'JavaScript',
    },
    {
      id: 'js-advanced',
      title: 'JavaScript: Avanzado',
      description: 'Closures, ES6+',
      icon: '🚀',
      status: 'locked' as const,
      xp: 450,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 255 },
      prerequisites: ['js-async'],
      color: 'from-yellow-500 to-orange-500',
      language: 'JavaScript',
    },
    
    // Modern Stack
    {
      id: 'typescript',
      title: 'TypeScript',
      description: 'JavaScript tipado',
      icon: '📘',
      status: 'locked' as const,
      xp: 450,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 290 },
      prerequisites: ['js-advanced'],
      color: 'from-stone-600 to-stone-800',
      language: 'JavaScript',
    },
    {
      id: 'react',
      title: 'React.js',
      description: 'Biblioteca UI moderna',
      icon: '⚛️',
      status: 'locked' as const,
      xp: 500,
      lessons: 8,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 325 },
      prerequisites: ['js-advanced', 'web-responsive'],
      color: 'from-cyan-500 to-stone-500',
      language: 'JavaScript',
    },
    {
      id: 'nextjs',
      title: 'Next.js',
      description: 'Framework React SSR',
      icon: '▲',
      status: 'locked' as const,
      xp: 500,
      lessons: 7,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 360 },
      prerequisites: ['react'],
      color: 'from-gray-800 to-gray-600',
      language: 'JavaScript',
    },
    
    // Backend
    {
      id: 'nodejs',
      title: 'Node.js',
      description: 'JavaScript en servidor',
      icon: '🟢',
      status: 'locked' as const,
      xp: 450,
      lessons: 7,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 50, y: 395 },
      prerequisites: ['typescript'],
      color: 'from-green-600 to-emerald-600',
      language: 'JavaScript',
    },
    {
      id: 'express',
      title: 'Express.js',
      description: 'Framework web Node',
      icon: '🚂',
      status: 'locked' as const,
      xp: 450,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 100, y: 395 },
      prerequisites: ['nodejs'],
      color: 'from-gray-700 to-gray-500',
      language: 'JavaScript',
    },
    {
      id: 'master-fullstack',
      title: 'Full Stack Master',
      description: 'Desarrollo completo',
      icon: '🏆',
      status: 'locked' as const,
      xp: 1000,
      lessons: 15,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 435 },
      prerequisites: ['nextjs', 'express'],
      color: 'from-yellow-700 to-orange-700',
      language: 'JavaScript',
    },
  ];

  return (
    <SkillTreeRoadmap
      title="🌐 Roadmap de Desarrollo Web"
      description="HTML, CSS, JavaScript, React y más • Haz clic para comenzar"
      nodes={webNodes}
      completedCourses={completedCourses}
      courseProgress={courseProgress}
      language="Web"
      backUrl="/skill-tree"
      isAdmin={isAdmin}
    />
  );
}
