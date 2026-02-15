'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { MessageCircle, Plus, AlertCircle, CheckCircle, Clock, XCircle, Send } from 'lucide-react';

interface Ticket {
  id: string;
  subject: string;
  description: string;
  status: string;
  priority: string;
  category: string;
  created_at: string;
  updated_at: string;
}

interface Message {
  id: string;
  message: string;
  is_admin: boolean;
  created_at: string;
}

export default function SupportPage() {
  const router = useRouter();
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNewTicket, setShowNewTicket] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');

  const [formData, setFormData] = useState({
    subject: '',
    description: '',
    priority: 'medium',
    category: 'general',
  });

  useEffect(() => {
    fetchTickets();
  }, []);

  useEffect(() => {
    if (selectedTicket) {
      fetchTicketMessages(selectedTicket.id);
    }
  }, [selectedTicket]);

  async function fetchTickets() {
    try {
      const response = await fetch('/api/tickets');
      const data = await response.json();
      
      if (response.ok) {
        setTickets(data.tickets || []);
      }
    } catch (error) {
      console.error('Error fetching tickets:', error);
    } finally {
      setLoading(false);
    }
  }

  async function fetchTicketMessages(ticketId: string) {
    try {
      const response = await fetch(`/api/tickets?id=${ticketId}`);
      const data = await response.json();
      
      if (response.ok) {
        setMessages(data.messages || []);
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  }

  async function createTicket(e: React.FormEvent) {
    e.preventDefault();
    
    try {
      const response = await fetch('/api/tickets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setShowNewTicket(false);
        setFormData({
          subject: '',
          description: '',
          priority: 'medium',
          category: 'general',
        });
        await fetchTickets();
      }
    } catch (error) {
      console.error('Error creating ticket:', error);
    }
  }

  async function sendMessage(e: React.FormEvent) {
    e.preventDefault();
    
    if (!newMessage.trim() || !selectedTicket) return;

    try {
      const response = await fetch('/api/tickets/messages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ticketId: selectedTicket.id,
          message: newMessage,
        }),
      });

      if (response.ok) {
        setNewMessage('');
        await fetchTicketMessages(selectedTicket.id);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  }

  async function closeTicket(ticketId: string) {
    try {
      await fetch('/api/tickets', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticketId, status: 'closed' }),
      });
      
      await fetchTickets();
      setSelectedTicket(null);
    } catch (error) {
      console.error('Error closing ticket:', error);
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'open': return <AlertCircle className="w-4 h-4 text-blue-400" />;
      case 'in_progress': return <Clock className="w-4 h-4 text-yellow-400" />;
      case 'resolved': return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'closed': return <XCircle className="w-4 h-4 text-stone-400" />;
      default: return null;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'text-red-400';
      case 'high': return 'text-orange-400';
      case 'medium': return 'text-yellow-400';
      case 'low': return 'text-green-400';
      default: return 'text-stone-400';
    }
  };

  if (selectedTicket) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-stone-950 via-stone-900 to-stone-950 py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <button
            onClick={() => setSelectedTicket(null)}
            className="mb-4 text-stone-400 hover:text-stone-200 transition-colors"
          >
            ← Volver a tickets
          </button>

          <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
            <div className="flex items-start justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold text-white mb-2">{selectedTicket.subject}</h1>
                <div className="flex items-center gap-4 text-sm">
                  <span className="flex items-center gap-1">
                    {getStatusIcon(selectedTicket.status)}
                    <span className="capitalize">{selectedTicket.status}</span>
                  </span>
                  <span className={`capitalize ${getPriorityColor(selectedTicket.priority)}`}>
                    {selectedTicket.priority} priority
                  </span>
                  <span className="text-stone-400">
                    {new Date(selectedTicket.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
              {selectedTicket.status !== 'closed' && (
                <button
                  onClick={() => closeTicket(selectedTicket.id)}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  Cerrar Ticket
                </button>
              )}
            </div>

            {/* Mensajes */}
            <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`p-4 rounded-lg ${
                    msg.is_admin
                      ? 'bg-blue-900/20 border border-blue-800/30'
                      : 'bg-stone-700/50'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-stone-300">
                      {msg.is_admin ? 'Soporte' : 'Tú'}
                    </span>
                    <span className="text-xs text-stone-500">
                      {new Date(msg.created_at).toLocaleString()}
                    </span>
                  </div>
                  <p className="text-stone-200">{msg.message}</p>
                </div>
              ))}
            </div>

            {/* Formulario de respuesta */}
            {selectedTicket.status !== 'closed' && (
              <form onSubmit={sendMessage} className="flex gap-2">
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Escribe tu mensaje..."
                  className="flex-1 px-4 py-2 bg-stone-900 border border-stone-700 rounded-lg text-stone-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  type="submit"
                  disabled={!newMessage.trim()}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  <Send className="w-4 h-4" />
                  Enviar
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-stone-950 via-stone-900 to-stone-950 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <MessageCircle className="w-8 h-8 text-blue-400" />
            <h1 className="text-3xl font-bold text-white">Soporte</h1>
          </div>
          <button
            onClick={() => setShowNewTicket(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Nuevo Ticket
          </button>
        </div>

        {/* Formulario nuevo ticket */}
        {showNewTicket && (
          <div className="bg-stone-800 border border-stone-700 rounded-lg p-6 mb-6">
            <h2 className="text-xl font-bold text-white mb-4">Crear Nuevo Ticket</h2>
            <form onSubmit={createTicket} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-stone-300 mb-2">
                  Asunto
                </label>
                <input
                  type="text"
                  required
                  value={formData.subject}
                  onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                  className="w-full px-4 py-2 bg-stone-900 border border-stone-700 rounded-lg text-stone-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Describe brevemente tu problema"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-stone-300 mb-2">
                    Categoría
                  </label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full px-4 py-2 bg-stone-900 border border-stone-700 rounded-lg text-stone-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="general">General</option>
                    <option value="technical">Técnico</option>
                    <option value="billing">Facturación</option>
                    <option value="content">Contenido</option>
                    <option value="account">Cuenta</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-stone-300 mb-2">
                    Prioridad
                  </label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    className="w-full px-4 py-2 bg-stone-900 border border-stone-700 rounded-lg text-stone-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="low">Baja</option>
                    <option value="medium">Media</option>
                    <option value="high">Alta</option>
                    <option value="urgent">Urgente</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-stone-300 mb-2">
                  Descripción
                </label>
                <textarea
                  required
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={5}
                  className="w-full px-4 py-2 bg-stone-900 border border-stone-700 rounded-lg text-stone-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Describe detalladamente tu problema..."
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => setShowNewTicket(false)}
                  className="flex-1 px-4 py-2 bg-stone-700 text-stone-200 rounded-lg hover:bg-stone-600 transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Crear Ticket
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Lista de tickets */}
        <div className="space-y-4">
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400 mx-auto"></div>
            </div>
          ) : tickets.length === 0 ? (
            <div className="text-center py-12 text-stone-400">
              No tienes tickets de soporte. Crea uno si necesitas ayuda.
            </div>
          ) : (
            tickets.map((ticket) => (
              <div
                key={ticket.id}
                onClick={() => setSelectedTicket(ticket)}
                className="bg-stone-800 border border-stone-700 rounded-lg p-6 hover:bg-stone-700/50 transition-colors cursor-pointer"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-white mb-2">{ticket.subject}</h3>
                    <div className="flex items-center gap-4 text-sm">
                      <span className="flex items-center gap-1 text-stone-300">
                        {getStatusIcon(ticket.status)}
                        <span className="capitalize">{ticket.status}</span>
                      </span>
                      <span className={`capitalize ${getPriorityColor(ticket.priority)}`}>
                        {ticket.priority}
                      </span>
                      <span className="text-stone-400">
                        {new Date(ticket.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
