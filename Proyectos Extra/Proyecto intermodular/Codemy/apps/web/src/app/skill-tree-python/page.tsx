'use client';

import React, { useState, useEffect } from 'react';
import SkillTreeRoadmap from '@/components/SkillTreeRoadmap';
import { getSafeUserClient } from '@/lib/auth-helpers-client';

export default function PythonSkillTree() {
  const [completedCourses, setCompletedCourses] = useState<string[]>([]);
  const [courseProgress, setCourseProgress] = useState<{[key: string]: number}>({});
  const [isAdmin, setIsAdmin] = useState(false);

  // Check if user is admin
  useEffect(() => {
    async function checkAdmin() {
      try {
        const { user } = await getSafeUserClient();
        const isAdminUser = user?.email === 'admin@codedungeon.es';
        setIsAdmin(isAdminUser);
      } catch (error) {
        console.error('Error checking admin:', error);
      }
    }
    checkAdmin();
  }, []);

  // Cargar progreso desde localStorage
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const completed: string[] = [];
      const progress: {[key: string]: number} = {};
      
      const courses = [
        { id: 'py-intro', lessons: 4 },
        { id: 'py-variables', lessons: 5 },
        { id: 'py-control', lessons: 6 },
        { id: 'py-functions', lessons: 6 },
        { id: 'py-classes', lessons: 6 },
        { id: 'numpy', lessons: 6 },
        { id: 'pandas', lessons: 6 },
        { id: 'matplotlib', lessons: 6 },
        { id: 'scikit-learn', lessons: 6 },
        { id: 'pytorch', lessons: 6 },
        { id: 'tensorflow', lessons: 6 },
        { id: 'nlp', lessons: 6 },
        { id: 'computer-vision', lessons: 6 },
        { id: 'llm', lessons: 6 },
        { id: 'master-ai', lessons: 8 },
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

  const pythonNodes = [
    // Python Basics
    {
      id: 'py-intro',
      title: 'Python: Introducción',
      description: 'Primeros pasos en Python',
      icon: '🐍',
      status: 'available' as const,
      xp: 200,
      lessons: 4,
      progress: 0,
      category: 'foundation' as const,
      position: { x: 75, y: 30 },
      prerequisites: [],
      color: 'from-stone-500 to-cyan-500',
      language: 'Python',
    },
    {
      id: 'py-variables',
      title: 'Python: Variables',
      description: 'Tipos de datos y variables',
      icon: '📦',
      status: 'locked' as const,
      xp: 250,
      lessons: 5,
      progress: 0,
      category: 'foundation' as const,
      position: { x: 75, y: 60 },
      prerequisites: ['py-intro'],
      color: 'from-stone-500 to-cyan-500',
      language: 'Python',
    },
    {
      id: 'py-control',
      title: 'Python: Control',
      description: 'Estructuras de control',
      icon: '🔀',
      status: 'locked' as const,
      xp: 300,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 90 },
      prerequisites: ['py-variables'],
      color: 'from-stone-500 to-cyan-500',
      language: 'Python',
    },
    {
      id: 'py-functions',
      title: 'Python: Funciones',
      description: 'Funciones y modularidad',
      icon: '⚡',
      status: 'locked' as const,
      xp: 300,
      lessons: 6,
      progress: 0,
      category: 'intermediate' as const,
      position: { x: 75, y: 120 },
      prerequisites: ['py-control'],
      color: 'from-stone-500 to-cyan-500',
      language: 'Python',
    },
    {
      id: 'py-classes',
      title: 'Python: POO',
      description: 'Clases y objetos',
      icon: '🏗️',
      status: 'locked' as const,
      xp: 350,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 150 },
      prerequisites: ['py-functions'],
      color: 'from-stone-500 to-cyan-500',
      language: 'Python',
    },
    
    // Data Science
    {
      id: 'numpy',
      title: 'NumPy',
      description: 'Computación numérica',
      icon: '🔢',
      status: 'locked' as const,
      xp: 400,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 185 },
      prerequisites: ['py-classes'],
      color: 'from-stone-400 to-cyan-400',
      language: 'Python',
    },
    {
      id: 'pandas',
      title: 'Pandas',
      description: 'Análisis de datos',
      icon: '🐼',
      status: 'locked' as const,
      xp: 450,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 215 },
      prerequisites: ['numpy'],
      color: 'from-cyan-500 to-stone-500',
      language: 'Python',
    },
    {
      id: 'matplotlib',
      title: 'Matplotlib',
      description: 'Visualización de datos',
      icon: '📊',
      status: 'locked' as const,
      xp: 400,
      lessons: 6,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 245 },
      prerequisites: ['pandas'],
      color: 'from-orange-500 to-red-500',
      language: 'Python',
    },
    
    // Machine Learning
    {
      id: 'scikit-learn',
      title: 'Scikit-learn',
      description: 'Machine Learning',
      icon: '🤖',
      status: 'locked' as const,
      xp: 500,
      lessons: 8,
      progress: 0,
      category: 'advanced' as const,
      position: { x: 75, y: 280 },
      prerequisites: ['pandas', 'matplotlib'],
      color: 'from-orange-500 to-amber-500',
      language: 'AI',
    },
    {
      id: 'tensorflow',
      title: 'TensorFlow',
      description: 'Deep Learning',
      icon: '🧠',
      status: 'locked' as const,
      xp: 600,
      lessons: 10,
      progress: 0,
      category: 'expert' as const,
      position: { x: 55, y: 320 },
      prerequisites: ['scikit-learn'],
      color: 'from-orange-600 to-red-600',
      language: 'AI',
    },
    {
      id: 'pytorch',
      title: 'PyTorch',
      description: 'Deep Learning',
      icon: '🔥',
      status: 'locked' as const,
      xp: 600,
      lessons: 10,
      progress: 0,
      category: 'expert' as const,
      position: { x: 95, y: 320 },
      prerequisites: ['scikit-learn'],
      color: 'from-red-500 to-orange-500',
      language: 'AI',
    },
    
    // Advanced AI
    {
      id: 'computer-vision',
      title: 'Computer Vision',
      description: 'OpenCV, reconocimiento',
      icon: '👁️',
      status: 'locked' as const,
      xp: 650,
      lessons: 9,
      progress: 0,
      category: 'expert' as const,
      position: { x: 40, y: 360 },
      prerequisites: ['tensorflow', 'pytorch'],
      color: 'from-stone-500 to-amber-500',
      language: 'AI',
    },
    {
      id: 'nlp',
      title: 'NLP',
      description: 'Procesamiento de lenguaje',
      icon: '💬',
      status: 'locked' as const,
      xp: 650,
      lessons: 9,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 360 },
      prerequisites: ['tensorflow', 'pytorch'],
      color: 'from-stone-500 to-stone-500',
      language: 'AI',
    },
    {
      id: 'llm',
      title: 'LLMs & GPT',
      description: 'Large Language Models',
      icon: '🧠',
      status: 'locked' as const,
      xp: 800,
      lessons: 12,
      progress: 0,
      category: 'expert' as const,
      position: { x: 110, y: 360 },
      prerequisites: ['nlp', 'computer-vision'],
      color: 'from-violet-600 to-stone-600',
      language: 'AI',
    },
    {
      id: 'master-ai',
      title: 'AI Master',
      description: 'Dominio completo de IA',
      icon: '🏆',
      status: 'locked' as const,
      xp: 1000,
      lessons: 15,
      progress: 0,
      category: 'expert' as const,
      position: { x: 75, y: 400 },
      prerequisites: ['llm', 'computer-vision', 'nlp'],
      color: 'from-stone-700 to-amber-700',
      language: 'AI',
    },
  ];

  return (
    <SkillTreeRoadmap
      title="🐍 Roadmap de Python & IA"
      description="Acerca el ratón a los bordes para navegar • Haz clic en un nodo para empezar"
      nodes={pythonNodes}
      completedCourses={completedCourses}
      courseProgress={courseProgress}
      language="Python"
      backUrl="/skill-tree"
      isAdmin={isAdmin}
    />
  );
}
