'use client';

import Link from 'next/link';
import { BookOpen, Download, Code, Zap, ArrowRight, CheckCircle } from 'lucide-react';

export default function IntroProgramacion() {
  const lessons = [
    {
      id: 1,
      title: '¿Qué es programar?',
      description: 'Entiende qué significa programar y por qué es importante',
      duration: '5 min',
      icon: '💭',
    },
    {
      id: 2,
      title: 'Pensamiento computacional',
      description: 'Aprende a pensar como un programador',
      duration: '8 min',
      icon: '🧠',
    },
    {
      id: 3,
      title: 'Tu primer IDE',
      description: 'Instala y configura Visual Studio Code',
      duration: '10 min',
      icon: '💻',
    },
    {
      id: 4,
      title: 'Hola Mundo',
      description: 'Escribe tu primer programa',
      duration: '7 min',
      icon: '🌍',
    },
    {
      id: 5,
      title: 'Tipos de lenguajes',
      description: 'Python, JavaScript, Java... ¿cuál elegir?',
      duration: '10 min',
      icon: '🔤',
    },
    {
      id: 6,
      title: '¿Qué camino seguir?',
      description: 'Elige tu roadmap de aprendizaje',
      duration: '5 min',
      icon: '🗺️',
    },
  ];

  return (
    <div className="min-h-screen bg-stone-900">
      {/* Header */}
      <div className="bg-stone-800 backdrop-blur-sm border-b-2 border-stone-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold text-stone-100">
              Code Dungeon
            </Link>
            <Link href="/skill-tree" className="text-sm text-stone-300 hover:text-stone-100 font-medium">
              ← Volver a Roadmaps
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-amber-700 border-2 border-amber-800 rounded-2xl mb-6">
            <span className="text-4xl">💡</span>
          </div>
          <h1 className="text-5xl font-bold text-stone-100 mb-4">
            Introducción a la Programación
          </h1>
          <p className="text-xl text-stone-300 mb-6">
            Piensa como un programador
          </p>
          <div className="flex items-center justify-center gap-6 text-stone-400">
            <div className="flex items-center gap-2">
              <BookOpen className="w-5 h-5" />
              <span>6 lecciones</span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="w-5 h-5" />
              <span>45 minutos</span>
            </div>
            <div className="flex items-center gap-2">
              <Code className="w-5 h-5" />
              <span>Principiante</span>
            </div>
          </div>
        </div>

        {/* What you'll learn */}
        <div className="bg-stone-800 backdrop-blur-sm rounded-2xl p-8 mb-8 border-2 border-stone-700">
          <h2 className="text-2xl font-bold text-stone-100 mb-4">¿Qué aprenderás?</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
              <div>
                <p className="text-stone-100 font-semibold">Fundamentos básicos</p>
                <p className="text-stone-400 text-sm">Entiende qué es programar y cómo piensan los programadores</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
              <div>
                <p className="text-stone-100 font-semibold">Instalar tu IDE</p>
                <p className="text-stone-400 text-sm">Configura Visual Studio Code paso a paso</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
              <div>
                <p className="text-stone-100 font-semibold">Tu primer programa</p>
                <p className="text-stone-400 text-sm">Escribe y ejecuta tu primer "Hola Mundo"</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
              <div>
                <p className="text-stone-100 font-semibold">Elegir tu camino</p>
                <p className="text-stone-400 text-sm">Descubre qué lenguaje aprender según tus objetivos</p>
              </div>
            </div>
          </div>
        </div>

        {/* Lessons */}
        <div className="space-y-4 mb-8">
          <h2 className="text-2xl font-bold text-stone-100 mb-6">Contenido del curso</h2>
          {lessons.map((lesson, index) => (
            <div
              key={lesson.id}
              className="bg-stone-800 backdrop-blur-sm rounded-xl p-6 border-2 border-stone-700 hover:bg-stone-700 transition-all group cursor-pointer"
            >
              <div className="flex items-center gap-4">
                <div className="flex-shrink-0 w-12 h-12 bg-amber-700 border-2 border-amber-800 rounded-xl flex items-center justify-center text-2xl">
                  {lesson.icon}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-stone-500 text-sm font-semibold">Lección {lesson.id}</span>
                    <span className="text-stone-500 text-sm">•</span>
                    <span className="text-stone-500 text-sm">{lesson.duration}</span>
                  </div>
                  <h3 className="text-stone-100 font-bold text-lg mb-1">{lesson.title}</h3>
                  <p className="text-stone-400 text-sm">{lesson.description}</p>
                </div>
                <ArrowRight className="w-5 h-5 text-stone-500 group-hover:text-stone-100 group-hover:translate-x-1 transition-all" />
              </div>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="bg-amber-700 border-2 border-amber-800 rounded-2xl p-8 text-center">
          <h3 className="text-2xl font-bold text-stone-100 mb-4">
            ¿Listo para empezar?
          </h3>
          <p className="text-stone-200 mb-6">
            Comienza tu viaje en la programación con esta introducción práctica y completa
          </p>
          <Link
            href="/course/py-intro"
            className="inline-flex items-center gap-2 bg-stone-900 border-2 border-stone-800 text-stone-100 px-8 py-3 rounded-lg font-bold hover:bg-stone-800 transition-all"
          >
            Comenzar ahora
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
