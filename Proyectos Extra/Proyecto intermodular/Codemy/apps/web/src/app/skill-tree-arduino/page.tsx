'use client';

import React, { useState, useEffect } from 'react';
import SkillTreeRoadmap from '@/components/SkillTreeRoadmap';
import { getSafeUserClient } from '@/lib/auth-helpers-client';

export default function ArduinoSkillTree() {
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
        { id: 'arduino-intro', lessons: 6 },
        { id: 'arduino-sensors', lessons: 6 },
        { id: 'arduino-actuators', lessons: 6 },
        { id: 'arduino-wifi', lessons: 6 },
        { id: 'arduino-iot', lessons: 8 },
        { id: 'arduino-master', lessons: 10 },
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

  const arduinoNodes = [
    {
      id: 'arduino-intro',
      title: 'Arduino: Introducción',
      description: 'Programación de hardware',
      icon: '🔌',
      status: 'available' as const,
      xp: 350,
      lessons: 6,
      progress: 0,
      category: 'foundation' as const,
      position: { x: 75, y: 30 },
      prerequisites: [],
      color: 'from-teal-500 to-cyan-500',
      language: 'Arduino',
    },
    {
      id: 'arduino-sensors',
      title: 'Arduino: Sensores',
      description: 'Temperatura, luz, movimiento',
      icon: '📡',
      status: 'locked' as const,
      xp: 400,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 80 },
      prerequisites: ['arduino-intro'],
      color: 'from-teal-500 to-cyan-500',
      language: 'Arduino',
    },
    {
      id: 'arduino-actuators',
      title: 'Arduino: Actuadores',
      description: 'Motores, servos, relés',
      icon: '⚡',
      status: 'locked' as const,
      xp: 450,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 130 },
      prerequisites: ['arduino-sensors'],
      color: 'from-teal-500 to-cyan-500',
      language: 'Arduino',
    },
    {
      id: 'arduino-wifi',
      title: 'Arduino: WiFi',
      description: 'Conectividad inalámbrica',
      icon: '📶',
      status: 'locked' as const,
      xp: 500,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 180 },
      prerequisites: ['arduino-actuators'],
      color: 'from-teal-500 to-cyan-500',
      language: 'Arduino',
    },
    {
      id: 'arduino-iot',
      title: 'Arduino: IoT',
      description: 'Internet de las cosas',
      icon: '🌐',
      status: 'locked' as const,
      xp: 600,
      lessons: 8,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 230 },
      prerequisites: ['arduino-wifi'],
      color: 'from-cyan-500 to-stone-500',
      language: 'Arduino',
    },
    {
      id: 'arduino-master',
      title: 'Arduino Master',
      description: 'Proyectos IoT completos',
      icon: '🏆',
      status: 'locked' as const,
      xp: 1000,
      lessons: 10,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 290 },
      prerequisites: ['arduino-iot'],
      color: 'from-teal-600 to-cyan-600',
      language: 'Arduino',
    },
  ];

  return (
    <SkillTreeRoadmap
      title="🔌 Roadmap de Arduino & IoT"
      description="Acerca el ratón a los bordes para navegar • Haz clic en un nodo para empezar"
      nodes={arduinoNodes}
      completedCourses={completedCourses}
      courseProgress={courseProgress}
      language="Arduino"
      backUrl="/skill-tree"
      isAdmin={isAdmin}
    />
  );
}
