'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  MessageSquare, ThumbsUp, MessageCircle, TrendingUp, Star, Award,
  Filter, Search, Users, Flame, Crown, Zap, Eye, Clock, Pin, Lock,
  MoreVertical, Flag, Bookmark, Share2, ArrowUp, ArrowDown, CheckCircle2
} from 'lucide-react';
import { createClient } from '@/lib/supabase/client';

interface User {
  id: string;
  name: string;
  avatar?: string;
  reputation: number;
  badges: string[];
  role: 'user' | 'moderator' | 'admin';
  createdAt: Date;
}

interface Comment {
  id: string;
  userId: string;
  user: User;
  content: string;
  votes: number;
  userVote?: 'up' | 'down';
  createdAt: Date;
  updatedAt?: Date;
  isAccepted?: boolean;
}

interface Post {
  id: string;
  userId: string;
  user: User;
  title: string;
  content: string;
  category: string;
  tags: string[];
  votes: number;
  userVote?: 'up' | 'down';
  views: number;
  comments: Comment[];
  isPinned?: boolean;
  isClosed?: boolean;
  isSolved?: boolean;
  createdAt: Date;
  updatedAt?: Date;
}

export default function CommunityForum() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'hot' | 'new' | 'top' | 'trending'>('hot');
  const [searchQuery, setSearchQuery] = useState('');
  const [showNewPost, setShowNewPost] = useState(false);

  const categories = [
    { id: 'all', name: 'Todas', icon: '🌍', color: 'amber' },
    { id: 'general', name: 'General', icon: '💬', color: 'blue' },
    { id: 'questions', name: 'Preguntas', icon: '❓', color: 'green' },
    { id: 'tutorials', name: 'Tutoriales', icon: '📚', color: 'purple' },
    { id: 'projects', name: 'Proyectos', icon: '🚀', color: 'orange' },
    { id: 'jobs', name: 'Empleo', icon: '💼', color: 'cyan' },
    { id: 'announcements', name: 'Anuncios', icon: '📢', color: 'red' },
  ];

  useEffect(() => {
    loadPosts();
    loadCurrentUser();
  }, [selectedCategory, sortBy]);

  const loadCurrentUser = async () => {
    const supabase = createClient();
    const { data: { user } } = await supabase.auth.getUser();
    
    if (user) {
      // Mock user data - en producción vendría de Supabase
      setCurrentUser({
        id: user.id,
        name: user.email?.split('@')[0] || 'Usuario',
        reputation: 1250,
        badges: ['early-adopter', 'contributor'],
        role: user.email === 'admin@codedungeon.es' ? 'admin' : 'user',
        createdAt: new Date(),
      });
    }
  };

  const loadPosts = async () => {
    setLoading(true);
    
    // Mock data - en producción vendría de Supabase
    const mockPosts: Post[] = [
      {
        id: '1',
        userId: '1',
        user: {
          id: '1',
          name: 'Carlos Dev',
          reputation: 3420,
          badges: ['expert', 'helper'],
          role: 'moderator',
          createdAt: new Date('2024-01-15'),
        },
        title: '¿Cómo empezar con Next.js 14 y App Router?',
        content: 'Estoy migrando mi proyecto de Pages Router a App Router y tengo dudas sobre server components...',
        category: 'questions',
        tags: ['nextjs', 'react', 'typescript'],
        votes: 42,
        views: 328,
        comments: [],
        isSolved: true,
        createdAt: new Date('2024-11-18T10:00:00'),
      },
      {
        id: '2',
        userId: '2',
        user: {
          id: '2',
          name: 'Ana Backend',
          reputation: 5890,
          badges: ['expert', 'contributor', 'top-writer'],
          role: 'admin',
          createdAt: new Date('2023-06-10'),
        },
        title: '🚀 Tutorial: Arquitectura Hexagonal en Node.js',
        content: 'He creado un tutorial completo sobre cómo implementar arquitectura hexagonal (puertos y adaptadores) en un proyecto real de Node.js con TypeScript...',
        category: 'tutorials',
        tags: ['nodejs', 'architecture', 'typescript', 'clean-code'],
        votes: 127,
        views: 1204,
        comments: [],
        isPinned: true,
        createdAt: new Date('2024-11-17T15:30:00'),
      },
      {
        id: '3',
        userId: '3',
        user: {
          id: '3',
          name: 'Luis Frontend',
          reputation: 1820,
          badges: ['contributor'],
          role: 'user',
          createdAt: new Date('2024-03-20'),
        },
        title: 'Mi primer proyecto: Clon de Spotify con React',
        content: 'Después de 3 meses aprendiendo React, he terminado mi primer proyecto grande. Es un clon de Spotify funcional con reproductor de música...',
        category: 'projects',
        tags: ['react', 'proyecto', 'spotify', 'api'],
        votes: 85,
        views: 645,
        comments: [],
        createdAt: new Date('2024-11-16T12:20:00'),
      },
    ];

    setPosts(mockPosts);
    setLoading(false);
  };

  const votePost = (postId: string, voteType: 'up' | 'down') => {
    setPosts(posts.map(post => {
      if (post.id === postId) {
        const currentVote = post.userVote;
        let newVotes = post.votes;
        let newUserVote: 'up' | 'down' | undefined = voteType;

        if (currentVote === voteType) {
          // Quitar voto
          newVotes += voteType === 'up' ? -1 : 1;
          newUserVote = undefined;
        } else if (currentVote) {
          // Cambiar voto
          newVotes += voteType === 'up' ? 2 : -2;
        } else {
          // Nuevo voto
          newVotes += voteType === 'up' ? 1 : -1;
        }

        return { ...post, votes: newVotes, userVote: newUserVote };
      }
      return post;
    }));
  };

  const getFilteredPosts = () => {
    let filtered = posts;

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(p => p.category === selectedCategory);
    }

    if (searchQuery) {
      filtered = filtered.filter(p =>
        p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }

    // Ordenar
    filtered = [...filtered].sort((a, b) => {
      if (a.isPinned && !b.isPinned) return -1;
      if (!a.isPinned && b.isPinned) return 1;

      switch (sortBy) {
        case 'hot':
          // Algoritmo simple de "hot" - combina votos recientes
          const aScore = a.votes / Math.max(1, (Date.now() - a.createdAt.getTime()) / (1000 * 60 * 60));
          const bScore = b.votes / Math.max(1, (Date.now() - b.createdAt.getTime()) / (1000 * 60 * 60));
          return bScore - aScore;
        case 'new':
          return b.createdAt.getTime() - a.createdAt.getTime();
        case 'top':
          return b.votes - a.votes;
        case 'trending':
          return (b.votes + b.views) - (a.votes + a.views);
        default:
          return 0;
      }
    });

    return filtered;
  };

  const formatTime = (date: Date) => {
    const now = Date.now();
    const diff = now - date.getTime();
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days > 0) return `hace ${days}d`;
    if (hours > 0) return `hace ${hours}h`;
    if (minutes > 0) return `hace ${minutes}m`;
    return 'ahora';
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'admin': return 'text-red-500';
      case 'moderator': return 'text-purple-500';
      default: return 'text-stone-400';
    }
  };

  const getRoleBadge = (role: string) => {
    switch (role) {
      case 'admin': return <Crown className="w-3 h-3 text-red-500" />;
      case 'moderator': return <Award className="w-3 h-3 text-purple-500" />;
      default: return null;
    }
  };

  return (
    <div className="min-h-screen bg-stone-900">
      {/* Header */}
      <div className="bg-stone-800/50 backdrop-blur-sm border-b-2 border-stone-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between mb-4">
            <Link href="/dashboard" className="text-2xl font-bold text-white flex items-center gap-3">
              <MessageSquare className="w-8 h-8 text-amber-600" />
              Foro de la Comunidad
            </Link>
            
            <div className="flex items-center gap-4">
              {currentUser && (
                <div className="flex items-center gap-2 text-sm">
                  <div className="flex items-center gap-1 text-amber-600">
                    <Star className="w-4 h-4 fill-amber-600" />
                    <span className="font-bold">{currentUser.reputation}</span>
                  </div>
                </div>
              )}
              
              <button
                onClick={() => setShowNewPost(true)}
                className="bg-amber-700 hover:bg-amber-600 text-white px-4 py-2 rounded-lg font-semibold transition flex items-center gap-2"
              >
                <MessageSquare className="w-4 h-4" />
                Nueva Publicación
              </button>
            </div>
          </div>

          {/* Search & Filters */}
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-stone-400" />
              <input
                type="text"
                placeholder="Buscar en el foro..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-stone-900 border-2 border-stone-700 rounded-lg text-stone-100 focus:border-amber-700 focus:outline-none"
              />
            </div>

            <div className="flex gap-2 flex-wrap">
              {['hot', 'new', 'top', 'trending'].map((sort) => (
                <button
                  key={sort}
                  onClick={() => setSortBy(sort as any)}
                  className={`px-4 py-2 rounded-lg font-semibold transition flex items-center gap-2 ${
                    sortBy === sort
                      ? 'bg-amber-700 text-white'
                      : 'bg-stone-800 text-stone-300 hover:bg-stone-700'
                  }`}
                >
                  {sort === 'hot' && <Flame className="w-4 h-4" />}
                  {sort === 'new' && <Clock className="w-4 h-4" />}
                  {sort === 'top' && <TrendingUp className="w-4 h-4" />}
                  {sort === 'trending' && <Zap className="w-4 h-4" />}
                  {sort.charAt(0).toUpperCase() + sort.slice(1)}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar - Categorías */}
          <div className="lg:col-span-1">
            <div className="bg-stone-800 rounded-lg border-2 border-stone-700 p-4 sticky top-24">
              <h3 className="text-lg font-bold text-stone-100 mb-4 flex items-center gap-2">
                <Filter className="w-5 h-5 text-amber-600" />
                Categorías
              </h3>
              
              <div className="space-y-2">
                {categories.map((cat) => (
                  <button
                    key={cat.id}
                    onClick={() => setSelectedCategory(cat.id)}
                    className={`w-full text-left px-4 py-2 rounded-lg transition flex items-center gap-3 ${
                      selectedCategory === cat.id
                        ? 'bg-amber-700 text-white'
                        : 'text-stone-300 hover:bg-stone-700'
                    }`}
                  >
                    <span className="text-xl">{cat.icon}</span>
                    <span className="font-semibold">{cat.name}</span>
                  </button>
                ))}
              </div>

              {/* Stats */}
              <div className="mt-6 pt-6 border-t-2 border-stone-700">
                <h4 className="text-sm font-bold text-stone-400 mb-3">Estadísticas</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between text-stone-300">
                    <span>Publicaciones</span>
                    <span className="font-bold text-amber-600">{posts.length}</span>
                  </div>
                  <div className="flex justify-between text-stone-300">
                    <span>Usuarios activos</span>
                    <span className="font-bold text-green-600">342</span>
                  </div>
                  <div className="flex justify-between text-stone-300">
                    <span>Hoy</span>
                    <span className="font-bold text-blue-600">15 nuevos</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Posts */}
          <div className="lg:col-span-3 space-y-4">
            {loading ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-amber-600 border-t-transparent"></div>
                <p className="text-stone-400 mt-4">Cargando publicaciones...</p>
              </div>
            ) : getFilteredPosts().length === 0 ? (
              <div className="bg-stone-800 rounded-lg border-2 border-stone-700 p-12 text-center">
                <MessageSquare className="w-16 h-16 text-stone-600 mx-auto mb-4" />
                <p className="text-stone-400 text-lg">No hay publicaciones en esta categoría</p>
                <p className="text-stone-500 text-sm mt-2">¡Sé el primero en publicar!</p>
              </div>
            ) : (
              getFilteredPosts().map((post) => (
                <div
                  key={post.id}
                  className={`bg-stone-800 rounded-lg border-2 transition-all hover:border-amber-700/50 ${
                    post.isPinned ? 'border-amber-700' : 'border-stone-700'
                  }`}
                >
                  <div className="p-6">
                    <div className="flex gap-4">
                      {/* Votos */}
                      <div className="flex flex-col items-center gap-1 min-w-[50px]">
                        <button
                          onClick={() => votePost(post.id, 'up')}
                          className={`p-1 rounded transition ${
                            post.userVote === 'up'
                              ? 'text-amber-600'
                              : 'text-stone-400 hover:text-amber-600'
                          }`}
                        >
                          <ArrowUp className="w-6 h-6" />
                        </button>
                        
                        <span className={`text-xl font-bold ${
                          post.votes > 0 ? 'text-green-500' : post.votes < 0 ? 'text-red-500' : 'text-stone-400'
                        }`}>
                          {post.votes}
                        </span>
                        
                        <button
                          onClick={() => votePost(post.id, 'down')}
                          className={`p-1 rounded transition ${
                            post.userVote === 'down'
                              ? 'text-red-600'
                              : 'text-stone-400 hover:text-red-600'
                          }`}
                        >
                          <ArrowDown className="w-6 h-6" />
                        </button>
                      </div>

                      {/* Contenido */}
                      <div className="flex-1">
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center gap-2 flex-wrap">
                            {post.isPinned && (
                              <Pin className="w-4 h-4 text-amber-600" />
                            )}
                            {post.isSolved && (
                              <CheckCircle2 className="w-4 h-4 text-green-500" />
                            )}
                            {post.isClosed && (
                              <Lock className="w-4 h-4 text-red-500" />
                            )}
                          </div>
                        </div>

                        <Link href={`/community/post/${post.id}`}>
                          <h3 className="text-xl font-bold text-stone-100 hover:text-amber-600 transition mb-2">
                            {post.title}
                          </h3>
                        </Link>

                        <p className="text-stone-300 mb-3 line-clamp-2">
                          {post.content}
                        </p>

                        <div className="flex flex-wrap gap-2 mb-3">
                          {post.tags.map((tag) => (
                            <span
                              key={tag}
                              className="px-3 py-1 bg-stone-900 border border-stone-700 rounded-full text-xs text-stone-300 hover:border-amber-700 hover:text-amber-600 transition cursor-pointer"
                            >
                              #{tag}
                            </span>
                          ))}
                        </div>

                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-4 text-sm text-stone-400">
                            <div className="flex items-center gap-2">
                              <div className="w-8 h-8 bg-gradient-to-br from-amber-600 to-orange-600 rounded-full flex items-center justify-center text-white font-bold">
                                {post.user.name.charAt(0).toUpperCase()}
                              </div>
                              <div>
                                <div className="flex items-center gap-1">
                                  <span className={`font-semibold ${getRoleColor(post.user.role)}`}>
                                    {post.user.name}
                                  </span>
                                  {getRoleBadge(post.user.role)}
                                </div>
                                <div className="flex items-center gap-2 text-xs">
                                  <span>{post.user.reputation} reputación</span>
                                  <span>•</span>
                                  <span>{formatTime(post.createdAt)}</span>
                                </div>
                              </div>
                            </div>
                          </div>

                          <div className="flex items-center gap-4 text-sm text-stone-400">
                            <div className="flex items-center gap-1">
                              <Eye className="w-4 h-4" />
                              <span>{post.views}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <MessageCircle className="w-4 h-4" />
                              <span>{post.comments.length}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
