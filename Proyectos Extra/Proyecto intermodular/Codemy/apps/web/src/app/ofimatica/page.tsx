'use client';

import { useState } from 'react';
import { CheckCircle, FileSpreadsheet, AlertTriangle } from 'lucide-react';

export default function OfimaticaPage() {
  const [hoveredLesson, setHoveredLesson] = useState<number | null>(null);

  const lessons = [
    {
      id: 1,
      title: 'Procesador de textos profesional',
      description: 'Word/Google Docs: formato, estilos, índices automáticos',
      icon: '📝',
      duration: '40 min',
    },
    {
      id: 2,
      title: 'Excel nivel básico',
      description: 'Fórmulas esenciales: SUMA, PROMEDIO, SI, BUSCARV',
      icon: '📊',
      duration: '45 min',
    },
    {
      id: 3,
      title: 'Excel nivel intermedio',
      description: 'Tablas dinámicas, gráficos avanzados, validación de datos',
      icon: '📈',
      duration: '50 min',
    },
    {
      id: 4,
      title: 'Excel nivel avanzado',
      description: 'BUSCARV, SI.ERROR, funciones anidadas, macros básicas',
      icon: '⚡',
      duration: '60 min',
    },
    {
      id: 5,
      title: 'Presentaciones impactantes',
      description: 'PowerPoint/Google Slides: diseño, animaciones, storytelling',
      icon: '🎨',
      duration: '35 min',
    },
    {
      id: 6,
      title: 'Google Workspace completo',
      description: 'Docs, Sheets, Slides, Forms - colaboración en tiempo real',
      icon: '☁️',
      duration: '40 min',
    },
    {
      id: 7,
      title: 'Automatización con macros',
      description: 'Graba y edita macros para tareas repetitivas',
      icon: '🤖',
      duration: '45 min',
    },
    {
      id: 8,
      title: 'Bases de datos con Access',
      description: 'Crea y gestiona bases de datos relacionales',
      icon: '🗄️',
      duration: '50 min',
    },
    {
      id: 9,
      title: 'Visualización de datos',
      description: 'Power BI básico: dashboards interactivos',
      icon: '📊',
      duration: '55 min',
    },
    {
      id: 10,
      title: 'Productividad y atajos',
      description: 'Trucos, shortcuts y flujos de trabajo eficientes',
      icon: '⚡',
      duration: '30 min',
    },
  ];

  const learningObjectives = [
    'Dominar Excel desde lo básico hasta avanzado',
    'Crear presentaciones profesionales e impactantes',
    'Automatizar tareas repetitivas con macros',
    'Visualizar datos con gráficos y dashboards',
  ];

  const softwareList = [
    { name: 'Microsoft Office', description: 'Word, Excel, PowerPoint, Access', icon: '🔷' },
    { name: 'Google Workspace', description: 'Docs, Sheets, Slides, Forms (gratis)', icon: '🟢' },
    { name: 'LibreOffice', description: 'Suite ofimática gratuita y open source', icon: '🟠' },
    { name: 'Power BI', description: 'Visualización de datos avanzada', icon: '🟡' },
  ];

  const excelFormulas = [
    'SUMA, PROMEDIO, MAX, MIN',
    'SI, SI.ERROR, Y, O',
    'BUSCARV, BUSCARH, COINCIDIR',
    'CONCATENAR, TEXTO, FECHA',
    'CONTAR.SI, SUMAR.SI',
    'INDICE, COINCIDIR (avanzado)',
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-green-950 to-slate-950">
      {/* Header */}
      <header className="border-b border-green-900/20 bg-stone-950/50 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-3">
              <a
                href="/skill-tree"
                className="text-green-400 hover:text-green-300 transition-colors"
              >
                ← Volver
              </a>
              <div className="h-6 w-px bg-green-900/30" />
              <span className="text-sm text-stone-400">Curso Profesional</span>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-green-500 to-emerald-600 mb-6 shadow-lg shadow-green-500/30">
            <FileSpreadsheet className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-green-400 via-emerald-400 to-green-500 bg-clip-text text-transparent">
            Ofimática Profesional
          </h1>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto mb-8">
            Domina las herramientas que se usan en TODAS las empresas. Excel avanzado, presentaciones impactantes, automatización y análisis de datos.
          </p>

          {/* Course Stats */}
          <div className="flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-400"></div>
              <span className="text-stone-400">10 lecciones</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
              <span className="text-stone-400">~7 horas</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
              <span className="text-stone-400">Básico a Avanzado</span>
            </div>
          </div>
        </div>

        {/* Why Important */}
        <div className="mb-12 p-6 rounded-xl bg-gradient-to-r from-stone-900/20 to-cyan-900/20 border border-stone-700/30">
          <div className="flex items-start gap-4">
            <AlertTriangle className="w-6 h-6 text-stone-400 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-lg font-semibold text-stone-300 mb-2">
                ¿Por qué es clave para tu futuro?
              </h3>
              <p className="text-stone-300 mb-3">
                La ofimática es una habilidad universal requerida en casi cualquier trabajo:
              </p>
              <ul className="space-y-2 text-stone-400">
                <li>• El 90% de las ofertas laborales piden Excel intermedio/avanzado</li>
                <li>• En finanzas, marketing, RRHH, logística... Excel es obligatorio</li>
                <li>• Presentaciones efectivas = mejor comunicación de tus ideas</li>
                <li>• Automatización = ahorra horas de trabajo repetitivo</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Learning Objectives */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6">¿Qué aprenderás?</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {learningObjectives.map((objective, index) => (
              <div
                key={index}
                className="flex items-start gap-3 p-4 rounded-xl bg-stone-900/40 border border-green-900/20 hover:border-green-700/40 transition-all"
              >
                <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                <span className="text-stone-300">{objective}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Software Section */}
        <div className="mb-12 p-6 rounded-xl bg-stone-900/40 border border-green-900/20">
          <h3 className="text-lg font-semibold text-green-300 mb-4">
            Software compatible
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            {softwareList.map((software, index) => (
              <div key={index} className="flex items-start gap-3 p-3 rounded-lg bg-slate-800/30">
                <span className="text-2xl">{software.icon}</span>
                <div>
                  <h4 className="font-semibold text-white">{software.name}</h4>
                  <p className="text-sm text-stone-400">{software.description}</p>
                </div>
              </div>
            ))}
          </div>
          <p className="text-sm text-stone-500 mt-4">
            💡 Aprende con cualquier suite, los conceptos son transferibles
          </p>
        </div>

        {/* Excel Formulas Highlight */}
        <div className="mb-12 p-6 rounded-xl bg-gradient-to-r from-green-900/20 to-emerald-900/20 border border-green-700/30">
          <h3 className="text-lg font-semibold text-green-300 mb-4 flex items-center gap-2">
            ⚡ Fórmulas de Excel que dominarás
          </h3>
          <div className="grid md:grid-cols-3 gap-3">
            {excelFormulas.map((formula, index) => (
              <div key={index} className="p-3 rounded-lg bg-slate-800/40 border border-green-800/30">
                <p className="text-sm text-stone-300 font-mono">{formula}</p>
              </div>
            ))}
          </div>
          <p className="text-sm text-stone-500 mt-4">
            + Funciones anidadas, referencias absolutas/relativas, y mucho más
          </p>
        </div>

        {/* Lessons Grid */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6">Contenido del curso</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {lessons.map((lesson) => (
              <div
                key={lesson.id}
                onMouseEnter={() => setHoveredLesson(lesson.id)}
                onMouseLeave={() => setHoveredLesson(null)}
                className="group relative p-6 rounded-xl bg-stone-900/40 border border-green-900/20 hover:border-green-700/50 transition-all duration-300 hover:shadow-lg hover:shadow-green-500/10"
              >
                <div className="flex items-start gap-4">
                  <div className="text-4xl flex-shrink-0 transition-transform group-hover:scale-110">
                    {lesson.icon}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-semibold text-white group-hover:text-green-300 transition-colors">
                        {lesson.title}
                      </h3>
                      <span className="text-xs text-stone-500 bg-slate-800/50 px-2 py-1 rounded">
                        {lesson.duration}
                      </span>
                    </div>
                    <p className="text-sm text-stone-400 leading-relaxed">
                      {lesson.description}
                    </p>
                  </div>
                </div>
                
                {hoveredLesson === lesson.id && (
                  <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-green-500/5 to-emerald-500/5 pointer-events-none" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-green-600 via-emerald-600 to-green-700 p-12 text-center shadow-2xl shadow-green-500/20">
          <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
          <div className="relative">
            <h2 className="text-3xl font-bold text-white mb-4">
              Destaca en el mercado laboral
            </h2>
            <p className="text-green-100 mb-8 max-w-2xl mx-auto">
              Excel avanzado es una de las habilidades más demandadas. Aprende a automatizar, analizar datos y crear informes profesionales.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/course/ofimatica-intro"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-white text-green-700 font-semibold hover:bg-green-50 transition-all hover:scale-105 shadow-lg"
              >
                Comenzar ahora
              </a>
              <a
                href="/skill-tree"
                className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-green-800/50 backdrop-blur-sm text-white font-semibold hover:bg-green-800/70 transition-all border border-white/20"
              >
                Ver todos los cursos
              </a>
            </div>
          </div>
        </div>

        {/* Real World Applications */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Aplicaciones reales
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-gradient-to-br from-green-900/20 to-emerald-900/20 border border-green-700/30">
              <div className="text-3xl mb-3">💼</div>
              <h3 className="text-lg font-semibold text-white mb-2">Finanzas y Contabilidad</h3>
              <p className="text-sm text-stone-400">
                Presupuestos, flujos de caja, análisis financiero, conciliaciones bancarias
              </p>
            </div>
            <div className="p-6 rounded-xl bg-gradient-to-br from-emerald-900/20 to-green-900/20 border border-emerald-700/30">
              <div className="text-3xl mb-3">📊</div>
              <h3 className="text-lg font-semibold text-white mb-2">Marketing y Ventas</h3>
              <p className="text-sm text-stone-400">
                Análisis de campañas, reportes de ventas, segmentación de clientes, KPIs
              </p>
            </div>
            <div className="p-6 rounded-xl bg-gradient-to-br from-green-900/20 to-green-800/20 border border-green-700/30">
              <div className="text-3xl mb-3">📈</div>
              <h3 className="text-lg font-semibold text-white mb-2">Gestión de Proyectos</h3>
              <p className="text-sm text-stone-400">
                Cronogramas, control de recursos, seguimiento de tareas, reportes ejecutivos
              </p>
            </div>
          </div>
        </div>

        {/* Career Benefits */}
        <div className="mt-12 p-6 rounded-xl bg-gradient-to-r from-amber-900/20 to-yellow-900/20 border border-amber-700/30">
          <h3 className="text-lg font-semibold text-amber-300 mb-4">
            💰 Beneficios profesionales
          </h3>
          <div className="grid md:grid-cols-2 gap-4 text-stone-300">
            <div>
              <h4 className="font-semibold text-white mb-2">Aumento salarial</h4>
              <ul className="space-y-1 text-sm text-stone-400">
                <li>• Excel avanzado puede aumentar tu salario un 15-20%</li>
                <li>• Certificaciones Office son muy valoradas</li>
                <li>• Habilidad transferible a cualquier industria</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-2">Más oportunidades</h4>
              <ul className="space-y-1 text-sm text-stone-400">
                <li>• Acceso a puestos de analista de datos</li>
                <li>• Automatiza tareas = más tiempo para crecer</li>
                <li>• Base para Business Intelligence y Data Science</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Bonus Section */}
        <div className="mt-12 p-6 rounded-xl bg-stone-900/40 border border-green-900/20">
          <h3 className="text-lg font-semibold text-green-300 mb-4">
            🎁 Bonus incluidos
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3">
              <div className="text-2xl">📋</div>
              <div>
                <h4 className="font-semibold text-white text-sm">Plantillas profesionales</h4>
                <p className="text-xs text-stone-400">Hojas de cálculo listas para usar en proyectos reales</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="text-2xl">⌨️</div>
              <div>
                <h4 className="font-semibold text-white text-sm">Cheat sheet de atajos</h4>
                <p className="text-xs text-stone-400">Todos los shortcuts para trabajar 3x más rápido</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="text-2xl">🎯</div>
              <div>
                <h4 className="font-semibold text-white text-sm">Ejercicios prácticos</h4>
                <p className="text-xs text-stone-400">Casos reales de empresas para practicar</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="text-2xl">🏆</div>
              <div>
                <h4 className="font-semibold text-white text-sm">Certificado de finalización</h4>
                <p className="text-xs text-stone-400">Añádelo a tu CV y LinkedIn</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
