'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  Users, MessageCircle, UserPlus, Search, Send, MoreVertical, 
  Check, X, Clock, Star, Settings, Phone, Video, Paperclip,
  Smile, Image, ArrowLeft, Hash, Lock, Globe, Bell, BellOff
} from 'lucide-react';

type Friend = {
  id: string;
  name: string;
  username: string;
  avatar: number;
  level: number;
  status: 'online' | 'offline' | 'busy';
  lastSeen?: string;
  mutualFriends?: number;
};

type FriendRequest = {
  id: string;
  from: Friend;
  timestamp: string;
};

type Message = {
  id: string;
  senderId: string;
  content: string;
  timestamp: string;
  read: boolean;
};

type Chat = {
  id: string;
  type: 'direct' | 'group';
  name: string;
  avatar?: number;
  participants: Friend[];
  lastMessage?: Message;
  unreadCount: number;
  isTyping?: boolean;
};

type Group = {
  id: string;
  name: string;
  description: string;
  members: number;
  privacy: 'public' | 'private' | 'premium';
  category: string;
  avatar: string;
  joined: boolean;
  isPremium?: boolean;
  cost?: number;
};

const AVATAR_COLORS = [
  'from-amber-500 to-orange-500',
  'from-cyan-500 to-blue-500',
  'from-green-500 to-emerald-500',
  'from-purple-500 to-pink-500',
  'from-red-500 to-rose-500',
  'from-yellow-500 to-amber-500',
  'from-teal-500 to-cyan-500',
  'from-indigo-500 to-purple-500',
];

export default function SocialPage() {
  const [activeTab, setActiveTab] = useState<'friends' | 'messages' | 'groups'>('friends');
  const [friendsView, setFriendsView] = useState<'all' | 'online' | 'requests'>('all');
  const [selectedChat, setSelectedChat] = useState<Chat | null>(null);
  const [messageInput, setMessageInput] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [isMounted, setIsMounted] = useState(false);

  // Mock data - En producción vendría de un backend
  const [friends, setFriends] = useState<Friend[]>([
    {
      id: '1',
      name: 'Ana García',
      username: 'anadev',
      avatar: 0,
      level: 15,
      status: 'online',
      mutualFriends: 5
    },
    {
      id: '2',
      name: 'Carlos Ruiz',
      username: 'carlosdev',
      avatar: 1,
      level: 12,
      status: 'online',
      mutualFriends: 3
    },
    {
      id: '3',
      name: 'María López',
      username: 'mariacode',
      avatar: 2,
      level: 18,
      status: 'offline',
      lastSeen: 'Hace 2 horas',
      mutualFriends: 7
    },
    {
      id: '4',
      name: 'Juan Pérez',
      username: 'juanpy',
      avatar: 3,
      level: 10,
      status: 'busy',
      mutualFriends: 2
    },
  ]);

  const [friendRequests, setFriendRequests] = useState<FriendRequest[]>([
    {
      id: '1',
      from: {
        id: '5',
        name: 'Laura Martínez',
        username: 'lauracodes',
        avatar: 4,
        level: 14,
        status: 'online',
        mutualFriends: 4
      },
      timestamp: 'Hace 5 min'
    },
    {
      id: '2',
      from: {
        id: '6',
        name: 'David Silva',
        username: 'davidjs',
        avatar: 5,
        level: 16,
        status: 'offline',
        mutualFriends: 2
      },
      timestamp: 'Hace 1 hora'
    }
  ]);

  const [chats, setChats] = useState<Chat[]>([
    {
      id: '1',
      type: 'direct',
      name: 'Ana García',
      avatar: 0,
      participants: [friends[0]],
      lastMessage: {
        id: '1',
        senderId: '1',
        content: '¿Terminaste el curso de Python?',
        timestamp: 'Hace 2 min',
        read: false
      },
      unreadCount: 2,
      isTyping: false
    },
    {
      id: '2',
      type: 'group',
      name: 'Grupo Python 2025',
      participants: [friends[0], friends[1], friends[2]],
      lastMessage: {
        id: '2',
        senderId: '2',
        content: 'Carlos: Mañana hay nueva lección',
        timestamp: 'Hace 10 min',
        read: true
      },
      unreadCount: 0,
      isTyping: true
    },
    {
      id: '3',
      type: 'direct',
      name: 'María López',
      avatar: 2,
      participants: [friends[2]],
      lastMessage: {
        id: '3',
        senderId: '3',
        content: '¡Gracias por la ayuda! 🎉',
        timestamp: 'Ayer',
        read: true
      },
      unreadCount: 0
    }
  ]);

  const [groups, setGroups] = useState<Group[]>([
    {
      id: '1',
      name: 'Python Developers',
      description: 'Comunidad de desarrolladores Python',
      members: 1234,
      privacy: 'public',
      category: 'Programación',
      avatar: '🐍',
      joined: true
    },
    {
      id: '2',
      name: 'Web Dev Masters',
      description: 'Aprende desarrollo web moderno',
      members: 856,
      privacy: 'public',
      category: 'Desarrollo Web',
      avatar: '🌐',
      joined: true
    },
    {
      id: '3',
      name: 'JavaScript Ninjas',
      description: 'Todo sobre JS, React, Node',
      members: 2341,
      privacy: 'public',
      category: 'JavaScript',
      avatar: '⚡',
      joined: false
    },
    {
      id: '4',
      name: 'Code Dungeon VIP',
      description: 'Grupo exclusivo de estudiantes destacados',
      members: 42,
      privacy: 'private',
      category: 'Comunidad',
      avatar: '👑',
      joined: false
    },
    {
      id: '5',
      name: 'Premium Mentors Club',
      description: 'Mentoría personalizada y proyectos reales',
      members: 15,
      privacy: 'premium',
      category: 'Mentoría',
      avatar: '🎓',
      joined: false,
      isPremium: true,
      cost: 500
    },
    {
      id: '6',
      name: 'AI & ML Masters',
      description: 'Grupo premium de IA y Machine Learning',
      members: 28,
      privacy: 'premium',
      category: 'IA',
      avatar: '🤖',
      joined: false,
      isPremium: true,
      cost: 800
    }
  ]);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const handleAcceptRequest = (requestId: string) => {
    const request = friendRequests.find(r => r.id === requestId);
    if (request) {
      setFriends([...friends, request.from]);
      setFriendRequests(friendRequests.filter(r => r.id !== requestId));
    }
  };

  const handleRejectRequest = (requestId: string) => {
    setFriendRequests(friendRequests.filter(r => r.id !== requestId));
  };

  const handleSendMessage = () => {
    if (!messageInput.trim() || !selectedChat) return;
    
    // Aquí iría la lógica para enviar el mensaje al backend
    setMessageInput('');
  };

  const handleJoinGroup = (groupId: string) => {
    setGroups(groups.map(g => 
      g.id === groupId ? { ...g, joined: true, members: g.members + 1 } : g
    ));
  };

  const handleLeaveGroup = (groupId: string) => {
    setGroups(groups.map(g => 
      g.id === groupId ? { ...g, joined: false, members: g.members - 1 } : g
    ));
  };

  const getInitials = (name: string) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  const filteredFriends = friends.filter(f => {
    const matchesSearch = f.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         f.username.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesView = friendsView === 'all' || 
                       (friendsView === 'online' && f.status === 'online');
    return matchesSearch && matchesView;
  });

  const filteredGroups = groups.filter(g =>
    g.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    g.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

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
              <h1 className="text-2xl font-bold bg-gradient-to-r from-amber-600 to-amber-500 bg-clip-text text-transparent">
                Social Hub
              </h1>
            </div>
            <div className="flex items-center gap-3">
              <button className="p-2 bg-stone-700 hover:bg-stone-600 rounded-lg transition-colors">
                <Bell className="w-5 h-5 text-stone-300" />
              </button>
              <button className="p-2 bg-stone-700 hover:bg-stone-600 rounded-lg transition-colors">
                <Settings className="w-5 h-5 text-stone-300" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Main Tabs */}
        <div className="mb-6">
          <div className="flex gap-2 bg-stone-800 rounded-xl p-2 border-2 border-stone-700">
            <button
              onClick={() => setActiveTab('friends')}
              className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all flex items-center justify-center gap-2 ${
                activeTab === 'friends'
                  ? 'bg-amber-700 border-2 border-amber-800 text-stone-100'
                  : 'text-stone-400 hover:text-stone-100 hover:bg-stone-700'
              }`}
            >
              <Users className="w-5 h-5" />
              Amigos ({friends.length})
            </button>
            <button
              onClick={() => setActiveTab('messages')}
              className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all flex items-center justify-center gap-2 relative ${
                activeTab === 'messages'
                  ? 'bg-amber-700 border-2 border-amber-800 text-stone-100'
                  : 'text-stone-400 hover:text-stone-100 hover:bg-stone-700'
              }`}
            >
              <MessageCircle className="w-5 h-5" />
              Mensajes
              {chats.some(c => c.unreadCount > 0) && (
                <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full"></span>
              )}
            </button>
            <button
              onClick={() => setActiveTab('groups')}
              className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all flex items-center justify-center gap-2 ${
                activeTab === 'groups'
                  ? 'bg-amber-700 border-2 border-amber-800 text-stone-100'
                  : 'text-stone-400 hover:text-stone-100 hover:bg-stone-700'
              }`}
            >
              <Hash className="w-5 h-5" />
              Grupos ({groups.filter(g => g.joined).length})
            </button>
          </div>
        </div>

        {/* Friends Tab */}
        {activeTab === 'friends' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Friends List */}
            <div className="lg:col-span-2 space-y-4">
              {/* Search and Filter */}
              <div className="bg-stone-800 rounded-xl p-4 border-2 border-stone-700">
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-stone-400" />
                    <input
                      type="text"
                      placeholder="Buscar amigos..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full pl-10 pr-4 py-2 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700"
                    />
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setFriendsView('all')}
                      className={`px-4 py-2 rounded-lg font-medium transition-all ${
                        friendsView === 'all'
                          ? 'bg-amber-700 text-stone-100'
                          : 'bg-stone-700 text-stone-300 hover:bg-stone-600'
                      }`}
                    >
                      Todos
                    </button>
                    <button
                      onClick={() => setFriendsView('online')}
                      className={`px-4 py-2 rounded-lg font-medium transition-all ${
                        friendsView === 'online'
                          ? 'bg-amber-700 text-stone-100'
                          : 'bg-stone-700 text-stone-300 hover:bg-stone-600'
                      }`}
                    >
                      Online
                    </button>
                    <button
                      onClick={() => setFriendsView('requests')}
                      className={`px-4 py-2 rounded-lg font-medium transition-all relative ${
                        friendsView === 'requests'
                          ? 'bg-amber-700 text-stone-100'
                          : 'bg-stone-700 text-stone-300 hover:bg-stone-600'
                      }`}
                    >
                      Solicitudes
                      {friendRequests.length > 0 && (
                        <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                          {friendRequests.length}
                        </span>
                      )}
                    </button>
                  </div>
                </div>
              </div>

              {/* Friend Requests */}
              {friendsView === 'requests' && (
                <div className="space-y-3">
                  {friendRequests.length === 0 ? (
                    <div className="bg-stone-800 rounded-xl p-12 border-2 border-stone-700 text-center">
                      <UserPlus className="w-16 h-16 text-stone-500 mx-auto mb-4" />
                      <p className="text-stone-400">No tienes solicitudes pendientes</p>
                    </div>
                  ) : (
                    friendRequests.map(request => (
                      <div key={request.id} className="bg-stone-800 rounded-xl p-6 border-2 border-stone-700 hover:border-amber-700 transition-all">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-4">
                            <div className={`w-16 h-16 bg-gradient-to-br ${AVATAR_COLORS[request.from.avatar]} rounded-xl flex items-center justify-center text-white font-bold text-xl`}>
                              {getInitials(request.from.name)}
                            </div>
                            <div>
                              <h3 className="text-lg font-bold text-stone-100">{request.from.name}</h3>
                              <p className="text-sm text-stone-400">@{request.from.username} • Nivel {request.from.level}</p>
                              <p className="text-xs text-stone-500">{request.from.mutualFriends} amigos en común</p>
                            </div>
                          </div>
                          <div className="flex gap-2">
                            <button
                              onClick={() => handleAcceptRequest(request.id)}
                              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
                            >
                              <Check className="w-4 h-4" />
                              Aceptar
                            </button>
                            <button
                              onClick={() => handleRejectRequest(request.id)}
                              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
                            >
                              <X className="w-4 h-4" />
                              Rechazar
                            </button>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* Friends Grid */}
              {friendsView !== 'requests' && (
                <div className="grid grid-cols-1 gap-4">
                  {filteredFriends.map(friend => (
                    <div key={friend.id} className="bg-stone-800 rounded-xl p-6 border-2 border-stone-700 hover:border-amber-700 transition-all group">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <div className="relative">
                            <div className={`w-16 h-16 bg-gradient-to-br ${AVATAR_COLORS[friend.avatar]} rounded-xl flex items-center justify-center text-white font-bold text-xl`}>
                              {getInitials(friend.name)}
                            </div>
                            <div className={`absolute bottom-0 right-0 w-4 h-4 rounded-full border-2 border-stone-800 ${
                              friend.status === 'online' ? 'bg-green-500' :
                              friend.status === 'busy' ? 'bg-yellow-500' :
                              'bg-stone-500'
                            }`}></div>
                          </div>
                          <div>
                            <h3 className="text-lg font-bold text-stone-100">{friend.name}</h3>
                            <p className="text-sm text-stone-400">@{friend.username} • Nivel {friend.level}</p>
                            {friend.status === 'online' ? (
                              <p className="text-xs text-green-400">● En línea</p>
                            ) : friend.lastSeen ? (
                              <p className="text-xs text-stone-500">{friend.lastSeen}</p>
                            ) : (
                              <p className="text-xs text-yellow-400">● Ocupado</p>
                            )}
                          </div>
                        </div>
                        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button className="px-4 py-2 bg-amber-700 hover:bg-amber-600 text-stone-100 rounded-lg font-medium transition-colors flex items-center gap-2">
                            <MessageCircle className="w-4 h-4" />
                            Mensaje
                          </button>
                          <button className="p-2 bg-stone-700 hover:bg-stone-600 text-stone-300 rounded-lg transition-colors">
                            <MoreVertical className="w-5 h-5" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Sidebar - Find Friends */}
            <div className="space-y-4">
              <div className="bg-stone-800 rounded-xl p-6 border-2 border-stone-700">
                <h3 className="text-xl font-bold text-stone-100 mb-4 flex items-center gap-2">
                  <UserPlus className="w-5 h-5 text-amber-600" />
                  Buscar Amigos
                </h3>
                <button className="w-full px-4 py-3 bg-amber-700 hover:bg-amber-600 text-stone-100 rounded-lg font-medium transition-colors flex items-center justify-center gap-2">
                  <Search className="w-5 h-5" />
                  Explorar Usuarios
                </button>
              </div>

              <div className="bg-stone-800 rounded-xl p-6 border-2 border-stone-700">
                <h3 className="text-lg font-bold text-stone-100 mb-4">Estadísticas</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-stone-400">Total amigos:</span>
                    <span className="text-stone-100 font-bold">{friends.length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-stone-400">En línea:</span>
                    <span className="text-green-400 font-bold">{friends.filter(f => f.status === 'online').length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-stone-400">Solicitudes:</span>
                    <span className="text-amber-600 font-bold">{friendRequests.length}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Messages Tab */}
        {activeTab === 'messages' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Chats List */}
            <div className="lg:col-span-1 bg-stone-800 rounded-xl border-2 border-stone-700 overflow-hidden">
              <div className="p-4 border-b-2 border-stone-700">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-stone-400" />
                  <input
                    type="text"
                    placeholder="Buscar conversaciones..."
                    className="w-full pl-10 pr-4 py-2 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700"
                  />
                </div>
              </div>
              <div className="overflow-y-auto" style={{ maxHeight: '600px' }}>
                {chats.map(chat => (
                  <button
                    key={chat.id}
                    onClick={() => setSelectedChat(chat)}
                    className={`w-full p-4 border-b-2 border-stone-700 hover:bg-stone-700 transition-colors text-left ${
                      selectedChat?.id === chat.id ? 'bg-stone-700' : ''
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className="relative">
                        {chat.type === 'direct' ? (
                          <div className={`w-12 h-12 bg-gradient-to-br ${AVATAR_COLORS[chat.avatar || 0]} rounded-xl flex items-center justify-center text-white font-bold`}>
                            {getInitials(chat.name)}
                          </div>
                        ) : (
                          <div className="w-12 h-12 bg-amber-700 rounded-xl flex items-center justify-center text-white text-xl">
                            <Hash className="w-6 h-6" />
                          </div>
                        )}
                        {chat.unreadCount > 0 && (
                          <div className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                            {chat.unreadCount}
                          </div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <h4 className="font-semibold text-stone-100 truncate">{chat.name}</h4>
                          <span className="text-xs text-stone-500">{chat.lastMessage?.timestamp}</span>
                        </div>
                        <p className="text-sm text-stone-400 truncate">
                          {chat.isTyping ? (
                            <span className="text-amber-600 italic">Escribiendo...</span>
                          ) : (
                            chat.lastMessage?.content
                          )}
                        </p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Chat Window */}
            <div className="lg:col-span-2">
              {selectedChat ? (
                <div className="bg-stone-800 rounded-xl border-2 border-stone-700 flex flex-col" style={{ height: '700px' }}>
                  {/* Chat Header */}
                  <div className="p-4 border-b-2 border-stone-700 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {selectedChat.type === 'direct' ? (
                        <div className={`w-10 h-10 bg-gradient-to-br ${AVATAR_COLORS[selectedChat.avatar || 0]} rounded-lg flex items-center justify-center text-white font-bold`}>
                          {getInitials(selectedChat.name)}
                        </div>
                      ) : (
                        <div className="w-10 h-10 bg-amber-700 rounded-lg flex items-center justify-center text-white">
                          <Hash className="w-5 h-5" />
                        </div>
                      )}
                      <div>
                        <h3 className="font-bold text-stone-100">{selectedChat.name}</h3>
                        {selectedChat.type === 'group' ? (
                          <p className="text-xs text-stone-400">{selectedChat.participants.length} miembros</p>
                        ) : (
                          <p className="text-xs text-green-400">En línea</p>
                        )}
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <button className="p-2 bg-stone-700 hover:bg-stone-600 rounded-lg transition-colors">
                        <Phone className="w-5 h-5 text-stone-300" />
                      </button>
                      <button className="p-2 bg-stone-700 hover:bg-stone-600 rounded-lg transition-colors">
                        <Video className="w-5 h-5 text-stone-300" />
                      </button>
                      <button className="p-2 bg-stone-700 hover:bg-stone-600 rounded-lg transition-colors">
                        <MoreVertical className="w-5 h-5 text-stone-300" />
                      </button>
                    </div>
                  </div>

                  {/* Messages */}
                  <div className="flex-1 p-4 overflow-y-auto bg-stone-950">
                    <div className="space-y-4">
                      <div className="flex justify-start">
                        <div className="bg-stone-800 rounded-lg p-3 max-w-md border-2 border-stone-700">
                          <p className="text-stone-100">¡Hola! ¿Cómo vas con el curso de Python?</p>
                          <span className="text-xs text-stone-500 mt-1 block">10:30</span>
                        </div>
                      </div>
                      <div className="flex justify-end">
                        <div className="bg-amber-700 rounded-lg p-3 max-w-md">
                          <p className="text-white">¡Muy bien! Ya terminé la lección de funciones</p>
                          <span className="text-xs text-amber-200 mt-1 block">10:32</span>
                        </div>
                      </div>
                      <div className="flex justify-start">
                        <div className="bg-stone-800 rounded-lg p-3 max-w-md border-2 border-stone-700">
                          <p className="text-stone-100">¿Terminaste el curso de Python?</p>
                          <span className="text-xs text-stone-500 mt-1 block">Ahora</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Message Input */}
                  <div className="p-4 border-t-2 border-stone-700">
                    <div className="flex gap-2">
                      <button className="p-2 bg-stone-700 hover:bg-stone-600 rounded-lg transition-colors">
                        <Paperclip className="w-5 h-5 text-stone-300" />
                      </button>
                      <button className="p-2 bg-stone-700 hover:bg-stone-600 rounded-lg transition-colors">
                        <Image className="w-5 h-5 text-stone-300" />
                      </button>
                      <input
                        type="text"
                        value={messageInput}
                        onChange={(e) => setMessageInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                        placeholder="Escribe un mensaje..."
                        className="flex-1 px-4 py-2 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700"
                      />
                      <button className="p-2 bg-stone-700 hover:bg-stone-600 rounded-lg transition-colors">
                        <Smile className="w-5 h-5 text-stone-300" />
                      </button>
                      <button
                        onClick={handleSendMessage}
                        className="px-4 py-2 bg-amber-700 hover:bg-amber-600 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
                      >
                        <Send className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-stone-800 rounded-xl border-2 border-stone-700 flex items-center justify-center" style={{ height: '700px' }}>
                  <div className="text-center">
                    <MessageCircle className="w-16 h-16 text-stone-500 mx-auto mb-4" />
                    <p className="text-stone-400 text-lg">Selecciona una conversación para empezar</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Groups Tab */}
        {activeTab === 'groups' && (
          <div className="space-y-6">
            {/* Search */}
            <div className="bg-stone-800 rounded-xl p-4 border-2 border-stone-700">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-stone-400" />
                <input
                  type="text"
                  placeholder="Buscar grupos..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-stone-950 border-2 border-stone-700 rounded-lg text-stone-100 focus:outline-none focus:ring-2 focus:ring-amber-700"
                />
              </div>
            </div>

            {/* Groups Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredGroups.map(group => (
                <div key={group.id} className={`bg-stone-800 rounded-xl p-6 border-2 transition-all ${
                  group.isPremium 
                    ? 'border-amber-500/50 bg-gradient-to-br from-stone-800 to-amber-900/10' 
                    : 'border-stone-700 hover:border-amber-700'
                }`}>
                  {group.isPremium && (
                    <div className="mb-3">
                      <span className="inline-flex items-center gap-1 px-2 py-1 bg-amber-500/20 border border-amber-500/30 rounded-full text-xs text-amber-400 font-bold">
                        ⭐ PREMIUM
                      </span>
                    </div>
                  )}
                  <div className="text-center mb-4">
                    <div className={`w-20 h-20 rounded-xl flex items-center justify-center text-4xl mx-auto mb-3 ${
                      group.isPremium ? 'bg-gradient-to-br from-amber-600 to-yellow-600' : 'bg-amber-700'
                    }`}>
                      {group.avatar}
                    </div>
                    <h3 className="text-xl font-bold text-stone-100 mb-1">{group.name}</h3>
                    <p className="text-sm text-stone-400 mb-2">{group.description}</p>
                    <div className="flex items-center justify-center gap-4 text-sm text-stone-500">
                      <span className="flex items-center gap-1">
                        <Users className="w-4 h-4" />
                        {group.members} miembros
                      </span>
                      <span className="flex items-center gap-1">
                        {group.privacy === 'public' ? (
                          <><Globe className="w-4 h-4" /> Público</>
                        ) : group.privacy === 'premium' ? (
                          <><Star className="w-4 h-4 text-amber-400" /> Premium</>
                        ) : (
                          <><Lock className="w-4 h-4" /> Privado</>
                        )}
                      </span>
                    </div>
                    {group.cost && (
                      <div className="mt-2 flex items-center justify-center gap-1 text-yellow-400">
                        <Star className="w-4 h-4" />
                        <span className="font-bold">{group.cost} Coins</span>
                      </div>
                    )}
                  </div>
                  <div className="space-y-2">
                    {group.joined ? (
                      <>
                        <button className="w-full px-4 py-2 bg-amber-700 hover:bg-amber-600 text-stone-100 rounded-lg font-medium transition-colors">
                          Abrir Grupo
                        </button>
                        <button
                          onClick={() => handleLeaveGroup(group.id)}
                          className="w-full px-4 py-2 bg-stone-700 hover:bg-stone-600 text-stone-300 rounded-lg font-medium transition-colors"
                        >
                          Salir del Grupo
                        </button>
                      </>
                    ) : (
                      <button
                        onClick={() => handleJoinGroup(group.id)}
                        className={`w-full px-4 py-2 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 ${
                          group.isPremium
                            ? 'bg-gradient-to-r from-amber-700 to-yellow-600 hover:from-amber-600 hover:to-yellow-500 text-white'
                            : 'bg-amber-700 hover:bg-amber-600 text-stone-100'
                        }`}
                      >
                        <UserPlus className="w-4 h-4" />
                        {group.isPremium ? 'Unirse con Coins' : group.privacy === 'public' ? 'Unirse' : 'Solicitar Unirse'}
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
