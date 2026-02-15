'use client';

import { useState, useEffect, useMemo } from 'react';
import dynamic from 'next/dynamic';
import { 
  PracticeChallenge,
} from '@/data/practice-challenges';
import { ProjectIdea } from '@/data/project-ideas';

// Lazy load de datos
const loadPracticeChallenges = () => import('@/data/practice-challenges');
const loadProjectIdeas = () => import('@/data/project-ideas');

export default function PracticePage() {
  const [activeTab, setActiveTab] = useState<'challenges' | 'projects'>('challenges');
  const [selectedLanguage, setSelectedLanguage] = useState<string>('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('all');
  const [challenges, setChallenges] = useState<PracticeChallenge[]>([]);
  const [projects, setProjects] = useState<ProjectIdea[]>([]);
  const [selectedChallenge, setSelectedChallenge] = useState<PracticeChallenge | null>(null);
  const [showSolution, setShowSolution] = useState(false);
  const [completedChallenges, setCompletedChallenges] = useState<Set<string>>(new Set());
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function init() {
      setIsLoading(true);
      
      // Cargar desafíos completados de localStorage
      const completed = localStorage.getItem('completedChallenges');
      if (completed) {
        setCompletedChallenges(new Set(JSON.parse(completed)));
      }

      // Cargar módulos dinámicamente
      const [challengesModule, projectsModule] = await Promise.all([
        loadPracticeChallenges(),
        loadProjectIdeas()
      ]);

      // Cargar cursos completados para sugerencias
      const completedCourses = JSON.parse(localStorage.getItem('completedLessons') || '[]');
      const suggested = projectsModule.suggestProjects(completedCourses);
      setProjects(suggested);
      
      // Cargar desafíos iniciales
      let allChallenges: PracticeChallenge[] = [];
      Object.values(challengesModule.practiceChallenges).forEach((cats: any) => {
        allChallenges.push(...cats);
      });
      setChallenges(allChallenges);
      
      setIsLoading(false);
    }
    
    init();
  }, []);

  useEffect(() => {
    if (!isLoading) {
      loadChallenges();
    }
  }, [selectedLanguage, selectedDifficulty, isLoading]);

  const loadChallenges = async () => {
    const challengesModule = await loadPracticeChallenges();
    let allChallenges: PracticeChallenge[] = [];
    
    if (selectedLanguage === 'all') {
      Object.values(challengesModule.practiceChallenges).forEach((cats: any) => {
        allChallenges.push(...cats);
      });
    } else {
      allChallenges = challengesModule.getChallengesByLanguage(selectedLanguage);
    }

    if (selectedDifficulty !== 'all') {
      allChallenges = allChallenges.filter(c => c.difficulty === selectedDifficulty);
    }

    setChallenges(allChallenges);
  };

  const markAsCompleted = (challengeId: string) => {
    const newCompleted = new Set(completedChallenges);
    newCompleted.add(challengeId);
    setCompletedChallenges(newCompleted);
    localStorage.setItem('completedChallenges', JSON.stringify([...newCompleted]));
  };

  const languages = [
    { id: 'all', name: 'Todos', icon: '🌐' },
    { id: 'python', name: 'Python', icon: '🐍' },
    { id: 'javascript', name: 'JavaScript', icon: '⚡' },
    { id: 'cpp', name: 'C++', icon: '⚙️' },
    { id: 'java', name: 'Java', icon: '☕' },
    { id: 'html', name: 'Web', icon: '🌐' },
  ];

  const difficulties = [
    { id: 'all', name: 'Todas', color: 'gray' },
    { id: 'fácil', name: 'Fácil', color: 'green' },
    { id: 'medio', name: 'Medio', color: 'yellow' },
    { id: 'difícil', name: 'Difícil', color: 'red' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 py-8 px-4">
      {isLoading ? (
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-stone-500 mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300 text-xl">Cargando ejercicios...</p>
          </div>
        </div>
      ) : (
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            🎯 Zona de Práctica
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Refuerza tus conocimientos con ejercicios y descubre proyectos inspiradores
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-8 justify-center">
          <button
            onClick={() => setActiveTab('challenges')}
            className={`px-8 py-3 rounded-xl font-semibold transition-all ${
              activeTab === 'challenges'
                ? 'bg-stone-600 text-white shadow-lg scale-105'
                : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50'
            }`}
          >
            💪 Ejercicios de Refuerzo
          </button>
          <button
            onClick={() => setActiveTab('projects')}
            className={`px-8 py-3 rounded-xl font-semibold transition-all ${
              activeTab === 'projects'
                ? 'bg-amber-600 text-white shadow-lg scale-105'
                : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50'
            }`}
          >
            🚀 Ideas de Proyectos
          </button>
        </div>

        {/* Challenges Tab */}
        {activeTab === 'challenges' && (
          <div>
            {/* Filters */}
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 mb-6 shadow-lg">
              <div className="grid md:grid-cols-2 gap-6">
                {/* Language Filter */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    Lenguaje
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {languages.map(lang => (
                      <button
                        key={lang.id}
                        onClick={() => setSelectedLanguage(lang.id)}
                        className={`px-4 py-2 rounded-lg font-medium transition-all ${
                          selectedLanguage === lang.id
                            ? 'bg-stone-600 text-white shadow-md'
                            : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200'
                        }`}
                      >
                        {lang.icon} {lang.name}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Difficulty Filter */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    Dificultad
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {difficulties.map(diff => (
                      <button
                        key={diff.id}
                        onClick={() => setSelectedDifficulty(diff.id)}
                        className={`px-4 py-2 rounded-lg font-medium transition-all ${
                          selectedDifficulty === diff.id
                            ? 'bg-stone-600 text-white shadow-md'
                            : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200'
                        }`}
                      >
                        {diff.name}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div className="mt-4 flex items-center justify-between">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {challenges.length} ejercicios encontrados
                </p>
                <p className="text-sm font-semibold text-green-600 dark:text-green-400">
                  ✅ {completedChallenges.size} completados
                </p>
              </div>
            </div>

            {/* Challenges Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {challenges.map(challenge => (
                <div
                  key={challenge.id}
                  className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all cursor-pointer"
                  onClick={() => {
                    setSelectedChallenge(challenge);
                    setShowSolution(false);
                  }}
                >
                  {/* Badge de completado */}
                  {completedChallenges.has(challenge.id) && (
                    <div className="inline-block bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded-full mb-2">
                      ✓ Completado
                    </div>
                  )}

                  <div className="flex items-start justify-between mb-3">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                      {challenge.title}
                    </h3>
                    <span className="text-2xl">{challenge.language === 'python' ? '🐍' : challenge.language === 'javascript' ? '⚡' : challenge.language === 'cpp' ? '⚙️' : challenge.language === 'java' ? '☕' : '🌐'}</span>
                  </div>

                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    {challenge.description}
                  </p>

                  <div className="flex items-center justify-between">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      challenge.difficulty === 'fácil' ? 'bg-green-100 text-green-800' :
                      challenge.difficulty === 'medio' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {challenge.difficulty}
                    </span>
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      ⏱️ {challenge.timeEstimate}
                    </span>
                  </div>

                  <div className="mt-4 flex items-center justify-between">
                    <span className="text-sm font-semibold text-stone-600">
                      +{challenge.xp} XP
                    </span>
                    <span className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">
                      {challenge.type}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Projects Tab */}
        {activeTab === 'projects' && (
          <div>
            <div className="bg-gradient-to-r from-stone-100 to-amber-100 dark:from-stone-900 dark:to-amber-900 rounded-xl p-6 mb-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                💡 Proyectos Sugeridos Para Ti
              </h2>
              <p className="text-gray-700 dark:text-gray-300">
                Basados en los {projects.length} cursos que has completado
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {projects.map(project => (
                <div
                  key={project.id}
                  className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg hover:shadow-2xl transition-all"
                >
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                      {project.title}
                    </h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      project.difficulty === 'principiante' ? 'bg-green-100 text-green-800' :
                      project.difficulty === 'intermedio' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {project.difficulty}
                    </span>
                  </div>

                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    {project.description}
                  </p>

                  <div className="mb-4">
                    <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                      📋 Características:
                    </p>
                    <ul className="space-y-1">
                      {project.features.slice(0, 3).map((feature, idx) => (
                        <li key={idx} className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                          <span className="text-stone-500 mr-2">•</span>
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="mb-4">
                    <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                      🎁 Bonus:
                    </p>
                    <ul className="space-y-1">
                      {project.bonus.slice(0, 2).map((bonus, idx) => (
                        <li key={idx} className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                          <span className="text-stone-500 mr-2">✨</span>
                          {bonus}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t dark:border-gray-700">
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      ⏱️ {project.estimatedTime}
                    </span>
                    <span className="text-sm font-semibold text-stone-600">
                      {project.language.toUpperCase()}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            {projects.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  ¡Completa más cursos para recibir sugerencias personalizadas!
                </p>
              </div>
            )}
          </div>
        )}

        {/* Challenge Modal */}
        {selectedChallenge && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" onClick={() => setSelectedChallenge(null)}>
            <div className="bg-white dark:bg-gray-800 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto p-8" onClick={e => e.stopPropagation()}>
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                    {selectedChallenge.title}
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400">
                    {selectedChallenge.description}
                  </p>
                </div>
                <button
                  onClick={() => setSelectedChallenge(null)}
                  className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 text-2xl"
                >
                  ×
                </button>
              </div>

              {/* Challenge Details */}
              <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 mb-6">
                <p className="text-gray-800 dark:text-gray-200 mb-4">
                  {selectedChallenge.prompt}
                </p>

                {selectedChallenge.initialCode && (
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                      Código inicial:
                    </h3>
                    <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
                      <code>{selectedChallenge.initialCode}</code>
                    </pre>
                  </div>
                )}
              </div>

              {/* Hints */}
              {selectedChallenge.hints && selectedChallenge.hints.length > 0 && (
                <div className="mb-6">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
                    💡 Pistas:
                  </h3>
                  <ul className="space-y-2">
                    {selectedChallenge.hints.map((hint, idx) => (
                      <li key={idx} className="text-sm text-gray-600 dark:text-gray-400 bg-stone-50 dark:bg-stone-900/20 p-3 rounded-lg">
                        {idx + 1}. {hint}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Solution Toggle */}
              <div className="flex gap-4">
                <button
                  onClick={() => setShowSolution(!showSolution)}
                  className="px-6 py-3 bg-yellow-500 text-white rounded-lg font-semibold hover:bg-yellow-600 transition"
                >
                  {showSolution ? '🙈 Ocultar' : '👀 Ver'} Solución
                </button>
                <button
                  onClick={() => {
                    markAsCompleted(selectedChallenge.id);
                    setSelectedChallenge(null);
                  }}
                  className="px-6 py-3 bg-green-500 text-white rounded-lg font-semibold hover:bg-green-600 transition"
                >
                  ✓ Marcar como Completado
                </button>
              </div>

              {/* Solution */}
              {showSolution && selectedChallenge.solution && (
                <div className="mt-6 border-t dark:border-gray-700 pt-6">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
                    ✅ Solución:
                  </h3>
                  <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
                    <code>{selectedChallenge.solution}</code>
                  </pre>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
      )}
    </div>
  );
}
