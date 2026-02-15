'use client';

import React, { useState, useEffect } from 'react';
import SkillTreeRoadmap from '@/components/SkillTreeRoadmap';
import { getSafeUserClient } from '@/lib/auth-helpers-client';

export default function DevOpsSkillTree() {
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
        { id: 'git', lessons: 5 },
        { id: 'linux', lessons: 6 },
        { id: 'docker', lessons: 6 },
        { id: 'kubernetes', lessons: 8 },
        { id: 'cicd', lessons: 6 },
        { id: 'cloud-aws', lessons: 8 },
        { id: 'devops-master', lessons: 10 },
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

  const devopsNodes = [
    {
      id: 'git',
      title: 'Git & GitHub',
      description: 'Control de versiones',
      icon: '🌿',
      status: 'available' as const,
      xp: 350,
      lessons: 5,
      progress: 0,
      category: 'foundation' as const,
      position: { x: 75, y: 30 },
      prerequisites: [],
      color: 'from-orange-600 to-red-600',
      language: 'DevOps',
    },
    {
      id: 'linux',
      title: 'Linux & Terminal',
      description: 'Comandos y scripting',
      icon: '🐧',
      status: 'locked' as const,
      xp: 400,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 75 },
      prerequisites: ['git'],
      color: 'from-gray-600 to-slate-600',
      language: 'DevOps',
    },
    {
      id: 'docker',
      title: 'Docker',
      description: 'Contenedores',
      icon: '🐳',
      status: 'locked' as const,
      xp: 500,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 120 },
      prerequisites: ['linux'],
      color: 'from-stone-600 to-cyan-600',
      language: 'DevOps',
    },
    {
      id: 'kubernetes',
      title: 'Kubernetes',
      description: 'Orquestación de contenedores',
      icon: '☸️',
      status: 'locked' as const,
      xp: 700,
      lessons: 8,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 170 },
      prerequisites: ['docker'],
      color: 'from-stone-500 to-stone-600',
      language: 'DevOps',
    },
    {
      id: 'cicd',
      title: 'CI/CD',
      description: 'Integración y despliegue continuo',
      icon: '🔄',
      status: 'locked' as const,
      xp: 600,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 220 },
      prerequisites: ['kubernetes'],
      color: 'from-green-500 to-emerald-600',
      language: 'DevOps',
    },
    {
      id: 'cloud-aws',
      title: 'AWS Cloud',
      description: 'Amazon Web Services',
      icon: '☁️',
      status: 'locked' as const,
      xp: 800,
      lessons: 8,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 270 },
      prerequisites: ['cicd'],
      color: 'from-orange-500 to-yellow-500',
      language: 'DevOps',
    },
    {
      id: 'devops-master',
      title: 'DevOps Master',
      description: 'Arquitectura cloud completa',
      icon: '🏆',
      status: 'locked' as const,
      xp: 1000,
      lessons: 10,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 330 },
      prerequisites: ['cloud-aws'],
      color: 'from-stone-600 to-amber-600',
      language: 'DevOps',
    },
  ];

  return (
    <SkillTreeRoadmap
      title="🔄 Roadmap de DevOps & Cloud"
      description="Acerca el ratón a los bordes para navegar • Haz clic en un nodo para empezar"
      nodes={devopsNodes}
      completedCourses={completedCourses}
      courseProgress={courseProgress}
      language="DevOps"
      backUrl="/skill-tree"
      isAdmin={isAdmin}
    />
  );
}
