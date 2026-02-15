'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { Lock, CheckCircle, X, Play } from 'lucide-react';

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

interface SkillTreeRoadmapProps {
  title: string;
  description: string;
  nodes: SkillNode[];
  completedCourses: string[];
  courseProgress: { [key: string]: number };
  language: string;
  onNodeClick?: (node: SkillNode) => void;
  backUrl?: string;
  isAdmin?: boolean;
}

export default function SkillTreeRoadmap({
  title,
  description,
  nodes,
  completedCourses,
  courseProgress,
  language,
  onNodeClick,
  backUrl = '/skill-tree',
  isAdmin = false
}: SkillTreeRoadmapProps) {
  const [selectedNode, setSelectedNode] = useState<SkillNode | null>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll on edge approach
  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    let mouseX = 0;
    let mouseY = 0;
    let animationFrameId: number;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
    };

    const animate = () => {
      const threshold = 120;
      const maxSpeed = 12;
      const rect = container.getBoundingClientRect();

      let scrollX = 0;
      let scrollY = 0;

      if (mouseX < threshold) {
        scrollX = -maxSpeed * ((threshold - mouseX) / threshold);
      } else if (mouseX > rect.width - threshold) {
        scrollX = maxSpeed * ((mouseX - (rect.width - threshold)) / threshold);
      }

      if (mouseY < threshold) {
        scrollY = -maxSpeed * ((threshold - mouseY) / threshold);
      } else if (mouseY > rect.height - threshold) {
        scrollY = maxSpeed * ((mouseY - (rect.height - threshold)) / threshold);
      }

      if (scrollX !== 0 || scrollY !== 0) {
        container.scrollLeft += scrollX;
        container.scrollTop += scrollY;
      }

      animationFrameId = requestAnimationFrame(animate);
    };

    container.addEventListener('mousemove', handleMouseMove);
    animationFrameId = requestAnimationFrame(animate);

    return () => {
      container.removeEventListener('mousemove', handleMouseMove);
      if (animationFrameId) cancelAnimationFrame(animationFrameId);
    };
  }, []);

  const getLineColor = (lang: string): string => {
    const colors: Record<string, string> = {
      'Python': '#3b82f6',
      'JavaScript': '#eab308',
      'TypeScript': '#3178c6',
      'Web': '#a855f7',
      'Java': '#f97316',
      'C++': '#6366f1',
      'SQL': '#059669',
      'Arduino': '#00979d',
      'DevOps': '#ec4899',
      'Security': '#dc2626',
      'Mobile': '#8b5cf6',
      'Game': '#f59e0b',
      'Cloud': '#0ea5e9',
      'IoT': '#14b8a6',
    };
    return colors[lang] || colors[language] || '#3b82f6';
  };

  const handleNodeClick = (node: SkillNode) => {
    setSelectedNode(node);
    if (onNodeClick) {
      onNodeClick(node);
    }
  };

  return (
    <div className="min-h-screen bg-stone-900">
      <style jsx>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 0.9;
          }
          50% {
            opacity: 1;
          }
        }
      `}</style>
      
      {/* Header */}
      <div className="bg-stone-800/50 backdrop-blur-sm border-b-2 border-stone-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold text-white">
              Code Dungeon
            </Link>
            <div className="flex gap-4">
              <Link href="/skill-tree-general" className="text-sm text-white/80 hover:text-white font-medium">
                Ver Mapa General
              </Link>
              <Link href={backUrl} className="text-sm text-white/80 hover:text-white font-medium">
                ← Volver
              </Link>
            </div>
          </div>
        </div>
      </div>

      <div className="px-4 py-6">
        {/* Title */}
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-white mb-2">
            {title}
          </h1>
          <p className="text-sm text-gray-400">
            {description}
          </p>
        </div>

        {/* Skill Tree - Roadmap Vertical */}
        <div 
          ref={scrollContainerRef}
          className="relative bg-stone-800 rounded-lg overflow-auto border-2 border-stone-700 shadow-2xl" 
          style={{ height: '78vh', maxHeight: '850px' }}
        >
          {/* Canvas vertical para scroll */}
          <div 
            className="relative mx-auto" 
            style={{ 
              width: '800px', 
              minHeight: '3000px',
              backgroundImage: 'radial-gradient(circle, rgb(55 65 81 / 0.5) 1px, transparent 1px)',
              backgroundSize: '40px 40px'
            }}
          >
            {/* Connection Lines */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 1 }}>
              {nodes.map((node: SkillNode, nodeIndex: number) =>
                node.prerequisites.map((prereqId: string, prereqIndex: number) => {
                  const prereq = nodes.find((n: SkillNode) => n.id === prereqId);
                  if (!prereq) return null;
                  
                  const isCompleted = completedCourses.includes(node.id);
                  const prereqCompleted = completedCourses.includes(prereqId);
                  const bothCompleted = isCompleted && prereqCompleted;
                  const lineColor = getLineColor(node.language);
                  
                  // Dimensiones de las cards
                  const CARD_WIDTH = 160;
                  const CARD_HEIGHT_BASE = 110;
                  const CARD_HEIGHT_COMPLETED = 130; // Altura extra cuando muestra badge "Completado"
                  
                  // Calcular altura según si el prerequisito está completado
                  const prereqHeight = prereqCompleted ? CARD_HEIGHT_COMPLETED : CARD_HEIGHT_BASE;
                  
                  // Posiciones exactas - centro horizontal de las cards
                  const x1 = (prereq.position.x / 150) * 800 + CARD_WIDTH / 2;
                  const y1 = (prereq.position.y / 450) * 3000 + prereqHeight;
                  const x2 = (node.position.x / 150) * 800 + CARD_WIDTH / 2;
                  const y2 = (node.position.y / 450) * 3000;
                  
                  const dx = x2 - x1;
                  const dy = y2 - y1;
                  const radius = 8;
                  
                  // Línea simple: vertical -> horizontal -> vertical
                  let pathData = '';
                  
                  if (Math.abs(dx) < 5) {
                    // Completamente vertical
                    pathData = `M ${x1},${y1} L ${x2},${y2}`;
                  } else {
                    // Con giro horizontal en el medio
                    const midY = y1 + dy / 2;
                    
                    if (dx > 0) {
                      // Hacia la derecha
                      pathData = `M ${x1},${y1} 
                                  L ${x1},${midY - radius} 
                                  Q ${x1},${midY} ${x1 + radius},${midY} 
                                  L ${x2 - radius},${midY} 
                                  Q ${x2},${midY} ${x2},${midY + radius} 
                                  L ${x2},${y2}`;
                    } else {
                      // Hacia la izquierda
                      pathData = `M ${x1},${y1} 
                                  L ${x1},${midY - radius} 
                                  Q ${x1},${midY} ${x1 - radius},${midY} 
                                  L ${x2 + radius},${midY} 
                                  Q ${x2},${midY} ${x2},${midY + radius} 
                                  L ${x2},${y2}`;
                    }
                  }
                  
                  return (
                    <React.Fragment key={`${prereqId}-${node.id}`}>
                      <path
                        d={pathData}
                        stroke={bothCompleted ? 'transparent' : lineColor}
                        strokeWidth="2"
                        fill="none"
                        opacity="0.2"
                        strokeLinecap="round"
                      />
                      {bothCompleted && (
                        <path
                          d={pathData}
                          stroke={lineColor}
                          strokeWidth="2.5"
                          fill="none"
                          opacity="0.8"
                          strokeLinecap="round"
                          className="animate-pulse"
                        />
                      )}
                    </React.Fragment>
                  );
                })
              )}
            </svg>

            {/* Skill Nodes */}
            <div className="relative" style={{ zIndex: 10, minHeight: '100%' }}>
              {nodes.map((node: SkillNode) => {
                const isCompleted = completedCourses.includes(node.id);
                const courseProgressValue = courseProgress[node.id] || 0;
                const totalLessons = node.lessons || 1;
                const lessonsCompleted = Math.min(courseProgressValue, totalLessons);
                // Admin tiene todo desbloqueado
                const isLocked = isAdmin ? false : !node.prerequisites.every((prereqId: string) => 
                  completedCourses.includes(prereqId)
                );
                
                // Posiciones para layout vertical (800px ancho)
                const left = (node.position.x / 150) * 800;
                const top = (node.position.y / 450) * 3000;
                const borderColor = getLineColor(node.language);

                return (
                  <div
                    key={node.id}
                    className="absolute cursor-pointer transition-transform hover:scale-105"
                    style={{
                      left: `${left}px`,
                      top: `${top}px`,
                      width: '160px',
                    }}
                    onClick={() => !isLocked && handleNodeClick(node)}
                  >
                    <div 
                      className="p-3 rounded-lg border-2 transition-all duration-300"
                      style={{
                        borderColor: isLocked ? '#57534e' : borderColor,
                        backgroundColor: isLocked ? 'rgba(28, 25, 23, 0.6)' : 'rgba(28, 25, 23, 0.95)',
                        opacity: isLocked ? 0.6 : 1
                      }}
                    >
                      <div className="relative mb-2">
                        <div className={`
                          w-10 h-10 rounded-lg flex items-center justify-center text-xl
                          ${isCompleted ? 'bg-amber-700' : 'bg-stone-800'}
                        `}>
                          {isLocked ? <Lock className="w-5 h-5 text-stone-500" /> : node.icon}
                        </div>
                        {!isCompleted && lessonsCompleted > 0 && (
                          <div className="absolute -top-1 -right-1 bg-amber-700 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center border-2 border-amber-800">
                            {lessonsCompleted}
                          </div>
                        )}
                      </div>

                      <h3 className="text-stone-100 font-bold text-xs text-center mb-2 leading-tight">
                        {node.title}
                      </h3>

                      {node.lessons && (
                        <div className="flex gap-1 justify-center flex-wrap">
                          {Array.from({ length: Math.min(node.lessons, 8) }).map((_, idx) => (
                            <div
                              key={idx}
                              className={`
                                w-2.5 h-2.5 rounded-full
                                ${idx < lessonsCompleted ? 'bg-white' : 'bg-gray-700'}
                                ${!isLocked && idx === lessonsCompleted ? 'ring-1 ring-white ring-offset-1 ring-offset-gray-900' : ''}
                              `}
                            />
                          ))}
                        </div>
                      )}

                      {isCompleted && (
                        <div className="mt-2 flex items-center justify-center gap-1 text-green-400 text-xs">
                          <CheckCircle className="w-3 h-3" />
                          <span className="font-semibold">Completado</span>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Node Detail Modal */}
      {selectedNode && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-stone-800 rounded-lg max-w-md w-full p-6 relative border-2 border-stone-700">
            <button
              onClick={() => setSelectedNode(null)}
              className="absolute top-4 right-4 text-gray-400 hover:text-white"
            >
              <X className="w-6 h-6" />
            </button>

            <div className="flex items-start gap-4 mb-4">
              <div className="text-4xl">{selectedNode.icon}</div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-white mb-1">
                  {selectedNode.title}
                </h2>
                <p className="text-gray-400 text-sm">
                  {selectedNode.description}
                </p>
              </div>
            </div>

            <Link
              href={`/course/${selectedNode.id}`}
              className="w-full bg-amber-700 text-white px-6 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 hover:bg-amber-600 transition-all border-2 border-amber-800"
            >
              <Play className="w-5 h-5" />
              Iniciar Curso
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
