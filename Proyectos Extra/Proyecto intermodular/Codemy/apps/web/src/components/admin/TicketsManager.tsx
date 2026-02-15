'use client';

import { useState, useEffect } from 'react';
import { MessageCircle, Send, AlertCircle, CheckCircle, Clock, XCircle } from 'lucide-react';

interface Ticket {
  id: string;
  user_id: string;
  subject: string;
  description: string;
  status: string;
  priority: string;
  category: string;
  created_at: string;
}

interface Message {
  id: string;
  message: string;
  is_admin: boolean;
  created_at: string;
}

export default function TicketsManager() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [responseMessage, setResponseMessage] = useState('');
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTickets();
  }, [filter]);

  useEffect(() => {
    if (selectedTicket) {
      fetchMessages(selectedTicket.id);
    }
  }, [selectedTicket]);

  async function fetchTickets() {
    setLoading(true);
    try {
      const url = filter === 'all' 
        ? '/api/admin/tickets' 
        : `/api/admin/tickets?status=${filter}`;
      
      const response = await fetch(url);
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

  async function fetchMessages(ticketId: string) {
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

  async function respondToTicket(updateStatus?: string) {
    if (!responseMessage.trim() || !selectedTicket) return;

    try {
      const response = await fetch('/api/admin/tickets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ticketId: selectedTicket.id,
          message: responseMessage,
          updateStatus,
        }),
      });

      if (response.ok) {
        setResponseMessage('');
        await fetchMessages(selectedTicket.id);
        await fetchTickets();
      }
    } catch (error) {
      console.error('Error responding:', error);
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
      case 'urgent': return 'bg-red-600';
      case 'high': return 'bg-orange-600';
      case 'medium': return 'bg-yellow-600';
      case 'low': return 'bg-green-600';
      default: return 'bg-stone-600';
    }
  };

  if (selectedTicket) {
    return (
      <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
        <button
          onClick={() => setSelectedTicket(null)}
          className="mb-4 text-stone-400 hover:text-stone-200 transition-colors"
        >
          ← Volver a tickets
        </button>

        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white mb-2">{selectedTicket.subject}</h2>
          <div className="flex items-center gap-4 text-sm">
            <span className="flex items-center gap-1">
              {getStatusIcon(selectedTicket.status)}
              <span className="capitalize text-stone-300">{selectedTicket.status}</span>
            </span>
            <span className={`px-2 py-1 rounded text-white text-xs ${getPriorityColor(selectedTicket.priority)}`}>
              {selectedTicket.priority}
            </span>
            <span className="text-stone-400">
              {selectedTicket.category}
            </span>
            <span className="text-stone-400">
              {new Date(selectedTicket.created_at).toLocaleString()}
            </span>
          </div>
        </div>

        {/* Mensajes */}
        <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`p-4 rounded-lg ${
                msg.is_admin
                  ? 'bg-green-900/20 border border-green-800/30 ml-8'
                  : 'bg-stone-700/50 mr-8'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-stone-300">
                  {msg.is_admin ? '🛡️ Admin' : '👤 Usuario'}
                </span>
                <span className="text-xs text-stone-500">
                  {new Date(msg.created_at).toLocaleString()}
                </span>
              </div>
              <p className="text-stone-200">{msg.message}</p>
            </div>
          ))}
        </div>

        {/* Respuesta */}
        {selectedTicket.status !== 'closed' && (
          <div>
            <textarea
              value={responseMessage}
              onChange={(e) => setResponseMessage(e.target.value)}
              placeholder="Escribe tu respuesta..."
              rows={4}
              className="w-full px-4 py-2 bg-stone-900 border border-stone-700 rounded-lg text-stone-200 focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3"
            />
            <div className="flex gap-2">
              <button
                onClick={() => respondToTicket()}
                disabled={!responseMessage.trim()}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <Send className="w-4 h-4" />
                Enviar Respuesta
              </button>
              <button
                onClick={() => respondToTicket('in_progress')}
                disabled={!responseMessage.trim()}
                className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors disabled:opacity-50"
              >
                En Progreso
              </button>
              <button
                onClick={() => respondToTicket('resolved')}
                disabled={!responseMessage.trim()}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
              >
                Resolver
              </button>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <MessageCircle className="w-6 h-6 text-blue-400" />
          <h2 className="text-xl font-bold text-white">Tickets de Soporte</h2>
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 rounded ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-stone-700 text-stone-300'}`}
          >
            Todos
          </button>
          <button
            onClick={() => setFilter('open')}
            className={`px-3 py-1 rounded ${filter === 'open' ? 'bg-blue-600 text-white' : 'bg-stone-700 text-stone-300'}`}
          >
            Abiertos
          </button>
          <button
            onClick={() => setFilter('in_progress')}
            className={`px-3 py-1 rounded ${filter === 'in_progress' ? 'bg-yellow-600 text-white' : 'bg-stone-700 text-stone-300'}`}
          >
            En Progreso
          </button>
          <button
            onClick={() => setFilter('resolved')}
            className={`px-3 py-1 rounded ${filter === 'resolved' ? 'bg-green-600 text-white' : 'bg-stone-700 text-stone-300'}`}
          >
            Resueltos
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400 mx-auto"></div>
        </div>
      ) : tickets.length === 0 ? (
        <div className="text-center py-12 text-stone-400">
          No hay tickets en esta categoría
        </div>
      ) : (
        <div className="space-y-3">
          {tickets.map((ticket) => (
            <div
              key={ticket.id}
              onClick={() => setSelectedTicket(ticket)}
              className="p-4 bg-stone-700/50 hover:bg-stone-700 rounded-lg cursor-pointer transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="font-semibold text-white mb-1">{ticket.subject}</h3>
                  <p className="text-sm text-stone-400 line-clamp-1">{ticket.description}</p>
                  <div className="flex items-center gap-3 mt-2 text-xs">
                    <span className="flex items-center gap-1 text-stone-300">
                      {getStatusIcon(ticket.status)}
                      {ticket.status}
                    </span>
                    <span className={`px-2 py-0.5 rounded text-white ${getPriorityColor(ticket.priority)}`}>
                      {ticket.priority}
                    </span>
                    <span className="text-stone-500">
                      {new Date(ticket.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
