// Voice Assistant Widget - Floating panel with speech recognition
(function(){
  if(window.__voiceAssistantLoaded) return; window.__voiceAssistantLoaded=true;
  
  let recognition = null;
  let isListening = false;
  let conversationId = null;

  function ensureVoiceWidget(){
    if(document.getElementById('voice-widget-panel')) return;
    
    const panel = document.createElement('div');
    panel.id = 'voice-widget-panel';
    panel.className = 'voice-widget-panel hidden-taskbar';
    panel.innerHTML = `
      <div class="voice-widget-header">
        <h3 style="margin:0;font-size:15px;font-weight:600;">🎙️ Asistente de Voz</h3>
        <div style="display:flex;gap:6px;align-items:center;">
          <button id="voice-widget-collapse" aria-label="Minimizar voz" style="background:var(--bg-primary);color:var(--text-primary);padding:6px 8px;border-radius:6px;border:1px solid var(--border-color);cursor:pointer;">_</button>
        </div>
      </div>
      <div class="voice-widget-body" id="voice-widget-body">
        <div class="voice-bubble assistant">Hola, soy tu asistente de voz. Presiona el micrófono o escribe un comando.</div>
      </div>
      <div class="voice-widget-footer">
        <button id="voice-mic-btn" class="voice-mic-btn" title="Presiona para hablar">🎤</button>
        <input type="text" id="voice-widget-input" placeholder="O escribe tu comando..." />
        <button id="voice-widget-send">Enviar</button>
      </div>`;
    document.body.appendChild(panel);

    const bodyChat = panel.querySelector('#voice-widget-body');
    const input = panel.querySelector('#voice-widget-input');
    const sendBtn = panel.querySelector('#voice-widget-send');
    const micBtn = panel.querySelector('#voice-mic-btn');
    const collapseBtn = panel.querySelector('#voice-widget-collapse');

    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognition = new SpeechRecognition();
      recognition.lang = 'es-ES';
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        input.value = transcript;
        sendMessage(transcript);
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        isListening = false;
        micBtn.classList.remove('listening');
      };

      recognition.onend = () => {
        isListening = false;
        micBtn.classList.remove('listening');
      };
    } else {
      micBtn.disabled = true;
      micBtn.title = 'Reconocimiento de voz no disponible';
    }

    function appendBubble(text, type) {
      const div = document.createElement('div');
      div.className = `voice-bubble ${type}`;
      // Soportar texto con saltos de línea y emojis
      div.innerHTML = text.replace(/\n/g, '<br>');
      bodyChat.appendChild(div);
      bodyChat.scrollTop = bodyChat.scrollHeight;
    }

    async function sendMessage(text) {
      if (!text.trim()) return;
      appendBubble(text, 'user');
      input.value = '';
      
      const thinkingBubble = document.createElement('div');
      thinkingBubble.className = 'voice-bubble assistant thinking';
      thinkingBubble.innerHTML = '💭 Pensando...';
      bodyChat.appendChild(thinkingBubble);
      bodyChat.scrollTop = bodyChat.scrollHeight;
      
      try {
        const resp = await fetch('/api/voice-assistant/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: text, conversation_id: conversationId })
        });
        
        if (!resp.ok) throw new Error('Error al procesar comando');
        
        const data = await resp.json();
        conversationId = data.conversation_id;
        
        // Remover "pensando..."
        if (bodyChat.contains(thinkingBubble)) {
          bodyChat.removeChild(thinkingBubble);
        }
        
        // Mostrar respuesta de Ollama
        appendBubble(data.message || 'Sin respuesta', 'assistant');
        
        // Mostrar datos del ERP si hay
        if (data.data) {
          if (data.data.productos && data.data.productos.length > 0) {
            const productList = data.data.productos.map(p => 
              `<div style="padding:6px 0;border-bottom:1px solid var(--border-color);">
                <strong>${p.codigo}</strong> - ${p.nombre}<br>
                <span style="font-size:11px;color:var(--text-secondary);">Stock: ${p.stock_actual} | €${p.precio_venta.toFixed(2)}</span>
              </div>`
            ).join('');
            const dataDiv = document.createElement('div');
            dataDiv.className = 'voice-bubble assistant';
            dataDiv.style.background = 'var(--color-success-light)';
            dataDiv.innerHTML = `<strong>📦 Productos encontrados:</strong><br>${productList}`;
            bodyChat.appendChild(dataDiv);
          }
          
          if (data.data.alquileres && data.data.alquileres.length > 0) {
            const rentalList = data.data.alquileres.map(a => 
              `<div style="padding:6px 0;">
                ${a.disponible ? '✅' : '❌'} ${a.nombre} - €${a.precio_venta.toFixed(2)}/día
              </div>`
            ).join('');
            const dataDiv = document.createElement('div');
            dataDiv.className = 'voice-bubble assistant';
            dataDiv.style.background = 'var(--color-warning-light)';
            dataDiv.innerHTML = `<strong>🎪 Alquileres:</strong><br>${rentalList}`;
            bodyChat.appendChild(dataDiv);
          }
          
          if (data.data.ventas_stats) {
            const stats = data.data.ventas_stats;
            const dataDiv = document.createElement('div');
            dataDiv.className = 'voice-bubble assistant';
            dataDiv.style.background = 'var(--color-info-light)';
            dataDiv.innerHTML = `<strong>📊 Estadísticas de ventas:</strong><br>
              ${stats.cantidad_ventas} ventas<br>
              Total: €${stats.total_vendido.toFixed(2)}<br>
              Promedio: €${stats.ticket_promedio.toFixed(2)}`;
            bodyChat.appendChild(dataDiv);
          }
          
          if (data.data.clientes && data.data.clientes.length > 0) {
            const clientList = data.data.clientes.map(c => 
              `<div style="padding:6px 0;border-bottom:1px solid var(--border-color);">
                <strong>${c.nombre}</strong><br>
                <span style="font-size:11px;color:var(--text-secondary);">${c.email} | ${c.telefono}</span>
              </div>`
            ).join('');
            const dataDiv = document.createElement('div');
            dataDiv.className = 'voice-bubble assistant';
            dataDiv.style.background = 'var(--primary-light)';
            dataDiv.innerHTML = `<strong>👥 Clientes:</strong><br>${clientList}`;
            bodyChat.appendChild(dataDiv);
          }
        }
        
        bodyChat.scrollTop = bodyChat.scrollHeight;
        
        // Ejecutar acción si hay
        if (data.action) {
          setTimeout(() => executeAction(data.action, data.action_params), 1000);
        }
      } catch (err) {
        if (bodyChat.contains(thinkingBubble)) {
          bodyChat.removeChild(thinkingBubble);
        }
        appendBubble('❌ Error: ' + err.message, 'assistant');
      }
    }

    function executeAction(action, params = {}) {
      console.log('Voice action:', action, params);
      appendBubble('✅ Ejecutando acción...', 'assistant');
      
      switch (action) {
        case 'navigate':
          const dest = params.destination || 'dashboard';
          setTimeout(() => window.location.href = `/app/${dest}`, 500);
          break;
        case 'open_form':
          const entity = params.entity_type || 'producto';
          setTimeout(() => window.location.href = `/app/inventario?mode=crear`, 500);
          break;
        case 'apply_filter':
          appendBubble('🔧 Aplicando filtros en la vista actual...', 'assistant');
          // TODO: Implementar filtrado dinámico
          break;
        default:
          console.log('Unknown voice action:', action);
      }
    }

    function toggleListening() {
      if (!recognition) return;
      if (isListening) {
        recognition.stop();
      } else {
        isListening = true;
        micBtn.classList.add('listening');
        recognition.start();
      }
    }

    if (micBtn) micBtn.addEventListener('click', toggleListening);
    if (sendBtn) sendBtn.addEventListener('click', () => sendMessage(input.value));
    if (input) input.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage(input.value);
      }
    });
    if (collapseBtn) collapseBtn.addEventListener('click', () => {
      panel.classList.toggle('collapsed');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureVoiceWidget);
  } else {
    ensureVoiceWidget();
  }
})();
