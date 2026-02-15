'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  Trophy, Calendar, Target, Zap, Star, Clock, Award, CheckCircle, 
  Lock, TrendingUp, Users, Gift, Flame, ArrowLeft, Crown, Medal,
  Code, BookOpen, MessageCircle, Heart, Share2, Filter, Sparkles,
  Rocket, GraduationCap, Pin
} from 'lucide-react';

type ChallengeType = 'daily' | 'weekly' | 'monthly';
type ChallengeCategory = 'coding' | 'learning' | 'social' | 'streak';
type ChallengeStatus = 'active' | 'completed' | 'locked' | 'expired';

type Challenge = {
  id: string;
  type: ChallengeType;
  category: ChallengeCategory;
  title: string;
  description: string;
  icon: string;
  difficulty: 'easy' | 'medium' | 'hard';
  progress: number;
  target: number;
  reward: {
    xp: number;
    coins?: number;
    badge?: string;
  };
  status: ChallengeStatus;
  expiresIn?: string;
  participants?: number;
};

type Reward = {
  id: string;
  title: string;
  description: string;
  icon: string;
  cost: number;
  type: 'avatar' | 'badge' | 'theme' | 'boost';
  unlocked: boolean;
};

export default function ChallengesPage() {
  const [activeTab, setActiveTab] = useState<'daily' | 'weekly' | 'monthly' | 'rewards'>('weekly');
  const [isMounted, setIsMounted] = useState(false);
  const [userCoins, setUserCoins] = useState(0);
  const [userLevel, setUserLevel] = useState(1);
  const [rewardFilter, setRewardFilter] = useState<'all' | 'avatar' | 'badge' | 'theme' | 'boost'>('all');

  useEffect(() => {
    setIsMounted(true);
    loadUserProgress();
  }, []);

  const loadUserProgress = () => {
    if (typeof window === 'undefined') return;
    const coins = parseInt(localStorage.getItem('user_coins') || '250');
    const level = parseInt(localStorage.getItem('user_level') || '1');
    setUserCoins(coins);
    setUserLevel(level);
  };

  // Retos Diarios
  const dailyChallenges: Challenge[] = [
    {
      id: 'd1',
      type: 'daily',
      category: 'coding',
      title: 'Completa 3 Lecciones',
      description: 'Termina 3 lecciones de cualquier curso',
      icon: '📚',
      difficulty: 'easy',
      progress: 2,
      target: 3,
      reward: { xp: 50, coins: 10 },
      status: 'active',
      expiresIn: '8h 23min'
    },
    {
      id: 'd2',
      type: 'daily',
      category: 'streak',
      title: 'Mantén la Racha',
      description: 'Inicia sesión hoy para mantener tu racha',
      icon: '🔥',
      difficulty: 'easy',
      progress: 1,
      target: 1,
      reward: { xp: 25, coins: 5 },
      status: 'completed',
      expiresIn: '8h 23min'
    },
    {
      id: 'd3',
      type: 'daily',
      category: 'coding',
      title: 'Código Perfecto',
      description: 'Completa un ejercicio sin errores',
      icon: '✨',
      difficulty: 'medium',
      progress: 0,
      target: 1,
      reward: { xp: 75, coins: 15 },
      status: 'active',
      expiresIn: '8h 23min'
    }
  ];

  // Retos Semanales
  const weeklyChallenges: Challenge[] = [
    {
      id: 'w1',
      type: 'weekly',
      category: 'learning',
      title: 'Maestro Python',
      description: 'Completa 10 lecciones del curso de Python',
      icon: '🐍',
      difficulty: 'medium',
      progress: 6,
      target: 10,
      reward: { xp: 500, coins: 100, badge: 'Python Weekly Master' },
      status: 'active',
      expiresIn: '3 días',
      participants: 1234
    },
    {
      id: 'w2',
      type: 'weekly',
      category: 'coding',
      title: 'Desafío de Código',
      description: 'Resuelve 15 ejercicios de programación',
      icon: '💻',
      difficulty: 'hard',
      progress: 8,
      target: 15,
      reward: { xp: 750, coins: 150, badge: 'Code Warrior' },
      status: 'active',
      expiresIn: '3 días',
      participants: 856
    },
    {
      id: 'w3',
      type: 'weekly',
      category: 'social',
      title: 'Constructor de Comunidad',
      description: 'Ayuda a 5 compañeros en el foro',
      icon: '🤝',
      difficulty: 'easy',
      progress: 3,
      target: 5,
      reward: { xp: 300, coins: 50 },
      status: 'active',
      expiresIn: '3 días',
      participants: 543
    },
    {
      id: 'w4',
      type: 'weekly',
      category: 'streak',
      title: 'Racha Semanal',
      description: 'Estudia 5 días consecutivos',
      icon: '🔥',
      difficulty: 'medium',
      progress: 3,
      target: 5,
      reward: { xp: 400, coins: 80 },
      status: 'active',
      expiresIn: '3 días',
      participants: 2341
    },
    {
      id: 'w5',
      type: 'weekly',
      category: 'learning',
      title: 'Explorador Web',
      description: 'Completa el módulo de HTML y CSS',
      icon: '🌐',
      difficulty: 'medium',
      progress: 0,
      target: 1,
      reward: { xp: 600, coins: 120 },
      status: 'locked',
      expiresIn: '3 días'
    }
  ];

  // Retos Mensuales
  const monthlyChallenges: Challenge[] = [
    {
      id: 'm1',
      type: 'monthly',
      category: 'learning',
      title: 'Dominio Full Stack',
      description: 'Completa 3 cursos completos este mes',
      icon: '🎯',
      difficulty: 'hard',
      progress: 1,
      target: 3,
      reward: { xp: 2000, coins: 500, badge: 'Full Stack Champion' },
      status: 'active',
      expiresIn: '15 días',
      participants: 3421
    },
    {
      id: 'm2',
      type: 'monthly',
      category: 'coding',
      title: 'Maratón de Código',
      description: 'Completa 50 ejercicios de programación',
      icon: '🏃',
      difficulty: 'hard',
      progress: 23,
      target: 50,
      reward: { xp: 3000, coins: 750, badge: 'Code Marathon Runner' },
      status: 'active',
      expiresIn: '15 días',
      participants: 1876
    },
    {
      id: 'm3',
      type: 'monthly',
      category: 'social',
      title: 'Líder Comunitario',
      description: 'Obtén 100 likes en tus respuestas del foro',
      icon: '⭐',
      difficulty: 'medium',
      progress: 45,
      target: 100,
      reward: { xp: 1500, coins: 300, badge: 'Community Leader' },
      status: 'active',
      expiresIn: '15 días',
      participants: 654
    },
    {
      id: 'm4',
      type: 'monthly',
      category: 'streak',
      title: 'Racha Legendaria',
      description: 'Mantén una racha de 30 días',
      icon: '👑',
      difficulty: 'hard',
      progress: 12,
      target: 30,
      reward: { xp: 5000, coins: 1000, badge: 'Legendary Streak' },
      status: 'active',
      expiresIn: '15 días',
      participants: 234
    }
  ];

  // Tienda de Recompensas
  const rewards: Reward[] = [
    // Boosters de Aprendizaje
    {
      id: 'r1',
      title: 'XP Boost x2',
      description: 'Duplica tu XP durante 24 horas',
      icon: '⚡',
      cost: 150,
      type: 'boost',
      unlocked: false
    },
    {
      id: 'r2',
      title: 'XP Boost x3',
      description: 'Triplica tu XP durante 12 horas',
      icon: '💥',
      cost: 300,
      type: 'boost',
      unlocked: false
    },
    {
      id: 'r3',
      title: '3 Pistas Premium',
      description: 'Obtén ayuda en ejercicios difíciles',
      icon: '💡',
      cost: 100,
      type: 'boost',
      unlocked: false
    },
    
    // Funcionalidades Premium
    {
      id: 'r4',
      title: 'Crear Grupo Premium',
      description: 'Crea tu propio grupo/foro privado',
      icon: '🎯',
      cost: 500,
      type: 'badge',
      unlocked: false
    },
    {
      id: 'r5',
      title: 'Pin de Publicación',
      description: 'Destaca tu post en el foro durante 7 días',
      icon: '📌',
      cost: 200,
      type: 'boost',
      unlocked: false
    },
    {
      id: 'r6',
      title: 'Acceso Anticipado',
      description: 'Nuevos cursos y features antes que nadie',
      icon: '🚀',
      cost: 800,
      type: 'badge',
      unlocked: false
    },
    
    // Personalización
    {
      id: 'r7',
      title: 'Avatar Dorado',
      description: 'Marco dorado exclusivo para tu avatar',
      icon: '👑',
      cost: 400,
      type: 'avatar',
      unlocked: false
    },
    {
      id: 'r8',
      title: 'Avatar Ninja',
      description: 'Avatar especial de ninja del código',
      icon: '🥷',
      cost: 450,
      type: 'avatar',
      unlocked: false
    },
    {
      id: 'r9',
      title: 'Tema Cyberpunk',
      description: 'Tema futurista con efectos neón',
      icon: '🌃',
      cost: 600,
      type: 'theme',
      unlocked: false
    },
    
    // Certificados y Reconocimiento
    {
      id: 'r10',
      title: 'Certificado Premium',
      description: 'Certificado exclusivo con sello holográfico',
      icon: '📜',
      cost: 1000,
      type: 'badge',
      unlocked: false
    },
    {
      id: 'r11',
      title: 'Insignia Elite',
      description: 'Muestra tu estatus de elite en el perfil',
      icon: '🏆',
      cost: 350,
      type: 'badge',
      unlocked: false
    },
    {
      id: 'r12',
      title: 'Rango Legendario',
      description: 'Badge exclusivo color dorado animado',
      icon: '⭐',
      cost: 1500,
      type: 'badge',
      unlocked: false
    },
    
    // Educación Avanzada
    {
      id: 'r13',
      title: 'Mentoría 1-a-1',
      description: 'Sesión de 30 min con instructor experto',
      icon: '👨‍🏫',
      cost: 1200,
      type: 'badge',
      unlocked: false
    },
    {
      id: 'r14',
      title: 'Proyecto Avanzado',
      description: 'Desbloquea proyecto real de empresa',
      icon: '🚀',
      cost: 700,
      type: 'boost',
      unlocked: false
    },
    {
      id: 'r15',
      title: 'Code Review Pro',
      description: 'Revisión profesional de tu código',
      icon: '🔍',
      cost: 500,
      type: 'boost',
      unlocked: false
    }
  ];

  const getDifficultyColor = (difficulty: string) => {
    switch(difficulty) {
      case 'easy': return 'text-green-400';
      case 'medium': return 'text-yellow-400';
      case 'hard': return 'text-red-400';
      default: return 'text-stone-400';
    }
  };

  const getDifficultyBg = (difficulty: string) => {
    switch(difficulty) {
      case 'easy': return 'bg-green-500/20 border-green-500/30';
      case 'medium': return 'bg-yellow-500/20 border-yellow-500/30';
      case 'hard': return 'bg-red-500/20 border-red-500/30';
      default: return 'bg-stone-500/20 border-stone-500/30';
    }
  };

  const handleClaimReward = (challengeId: string) => {
    // Aquí iría la lógica para reclamar la recompensa
    console.log('Claiming reward for challenge:', challengeId);
  };

  const handleUnlockReward = (rewardId: string, cost: number) => {
    if (userCoins >= cost) {
      setUserCoins(userCoins - cost);
      localStorage.setItem('user_coins', (userCoins - cost).toString());
      // Aquí iría la lógica para desbloquear la recompensa
      console.log('Unlocking reward:', rewardId);
    }
  };

  const ChallengeCard = ({ challenge }: { challenge: Challenge }) => {
    const progressPercentage = (challenge.progress / challenge.target) * 100;
    const isCompleted = challenge.status === 'completed';
    const isLocked = challenge.status === 'locked';

    return (
      <div className={`bg-stone-800 rounded-xl p-6 border-2 transition-all ${
        isCompleted 
          ? 'border-green-500/50 bg-green-900/10' 
          : isLocked
          ? 'border-stone-700 opacity-60'
          : 'border-stone-700 hover:border-amber-700'
      }`}>
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-start gap-4">
            <div className={`text-5xl ${isLocked ? 'grayscale' : ''}`}>
              {isLocked ? <Lock className="w-12 h-12 text-stone-500" /> : challenge.icon}
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h3 className="text-xl font-bold text-stone-100">{challenge.title}</h3>
                {isCompleted && <CheckCircle className="w-5 h-5 text-green-400" />}
              </div>
              <p className="text-stone-400 text-sm mb-2">{challenge.description}</p>
              <div className="flex items-center gap-3 flex-wrap">
                <span className={`text-xs px-2 py-1 rounded-full border ${getDifficultyBg(challenge.difficulty)}`}>
                  <span className={getDifficultyColor(challenge.difficulty)}>{challenge.difficulty.toUpperCase()}</span>
                </span>
                {challenge.expiresIn && (
                  <span className="text-xs text-stone-500 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {challenge.expiresIn}
                  </span>
                )}
                {challenge.participants && (
                  <span className="text-xs text-stone-500 flex items-center gap-1">
                    <Users className="w-3 h-3" />
                    {challenge.participants.toLocaleString()} participantes
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>

        {!isLocked && (
          <>
            {/* Progress Bar */}
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-stone-400">Progreso</span>
                <span className="text-stone-100 font-semibold">
                  {challenge.progress} / {challenge.target}
                </span>
              </div>
              <div className="w-full bg-stone-700 rounded-full h-3 overflow-hidden">
                <div 
                  className={`h-full rounded-full transition-all duration-500 ${
                    isCompleted ? 'bg-green-500' : 'bg-amber-600'
                  }`}
                  style={{ width: `${progressPercentage}%` }}
                />
              </div>
            </div>

            {/* Rewards */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-amber-600">
                  <Zap className="w-5 h-5" />
                  <span className="font-bold">+{challenge.reward.xp} XP</span>
                </div>
                {challenge.reward.coins && (
                  <div className="flex items-center gap-2 text-yellow-400">
                    <Star className="w-5 h-5" />
                    <span className="font-bold">+{challenge.reward.coins} Coins</span>
                  </div>
                )}
                {challenge.reward.badge && (
                  <div className="flex items-center gap-2 text-purple-400">
                    <Award className="w-5 h-5" />
                    <span className="text-sm font-medium">{challenge.reward.badge}</span>
                  </div>
                )}
              </div>
              {isCompleted ? (
                <button
                  onClick={() => handleClaimReward(challenge.id)}
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
                >
                  <Gift className="w-4 h-4" />
                  Reclamar
                </button>
              ) : (
                <div className="px-4 py-2 bg-stone-700/50 text-stone-400 rounded-lg font-medium">
                  {Math.round(progressPercentage)}%
                </div>
              )}
            </div>
          </>
        )}

        {isLocked && (
          <div className="text-center py-4">
            <Lock className="w-8 h-8 text-stone-500 mx-auto mb-2" />
            <p className="text-stone-500 text-sm">Completa los retos anteriores para desbloquear</p>
          </div>
        )}
      </div>
    );
  };

  if (!isMounted) return null;

  return (
    <div className="min-h-screen bg-stone-900">
      {/* Header */}
      <div className="bg-stone-800 backdrop-blur-sm shadow-lg border-b-2 border-stone-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/dashboard" className="text-stone-300 hover:text-stone-100">
                <ArrowLeft className="w-5 h-5" />
              </Link>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-amber-600 to-amber-500 bg-clip-text text-transparent">
                  Retos & Recompensas
                </h1>
                <p className="text-sm text-stone-400">Completa desafíos y gana recompensas exclusivas</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-4 py-2 bg-stone-700 rounded-lg border-2 border-yellow-500/30">
                <Star className="w-5 h-5 text-yellow-400" />
                <span className="font-bold text-stone-100">{userCoins}</span>
                <span className="text-sm text-stone-400">Coins</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Coins Info Banner */}
        <div className="bg-gradient-to-r from-amber-700/20 to-yellow-600/20 rounded-xl p-6 mb-8 border-2 border-amber-700/30">
          <div className="flex items-start gap-4">
            <div className="w-16 h-16 bg-yellow-500/20 rounded-xl flex items-center justify-center flex-shrink-0">
              <Star className="w-8 h-8 text-yellow-400" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-stone-100 mb-2">💰 ¿Cómo usar tus Coins?</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-stone-300">
                <div>
                  <p className="font-bold text-amber-600 mb-1">🎯 Potencia tu aprendizaje</p>
                  <ul className="space-y-1 text-stone-400">
                    <li>• Boosters de XP x2/x3</li>
                    <li>• Pistas en ejercicios</li>
                    <li>• Proyectos avanzados</li>
                  </ul>
                </div>
                <div>
                  <p className="font-bold text-amber-600 mb-1">👥 Crea comunidad</p>
                  <ul className="space-y-1 text-stone-400">
                    <li>• Grupos premium privados</li>
                    <li>• Pin tus publicaciones</li>
                    <li>• Acceso anticipado</li>
                  </ul>
                </div>
                <div>
                  <p className="font-bold text-amber-600 mb-1">✨ Personalización</p>
                  <ul className="space-y-1 text-stone-400">
                    <li>• Avatares exclusivos</li>
                    <li>• Temas premium</li>
                    <li>• Certificados especiales</li>
                  </ul>
                </div>
              </div>
              <p className="mt-3 text-xs text-stone-500">💡 Gana coins completando retos diarios, semanales y mensuales</p>
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-stone-800 rounded-xl p-6 border-2 border-stone-700">
            <div className="flex items-center justify-between mb-2">
              <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
                <CheckCircle className="w-6 h-6 text-green-400" />
              </div>
              <TrendingUp className="w-5 h-5 text-green-400" />
            </div>
            <div className="text-3xl font-bold text-stone-100 mb-1">12</div>
            <div className="text-sm text-stone-400">Retos Completados</div>
          </div>

          <div className="bg-stone-800 rounded-xl p-6 border-2 border-stone-700">
            <div className="flex items-center justify-between mb-2">
              <div className="w-12 h-12 bg-amber-700/20 rounded-lg flex items-center justify-center">
                <Target className="w-6 h-6 text-amber-600" />
              </div>
              <Flame className="w-5 h-5 text-amber-600" />
            </div>
            <div className="text-3xl font-bold text-stone-100 mb-1">8</div>
            <div className="text-sm text-stone-400">Retos Activos</div>
          </div>

          <div className="bg-stone-800 rounded-xl p-6 border-2 border-stone-700">
            <div className="flex items-center justify-between mb-2">
              <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center">
                <Medal className="w-6 h-6 text-purple-400" />
              </div>
              <Crown className="w-5 h-5 text-purple-400" />
            </div>
            <div className="text-3xl font-bold text-stone-100 mb-1">5</div>
            <div className="text-sm text-stone-400">Insignias Ganadas</div>
          </div>

          <div className="bg-stone-800 rounded-xl p-6 border-2 border-stone-700">
            <div className="flex items-center justify-between mb-2">
              <div className="w-12 h-12 bg-yellow-500/20 rounded-lg flex items-center justify-center">
                <Star className="w-6 h-6 text-yellow-400" />
              </div>
              <Gift className="w-5 h-5 text-yellow-400" />
            </div>
            <div className="text-3xl font-bold text-stone-100 mb-1">{userCoins}</div>
            <div className="text-sm text-stone-400 mb-3">Total Coins</div>
            <Link 
              href="/seminars"
              className="text-xs text-purple-400 hover:text-purple-300 flex items-center gap-1 transition-colors"
            >
              <Sparkles className="w-3 h-3" />
              <span>Úsalas en seminarios →</span>
            </Link>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-6">
          <div className="flex gap-2 bg-stone-800 rounded-xl p-2 border-2 border-stone-700 overflow-x-auto">
            <button
              onClick={() => setActiveTab('daily')}
              className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all whitespace-nowrap flex items-center justify-center gap-2 ${
                activeTab === 'daily'
                  ? 'bg-amber-700 border-2 border-amber-800 text-stone-100'
                  : 'text-stone-400 hover:text-stone-100 hover:bg-stone-700'
              }`}
            >
              <Calendar className="w-5 h-5" />
              Diarios
              <span className="px-2 py-0.5 bg-stone-900 rounded-full text-xs">3</span>
            </button>
            <button
              onClick={() => setActiveTab('weekly')}
              className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all whitespace-nowrap flex items-center justify-center gap-2 ${
                activeTab === 'weekly'
                  ? 'bg-amber-700 border-2 border-amber-800 text-stone-100'
                  : 'text-stone-400 hover:text-stone-100 hover:bg-stone-700'
              }`}
            >
              <Target className="w-5 h-5" />
              Semanales
              <span className="px-2 py-0.5 bg-stone-900 rounded-full text-xs">5</span>
            </button>
            <button
              onClick={() => setActiveTab('monthly')}
              className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all whitespace-nowrap flex items-center justify-center gap-2 ${
                activeTab === 'monthly'
                  ? 'bg-amber-700 border-2 border-amber-800 text-stone-100'
                  : 'text-stone-400 hover:text-stone-100 hover:bg-stone-700'
              }`}
            >
              <Trophy className="w-5 h-5" />
              Mensuales
              <span className="px-2 py-0.5 bg-stone-900 rounded-full text-xs">4</span>
            </button>
            <button
              onClick={() => setActiveTab('rewards')}
              className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all whitespace-nowrap flex items-center justify-center gap-2 ${
                activeTab === 'rewards'
                  ? 'bg-amber-700 border-2 border-amber-800 text-stone-100'
                  : 'text-stone-400 hover:text-stone-100 hover:bg-stone-700'
              }`}
            >
              <Gift className="w-5 h-5" />
              Tienda
            </button>
          </div>
        </div>

        {/* Daily Challenges */}
        {activeTab === 'daily' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-stone-100">Retos Diarios</h2>
              <div className="flex items-center gap-2 text-stone-400">
                <Clock className="w-5 h-5" />
                <span className="text-sm">Reinicia en 8h 23min</span>
              </div>
            </div>
            {dailyChallenges.map(challenge => (
              <ChallengeCard key={challenge.id} challenge={challenge} />
            ))}
          </div>
        )}

        {/* Weekly Challenges */}
        {activeTab === 'weekly' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-stone-100">Retos Semanales</h2>
              <div className="flex items-center gap-2 text-stone-400">
                <Calendar className="w-5 h-5" />
                <span className="text-sm">Termina en 3 días</span>
              </div>
            </div>
            {weeklyChallenges.map(challenge => (
              <ChallengeCard key={challenge.id} challenge={challenge} />
            ))}
          </div>
        )}

        {/* Monthly Challenges */}
        {activeTab === 'monthly' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-stone-100">Retos Mensuales</h2>
              <div className="flex items-center gap-2 text-stone-400">
                <Trophy className="w-5 h-5" />
                <span className="text-sm">Termina en 15 días</span>
              </div>
            </div>
            {monthlyChallenges.map(challenge => (
              <ChallengeCard key={challenge.id} challenge={challenge} />
            ))}
          </div>
        )}

        {/* Rewards Shop */}
        {activeTab === 'rewards' && (
          <div>
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-stone-100 mb-2">Tienda de Recompensas</h2>
              <p className="text-stone-400 mb-4">Canjea tus coins por recompensas exclusivas</p>
              
              {/* Filter Buttons */}
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={() => setRewardFilter('all')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    rewardFilter === 'all'
                      ? 'bg-amber-700 text-stone-100 border-2 border-amber-800'
                      : 'bg-stone-800 text-stone-400 border-2 border-stone-700 hover:text-stone-100'
                  }`}
                >
                  <Filter className="w-4 h-4 inline mr-2" />
                  Todas
                </button>
                <button
                  onClick={() => setRewardFilter('boost')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    rewardFilter === 'boost'
                      ? 'bg-amber-700 text-stone-100 border-2 border-amber-800'
                      : 'bg-stone-800 text-stone-400 border-2 border-stone-700 hover:text-stone-100'
                  }`}
                >
                  <Zap className="w-4 h-4 inline mr-2" />
                  Boosters
                </button>
                <button
                  onClick={() => setRewardFilter('badge')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    rewardFilter === 'badge'
                      ? 'bg-amber-700 text-stone-100 border-2 border-amber-800'
                      : 'bg-stone-800 text-stone-400 border-2 border-stone-700 hover:text-stone-100'
                  }`}
                >
                  <Award className="w-4 h-4 inline mr-2" />
                  Premium
                </button>
                <button
                  onClick={() => setRewardFilter('avatar')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    rewardFilter === 'avatar'
                      ? 'bg-amber-700 text-stone-100 border-2 border-amber-800'
                      : 'bg-stone-800 text-stone-400 border-2 border-stone-700 hover:text-stone-100'
                  }`}
                >
                  <Crown className="w-4 h-4 inline mr-2" />
                  Avatares
                </button>
                <button
                  onClick={() => setRewardFilter('theme')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    rewardFilter === 'theme'
                      ? 'bg-amber-700 text-stone-100 border-2 border-amber-800'
                      : 'bg-stone-800 text-stone-400 border-2 border-stone-700 hover:text-stone-100'
                  }`}
                >
                  <Sparkles className="w-4 h-4 inline mr-2" />
                  Temas
                </button>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {rewards
                .filter(reward => rewardFilter === 'all' || reward.type === rewardFilter)
                .map(reward => {
                  const getTypeIcon = () => {
                    switch(reward.type) {
                      case 'boost': return <Zap className="w-4 h-4" />;
                      case 'badge': return <Award className="w-4 h-4" />;
                      case 'avatar': return <Crown className="w-4 h-4" />;
                      case 'theme': return <Sparkles className="w-4 h-4" />;
                    }
                  };
                  
                  const getTypeBg = () => {
                    switch(reward.type) {
                      case 'boost': return 'bg-blue-500/20 border-blue-500/30 text-blue-400';
                      case 'badge': return 'bg-purple-500/20 border-purple-500/30 text-purple-400';
                      case 'avatar': return 'bg-amber-500/20 border-amber-500/30 text-amber-400';
                      case 'theme': return 'bg-pink-500/20 border-pink-500/30 text-pink-400';
                    }
                  };
                  
                  return (
                    <div key={reward.id} className="bg-stone-800 rounded-xl p-6 border-2 border-stone-700 hover:border-amber-700 transition-all">
                      <div className="text-center mb-4">
                        <div className="flex items-center justify-between mb-3">
                          <span className={`text-xs px-2 py-1 rounded-full border ${getTypeBg()} flex items-center gap-1 font-medium`}>
                            {getTypeIcon()}
                            {reward.type.toUpperCase()}
                          </span>
                          {reward.unlocked && (
                            <CheckCircle className="w-5 h-5 text-green-400" />
                          )}
                        </div>
                        <div className="text-6xl mb-3">{reward.icon}</div>
                        <h3 className="text-lg font-bold text-stone-100 mb-1">{reward.title}</h3>
                        <p className="text-sm text-stone-400 mb-3">{reward.description}</p>
                        <div className="flex items-center justify-center gap-2 text-yellow-400 mb-4">
                          <Star className="w-5 h-5" />
                          <span className="text-2xl font-bold">{reward.cost}</span>
                          <span className="text-sm">Coins</span>
                        </div>
                      </div>
                      {reward.unlocked ? (
                        <button className="w-full px-4 py-2 bg-green-600 text-white rounded-lg font-medium flex items-center justify-center gap-2">
                          <CheckCircle className="w-4 h-4" />
                          Desbloqueado
                        </button>
                      ) : userCoins >= reward.cost ? (
                        <button
                          onClick={() => handleUnlockReward(reward.id, reward.cost)}
                          className="w-full px-4 py-2 bg-amber-700 hover:bg-amber-600 text-stone-100 rounded-lg font-medium transition-colors"
                        >
                          Desbloquear
                        </button>
                      ) : (
                        <button className="w-full px-4 py-2 bg-stone-700 text-stone-500 rounded-lg font-medium cursor-not-allowed">
                          Coins Insuficientes
                        </button>
                      )}
                    </div>
                  );
                })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
