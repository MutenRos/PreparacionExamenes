'use client';

import { useEffect, useState } from 'react';
import SkillTreeRoadmap from '@/components/SkillTreeRoadmap';

interface SkillNode {
  id: string;
  title: string;
  description: string;
  icon: string;
  status: 'locked' | 'available' | 'completed';
  xp: number;
  lessons: number;
  progress: number;
  category: 'foundation' | 'intermediate' | 'advanced' | 'expert';
  position: { x: number; y: number };
  prerequisites: string[];
  color: string;
  language: string;
}

export default function SkillTree3DPage() {
  const [completedCourses, setCompletedCourses] = useState<string[]>([]);
  const [courseProgress, setCourseProgress] = useState<{ [key: string]: number }>({});

  useEffect(() => {
    const saved = localStorage.getItem('completedSkills-3d');
    if (saved) {
      setCompletedCourses(JSON.parse(saved));
    }
  }, []);

  const skills: SkillNode[] = [
    // NIVEL FOUNDATION
    {
      id: '3d-intro',
      title: 'Introducción al 3D',
      description: 'Conceptos básicos: vértices, aristas, caras, mallas',
      icon: '📐',
      status: 'available',
      xp: 50,
      lessons: 5,
      progress: 0,
      category: 'foundation',
      position: { x: 50, y: 10 },
      prerequisites: [],
      color: '#6366f1',
      language: 'es',
    },
    {
      id: 'tinkercad',
      title: 'Tinkercad',
      description: 'Primeros modelos 3D sin experiencia previa',
      icon: '🧊',
      status: 'locked',
      xp: 60,
      lessons: 6,
      progress: 0,
      category: 'foundation',
      position: { x: 50, y: 25 },
      prerequisites: ['3d-intro'],
      color: '#8b5cf6',
      language: 'es',
    },
    // NIVEL INTERMEDIATE
    {
      id: 'blender-basics',
      title: 'Blender Básico',
      description: 'Interfaz, herramientas de modelado y edición',
      icon: '🔶',
      status: 'locked',
      xp: 100,
      lessons: 10,
      progress: 0,
      category: 'intermediate',
      position: { x: 30, y: 40 },
      prerequisites: ['tinkercad'],
      color: '#f97316',
      language: 'es',
    },
    {
      id: 'fusion360-basics',
      title: 'Fusion 360 Básico',
      description: 'CAD paramétrico para diseño mecánico',
      icon: '⚙️',
      status: 'locked',
      xp: 100,
      lessons: 10,
      progress: 0,
      category: 'intermediate',
      position: { x: 70, y: 40 },
      prerequisites: ['tinkercad'],
      color: '#0ea5e9',
      language: 'es',
    },
    // NIVEL ADVANCED
    {
      id: 'sculpting',
      title: 'Esculpido Digital',
      description: 'Sculpt mode en Blender, brushes básicos',
      icon: '🎨',
      status: 'locked',
      xp: 120,
      lessons: 8,
      progress: 0,
      category: 'advanced',
      position: { x: 20, y: 60 },
      prerequisites: ['blender-basics'],
      color: '#ec4899',
      language: 'es',
    },
    {
      id: 'materials-shaders',
      title: 'Materiales y Shaders',
      description: 'Crear materiales PBR realistas',
      icon: '✨',
      status: 'locked',
      xp: 130,
      lessons: 9,
      progress: 0,
      category: 'advanced',
      position: { x: 40, y: 60 },
      prerequisites: ['blender-basics'],
      color: '#a855f7',
      language: 'es',
    },
    {
      id: 'rendering',
      title: 'Rendering Avanzado',
      description: 'Cycles, iluminación, compositing',
      icon: '📷',
      status: 'locked',
      xp: 140,
      lessons: 10,
      progress: 0,
      category: 'advanced',
      position: { x: 50, y: 75 },
      prerequisites: ['materials-shaders'],
      color: '#14b8a6',
      language: 'es',
    },
    // NIVEL EXPERT
    {
      id: 'geometry-nodes',
      title: 'Geometry Nodes',
      description: 'Modelado procedural en Blender',
      icon: '🔗',
      status: 'locked',
      xp: 200,
      lessons: 12,
      progress: 0,
      category: 'expert',
      position: { x: 30, y: 90 },
      prerequisites: ['rendering'],
      color: '#f59e0b',
      language: 'es',
    },
    {
      id: '3d-printing-prep',
      title: 'Impresión 3D',
      description: 'Optimización de mallas, soportes, slicing',
      icon: '🖨️',
      status: 'locked',
      xp: 180,
      lessons: 8,
      progress: 0,
      category: 'expert',
      position: { x: 70, y: 90 },
      prerequisites: ['fusion360-basics'],
      color: '#22c55e',
      language: 'es',
    },
  ];

  return (
    <SkillTreeRoadmap
      title="Diseño y Modelado 3D"
      description="Desde CAD técnico hasta arte digital. Aprende Fusion 360, Blender y prepara modelos para impresión 3D."
      nodes={skills}
      completedCourses={completedCourses}
      courseProgress={courseProgress}
      language="es"
      backUrl="/skill-tree"
    />
  );
}
