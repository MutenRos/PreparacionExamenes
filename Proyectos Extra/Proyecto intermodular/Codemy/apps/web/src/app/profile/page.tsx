'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  User, Trophy, Star, BookOpen, Calendar, Mail, Award, Edit2, Check, X, 
  Shield, Target, Zap, TrendingUp, Clock, Flame, Camera, Settings,
  LogOut, Save, Trash2, MapPin, Briefcase, Link as LinkIcon, Palette,
  Code, FileText, Eye, EyeOff
} from 'lucide-react';
import { checkAchievements } from '@/data/achievements';
import './profile-custom.css';

// Avatar colors presets
const AVATAR_COLORS = [
  'from-stone-500 to-amber-500',
  'from-stone-500 to-cyan-500',
  'from-green-500 to-emerald-500',
  'from-orange-500 to-red-500',
  'from-stone-500 to-stone-500',
  'from-amber-500 to-rose-500',
  'from-teal-500 to-green-500',
  'from-yellow-500 to-orange-500',
];

export default function ProfilePage() {
  const [activeTab, setActiveTab] = useState<'overview' | 'settings' | 'activity' | 'customize'>('overview');
  const [isEditing, setIsEditing] = useState(false);
  const [showAvatarPicker, setShowAvatarPicker] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  
  // Profile customization
  const [profileType, setProfileType] = useState<'auto' | 'html' | 'markdown'>('auto');
  const [customHTML, setCustomHTML] = useState('');
  const [customMarkdown, setCustomMarkdown] = useState('');
  const [showPreview, setShowPreview] = useState(false);
  
  // User data
  const [userData, setUserData] = useState({
    name: 'Estudiante',
    email: 'estudiante@ejemplo.com',
    bio: '',
    location: '',
    occupation: '',
    website: '',
    avatarColor: 0,
    emailVerified: false,
  });

  const [tempData, setTempData] = useState(userData);

  // Stats
  const [stats, setStats] = useState({
    totalXP: 0,
    level: 1,
    completedLessons: 0,
    completedCourses: 0,
    achievements: 0,
    streakDays: 0,
    joinDate: 'Enero 2025',
    lastActive: 'Hoy',
    studyTime: 0, // minutes
  });

  // Activity log
  const [recentActivity, setRecentActivity] = useState<Array<{
    type: 'lesson' | 'course' | 'achievement';
    title: string;
    date: string;
    xp?: number;
  }>>([]);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (isMounted) {
      loadUserData();
      calculateStats();
      loadRecentActivity();
    }
  }, [isMounted]);

  const loadUserData = () => {
    if (typeof window === 'undefined') return;
    
    const savedData = {
      name: localStorage.getItem('user_name') || 'Estudiante',
      email: localStorage.getItem('user_email') || 'estudiante@ejemplo.com',
      bio: localStorage.getItem('user_bio') || '',
      location: localStorage.getItem('user_location') || '',
      occupation: localStorage.getItem('user_occupation') || '',
      website: localStorage.getItem('user_website') || '',
      avatarColor: parseInt(localStorage.getItem('user_avatar_color') || '0'),
      emailVerified: localStorage.getItem('user_email_verified') === 'true',
    };
    setUserData(savedData);
    setTempData(savedData);
    
    // Load profile customization
    const savedProfileType = localStorage.getItem('profile_type') as 'auto' | 'html' | 'markdown' || 'auto';
    const savedHTML = localStorage.getItem('profile_html') || '';
    const savedMarkdown = localStorage.getItem('profile_markdown') || '';
    
    setProfileType(savedProfileType);
    setCustomHTML(savedHTML);
    setCustomMarkdown(savedMarkdown);
  };
  
  // Simple Markdown to HTML converter
  const markdownToHTML = (markdown: string): string => {
    if (!markdown) return '';
    
    let html = markdown
      // Headers
      .replace(/^### (.*$)/gim, '<h3 class="text-xl font-bold text-stone-100 mb-3 mt-6">$1</h3>')
      .replace(/^## (.*$)/gim, '<h2 class="text-2xl font-bold text-stone-100 mb-4 mt-8">$1</h2>')
      .replace(/^# (.*$)/gim, '<h1 class="text-3xl font-bold text-stone-100 mb-6 mt-8">$1</h1>')
      // Bold
      .replace(/\*\*(.*?)\*\*/gim, '<strong class="text-amber-600 font-bold">$1</strong>')
      // Italic
      .replace(/\*(.*?)\*/gim, '<em class="text-stone-300 italic">$1</em>')
      // Links
      .replace(/\[([^\]]+)\]\(([^\)]+)\)/gim, '<a href="$2" class="text-amber-600 hover:text-amber-500 underline" target="_blank" rel="noopener noreferrer">$1</a>')
      // Code inline
      .replace(/`([^`]+)`/gim, '<code class="bg-stone-950 text-amber-400 px-2 py-1 rounded font-mono text-sm">$1</code>')
      // Code blocks
      .replace(/```([\s\S]*?)```/gim, '<pre class="bg-stone-950 text-amber-400 p-4 rounded-lg overflow-x-auto my-4 border-2 border-stone-700"><code>$1</code></pre>')
      // Line breaks
      .replace(/\n\n/g, '</p><p class="text-stone-300 mb-4">')
      .replace(/\n/g, '<br />');
    
    return `<div class="prose prose-invert max-w-none"><p class="text-stone-300 mb-4">${html}</p></div>`;
  };
  
  // Basic HTML sanitization (removes script tags and dangerous attributes)
  const sanitizeHTML = (html: string): string => {
    // Remove script tags
    let sanitized = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
    // Remove event handlers
    sanitized = sanitized.replace(/on\w+\s*=\s*["'][^"']*["']/gi, '');
    sanitized = sanitized.replace(/on\w+\s*=\s*[^\s>]*/gi, '');
    return sanitized;
  };
  
  const saveProfileCustomization = () => {
    if (typeof window === 'undefined') return;
    
    localStorage.setItem('profile_type', profileType);
    localStorage.setItem('profile_html', customHTML);
    localStorage.setItem('profile_markdown', customMarkdown);
  };

  const calculateStats = () => {
    if (typeof window === 'undefined') return;
    
    let totalXP = 0;
    let completedLessons = 0;
    let completedCoursesCount = 0;

    const courses = [
      { id: 'py-intro', lessons: 4, xpPerLesson: 50 },
      { id: 'py-variables', lessons: 5, xpPerLesson: 50 },
      { id: 'py-control', lessons: 6, xpPerLesson: 50 },
      { id: 'py-functions', lessons: 6, xpPerLesson: 50, bonusLastLesson: 50 },
      { id: 'py-classes', lessons: 6, xpPerLesson: 50, bonusLastLesson: 50 },
      { id: 'py-files', lessons: 6, xpPerLesson: 50, bonusLastLesson: 50 },
    ];

    courses.forEach(course => {
      let courseLessonsCompleted = 0;
      
      for (let i = 1; i <= course.lessons; i++) {
        const key = `lesson_${course.id}_${i}`;
        if (localStorage.getItem(key) === 'completed') {
          const isProjectLesson = course.bonusLastLesson && i === course.lessons;
          const lessonXP = isProjectLesson ? course.xpPerLesson + course.bonusLastLesson : course.xpPerLesson;
          
          totalXP += lessonXP;
          completedLessons++;
          courseLessonsCompleted++;
        }
      }

      if (courseLessonsCompleted === course.lessons) {
        totalXP += 100;
        completedCoursesCount++;
      }
    });

    const level = Math.floor(totalXP / 100) + 1;
    const streakDays = parseInt(localStorage.getItem('streak_days') || '0');
    
    const unlockedAchievements = checkAchievements({
      lessonsCompleted: completedLessons,
      coursesCompleted: completedCoursesCount,
      totalXP,
      streakDays,
      perfectLessons: 0,
      lessonsToday: 0,
    });

    const studyTime = parseInt(localStorage.getItem('total_study_time') || '0');

    setStats({
      totalXP,
      level,
      completedLessons,
      completedCourses: completedCoursesCount,
      achievements: unlockedAchievements.length,
      streakDays,
      joinDate: localStorage.getItem('join_date') || 'Enero 2025',
      lastActive: 'Hoy',
      studyTime,
    });
  };

  const loadRecentActivity = () => {
    if (typeof window === 'undefined') return;
    
    const activity: Array<{
      type: 'lesson' | 'course' | 'achievement';
      title: string;
      date: string;
      xp?: number;
    }> = [];

    const courses = [
      { id: 'py-intro', name: 'Introducción a Python', lessons: 4 },
      { id: 'py-variables', name: 'Variables y Datos', lessons: 5 },
      { id: 'py-control', name: 'Estructuras de Control', lessons: 6 },
    ];

    courses.forEach(course => {
      for (let i = course.lessons; i >= 1; i--) {
        const key = `lesson_${course.id}_${i}`;
        if (localStorage.getItem(key) === 'completed') {
          activity.push({
            type: 'lesson',
            title: `${course.name} - Lección ${i}`,
            date: 'Hoy',
            xp: 50,
          });
          if (activity.length >= 8) break;
        }
      }
      if (activity.length >= 8) return;
    });

    setRecentActivity(activity);
  };

  const handleSave = () => {
    Object.entries(tempData).forEach(([key, value]) => {
      localStorage.setItem(`user_${key}`, String(value));
    });
    setUserData(tempData);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTempData(userData);
    setIsEditing(false);
  };

  const handleAvatarColorChange = (colorIndex: number) => {
    const newData = { ...tempData, avatarColor: colorIndex };
    setTempData(newData);
    localStorage.setItem('user_avatar_color', String(colorIndex));
    setUserData(newData);
    setShowAvatarPicker(false);
  };

  const getInitials = () => {
    return userData.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  const getXPToNextLevel = () => {
    return (stats.level * 100) - stats.totalXP;
  };

  const getLevelProgress = () => {
    const xpInCurrentLevel = stats.totalXP % 100;
    return (xpInCurrentLevel / 100) * 100;
  };

  return (
    <div className="min-h-screen bg-stone-900">
      {/* Header */}
      <div className="bg-stone-800 backdrop-blur-sm shadow-lg border-b-2 border-stone-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-amber-600 to-amber-500 bg-clip-text text-transparent">
              Code Dungeon
            </Link>
            <Link 
              href="/dashboard" 
              className="text-sm text-stone-300 hover:text-stone-100 font-medium transition-colors"
            >
              ← Volver al dashboard
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Profile Header */}
        <div className="bg-stone-800 backdrop-blur-sm rounded-2xl shadow-2xl overflow-hidden mb-8 border-2 border-stone-700">
          {/* Banner with gradient */}
          <div className="h-48 bg-gradient-to-r from-amber-700 via-amber-600 to-amber-700 relative">
            <div className="absolute inset-0 bg-black/20"></div>
            {/* Decorative elements */}
            <div className="absolute top-4 right-4 flex gap-2">
                <button className="p-2 bg-stone-900/50 backdrop-blur-sm rounded-lg hover:bg-stone-900/70 transition-all">
                  <Settings className="w-5 h-5 text-stone-100" />
              </button>
            </div>
          </div>

          <div className="px-8 pb-8">
            <div className="flex flex-col md:flex-row items-start md:items-end gap-6 -mt-20">
              {/* Avatar with edit option */}
              <div className="relative">
                <div className={`w-40 h-40 bg-gradient-to-br ${AVATAR_COLORS[userData.avatarColor]} rounded-2xl flex items-center justify-center text-white font-bold text-5xl border-4 border-stone-900 shadow-2xl`}>
                  {getInitials()}
                </div>
                <button 
                  onClick={() => setShowAvatarPicker(!showAvatarPicker)}
                  className="absolute bottom-2 right-2 p-2 bg-stone-900 rounded-full border-2 border-stone-700 hover:bg-stone-800 transition-all shadow-lg group"
                  title="Cambiar color de avatar"
                >
                  <Palette className="w-4 h-4 text-stone-400 group-hover:text-amber-400 transition-colors" />
                </button>

                {/* Avatar color picker */}
                {showAvatarPicker && (
                  <div className="absolute top-full mt-2 bg-stone-800 rounded-xl shadow-2xl p-4 border-2 border-stone-700 z-10">
                    <p className="text-sm text-stone-300 mb-3 font-semibold">Elige el color de tu avatar</p>
                    <div className="grid grid-cols-4 gap-2">
                      {AVATAR_COLORS.map((color, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleAvatarColorChange(idx)}
                          className={`w-12 h-12 rounded-lg bg-gradient-to-br ${color} hover:scale-110 transition-transform ${
                            userData.avatarColor === idx ? 'ring-4 ring-white' : ''
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                )}
              </div>
              
              {/* User Info */}
              <div className="flex-1 mt-24 md:mt-0">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <h1 className="text-4xl font-bold text-stone-100">{userData.name}</h1>
                      {userData.emailVerified && (
                        <div className="flex items-center gap-1 px-3 py-1 bg-green-500/20 rounded-full">
                          <Check className="w-4 h-4 text-green-400" />
                          <span className="text-sm text-green-400 font-medium">Verificado</span>
                        </div>
                      )}
                    </div>
                    {userData.bio && (
                      <p className="text-stone-300 text-lg mb-3">{userData.bio}</p>
                    )}
                    <div className="flex flex-wrap items-center gap-4 text-stone-400 text-sm">
                      {userData.location && (
                        <div className="flex items-center gap-2">
                          <MapPin className="w-4 h-4" />
                          <span>{userData.location}</span>
                        </div>
                      )}
                      {userData.occupation && (
                        <div className="flex items-center gap-2">
                          <Briefcase className="w-4 h-4" />
                          <span>{userData.occupation}</span>
                        </div>
                      )}
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4" />
                        <span>Miembro desde {stats.joinDate}</span>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => setIsEditing(true)}
                    className="px-6 py-3 bg-amber-700 border-2 border-amber-800 text-stone-100 rounded-xl hover:bg-amber-800 transition-all shadow-lg font-medium flex items-center gap-2"
                  >
                    <Edit2 className="w-4 h-4" />
                    Editar Perfil
                  </button>
                </div>

                {/* Level Progress Bar */}
                <div className="bg-stone-950 rounded-xl p-4 border-2 border-stone-700">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-3">
                      <div className="flex items-center gap-2">
                        <Star className="w-5 h-5 text-yellow-500 fill-current" />
                        <span className="text-stone-100 font-bold text-lg">Nivel {stats.level}</span>
                      </div>
                      <span className="text-stone-400 text-sm">
                        {stats.totalXP} XP
                      </span>
                    </div>
                    <span className="text-sm text-stone-400">
                      {getXPToNextLevel()} XP para nivel {stats.level + 1}
                    </span>
                  </div>
                  <div className="w-full bg-stone-700 rounded-full h-3 overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-amber-600 to-amber-500 rounded-full transition-all duration-500"
                      style={{ width: `${getLevelProgress()}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-8">
          <div className="flex gap-2 bg-stone-800 backdrop-blur-sm rounded-xl p-2 border-2 border-stone-700 overflow-x-auto">
            <button
              onClick={() => setActiveTab('overview')}
              className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all whitespace-nowrap ${
                activeTab === 'overview'
                  ? 'bg-amber-700 border-2 border-amber-800 text-stone-100 shadow-lg'
                  : 'text-stone-400 hover:text-stone-100 hover:bg-stone-700'
              }`}
            >
              Vista General
            </button>
            <button
              onClick={() => setActiveTab('activity')}
              className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all whitespace-nowrap ${
                activeTab === 'activity'
                  ? 'bg-amber-700 border-2 border-amber-800 text-stone-100 shadow-lg'
                  : 'text-stone-400 hover:text-stone-100 hover:bg-stone-700'
              }`}
            >
              Actividad Reciente
            </button>
            <button
              onClick={() => setActiveTab('customize')}
              className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all whitespace-nowrap ${
                activeTab === 'customize'
                  ? 'bg-amber-700 border-2 border-amber-800 text-stone-100 shadow-lg'
                  : 'text-stone-400 hover:text-stone-100 hover:bg-stone-700'
              }`}
            >
              🎨 Personalizar
            </button>
            <button
              onClick={() => setActiveTab('settings')}
              className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all ${
                activeTab === 'settings'
                  ? 'bg-amber-700 border-2 border-amber-800 text-stone-100 shadow-lg'
                  : 'text-stone-400 hover:text-stone-100 hover:bg-stone-700'
              }`}
            >
              Configuración
            </button>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Custom Profile Content */}
            {profileType === 'markdown' && customMarkdown && (
              <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-8 border-2 border-stone-700">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-stone-100 flex items-center gap-3">
                    <FileText className="w-6 h-6 text-amber-600" />
                    Perfil Personalizado
                  </h2>
                  <button
                    onClick={() => setActiveTab('customize')}
                    className="px-4 py-2 bg-stone-700 hover:bg-stone-600 rounded-lg text-sm text-stone-300 flex items-center gap-2"
                  >
                    <Edit2 className="w-4 h-4" />
                    Editar
                  </button>
                </div>
                <div 
                  dangerouslySetInnerHTML={{ __html: markdownToHTML(customMarkdown) }}
                  className="markdown-content"
                />
              </div>
            )}

            {profileType === 'html' && customHTML && (
              <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-8 border-2 border-stone-700">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-stone-100 flex items-center gap-3">
                    <Code className="w-6 h-6 text-amber-600" />
                    Perfil Personalizado
                  </h2>
                  <button
                    onClick={() => setActiveTab('customize')}
                    className="px-4 py-2 bg-stone-700 hover:bg-stone-600 rounded-lg text-sm text-stone-300 flex items-center gap-2"
                  >
                    <Edit2 className="w-4 h-4" />
                    Editar
                  </button>
                </div>
                <div 
                  dangerouslySetInnerHTML={{ __html: sanitizeHTML(customHTML) }}
                  className="html-content"
                />
              </div>
            )}

            {/* Stats Grid - Always show */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-stone-700 hover:border-amber-600 transition-all">
                <div className="w-14 h-14 bg-amber-700/20 rounded-xl flex items-center justify-center mb-4">
                  <Star className="w-7 h-7 text-amber-600" />
                </div>
                <div className="text-4xl font-bold text-stone-100 mb-2">{stats.totalXP}</div>
                <div className="text-sm text-stone-400 font-medium">XP Total</div>
              </div>

              <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-stone-700 hover:border-amber-600 transition-all">
                <div className="w-14 h-14 bg-amber-700/20 rounded-xl flex items-center justify-center mb-4">
                  <BookOpen className="w-7 h-7 text-amber-600" />
                </div>
                <div className="text-4xl font-bold text-stone-100 mb-2">{stats.completedLessons}</div>
                <div className="text-sm text-stone-400 font-medium">Lecciones</div>
              </div>

              <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-stone-700 hover:border-green-400 transition-all">
                <div className="w-14 h-14 bg-green-500/20 rounded-xl flex items-center justify-center mb-4">
                  <Trophy className="w-7 h-7 text-green-400" />
                </div>
                <div className="text-4xl font-bold text-stone-100 mb-2">{stats.completedCourses}</div>
                <div className="text-sm text-stone-400 font-medium">Cursos</div>
              </div>

              <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-stone-700 hover:border-yellow-400 transition-all">
                <div className="w-14 h-14 bg-yellow-500/20 rounded-xl flex items-center justify-center mb-4">
                  <Award className="w-7 h-7 text-yellow-400" />
                </div>
                <div className="text-4xl font-bold text-stone-100 mb-2">{stats.achievements}</div>
                <div className="text-sm text-stone-400 font-medium">Logros</div>
              </div>

              <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-stone-700 hover:border-orange-400 transition-all">
                <div className="w-14 h-14 bg-orange-500/20 rounded-xl flex items-center justify-center mb-4">
                  <Flame className="w-7 h-7 text-orange-400" />
                </div>
                <div className="text-4xl font-bold text-stone-100 mb-2">{stats.streakDays}</div>
                <div className="text-sm text-stone-400 font-medium">Racha</div>
              </div>

              <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-stone-700 hover:border-amber-600 transition-all">
                <div className="w-14 h-14 bg-amber-700/20 rounded-xl flex items-center justify-center mb-4">
                  <Target className="w-7 h-7 text-amber-600" />
                </div>
                <div className="text-4xl font-bold text-stone-100 mb-2">{stats.level}</div>
                <div className="text-sm text-stone-400 font-medium">Nivel</div>
              </div>

              <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-stone-700 hover:border-teal-400 transition-all">
                <div className="w-14 h-14 bg-teal-500/20 rounded-xl flex items-center justify-center mb-4">
                  <Clock className="w-7 h-7 text-teal-400" />
                </div>
                <div className="text-4xl font-bold text-stone-100 mb-2">{Math.floor(stats.studyTime / 60)}h</div>
                <div className="text-sm text-stone-400 font-medium">Tiempo estudio</div>
              </div>

              <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-stone-700 hover:border-amber-600 transition-all">
                <div className="w-14 h-14 bg-amber-700/20 rounded-xl flex items-center justify-center mb-4">
                  <TrendingUp className="w-7 h-7 text-amber-600" />
                </div>
                <div className="text-4xl font-bold text-stone-100 mb-2">
                  {stats.completedLessons > 0 ? Math.floor((stats.completedLessons / 33) * 100) : 0}%
                </div>
                <div className="text-sm text-stone-400 font-medium">Progreso</div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Link 
                href="/skill-tree"
                className="bg-stone-800 backdrop-blur-sm rounded-xl p-6 border-2 border-stone-700 hover:border-amber-600 transition-all group"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-amber-700/20 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                    <BookOpen className="w-6 h-6 text-amber-600" />
                  </div>
                  <div>
                    <h3 className="text-stone-100 font-bold mb-1">Continuar Aprendiendo</h3>
                    <p className="text-stone-400 text-sm">Explora nuevas lecciones</p>
                  </div>
                </div>
              </Link>

              <Link 
                href="/achievements"
                className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-stone-500/20 hover:border-yellow-400/40 transition-all group"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-yellow-500/20 to-orange-500/20 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                    <Trophy className="w-6 h-6 text-yellow-400" />
                  </div>
                  <div>
                    <h3 className="text-white font-bold mb-1">Mis Logros</h3>
                    <p className="text-stone-300 text-sm">{stats.achievements} desbloqueados</p>
                  </div>
                </div>
              </Link>

              <Link 
                href="/leaderboard"
                className="bg-stone-800 backdrop-blur-sm rounded-xl p-6 border-2 border-stone-700 hover:border-green-400 transition-all group"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-green-500/20 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                    <TrendingUp className="w-6 h-6 text-green-400" />
                  </div>
                  <div>
                    <h3 className="text-stone-100 font-bold mb-1">Clasificación</h3>
                    <p className="text-stone-400 text-sm">Ve tu posición</p>
                  </div>
                </div>
              </Link>
            </div>

            {/* Progress by Course */}
            <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-8 border-2 border-stone-700">
              <h2 className="text-2xl font-bold text-stone-100 mb-6 flex items-center gap-3">
                <Target className="w-6 h-6 text-amber-600" />
                Progreso por Curso
              </h2>
              <div className="space-y-4">
                {isMounted && [
                  { id: 'py-intro', name: 'Introducción a Python', lessons: 4, icon: '🐍' },
                  { id: 'py-variables', name: 'Variables y Datos', lessons: 5, icon: '📦' },
                  { id: 'py-control', name: 'Estructuras de Control', lessons: 6, icon: '🔀' },
                  { id: 'py-functions', name: 'Funciones', lessons: 6, icon: '⚙️' },
                  { id: 'py-classes', name: 'Programación Orientada a Objetos', lessons: 6, icon: '🏗️' },
                  { id: 'py-files', name: 'Manejo de Archivos', lessons: 6, icon: '📁' },
                ].map(course => {
                  let completed = 0;
                  for (let i = 1; i <= course.lessons; i++) {
                    if (localStorage.getItem(`lesson_${course.id}_${i}`) === 'completed') {
                      completed++;
                    }
                  }
                  const progress = (completed / course.lessons) * 100;

                  return (
                    <div key={course.id} className="bg-stone-950 rounded-lg p-4 border-2 border-stone-700">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <span className="text-2xl">{course.icon}</span>
                          <div>
                            <h3 className="text-stone-100 font-semibold">{course.name}</h3>
                            <p className="text-sm text-stone-400">{completed} de {course.lessons} lecciones</p>
                          </div>
                        </div>
                        <span className="text-amber-600 font-bold">{Math.floor(progress)}%</span>
                      </div>
                      <div className="w-full bg-stone-700 rounded-full h-2 overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-amber-600 to-amber-500 rounded-full transition-all duration-500"
                          style={{ width: `${progress}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'activity' && (
          <div className="space-y-6">
            <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-8 border-2 border-stone-700">
              <h2 className="text-2xl font-bold text-stone-100 mb-6 flex items-center gap-3">
                <Clock className="w-6 h-6 text-amber-600" />
                Actividad Reciente
              </h2>

              {recentActivity.length > 0 ? (
                <div className="space-y-3">
                  {recentActivity.map((activity, idx) => (
                    <div 
                      key={idx}
                      className="flex items-center gap-4 p-4 bg-stone-950 rounded-lg border-2 border-stone-700 hover:border-amber-600 transition-all"
                    >
                      <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                        activity.type === 'lesson' ? 'bg-amber-700/20' :
                        activity.type === 'course' ? 'bg-green-500/20' :
                        'bg-yellow-500/20'
                      }`}>
                        {activity.type === 'lesson' && <BookOpen className="w-6 h-6 text-amber-600" />}
                        {activity.type === 'course' && <Trophy className="w-6 h-6 text-green-400" />}
                        {activity.type === 'achievement' && <Award className="w-6 h-6 text-yellow-400" />}
                      </div>
                      <div className="flex-1">
                        <h3 className="text-stone-100 font-semibold">{activity.title}</h3>
                        <p className="text-sm text-stone-400">{activity.date}</p>
                      </div>
                      {activity.xp && (
                        <div className="flex items-center gap-2 px-3 py-1 bg-amber-700/20 rounded-full">
                          <Zap className="w-4 h-4 text-amber-600" />
                          <span className="text-stone-100 font-semibold">+{activity.xp} XP</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Clock className="w-16 h-16 text-stone-500 mx-auto mb-4 opacity-50" />
                  <p className="text-stone-400 mb-4">Aún no tienes actividad reciente</p>
                  <Link
                    href="/skill-tree"
                    className="inline-flex items-center gap-2 px-6 py-3 bg-amber-700 border-2 border-amber-800 text-stone-100 rounded-lg hover:bg-amber-800 transition-all font-medium"
                  >
                    Comenzar a Aprender
                  </Link>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="space-y-6">
            <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-8 border-2 border-stone-700">
              <h2 className="text-2xl font-bold text-stone-100 mb-6 flex items-center gap-3">
                <User className="w-6 h-6 text-amber-600" />
                Información Personal
              </h2>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-stone-400 mb-2">
                    Nombre completo
                  </label>
                  <input
                    type="text"
                    value={isEditing ? tempData.name : userData.name}
                    onChange={(e) => isEditing && setTempData({ ...tempData, name: e.target.value })}
                    disabled={!isEditing}
                    className="w-full px-4 py-3 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700 focus:border-amber-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-stone-400 mb-2">
                    Email
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="email"
                      value={isEditing ? tempData.email : userData.email}
                      onChange={(e) => isEditing && setTempData({ ...tempData, email: e.target.value })}
                      disabled={!isEditing}
                      className="flex-1 px-4 py-3 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700 focus:border-amber-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    />
                    {userData.emailVerified && (
                      <div className="flex items-center px-4 py-3 bg-green-500/20 border-2 border-green-500/30 rounded-lg">
                        <Check className="w-5 h-5 text-green-400" />
                      </div>
                    )}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-stone-400 mb-2">
                    Biografía
                  </label>
                  <textarea
                    value={isEditing ? tempData.bio : userData.bio}
                    onChange={(e) => isEditing && setTempData({ ...tempData, bio: e.target.value })}
                    disabled={!isEditing}
                    rows={3}
                    placeholder="Cuéntanos sobre ti..."
                    className="w-full px-4 py-3 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700 focus:border-amber-700 disabled:opacity-50 disabled:cursor-not-allowed resize-none"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-stone-400 mb-2">
                      Ubicación
                    </label>
                    <input
                      type="text"
                      value={isEditing ? tempData.location : userData.location}
                      onChange={(e) => isEditing && setTempData({ ...tempData, location: e.target.value })}
                      disabled={!isEditing}
                      placeholder="Ciudad, País"
                      className="w-full px-4 py-3 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700 focus:border-amber-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-stone-400 mb-2">
                      Ocupación
                    </label>
                    <input
                      type="text"
                      value={isEditing ? tempData.occupation : userData.occupation}
                      onChange={(e) => isEditing && setTempData({ ...tempData, occupation: e.target.value })}
                      disabled={!isEditing}
                      placeholder="Estudiante, Desarrollador, etc."
                      className="w-full px-4 py-3 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700 focus:border-amber-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-stone-400 mb-2">
                    Sitio web
                  </label>
                  <input
                    type="url"
                    value={isEditing ? tempData.website : userData.website}
                    onChange={(e) => isEditing && setTempData({ ...tempData, website: e.target.value })}
                    disabled={!isEditing}
                    placeholder="https://..."
                    className="w-full px-4 py-3 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700 focus:border-amber-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  />
                </div>

                {isEditing && (
                  <div className="flex gap-3 pt-4">
                    <button
                      onClick={handleSave}
                      className="flex-1 px-6 py-3 bg-amber-700 border-2 border-amber-800 text-stone-100 rounded-lg hover:bg-amber-800 transition-all font-medium flex items-center justify-center gap-2"
                    >
                      <Save className="w-5 h-5" />
                      Guardar Cambios
                    </button>
                    <button
                      onClick={handleCancel}
                      className="px-6 py-3 bg-stone-700 border-2 border-stone-600 text-stone-100 rounded-lg hover:bg-stone-600 transition-all font-medium flex items-center gap-2"
                    >
                      <X className="w-5 h-5" />
                      Cancelar
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Danger Zone */}
            <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-8 border-2 border-red-500/30">
              <h2 className="text-2xl font-bold text-red-400 mb-6 flex items-center gap-3">
                <Shield className="w-6 h-6" />
                Zona Peligrosa
              </h2>

              <div className="space-y-4">
                <button className="w-full px-6 py-3 bg-red-500/10 text-red-400 border border-red-500/30 rounded-lg hover:bg-red-500/20 transition-all font-medium flex items-center justify-center gap-2">
                  <Trash2 className="w-5 h-5" />
                  Eliminar Progreso
                </button>

                <button className="w-full px-6 py-3 bg-red-500/10 text-red-400 border border-red-500/30 rounded-lg hover:bg-red-500/20 transition-all font-medium flex items-center justify-center gap-2">
                  <LogOut className="w-5 h-5" />
                  Cerrar Sesión
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'customize' && (
          <div className="space-y-6">
            {/* Profile Type Selector */}
            <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-8 border-2 border-stone-700">
              <h2 className="text-2xl font-bold text-stone-100 mb-6 flex items-center gap-3">
                <Palette className="w-6 h-6 text-amber-600" />
                Tipo de Perfil
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <button
                  onClick={() => setProfileType('auto')}
                  className={`p-6 rounded-xl border-2 transition-all ${
                    profileType === 'auto'
                      ? 'bg-amber-700/20 border-amber-700'
                      : 'bg-stone-900 border-stone-700 hover:border-amber-700/50'
                  }`}
                >
                  <div className="text-4xl mb-3">🤖</div>
                  <h3 className="font-bold text-stone-100 mb-2">Autogenerado</h3>
                  <p className="text-sm text-stone-400">Perfil generado automáticamente con tus estadísticas</p>
                </button>

                <button
                  onClick={() => setProfileType('markdown')}
                  className={`p-6 rounded-xl border-2 transition-all ${
                    profileType === 'markdown'
                      ? 'bg-amber-700/20 border-amber-700'
                      : 'bg-stone-900 border-stone-700 hover:border-amber-700/50'
                  }`}
                >
                  <FileText className="w-10 h-10 text-amber-600 mb-3" />
                  <h3 className="font-bold text-stone-100 mb-2">Markdown</h3>
                  <p className="text-sm text-stone-400">Escribe en Markdown para formato simple</p>
                </button>

                <button
                  onClick={() => setProfileType('html')}
                  className={`p-6 rounded-xl border-2 transition-all ${
                    profileType === 'html'
                      ? 'bg-amber-700/20 border-amber-700'
                      : 'bg-stone-900 border-stone-700 hover:border-amber-700/50'
                  }`}
                >
                  <Code className="w-10 h-10 text-amber-600 mb-3" />
                  <h3 className="font-bold text-stone-100 mb-2">HTML Personalizado</h3>
                  <p className="text-sm text-stone-400">Control total con HTML y CSS (inline)</p>
                </button>
              </div>

              {profileType === 'markdown' && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-sm font-medium text-stone-300">
                      Contenido Markdown
                    </label>
                    <button
                      onClick={() => setShowPreview(!showPreview)}
                      className="flex items-center gap-2 px-3 py-1 bg-stone-700 rounded-lg hover:bg-stone-600 transition-colors text-sm"
                    >
                      {showPreview ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      {showPreview ? 'Ocultar' : 'Preview'}
                    </button>
                  </div>
                  
                  <div className="grid grid-cols-1 gap-4">
                    <div>
                      <textarea
                        value={customMarkdown}
                        onChange={(e) => setCustomMarkdown(e.target.value)}
                        rows={12}
                        placeholder={`# Mi Perfil

## Sobre mí
Soy un **desarrollador apasionado** por la tecnología...

### Habilidades
- Python
- JavaScript
- React

[Mi GitHub](https://github.com/usuario)`}
                        className="w-full px-4 py-3 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700 focus:border-amber-700 resize-none font-mono text-sm"
                      />
                      <p className="text-xs text-stone-500 mt-2">
                        💡 Usa # para títulos, ** para negrita, * para cursiva, [texto](url) para links
                      </p>
                    </div>
                    
                    {showPreview && (
                      <div className="bg-stone-950 border-2 border-stone-700 rounded-lg p-6">
                        <div className="text-sm text-stone-400 mb-3 font-semibold">Vista Previa:</div>
                        <div 
                          dangerouslySetInnerHTML={{ __html: markdownToHTML(customMarkdown) }}
                          className="markdown-preview"
                        />
                      </div>
                    )}
                  </div>
                </div>
              )}

              {profileType === 'html' && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-sm font-medium text-stone-300">
                      HTML Personalizado
                    </label>
                    <button
                      onClick={() => setShowPreview(!showPreview)}
                      className="flex items-center gap-2 px-3 py-1 bg-stone-700 rounded-lg hover:bg-stone-600 transition-colors text-sm"
                    >
                      {showPreview ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      {showPreview ? 'Ocultar' : 'Preview'}
                    </button>
                  </div>
                  
                  <div className="grid grid-cols-1 gap-4">
                    <div>
                      <textarea
                        value={customHTML}
                        onChange={(e) => setCustomHTML(e.target.value)}
                        rows={12}
                        placeholder={`<div style="padding: 20px;">
  <h1 style="color: #d97706;">Mi Perfil Personalizado</h1>
  <p style="color: #d6d3d1;">Contenido personalizado con HTML...</p>
  <div style="background: #1c1917; padding: 10px; border-radius: 8px;">
    <p>¡Usa estilos inline para personalizar!</p>
  </div>
</div>`}
                        className="w-full px-4 py-3 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700 focus:border-amber-700 resize-none font-mono text-sm"
                      />
                      <p className="text-xs text-stone-500 mt-2">
                        ⚠️ Solo estilos inline. Scripts y eventos serán removidos por seguridad.
                      </p>
                    </div>
                    
                    {showPreview && (
                      <div className="bg-stone-950 border-2 border-stone-700 rounded-lg p-6">
                        <div className="text-sm text-stone-400 mb-3 font-semibold">Vista Previa:</div>
                        <div 
                          dangerouslySetInnerHTML={{ __html: sanitizeHTML(customHTML) }}
                          className="html-preview"
                        />
                      </div>
                    )}
                  </div>
                </div>
              )}

              {profileType === 'auto' && (
                <div className="bg-amber-700/10 border-2 border-amber-700 rounded-lg p-6">
                  <div className="flex items-start gap-3">
                    <div className="text-3xl">ℹ️</div>
                    <div>
                      <h3 className="font-bold text-stone-100 mb-2">Perfil Autogenerado</h3>
                      <p className="text-stone-300 text-sm">
                        Tu perfil se genera automáticamente mostrando tus estadísticas, logros recientes, 
                        cursos completados y actividad. Cambia a Markdown o HTML para personalizarlo completamente.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              <div className="flex gap-3 mt-6">
                <button
                  onClick={saveProfileCustomization}
                  className="flex-1 px-6 py-3 bg-amber-700 border-2 border-amber-800 text-stone-100 rounded-lg hover:bg-amber-800 transition-all font-medium flex items-center justify-center gap-2"
                >
                  <Save className="w-5 h-5" />
                  Guardar Personalización
                </button>
              </div>
            </div>

            {/* Quick Guide */}
            <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-8 border-2 border-stone-700">
              <h3 className="text-xl font-bold text-stone-100 mb-4">Guía Rápida</h3>
              
              <div className="space-y-4">
                <div className="bg-stone-950 rounded-lg p-4 border-2 border-stone-700">
                  <h4 className="font-semibold text-amber-600 mb-2">Markdown</h4>
                  <code className="text-sm text-stone-300 block whitespace-pre">
{`# Título grande
## Título mediano
**Negrita** *Cursiva*
[Link](https://url.com)
\`código inline\`
\`\`\`
bloque de código
\`\`\``}
                  </code>
                </div>

                <div className="bg-stone-950 rounded-lg p-4 border-2 border-stone-700">
                  <h4 className="font-semibold text-amber-600 mb-2">HTML con estilos inline</h4>
                  <code className="text-sm text-stone-300 block whitespace-pre">
{`<div style="padding: 20px;">
  <h1 style="color: #d97706;">Título</h1>
  <p style="color: #d6d3d1;">Párrafo</p>
</div>`}
                  </code>
                </div>
              </div>
            </div>

            {/* Templates */}
            <div className="bg-stone-800 backdrop-blur-sm rounded-xl shadow-lg p-8 border-2 border-stone-700">
              <h3 className="text-xl font-bold text-stone-100 mb-4">Plantillas de Ejemplo</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button
                  onClick={() => {
                    setProfileType('markdown');
                    setCustomMarkdown(`# ¡Hola! Soy ${userData.name} 👋

## Sobre mí
Soy un estudiante apasionado por la programación y la tecnología. 
Me encanta aprender cosas nuevas todos los días.

## Mis habilidades
- 🐍 Python
- 🌐 Desarrollo Web
- 💻 JavaScript

## Proyectos destacados
Actualmente estoy trabajando en varios proyectos interesantes...

[Visita mi GitHub](https://github.com)`);
                  }}
                  className="bg-stone-950 rounded-lg p-4 border-2 border-stone-700 hover:border-amber-700 transition-all text-left"
                >
                  <div className="text-amber-600 font-semibold mb-2">📝 Plantilla Markdown Simple</div>
                  <p className="text-sm text-stone-400">Perfil básico con secciones de sobre mí, habilidades y proyectos</p>
                </button>

                <button
                  onClick={() => {
                    setProfileType('html');
                    setCustomHTML(`<div style="padding: 24px; background: linear-gradient(135deg, #1c1917 0%, #292524 100%); border-radius: 12px;">
  <h1 style="color: #d97706; font-size: 32px; margin-bottom: 16px; font-weight: bold;">
    ${userData.name}
  </h1>
  <p style="color: #d6d3d1; font-size: 18px; margin-bottom: 24px;">
    Desarrollador Full Stack | Aprendiz Eterno
  </p>
  
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-top: 24px;">
    <div style="background: #44403c; padding: 16px; border-radius: 8px; border: 2px solid #78716c;">
      <div style="color: #fbbf24; font-size: 24px; margin-bottom: 8px;">💡</div>
      <div style="color: #fafaf9; font-weight: bold;">Pensamiento creativo</div>
    </div>
    <div style="background: #44403c; padding: 16px; border-radius: 8px; border: 2px solid #78716c;">
      <div style="color: #fbbf24; font-size: 24px; margin-bottom: 8px;">🚀</div>
      <div style="color: #fafaf9; font-weight: bold;">Siempre aprendiendo</div>
    </div>
  </div>
</div>`);
                  }}
                  className="bg-stone-950 rounded-lg p-4 border-2 border-stone-700 hover:border-amber-700 transition-all text-left"
                >
                  <div className="text-amber-600 font-semibold mb-2">🎨 Plantilla HTML Moderna</div>
                  <p className="text-sm text-stone-400">Diseño con gradientes y cards destacados</p>
                </button>

                <button
                  onClick={() => {
                    setProfileType('markdown');
                    setCustomMarkdown(`# ${userData.name} - Desarrollador en Formación

---

### 🎯 Objetivo
Convertirme en un desarrollador full-stack profesional

### 💼 Experiencia
- **Estudiante de Code Dungeon** - 2025
- Completando cursos de Python y Web Development

### 🛠️ Tecnologías que domino
\`\`\`
- Python 🐍
- JavaScript 📜
- HTML/CSS 🎨
- Git & GitHub 🔧
\`\`\`

### 📫 Contacto
- Email: ${userData.email}
${userData.website ? `- Web: ${userData.website}` : ''}

---
*"El código es poesía"* ✨`);
                  }}
                  className="bg-stone-950 rounded-lg p-4 border-2 border-stone-700 hover:border-amber-700 transition-all text-left"
                >
                  <div className="text-amber-600 font-semibold mb-2">💼 Plantilla Profesional</div>
                  <p className="text-sm text-stone-400">Formato tipo CV con secciones profesionales</p>
                </button>

                <button
                  onClick={() => {
                    setProfileType('html');
                    setCustomHTML(`<div style="text-align: center; padding: 40px 20px; background: #1c1917; border-radius: 12px;">
  <div style="font-size: 64px; margin-bottom: 16px;">🎮</div>
  <h1 style="color: #d97706; font-size: 36px; font-weight: bold; margin-bottom: 8px;">
    ${userData.name}
  </h1>
  <p style="color: #a8a29e; font-size: 18px; margin-bottom: 32px;">
    Code Dungeon Explorer | Level ${stats.level}
  </p>
  
  <div style="display: flex; justify-content: center; gap: 24px; flex-wrap: wrap;">
    <div style="background: #44403c; padding: 20px; border-radius: 12px; min-width: 150px; border: 2px solid #d97706;">
      <div style="color: #fbbf24; font-size: 32px; font-weight: bold;">${stats.totalXP}</div>
      <div style="color: #d6d3d1; margin-top: 4px;">XP Total</div>
    </div>
    <div style="background: #44403c; padding: 20px; border-radius: 12px; min-width: 150px; border: 2px solid #d97706;">
      <div style="color: #fbbf24; font-size: 32px; font-weight: bold;">${stats.completedCourses}</div>
      <div style="color: #d6d3d1; margin-top: 4px;">Cursos</div>
    </div>
    <div style="background: #44403c; padding: 20px; border-radius: 12px; min-width: 150px; border: 2px solid #d97706;">
      <div style="color: #fbbf24; font-size: 32px; font-weight: bold;">${stats.achievements}</div>
      <div style="color: #d6d3d1; margin-top: 4px;">Logros</div>
    </div>
  </div>
  
  <p style="color: #d6d3d1; margin-top: 32px; font-size: 16px; max-width: 600px; margin-left: auto; margin-right: auto;">
    Explorando las mazmorras del código, desbloqueando nuevas habilidades cada día. 
    ¡Únete a mi aventura!
  </p>
</div>`);
                  }}
                  className="bg-stone-950 rounded-lg p-4 border-2 border-stone-700 hover:border-amber-700 transition-all text-left"
                >
                  <div className="text-amber-600 font-semibold mb-2">🎮 Plantilla Gamer</div>
                  <p className="text-sm text-stone-400">Estilo gaming con tus estadísticas destacadas</p>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Edit Modal Overlay */}
      {isEditing && (
        <div 
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
          onClick={handleCancel}
        />
      )}
    </div>
  );
}
