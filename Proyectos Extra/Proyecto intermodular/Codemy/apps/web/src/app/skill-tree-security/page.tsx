'use client';

import React, { useState, useEffect } from 'react';
import SkillTreeRoadmap from '@/components/SkillTreeRoadmap';
import { getSafeUserClient } from '@/lib/auth-helpers-client';

export default function SecuritySkillTree() {
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
        { id: 'security-basics', lessons: 6 },
        { id: 'network-security', lessons: 6 },
        { id: 'web-security', lessons: 6 },
        { id: 'penetration-testing', lessons: 8 },
        { id: 'cryptography', lessons: 6 },
        { id: 'security-master', lessons: 10 },
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

  const securityNodes = [
    {
      id: 'security-basics',
      title: 'Security: Fundamentos',
      description: 'Conceptos básicos de seguridad',
      icon: '🔒',
      status: 'available' as const,
      xp: 350,
      lessons: 6,
      progress: 0,
      category: 'foundation' as const,
      position: { x: 75, y: 30 },
      prerequisites: [],
      color: 'from-red-600 to-amber-600',
      language: 'Security',
    },
    {
      id: 'network-security',
      title: 'Network Security',
      description: 'Seguridad de redes',
      icon: '🌐',
      status: 'locked' as const,
      xp: 450,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 80 },
      prerequisites: ['security-basics'],
      color: 'from-red-500 to-orange-500',
      language: 'Security',
    },
    {
      id: 'web-security',
      title: 'Web Security',
      description: 'OWASP Top 10, XSS, CSRF',
      icon: '🛡️',
      status: 'locked' as const,
      xp: 500,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 130 },
      prerequisites: ['network-security'],
      color: 'from-orange-500 to-yellow-500',
      language: 'Security',
    },
    {
      id: 'penetration-testing',
      title: 'Penetration Testing',
      description: 'Hacking ético',
      icon: '🎯',
      status: 'locked' as const,
      xp: 700,
      lessons: 8,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 180 },
      prerequisites: ['web-security'],
      color: 'from-stone-600 to-amber-600',
      language: 'Security',
    },
    {
      id: 'cryptography',
      title: 'Criptografía',
      description: 'Encriptación y hash',
      icon: '🔐',
      status: 'locked' as const,
      xp: 600,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 240 },
      prerequisites: ['penetration-testing'],
      color: 'from-stone-600 to-stone-600',
      language: 'Security',
    },
    {
      id: 'security-master',
      title: 'Security Master',
      description: 'Experto en ciberseguridad',
      icon: '🏆',
      status: 'locked' as const,
      xp: 1000,
      lessons: 10,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 300 },
      prerequisites: ['cryptography'],
      color: 'from-red-700 to-amber-700',
      language: 'Security',
    },
  ];

  return (
    <SkillTreeRoadmap
      title="🔒 Roadmap de Security & Pentesting"
      description="Acerca el ratón a los bordes para navegar • Haz clic en un nodo para empezar"
      nodes={securityNodes}
      completedCourses={completedCourses}
      courseProgress={courseProgress}
      language="Security"
      backUrl="/skill-tree"
      isAdmin={isAdmin}
    />
  );
}
