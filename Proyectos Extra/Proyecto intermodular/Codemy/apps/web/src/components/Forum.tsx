'use client'

import { useState, useEffect } from 'react'
import { 
  MessageSquare, ThumbsUp, Send, Filter, TrendingUp, Clock, Award, 
  ArrowUp, ArrowDown, Eye, Bookmark, Share2, MoreVertical, Pin,
  CheckCircle2, Flame, Zap, Search, Users, Star
} from 'lucide-react'

interface Comment {
  id: string
  author: string
  content: string
  timestamp: number
  likes: number
  votes?: number
  userVote?: 'up' | 'down'
}

interface Post {
  id: string
  author: string
  title: string
  content: string
  category: string
  timestamp: number
  likes: number
  votes?: number
  userVote?: 'up' | 'down'
  views?: number
  comments: Comment[]
  isPinned?: boolean
  isSolved?: boolean
  tags?: string[]
  authorReputation?: number
  authorRole?: 'user' | 'moderator' | 'admin'
}

interface ForumProps {
  courseId?: string
  title?: string
  categories?: string[]
}

export default function Forum({ 
  courseId, 
  title = 'Foro de la Comunidad',
  categories = ['General', 'Preguntas', 'Proyectos', 'Recursos', 'Eventos']
}: ForumProps) {
  const [posts, setPosts] = useState<Post[]>([])
  const [newPostTitle, setNewPostTitle] = useState('')
  const [newPostContent, setNewPostContent] = useState('')
  const [newPostTags, setNewPostTags] = useState('')
  const [selectedCategory, setSelectedCategory] = useState(categories[0])
  const [filterCategory, setFilterCategory] = useState<string>('Todos')
  const [sortBy, setSortBy] = useState<'hot' | 'recent' | 'popular' | 'trending'>('hot')
  const [activePostId, setActivePostId] = useState<string | null>(null)
  const [newComment, setNewComment] = useState('')
  const [searchQuery, setSearchQuery] = useState('')

  const storageKey = courseId ? `forum-${courseId}` : 'forum-general'

  useEffect(() => {
    const stored = localStorage.getItem(storageKey)
    if (stored) {
      setPosts(JSON.parse(stored))
    } else {
      // Inicializar con array vacío - los posts se crearán por los usuarios
      setPosts([])
      localStorage.setItem(storageKey, JSON.stringify([]))
    }
  }, [storageKey])

  const savePosts = (updatedPosts: Post[]) => {
    setPosts(updatedPosts)
    localStorage.setItem(storageKey, JSON.stringify(updatedPosts))
  }

  const createPost = () => {
    if (!newPostTitle.trim() || !newPostContent.trim()) return

    const newPost: Post = {
      id: Date.now().toString(),
      author: 'Tú',
      title: newPostTitle,
      content: newPostContent,
      category: selectedCategory,
      timestamp: Date.now(),
      likes: 0,
      votes: 0,
      views: 0,
      comments: [],
      tags: newPostTags ? newPostTags.split(',').map(t => t.trim()).filter(Boolean) : [],
      authorReputation: 100,
      authorRole: 'user'
    }

    savePosts([newPost, ...posts])
    setNewPostTitle('')
    setNewPostContent('')
    setNewPostTags('')
  }

  const votePost = (postId: string, voteType: 'up' | 'down') => {
    savePosts(posts.map(post => {
      if (post.id === postId) {
        const currentVote = post.userVote
        let newVotes = post.votes || 0
        let newUserVote: 'up' | 'down' | undefined = voteType

        if (currentVote === voteType) {
          newVotes += voteType === 'up' ? -1 : 1
          newUserVote = undefined
        } else if (currentVote) {
          newVotes += voteType === 'up' ? 2 : -2
        } else {
          newVotes += voteType === 'up' ? 1 : -1
        }

        return { ...post, votes: newVotes, userVote: newUserVote }
      }
      return post
    }))
  }

  const likePost = (postId: string) => {
    savePosts(posts.map(p => 
      p.id === postId ? { ...p, likes: p.likes + 1 } : p
    ))
  }

  const incrementViews = (postId: string) => {
    savePosts(posts.map(p => 
      p.id === postId ? { ...p, views: (p.views || 0) + 1 } : p
    ))
  }

  const addComment = (postId: string) => {
    if (!newComment.trim()) return

    const comment: Comment = {
      id: `${postId}-${Date.now()}`,
      author: 'Tú',
      content: newComment,
      timestamp: Date.now(),
      likes: 0
    }

    savePosts(posts.map(p =>
      p.id === postId ? { ...p, comments: [...p.comments, comment] } : p
    ))
    setNewComment('')
  }

  const likeComment = (postId: string, commentId: string) => {
    savePosts(posts.map(p =>
      p.id === postId
        ? {
            ...p,
            comments: p.comments.map(c =>
              c.id === commentId ? { ...c, likes: c.likes + 1 } : c
            )
          }
        : p
    ))
  }

  const getFilteredAndSortedPosts = () => {
    let filtered = posts.filter(p => 
      filterCategory === 'Todos' || p.category === filterCategory
    )

    // Búsqueda
    if (searchQuery) {
      filtered = filtered.filter(p =>
        p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (p.tags && p.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase())))
      )
    }

    switch (sortBy) {
      case 'hot':
        return filtered.sort((a, b) => {
          if (a.isPinned && !b.isPinned) return -1
          if (!a.isPinned && b.isPinned) return 1
          const aScore = (a.votes || 0) / Math.max(1, (Date.now() - a.timestamp) / (1000 * 60 * 60))
          const bScore = (b.votes || 0) / Math.max(1, (Date.now() - b.timestamp) / (1000 * 60 * 60))
          return bScore - aScore
        })
      case 'popular':
        return filtered.sort((a, b) => (b.votes || 0) - (a.votes || 0))
      case 'trending':
        return filtered.sort((a, b) => {
          const scoreA = (a.votes || 0) + (a.views || 0) * 0.1 + a.comments.length * 2
          const scoreB = (b.votes || 0) + (b.views || 0) * 0.1 + b.comments.length * 2
          return scoreB - scoreA
        })
      default: // recent
        return filtered.sort((a, b) => {
          if (a.isPinned && !b.isPinned) return -1
          if (!a.isPinned && b.isPinned) return 1
          return b.timestamp - a.timestamp
        })
    }
  }

  const formatTime = (timestamp: number) => {
    const diff = Date.now() - timestamp
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)

    if (days > 0) return `hace ${days}d`
    if (hours > 0) return `hace ${hours}h`
    if (minutes > 0) return `hace ${minutes}m`
    return 'ahora'
  }

  return (
    <div className="space-y-6">
      {/* Header con búsqueda */}
      <div className="bg-stone-800 rounded-lg border-2 border-stone-700 p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-3xl font-bold text-stone-100 flex items-center gap-3">
              <MessageSquare className="w-8 h-8 text-amber-600" />
              {title}
            </h2>
            <p className="text-stone-400 mt-1 flex items-center gap-2">
              <Users className="w-4 h-4" />
              {posts.length} {posts.length === 1 ? 'publicación' : 'publicaciones'}
              {searchQuery && ` · ${getFilteredAndSortedPosts().length} resultados`}
            </p>
          </div>

          <div className="flex items-center gap-2 text-sm text-stone-400">
            <span className="flex items-center gap-1">
              <Users className="w-4 h-4 text-green-500" />
              <span className="font-bold text-green-500">42</span> online
            </span>
          </div>
        </div>

        {/* Barra de búsqueda */}
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-stone-400" />
          <input
            type="text"
            placeholder="Buscar en el foro..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-stone-900 border-2 border-stone-700 rounded-lg text-stone-100 focus:border-amber-700 focus:outline-none"
          />
        </div>

        {/* Filtros y ordenamiento */}
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => setSortBy('hot')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition border-2 font-semibold ${
              sortBy === 'hot'
                ? 'bg-amber-700 text-white border-amber-800'
                : 'bg-stone-700 text-stone-300 hover:bg-stone-600 border-stone-600'
            }`}
          >
            <Flame className="w-4 h-4" />
            Hot
          </button>
          <button
            onClick={() => setSortBy('recent')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition border-2 font-semibold ${
              sortBy === 'recent'
                ? 'bg-amber-700 text-white border-amber-800'
                : 'bg-stone-700 text-stone-300 hover:bg-stone-600 border-stone-600'
            }`}
          >
            <Clock className="w-4 h-4" />
            Recientes
          </button>
          <button
            onClick={() => setSortBy('popular')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition border-2 font-semibold ${
              sortBy === 'popular'
                ? 'bg-amber-700 text-white border-amber-800'
                : 'bg-stone-700 text-stone-300 hover:bg-stone-600 border-stone-600'
            }`}
          >
            <ThumbsUp className="w-4 h-4" />
            Popular
          </button>
          <button
            onClick={() => setSortBy('trending')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition border-2 font-semibold ${
              sortBy === 'trending'
                ? 'bg-amber-700 text-white border-amber-800'
                : 'bg-stone-700 text-stone-300 hover:bg-stone-600 border-stone-600'
            }`}
          >
            <Zap className="w-4 h-4" />
            Trending
          </button>
        </div>
      </div>

      {/* Filtros por categoría */}
      <div className="flex items-center gap-2 flex-wrap">
        <Filter className="w-4 h-4 text-stone-500" />
        <button
          onClick={() => setFilterCategory('Todos')}
          className={`px-3 py-1 rounded-lg text-sm transition border-2 ${
            filterCategory === 'Todos'
              ? 'bg-amber-700 text-white border-amber-800'
              : 'bg-stone-800 text-stone-400 hover:bg-stone-700 border-stone-700'
          }`}
        >
          Todos
        </button>
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setFilterCategory(cat)}
            className={`px-3 py-1 rounded-lg text-sm transition border-2 ${
              filterCategory === cat
                ? 'bg-amber-700 text-white border-amber-800'
                : 'bg-stone-800 text-stone-400 hover:bg-stone-700 border-stone-700'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Crear nueva publicación */}
      <div className="bg-stone-800 rounded-lg p-6 border-2 border-stone-700">
        <h3 className="text-lg font-semibold text-stone-100 mb-4 flex items-center gap-2">
          <Send className="w-5 h-5 text-amber-600" />
          Nueva Publicación
        </h3>
        
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="w-full bg-stone-900 border-2 border-stone-700 rounded-lg px-4 py-2 text-stone-100 mb-3 focus:border-amber-700 focus:outline-none"
        >
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Título de tu publicación..."
          value={newPostTitle}
          onChange={(e) => setNewPostTitle(e.target.value)}
          className="w-full bg-stone-900 border-2 border-stone-700 rounded-lg px-4 py-3 text-stone-100 mb-3 focus:border-amber-700 focus:outline-none font-semibold"
        />

        <textarea
          placeholder="Comparte tus ideas, preguntas o proyectos..."
          value={newPostContent}
          onChange={(e) => setNewPostContent(e.target.value)}
          rows={4}
          className="w-full bg-stone-900 border-2 border-stone-700 rounded-lg px-4 py-3 text-stone-100 resize-none focus:border-amber-700 focus:outline-none mb-3"
        />

        <input
          type="text"
          placeholder="Tags (separados por comas): react, nextjs, javascript..."
          value={newPostTags}
          onChange={(e) => setNewPostTags(e.target.value)}
          className="w-full bg-stone-900 border-2 border-stone-700 rounded-lg px-4 py-2 text-stone-100 mb-3 focus:border-amber-700 focus:outline-none text-sm"
        />

        <button
          onClick={createPost}
          disabled={!newPostTitle.trim() || !newPostContent.trim()}
          className="bg-amber-700 text-white px-6 py-2 rounded-lg hover:bg-amber-600 transition flex items-center gap-2 border-2 border-amber-800 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
        >
          <Send className="w-4 h-4" />
          Publicar
        </button>
      </div>

      {/* Lista de publicaciones */}
      <div className="space-y-4">
        {getFilteredAndSortedPosts().map(post => (
          <div key={post.id} className="bg-stone-800 rounded-lg border-2 border-stone-700 overflow-hidden">
            <div className="flex">
              {/* Voting column */}
              <div className="flex flex-col items-center gap-1 bg-stone-900/50 p-4 border-r-2 border-stone-700">
                <button
                  onClick={() => votePost(post.id, 'up')}
                  className={`p-1 rounded hover:bg-stone-700 transition ${
                    post.userVote === 'up' ? 'text-green-500' : 'text-stone-400'
                  }`}
                >
                  <ArrowUp className="w-5 h-5" />
                </button>
                <span className={`font-bold text-sm ${
                  (post.votes || 0) > 0 ? 'text-green-500' : 
                  (post.votes || 0) < 0 ? 'text-red-500' : 
                  'text-stone-400'
                }`}>
                  {post.votes || 0}
                </span>
                <button
                  onClick={() => votePost(post.id, 'down')}
                  className={`p-1 rounded hover:bg-stone-700 transition ${
                    post.userVote === 'down' ? 'text-red-500' : 'text-stone-400'
                  }`}
                >
                  <ArrowDown className="w-5 h-5" />
                </button>
              </div>

              {/* Post content */}
              <div className="flex-1 p-6">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2 flex-wrap">
                      <span className="text-sm font-semibold text-amber-600 flex items-center gap-1">
                        {post.author}
                        {post.authorRole === 'admin' && (
                          <Star className="w-3 h-3 text-amber-500 fill-amber-500" />
                        )}
                        {post.authorRole === 'moderator' && (
                          <Award className="w-3 h-3 text-blue-400" />
                        )}
                      </span>
                      <span className="text-stone-500 text-xs">•</span>
                      <span className="text-stone-500 text-xs">{formatTime(post.timestamp)}</span>
                      <span className={`px-2 py-0.5 rounded-lg text-xs border-2 ${
                        post.category === 'Preguntas' ? 'bg-orange-900/30 text-orange-400 border-orange-800' :
                        post.category === 'Proyectos' ? 'bg-green-900/30 text-green-400 border-green-800' :
                        post.category === 'Recursos' ? 'bg-amber-900/30 text-amber-400 border-amber-800' :
                        'bg-stone-700 text-stone-400 border-stone-600'
                      }`}>
                        {post.category}
                      </span>
                      {post.isPinned && (
                        <span className="px-2 py-0.5 rounded-lg text-xs bg-amber-900/30 text-amber-400 flex items-center gap-1 border-2 border-amber-800">
                          <Pin className="w-3 h-3" />
                          Destacado
                        </span>
                      )}
                      {post.isSolved && (
                        <span className="px-2 py-0.5 rounded-lg text-xs bg-green-900/30 text-green-400 flex items-center gap-1 border-2 border-green-800">
                          <CheckCircle2 className="w-3 h-3" />
                          Resuelto
                        </span>
                      )}
                    </div>
                    <h3 className="text-xl font-bold text-stone-100 mb-2">{post.title}</h3>
                    <p className="text-stone-300 mb-3">{post.content}</p>
                    
                    {/* Tags */}
                    {post.tags && post.tags.length > 0 && (
                      <div className="flex flex-wrap gap-2 mb-3">
                        {post.tags.map((tag, idx) => (
                          <span 
                            key={idx}
                            className="px-2 py-1 bg-stone-900 text-stone-300 text-xs rounded border border-stone-600 hover:border-amber-700 cursor-pointer transition"
                          >
                            #{tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <button
                    onClick={() => setActivePostId(activePostId === post.id ? null : post.id)}
                    className="flex items-center gap-2 text-stone-400 hover:text-amber-600 transition"
                  >
                    <MessageSquare className="w-4 h-4" />
                    <span className="text-sm">{post.comments.length}</span>
                  </button>
                  <div className="flex items-center gap-2 text-stone-500 text-sm">
                    <Eye className="w-4 h-4" />
                    <span>{post.views || 0}</span>
                  </div>
                  <button className="flex items-center gap-2 text-stone-400 hover:text-amber-600 transition">
                    <Bookmark className="w-4 h-4" />
                  </button>
                  <button className="flex items-center gap-2 text-stone-400 hover:text-amber-600 transition">
                    <Share2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Comentarios */}
            {activePostId === post.id && (
              <div className="border-t-2 border-stone-700 bg-stone-900/50 p-6">
                <h4 className="text-sm font-semibold text-stone-400 mb-4">
                  {post.comments.length} {post.comments.length === 1 ? 'Comentario' : 'Comentarios'}
                </h4>

                <div className="space-y-3 mb-4">
                  {post.comments.map(comment => (
                    <div key={comment.id} className="bg-stone-800 rounded-lg p-4 border-2 border-stone-700">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-sm font-semibold text-amber-600">{comment.author}</span>
                        <span className="text-stone-500 text-xs">•</span>
                        <span className="text-stone-500 text-xs">{formatTime(comment.timestamp)}</span>
                      </div>
                      <p className="text-stone-300 text-sm mb-2">{comment.content}</p>
                      <button
                        onClick={() => likeComment(post.id, comment.id)}
                        className="flex items-center gap-1 text-stone-500 hover:text-amber-600 transition text-xs"
                      >
                        <ThumbsUp className="w-3 h-3" />
                        <span>{comment.likes}</span>
                      </button>
                    </div>
                  ))}
                </div>

                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Escribe un comentario..."
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && addComment(post.id)}
                    className="flex-1 bg-stone-800 border-2 border-stone-700 rounded-lg px-4 py-2 text-stone-100 text-sm focus:border-amber-700 focus:outline-none"
                  />
                  <button
                    onClick={() => addComment(post.id)}
                    className="bg-amber-700 text-white px-4 py-2 rounded-lg hover:bg-amber-600 transition border-2 border-amber-800"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}

        {getFilteredAndSortedPosts().length === 0 && (
          <div className="text-center py-12 bg-stone-800 rounded-lg border-2 border-stone-700">
            <MessageSquare className="w-12 h-12 text-stone-600 mx-auto mb-3" />
            <p className="text-stone-400">No hay publicaciones en esta categoría</p>
          </div>
        )}
      </div>
    </div>
  )
}
