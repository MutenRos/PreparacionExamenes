'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Lock, CheckCircle, Circle, Star, Trophy, ArrowRight, BookOpen, X, Play } from 'lucide-react';

interface Lesson {
  id: string;
  title: string;
  duration: string;
  status: 'locked' | 'available' | 'completed';
}

interface SkillNode {
  id: string;
  title: string;
  description: string;
  icon: string;
  status: 'locked' | 'available' | 'in-progress' | 'completed';
  xp: number;
  lessons: Lesson[];
  progress?: number;
  prerequisites: string[];
  category: 'foundation' | 'intermediate' | 'advanced' | 'expert';
  position: { x: number; y: number };
}

export default function SkillTreePage() {
  const [selectedPath, setSelectedPath] = useState<'python' | 'javascript' | 'web'>('python');
  const [selectedNode, setSelectedNode] = useState<SkillNode | null>(null);
  const [courseProgress, setCourseProgress] = useState<{[key: string]: number}>({});

  // Cargar progreso desde localStorage
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const progress: {[key: string]: number} = {};
      
      // Cursos y sus lecciones
      const courses = [
        { id: 'py-intro', lessons: 4 },
        { id: 'py-variables', lessons: 5 },
        { id: 'py-control', lessons: 6 },
        { id: 'py-functions', lessons: 6 },
        { id: 'py-classes', lessons: 6 },
        { id: 'py-files', lessons: 6 },
        { id: 'py-lists', lessons: 6 },
        { id: 'py-dicts', lessons: 6 },
        { id: 'py-modules', lessons: 5 },
        { id: 'py-web', lessons: 6 },
        { id: 'sql-intro', lessons: 6 },
        { id: 'js-intro', lessons: 5 },
        { id: 'js-dom', lessons: 6 },
        { id: 'js-async', lessons: 6 },
        { id: 'web-html', lessons: 5 },
        { id: 'web-css', lessons: 6 },
        { id: 'cpp-intro', lessons: 6 },
        { id: 'cpp-oop', lessons: 6 },
        { id: 'cpp-stl', lessons: 6 },
        { id: 'cpp-memory', lessons: 6 },
        { id: 'cpp-advanced', lessons: 6 },
        { id: 'java-intro', lessons: 6 },
        { id: 'java-oop', lessons: 6 },
        { id: 'java-collections', lessons: 6 },
      ];
      
      courses.forEach(course => {
        let completedLessons = 0;
        for (let i = 1; i <= course.lessons; i++) {
          const key = `lesson_${course.id}_${i}`;
          if (localStorage.getItem(key) === 'completed') {
            completedLessons++;
          }
        }
        progress[course.id] = Math.round((completedLessons / course.lessons) * 100);
      });
      
      setCourseProgress(progress);
      console.log('Course progress loaded:', progress);
    }
  }, []);

  const skillTrees = {
    python: [
      {
        id: 'py-intro',
        title: 'Introducción a Python',
        description: 'Primeros pasos con Python',
        icon: '🐍',
        status: (courseProgress['py-intro'] === 100 ? 'completed' : courseProgress['py-intro'] > 0 ? 'in-progress' : 'available'),
        xp: 200,
        lessons: [
          { id: '1', title: '¿Qué es Python?', duration: '5 min', status: 'available' as const },
          { id: '2', title: 'Instalación', duration: '10 min', status: 'locked' as const },
          { id: '3', title: 'Primer programa', duration: '8 min', status: 'locked' as const },
          { id: '4', title: 'print() básico', duration: '7 min', status: 'locked' as const },
        ],
        progress: courseProgress['py-intro'] || 0,
        prerequisites: [],
        category: 'foundation' as const,
        position: { x: 50, y: 8 },
      },
      {
        id: 'py-variables',
        title: 'Variables y Tipos',
        description: 'Aprende sobre datos',
        icon: '📦',
        status: (courseProgress['py-variables'] === 100 ? 'completed' : courseProgress['py-variables'] > 0 ? 'in-progress' : courseProgress['py-intro'] === 100 ? 'available' : 'locked'),
        xp: 250,
        lessons: [
          { id: '1', title: 'Qué es una variable', duration: '6 min', status: 'locked' as const },
          { id: '2', title: 'Números enteros', duration: '8 min', status: 'locked' as const },
          { id: '3', title: 'Números decimales', duration: '8 min', status: 'locked' as const },
          { id: '4', title: 'Cadenas de texto', duration: '10 min', status: 'locked' as const },
          { id: '5', title: 'Booleanos', duration: '7 min', status: 'locked' as const },
        ],
        progress: courseProgress['py-variables'] || 0,
        prerequisites: ['py-intro'],
        category: 'foundation' as const,
        position: { x: 50, y: 22 },
      },
      {
        id: 'py-control',
        title: 'Control de Flujo',
        description: 'If, while, for',
        icon: '🔀',
        status: (courseProgress['py-control'] === 100 ? 'completed' : courseProgress['py-control'] > 0 ? 'in-progress' : courseProgress['py-variables'] === 100 ? 'available' : 'locked'),
        xp: 300,
        lessons: [
          { id: '1', title: 'Condicionales if', duration: '10 min', status: 'available' as const },
          { id: '2', title: 'if-else', duration: '8 min', status: 'locked' as const },
          { id: '3', title: 'elif múltiple', duration: '12 min', status: 'locked' as const },
          { id: '4', title: 'Bucle while', duration: '10 min', status: 'locked' as const },
          { id: '5', title: 'Bucle for', duration: '10 min', status: 'locked' as const },
          { id: '6', title: 'break y continue', duration: '8 min', status: 'locked' as const },
        ],
        progress: courseProgress['py-control'] || 0,
        prerequisites: ['py-variables'],
        category: 'foundation' as const,
        position: { x: 50, y: 36 },
      },
      {
        id: 'py-functions',
        title: 'Funciones',
        description: 'Define tus propias funciones',
        icon: '⚙️',
        status: 'locked' as const,
        xp: 350,
        lessons: [
          { id: '1', title: 'Qué es una función', duration: '8 min', status: 'locked' as const },
          { id: '2', title: 'Parámetros', duration: '10 min', status: 'locked' as const },
          { id: '3', title: 'return', duration: '10 min', status: 'locked' as const },
          { id: '4', title: 'Scope de variables', duration: '12 min', status: 'locked' as const },
        ],
        prerequisites: ['py-control'],
        category: 'intermediate' as const,
        position: { x: 30, y: 50 },
      },
      {
        id: 'py-files',
        title: 'Archivos',
        description: 'Lectura y escritura',
        icon: '📂',
        status: 'locked' as const,
        xp: 300,
        lessons: [
          { id: '1', title: 'Abrir archivos', duration: '8 min', status: 'locked' as const },
          { id: '2', title: 'Leer archivos', duration: '10 min', status: 'locked' as const },
          { id: '3', title: 'Escribir archivos', duration: '10 min', status: 'locked' as const },
          { id: '4', title: 'with statement', duration: '8 min', status: 'locked' as const },
        ],
        prerequisites: ['py-control'],
        category: 'intermediate' as const,
        position: { x: 70, y: 50 },
      },
      {
        id: 'py-classes',
        title: 'Clases y Objetos',
        description: 'Programación Orientada a Objetos',
        icon: '🏗️',
        status: 'locked' as const,
        xp: 350,
        lessons: [
          { id: '1', title: 'Qué son las clases', duration: '10 min', status: 'locked' as const },
          { id: '2', title: 'Crear objetos', duration: '10 min', status: 'locked' as const },
          { id: '3', title: 'Atributos', duration: '12 min', status: 'locked' as const },
          { id: '4', title: 'Métodos', duration: '12 min', status: 'locked' as const },
          { id: '5', title: 'Constructor __init__', duration: '12 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Sistema de notas', duration: '20 min', status: 'locked' as const },
        ],
        prerequisites: ['py-functions'],
        category: 'intermediate' as const,
        position: { x: 20, y: 80 },
      },
      {
        id: 'py-files',
        title: 'Archivos',
        description: 'Leer y escribir archivos',
        icon: '📁',
        status: 'locked' as const,
        xp: 350,
        lessons: [
          { id: '1', title: 'Abrir archivos', duration: '10 min', status: 'locked' as const },
          { id: '2', title: 'Leer archivos', duration: '10 min', status: 'locked' as const },
          { id: '3', title: 'Escribir archivos', duration: '12 min', status: 'locked' as const },
          { id: '4', title: 'with statement', duration: '10 min', status: 'locked' as const },
          { id: '5', title: 'Manejo de errores', duration: '12 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Gestor de notas', duration: '20 min', status: 'locked' as const },
        ],
        prerequisites: ['py-lists'],
        category: 'intermediate' as const,
        position: { x: 80, y: 80 },
      },
      {
        id: 'py-dicts',
        title: 'Diccionarios',
        description: 'Pares clave-valor',
        icon: '📚',
        status: 'locked' as const,
        xp: 350,
        lessons: [
          { id: '1', title: 'Qué es un diccionario', duration: '8 min', status: 'locked' as const },
          { id: '2', title: 'Acceder y modificar', duration: '10 min', status: 'locked' as const },
          { id: '3', title: 'Métodos útiles', duration: '12 min', status: 'locked' as const },
          { id: '4', title: 'Iterar diccionarios', duration: '10 min', status: 'locked' as const },
          { id: '5', title: 'Diccionarios anidados', duration: '12 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Agenda contactos', duration: '18 min', status: 'locked' as const },
        ],
        prerequisites: ['py-lists'],
        category: 'intermediate' as const,
        position: { x: 50, y: 98 },
      },
      {
        id: 'py-modules',
        title: 'Módulos',
        description: 'Importar y reutilizar código',
        icon: '📦',
        status: 'locked' as const,
        xp: 300,
        lessons: [
          { id: '1', title: 'Importar módulos', duration: '10 min', status: 'locked' as const },
          { id: '2', title: 'Módulo random', duration: '12 min', status: 'locked' as const },
          { id: '3', title: 'Módulo datetime', duration: '12 min', status: 'locked' as const },
          { id: '4', title: 'Crear tus módulos', duration: '10 min', status: 'locked' as const },
          { id: '5', title: 'Proyecto: Juego dados', duration: '20 min', status: 'locked' as const },
        ],
        prerequisites: ['py-functions', 'py-dicts'],
        category: 'advanced' as const,
        position: { x: 20, y: 116 },
      },
      {
        id: 'py-web',
        title: 'Python Web',
        description: 'APIs y web scraping',
        icon: '🌐',
        status: 'locked' as const,
        xp: 400,
        lessons: [
          { id: '1', title: 'Requests básicos', duration: '10 min', status: 'locked' as const },
          { id: '2', title: 'Trabajar con JSON', duration: '12 min', status: 'locked' as const },
          { id: '3', title: 'APIs públicas', duration: '12 min', status: 'locked' as const },
          { id: '4', title: 'Web scraping básico', duration: '15 min', status: 'locked' as const },
          { id: '5', title: 'Manejo de errores', duration: '10 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: App clima', duration: '20 min', status: 'locked' as const },
        ],
        prerequisites: ['py-modules', 'py-dicts'],
        category: 'advanced' as const,
        position: { x: 80, y: 116 },
      },
      {
        id: 'sql-intro',
        title: 'Introducción a SQL',
        description: 'Bases de datos relacionales',
        icon: '🗄️',
        status: (courseProgress['sql-intro'] === 100 ? 'completed' : courseProgress['sql-intro'] > 0 ? 'in-progress' : courseProgress['py-control'] === 100 ? 'available' : 'locked'),
        xp: 300,
        lessons: [
          { id: '1', title: '¿Qué es SQL?', duration: '8 min', status: 'locked' as const },
          { id: '2', title: 'Bases de datos relacionales', duration: '10 min', status: 'locked' as const },
          { id: '3', title: 'SELECT básico', duration: '12 min', status: 'locked' as const },
          { id: '4', title: 'WHERE y filtros', duration: '15 min', status: 'locked' as const },
          { id: '5', title: 'ORDER BY y LIMIT', duration: '10 min', status: 'locked' as const },
          { id: '6', title: 'Operadores lógicos', duration: '10 min', status: 'locked' as const },
        ],
        progress: courseProgress['sql-intro'] || 0,
        prerequisites: ['py-control'],
        category: 'intermediate' as const,
        position: { x: 50, y: 92 },
      },
    ],
    
    javascript: [
      {
        id: 'js-intro',
        title: 'JavaScript Básico',
        description: 'Fundamentos de JS',
        icon: '⚡',
        status: 'available' as const,
        xp: 300,
        lessons: [
          { id: '1', title: 'Variables let y const', duration: '8 min', status: 'available' as const },
          { id: '2', title: 'Tipos de datos', duration: '10 min', status: 'locked' as const },
          { id: '3', title: 'Operadores', duration: '10 min', status: 'locked' as const },
          { id: '4', title: 'Funciones', duration: '12 min', status: 'locked' as const },
          { id: '5', title: 'Proyecto: Calculadora', duration: '20 min', status: 'locked' as const },
        ],
        prerequisites: [],
        category: 'foundation' as const,
        position: { x: 50, y: 8 },
      },
      {
        id: 'js-dom',
        title: 'DOM',
        description: 'Manipula el HTML',
        icon: '🎨',
        status: 'locked' as const,
        xp: 350,
        lessons: [
          { id: '1', title: 'Seleccionar elementos', duration: '10 min', status: 'locked' as const },
          { id: '2', title: 'Modificar contenido', duration: '10 min', status: 'locked' as const },
          { id: '3', title: 'Eventos', duration: '15 min', status: 'locked' as const },
          { id: '4', title: 'Crear elementos', duration: '12 min', status: 'locked' as const },
          { id: '5', title: 'Clases y estilos', duration: '10 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Lista tareas', duration: '20 min', status: 'locked' as const },
        ],
        prerequisites: ['js-intro'],
        category: 'intermediate' as const,
        position: { x: 50, y: 35 },
      },
      {
        id: 'js-async',
        title: 'JavaScript Async',
        description: 'Promesas y APIs',
        icon: '⏳',
        status: 'locked' as const,
        xp: 400,
        lessons: [
          { id: '1', title: 'Callbacks', duration: '10 min', status: 'locked' as const },
          { id: '2', title: 'Promesas', duration: '12 min', status: 'locked' as const },
          { id: '3', title: 'Async/Await', duration: '12 min', status: 'locked' as const },
          { id: '4', title: 'Fetch API', duration: '15 min', status: 'locked' as const },
          { id: '5', title: 'LocalStorage', duration: '10 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: App Clima', duration: '20 min', status: 'locked' as const },
        ],
        prerequisites: ['js-dom'],
        category: 'advanced' as const,
        position: { x: 50, y: 52 },
      },
      {
        id: 'js-react',
        title: 'React',
        description: 'Librería UI moderna',
        icon: '⚛️',
        status: 'locked' as const,
        xp: 600,
        lessons: [
          { id: '1', title: 'Componentes', duration: '15 min', status: 'locked' as const },
          { id: '2', title: 'Props', duration: '12 min', status: 'locked' as const },
          { id: '3', title: 'State', duration: '15 min', status: 'locked' as const },
          { id: '4', title: 'Hooks', duration: '20 min', status: 'locked' as const },
        ],
        prerequisites: ['js-async'],
        category: 'expert' as const,
        position: { x: 50, y: 70 },
      },
    ],
    
    web: [
      {
        id: 'web-html',
        title: 'HTML5',
        description: 'Estructura web',
        icon: '📄',
        status: 'available' as const,
        xp: 300,
        lessons: [
          { id: '1', title: 'Etiquetas básicas', duration: '8 min', status: 'available' as const },
          { id: '2', title: 'Enlaces', duration: '6 min', status: 'locked' as const },
          { id: '3', title: 'Imágenes', duration: '8 min', status: 'locked' as const },
          { id: '4', title: 'Listas', duration: '6 min', status: 'locked' as const },
          { id: '5', title: 'Proyecto: Mi página web', duration: '15 min', status: 'locked' as const },
        ],
        prerequisites: [],
        category: 'foundation' as const,
        position: { x: 25, y: 8 },
      },
      {
        id: 'web-css',
        title: 'CSS3',
        description: 'Diseño y estilos',
        icon: '🎨',
        status: 'locked' as const,
        xp: 350,
        lessons: [
          { id: '1', title: 'Selectores', duration: '10 min', status: 'locked' as const },
          { id: '2', title: 'Colores', duration: '8 min', status: 'locked' as const },
          { id: '3', title: 'Texto', duration: '10 min', status: 'locked' as const },
          { id: '4', title: 'Box model', duration: '12 min', status: 'locked' as const },
          { id: '5', title: 'Flexbox', duration: '12 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Perfil online', duration: '20 min', status: 'locked' as const },
        ],
        prerequisites: ['web-html'],
        category: 'foundation' as const,
        position: { x: 50, y: 22 },
      },
      {
        id: 'web-flexbox',
        title: 'Flexbox',
        description: 'Layout flexible',
        icon: '📐',
        status: 'locked' as const,
        xp: 200,
        lessons: [
          { id: '1', title: 'display: flex', duration: '10 min', status: 'locked' as const },
          { id: '2', title: 'flex-direction', duration: '8 min', status: 'locked' as const },
          { id: '3', title: 'justify-content', duration: '10 min', status: 'locked' as const },
          { id: '4', title: 'align-items', duration: '10 min', status: 'locked' as const },
        ],
        prerequisites: ['web-html', 'web-css'],
        category: 'intermediate' as const,
        position: { x: 50, y: 36 },
      },
    ],
    
    cpp: [
      {
        id: 'cpp-intro',
        title: 'C++ Básico',
        description: 'Fundamentos de C++',
        icon: '⚙️',
        status: 'available' as const,
        xp: 350,
        lessons: [
          { id: '1', title: 'Hola C++', duration: '8 min', status: 'available' as const },
          { id: '2', title: 'Variables y Tipos', duration: '10 min', status: 'locked' as const },
          { id: '3', title: 'Entrada de Datos', duration: '10 min', status: 'locked' as const },
          { id: '4', title: 'Operadores', duration: '10 min', status: 'locked' as const },
          { id: '5', title: 'Control de Flujo', duration: '12 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Calculadora', duration: '20 min', status: 'locked' as const },
        ],
        prerequisites: [],
        category: 'foundation' as const,
        position: { x: 50, y: 8 },
      },
      {
        id: 'cpp-oop',
        title: 'POO en C++',
        description: 'Clases y objetos',
        icon: '🏗️',
        status: 'locked' as const,
        xp: 400,
        lessons: [
          { id: '1', title: 'Clases en C++', duration: '12 min', status: 'locked' as const },
          { id: '2', title: 'Constructores', duration: '12 min', status: 'locked' as const },
          { id: '3', title: 'Encapsulamiento', duration: '12 min', status: 'locked' as const },
          { id: '4', title: 'Herencia', duration: '15 min', status: 'locked' as const },
          { id: '5', title: 'Polimorfismo', duration: '15 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Sistema RPG', duration: '25 min', status: 'locked' as const },
        ],
        prerequisites: ['cpp-intro'],
        category: 'intermediate' as const,
        position: { x: 50, y: 22 },
      },
      {
        id: 'cpp-stl',
        title: 'STL y Contenedores',
        description: 'Vectores, Maps, Sets',
        icon: '📦',
        status: 'locked' as const,
        xp: 450,
        lessons: [
          { id: '1', title: 'Vectores', duration: '12 min', status: 'locked' as const },
          { id: '2', title: 'Métodos de Vector', duration: '12 min', status: 'locked' as const },
          { id: '3', title: 'Maps', duration: '12 min', status: 'locked' as const },
          { id: '4', title: 'Sets', duration: '12 min', status: 'locked' as const },
          { id: '5', title: 'Stack y Queue', duration: '12 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Gestor Tareas', duration: '25 min', status: 'locked' as const },
        ],
        prerequisites: ['cpp-oop'],
        category: 'advanced' as const,
        position: { x: 30, y: 42 },
      },
      {
        id: 'cpp-memory',
        title: 'Punteros y Memoria',
        description: 'Gestión de memoria',
        icon: '🧠',
        status: 'locked' as const,
        xp: 500,
        lessons: [
          { id: '1', title: 'Punteros Básicos', duration: '12 min', status: 'locked' as const },
          { id: '2', title: 'Memoria Dinámica', duration: '15 min', status: 'locked' as const },
          { id: '3', title: 'Referencias', duration: '12 min', status: 'locked' as const },
          { id: '4', title: 'Smart Pointers', duration: '15 min', status: 'locked' as const },
          { id: '5', title: 'RAII', duration: '15 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Pool Memoria', duration: '30 min', status: 'locked' as const },
        ],
        prerequisites: ['cpp-oop'],
        category: 'advanced' as const,
        position: { x: 70, y: 42 },
      },
      {
        id: 'cpp-advanced',
        title: 'C++ Avanzado',
        description: 'Templates, Lambdas',
        icon: '🚀',
        status: 'locked' as const,
        xp: 550,
        lessons: [
          { id: '1', title: 'Templates', duration: '15 min', status: 'locked' as const },
          { id: '2', title: 'Lambda Functions', duration: '12 min', status: 'locked' as const },
          { id: '3', title: 'Move Semantics', duration: '18 min', status: 'locked' as const },
          { id: '4', title: 'Excepciones', duration: '15 min', status: 'locked' as const },
          { id: '5', title: 'C++11/14/17', duration: '15 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Sistema Eventos', duration: '30 min', status: 'locked' as const },
        ],
        prerequisites: ['cpp-stl', 'cpp-memory'],
        category: 'expert' as const,
        position: { x: 50, y: 62 },
      },
    ],
    
    java: [
      {
        id: 'java-intro',
        title: 'Introducción Java',
        description: 'Fundamentos',
        icon: '☕',
        status: 'available' as const,
        xp: 350,
        lessons: [
          { id: '1', title: 'Hello World', duration: '10 min', status: 'available' as const },
          { id: '2', title: 'Variables y Tipos', duration: '12 min', status: 'locked' as const },
          { id: '3', title: 'Operadores', duration: '10 min', status: 'locked' as const },
          { id: '4', title: 'Control de Flujo', duration: '12 min', status: 'locked' as const },
          { id: '5', title: 'Bucles', duration: '12 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Juego Adivinanza', duration: '20 min', status: 'locked' as const },
        ],
        prerequisites: [],
        category: 'foundation' as const,
        position: { x: 50, y: 8 },
      },
      {
        id: 'java-oop',
        title: 'POO en Java',
        description: 'Herencia, Polimorfismo',
        icon: '🏗️',
        status: 'locked' as const,
        xp: 450,
        lessons: [
          { id: '1', title: 'Clases y Objetos', duration: '15 min', status: 'locked' as const },
          { id: '2', title: 'Encapsulación', duration: '12 min', status: 'locked' as const },
          { id: '3', title: 'Herencia', duration: '15 min', status: 'locked' as const },
          { id: '4', title: 'Polimorfismo', duration: '18 min', status: 'locked' as const },
          { id: '5', title: 'Interfaces', duration: '15 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Sistema Biblioteca', duration: '30 min', status: 'locked' as const },
        ],
        prerequisites: ['java-intro'],
        category: 'intermediate' as const,
        position: { x: 50, y: 35 },
      },
      {
        id: 'java-collections',
        title: 'Collections',
        description: 'ArrayList, HashMap, Streams',
        icon: '📚',
        status: 'locked' as const,
        xp: 500,
        lessons: [
          { id: '1', title: 'ArrayList', duration: '12 min', status: 'locked' as const },
          { id: '2', title: 'HashMap', duration: '12 min', status: 'locked' as const },
          { id: '3', title: 'HashSet', duration: '10 min', status: 'locked' as const },
          { id: '4', title: 'LinkedList', duration: '12 min', status: 'locked' as const },
          { id: '5', title: 'Streams API', duration: '15 min', status: 'locked' as const },
          { id: '6', title: 'Proyecto: Gestor Estudiantes', duration: '25 min', status: 'locked' as const },
        ],
        prerequisites: ['java-oop'],
        category: 'advanced' as const,
        position: { x: 50, y: 42 },
      },
    ],
  };

  const currentTree = skillTrees[selectedPath];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500 border-green-600';
      case 'in-progress':
        return 'bg-amber-900/300 border-stone-600';
      case 'available':
        return 'bg-amber-900/300 border-stone-600';
      case 'locked':
        return 'bg-gray-400 border-gray-500';
      default:
        return 'bg-gray-400 border-gray-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'in-progress':
        return <Circle className="w-4 h-4 text-stone-600" />;
      case 'available':
        return <Star className="w-4 h-4 text-stone-600" />;
      case 'locked':
        return <Lock className="w-4 h-4 text-stone-300" />;
      default:
        return <Lock className="w-4 h-4 text-stone-300" />;
    }
  };

  const getLessonStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'available':
        return <Play className="w-4 h-4 text-stone-500" />;
      case 'locked':
        return <Lock className="w-4 h-4 text-gray-400" />;
      default:
        return <Lock className="w-4 h-4 text-gray-400" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <div className="bg-black/30 backdrop-blur-sm border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold text-white">
              CodeAcademy
            </Link>
            <div className="flex gap-4">
              <Link href="/skill-tree-general" className="text-sm text-white/80 hover:text-white font-medium">
                🌟 Árbol Completo
              </Link>
              <Link href="/dashboard" className="text-sm text-white/80 hover:text-white font-medium">
                ← Volver al dashboard
              </Link>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Title */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-4 flex items-center justify-center gap-3">
            <Trophy className="w-12 h-12 text-yellow-400" />
            Árbol de Habilidades - {
              selectedPath === 'python' ? '🐍 Python' :
              selectedPath === 'javascript' ? '⚡ JavaScript' :
              selectedPath === 'web' ? '🌐 Desarrollo Web' :
              selectedPath === 'cpp' ? '⚙️ C++' :
              selectedPath === 'java' ? '☕ Java' : 'Programación'
            }
          </h1>
          <p className="text-xl text-white/80">Desbloquea nuevas habilidades completando cursos</p>
          <Link 
            href="/skill-tree-general" 
            className="inline-block mt-3 px-4 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white rounded-lg font-semibold transition-all shadow-lg hover:scale-105"
          >
            🌟 Ver Árbol Completo de Programación
          </Link>
        </div>

        {/* Path Selector */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {[
            { id: 'python', name: 'Python', icon: '🐍', color: 'from-stone-500 to-cyan-500', desc: 'Ciencia de datos y IA' },
            { id: 'javascript', name: 'JavaScript', icon: '⚡', color: 'from-yellow-500 to-orange-500', desc: 'Web dinámico' },
            { id: 'web', name: 'Desarrollo Web', icon: '🌐', color: 'from-stone-500 to-amber-500', desc: 'HTML, CSS, Diseño' },
            { id: 'cpp', name: 'C++', icon: '⚙️', color: 'from-stone-500 to-stone-500', desc: 'Sistemas y rendimiento' },
            { id: 'java', name: 'Java', icon: '☕', color: 'from-orange-500 to-red-500', desc: 'Enterprise y Android' },
          ].map((path) => (
            <button
              key={path.id}
              onClick={() => setSelectedPath(path.id as any)}
              className={`px-6 py-4 rounded-xl font-bold text-lg transition-all ${
                selectedPath === path.id
                  ? `bg-gradient-to-r ${path.color} text-white shadow-2xl scale-110 ring-4 ring-white/30`
                  : 'bg-white/10 text-white/60 hover:bg-white/20 hover:scale-105'
              }`}
            >
              <div className="flex flex-col items-center">
                <span className="text-2xl mb-1">{path.icon}</span>
                <span>{path.name}</span>
                {selectedPath === path.id && (
                  <span className="text-xs text-white/80 mt-1 font-normal">{path.desc}</span>
                )}
              </div>
            </button>
          ))}
        </div>

        {/* Legend */}
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 mb-8 border border-white/20">
          <h3 className="text-white font-bold text-center mb-4 text-lg">Estado de los Cursos</h3>
          <div className="flex flex-wrap justify-center gap-8 text-sm">
            <div className="flex items-center gap-3 text-white/90">
              <div className="w-6 h-6 bg-green-500 rounded-full shadow-lg ring-2 ring-green-400/50"></div>
              <div>
                <div className="font-semibold">Completado</div>
                <div className="text-xs text-white/60">100% terminado</div>
              </div>
            </div>
            <div className="flex items-center gap-3 text-white/90">
              <div className="w-6 h-6 bg-amber-900/300 rounded-full shadow-lg ring-2 ring-blue-400/50"></div>
              <div>
                <div className="font-semibold">En progreso</div>
                <div className="text-xs text-white/60">Parcialmente completo</div>
              </div>
            </div>
            <div className="flex items-center gap-3 text-white/90">
              <div className="w-6 h-6 bg-amber-900/300 rounded-full shadow-lg ring-2 ring-purple-400/50"></div>
              <div>
                <div className="font-semibold">Disponible</div>
                <div className="text-xs text-white/60">Listo para comenzar</div>
              </div>
            </div>
            <div className="flex items-center gap-3 text-white/90">
              <div className="w-6 h-6 bg-gray-400 rounded-full shadow-lg opacity-60"></div>
              <div>
                <div className="font-semibold">Bloqueado</div>
                <div className="text-xs text-white/60">Completa requisitos</div>
              </div>
            </div>
          </div>
        </div>

        {/* Skill Tree */}
        <div className="relative bg-white/5 backdrop-blur-sm rounded-2xl p-8 overflow-auto" style={{ minHeight: '1300px', maxHeight: '1500px' }}>
          {/* Connection Lines */}
          <svg className="absolute inset-0 w-full h-full pointer-events-none" preserveAspectRatio="none">
            {currentTree.map((node: any) =>
              node.prerequisites.map((prereqId: string) => {
                const prereq = currentTree.find((n: any) => n.id === prereqId);
                if (!prereq) return null;
                
                // Líneas más cortas
                const x1 = prereq.position.x;
                const y1 = prereq.position.y + 2.5;
                const x2 = node.position.x;
                const y2 = node.position.y - 2.5;
                
                return (
                  <line
                    key={`${prereqId}-${node.id}`}
                    x1={`${x1}%`}
                    y1={`${y1}%`}
                    x2={`${x2}%`}
                    y2={`${y2}%`}
                    stroke={'#6b7280'}
                    strokeWidth="2"
                    strokeDasharray={'6,4'}
                    opacity={'0.25'}
                  />
                );
              })
            )}
          </svg>

          {/* Skill Nodes */}
          <div className="relative" style={{ minHeight: '1300px' }}>
            {currentTree.map((node: any) => (
              <div
                key={node.id}
                className="absolute cursor-pointer"
                style={{
                  left: `${node.position.x}%`,
                  top: `${node.position.y}%`,
                  transform: 'translate(-50%, -50%)',
                }}
                onClick={() => setSelectedNode(node)}
              >
                <div className="relative group transition-all duration-300 hover:scale-105">
                  {/* Círculo de fondo opaco pequeño - solo detrás del nodo */}
                  <div className="absolute inset-0 w-20 h-20 bg-stone-900 rounded-full -z-10 shadow-2xl" />
                  
                  {/* Node Circle */}
                  <div
                    className={`w-20 h-20 rounded-full border-4 flex items-center justify-center text-3xl shadow-xl transition-all ${getStatusColor(
                      node.status
                    )} ${node.status === 'locked' ? 'opacity-60' : ''} hover:shadow-2xl hover:ring-4 hover:ring-white/50`}
                  >
                    <span className={node.status === 'locked' ? 'grayscale' : ''}>{node.icon}</span>
                  </div>

                  {/* Status Icon */}
                  <div className="absolute -top-1 -right-1 bg-stone-900 rounded-full p-1.5 shadow-lg border border-white/20">
                    {getStatusIcon(node.status)}
                  </div>

                  {/* Node Label con fondo */}
                  <div className="text-center mt-2 w-36">
                    <div className="bg-stone-900/90 backdrop-blur-sm rounded-lg px-2 py-1 mb-1">
                      <p className="text-xs font-bold text-white drop-shadow-lg leading-tight">{node.title}</p>
                    </div>
                    <p className={`text-[9px] font-semibold uppercase tracking-wider ${
                      node.category === 'foundation' ? 'text-stone-300' :
                      node.category === 'intermediate' ? 'text-stone-300' :
                      node.category === 'advanced' ? 'text-orange-300' :
                      'text-red-300'
                    }`}>
                      {node.category}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-8">
          <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 backdrop-blur-sm rounded-xl p-6 text-center border-2 border-green-500/30 shadow-xl">
            <div className="text-5xl font-bold text-green-400 mb-2">
              {currentTree.filter((n: any) => n.status === 'completed').length}
            </div>
            <div className="text-white/90 font-semibold">Completados</div>
            <div className="text-xs text-green-300/70 mt-1">¡Excelente progreso!</div>
          </div>
          <div className="bg-gradient-to-br from-stone-500/20 to-stone-600/20 backdrop-blur-sm rounded-xl p-6 text-center border-2 border-stone-500/30 shadow-xl">
            <div className="text-5xl font-bold text-stone-400 mb-2">
              {currentTree.filter((n: any) => n.status === 'in-progress').length}
            </div>
            <div className="text-white/90 font-semibold">En Progreso</div>
            <div className="text-xs text-stone-300/70 mt-1">Sigue así</div>
          </div>
          <div className="bg-gradient-to-br from-stone-500/20 to-stone-600/20 backdrop-blur-sm rounded-xl p-6 text-center border-2 border-stone-500/30 shadow-xl">
            <div className="text-5xl font-bold text-stone-400 mb-2">
              {currentTree.filter((n: any) => n.status === 'available').length}
            </div>
            <div className="text-white/90 font-semibold">Disponibles</div>
            <div className="text-xs text-stone-300/70 mt-1">Listos para ti</div>
          </div>
          <div className="bg-gradient-to-br from-orange-500/20 to-orange-600/20 backdrop-blur-sm rounded-xl p-6 text-center border-2 border-orange-500/30 shadow-xl">
            <div className="text-5xl font-bold text-orange-400 mb-2">
              {currentTree.reduce((sum: number, n: any) => sum + (n.xp || 0), 0)}
            </div>
            <div className="text-white/90 font-semibold">XP Total</div>
            <div className="text-xs text-orange-300/70 mt-1">Del path completo</div>
          </div>
        </div>
      </div>

      {/* Modal con Lecciones */}
      {selectedNode && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setSelectedNode(null)}>
          <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto border-2 border-white/20 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            {/* Header */}
            <div className="sticky top-0 bg-gradient-to-r from-stone-600 to-amber-600 p-6 rounded-t-2xl">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-4">
                  <div className={`w-16 h-16 rounded-full border-4 flex items-center justify-center text-4xl ${getStatusColor(selectedNode.status)}`}>
                    {selectedNode.icon}
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-white mb-1">{selectedNode.title}</h2>
                    <p className="text-white/80">{selectedNode.description}</p>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedNode(null)}
                  className="text-white/80 hover:text-white p-2 hover:bg-white/10 rounded-lg transition-colors"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              {/* Progress Bar */}
              {selectedNode.progress !== undefined && (
                <div className="mt-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-white/80">Progreso</span>
                    <span className="text-sm font-bold text-white">{selectedNode.progress}%</span>
                  </div>
                  <div className="w-full bg-white/20 rounded-full h-3">
                    <div
                      className="bg-slate-800/50 backdrop-blur-sm h-3 rounded-full transition-all duration-500"
                      style={{ width: `${selectedNode.progress}%` }}
                    />
                  </div>
                </div>
              )}
            </div>

            {/* Content */}
            <div className="p-6">
              {/* Info */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-white/5 rounded-lg p-4">
                  <div className="flex items-center gap-2 text-white/60 mb-1">
                    <BookOpen className="w-4 h-4" />
                    <span className="text-sm">Lecciones</span>
                  </div>
                  <p className="text-2xl font-bold text-white">{selectedNode.lessons.length}</p>
                </div>
                <div className="bg-white/5 rounded-lg p-4">
                  <div className="flex items-center gap-2 text-white/60 mb-1">
                    <Trophy className="w-4 h-4" />
                    <span className="text-sm">XP Total</span>
                  </div>
                  <p className="text-2xl font-bold text-yellow-400">+{selectedNode.xp}</p>
                </div>
              </div>

              {/* Prerequisitos */}
              {selectedNode.status === 'locked' && selectedNode.prerequisites.length > 0 && (
                <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-6">
                  <h3 className="text-red-400 font-semibold mb-2 flex items-center gap-2">
                    <Lock className="w-4 h-4" />
                    Requisitos para desbloquear:
                  </h3>
                  <ul className="space-y-1">
                    {selectedNode.prerequisites.map((prereqId) => {
                      const prereq = currentTree.find((n) => n.id === prereqId);
                      return prereq ? (
                        <li key={prereqId} className="text-white/80 text-sm">
                          • Completar: {prereq.title}
                        </li>
                      ) : null;
                    })}
                  </ul>
                </div>
              )}

              {/* Lista de Lecciones */}
              <div>
                <h3 className="text-white font-bold text-lg mb-4">Lecciones</h3>
                <div className="space-y-2">
                  {selectedNode.lessons.map((lesson, index) => (
                    <div
                      key={lesson.id}
                      className={`flex items-center justify-between p-4 rounded-lg border-2 transition-all ${
                        lesson.status === 'completed'
                          ? 'bg-green-500/10 border-green-500/30'
                          : lesson.status === 'available'
                          ? 'bg-amber-900/300/10 border-stone-500/30 hover:bg-amber-900/300/20 cursor-pointer'
                          : 'bg-stone-900/500/10 border-gray-500/30 opacity-60'
                      }`}
                    >
                      <div className="flex items-center gap-3 flex-1">
                        {getLessonStatusIcon(lesson.status)}
                        <div>
                          <p className={`font-medium ${lesson.status === 'locked' ? 'text-white/50' : 'text-white'}`}>
                            {index + 1}. {lesson.title}
                          </p>
                          <p className="text-xs text-white/60">{lesson.duration}</p>
                        </div>
                      </div>
                      {lesson.status === 'available' && (
                        <Link
                          href={`/course/${selectedNode.id}/lesson/${lesson.id}`}
                          className="px-4 py-2 bg-amber-900/300 hover:bg-amber-600 text-white rounded-lg font-medium text-sm transition-colors"
                        >
                          Comenzar
                        </Link>
                      )}
                      {lesson.status === 'completed' && (
                        <span className="text-green-400 text-sm font-medium">Completado</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* CTA */}
              {selectedNode.status !== 'locked' && (
                <Link
                  href={`/course/${selectedNode.id}`}
                  className="mt-6 w-full bg-gradient-to-r from-stone-500 to-amber-500 text-white px-6 py-4 rounded-lg font-bold hover:from-stone-600 hover:to-stone-600 transition-all flex items-center justify-center gap-2 text-lg"
                >
                  {selectedNode.status === 'completed' ? 'Revisar Curso' : selectedNode.status === 'in-progress' ? 'Continuar Curso' : 'Comenzar Curso'}
                  <ArrowRight className="w-5 h-5" />
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
