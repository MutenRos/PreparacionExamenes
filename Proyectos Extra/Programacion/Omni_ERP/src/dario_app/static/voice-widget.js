/**
 * Voice Assistant Widget - Floating voice control across the entire web
 * Integrated into all pages via this script
 * Encoding: UTF-8
 */

(function(){"use strict";
    // Prevent multiple loads
    if(window.__voiceAssistantLoaded) return;
    window.__voiceAssistantLoaded = true;

    // Initialize on DOM ready
    if(document.readyState === 'loading'){
        document.addEventListener('DOMContentLoaded', initVoiceWidget);
    } else {
        initVoiceWidget();
    }

    function initVoiceWidget(){
        // Check if widget already exists
        if(document.getElementById('voice-widget-panel')) return;

        // Create widget container
        const widget = document.createElement('div');
        widget.id = 'voice-widget-panel';
        widget.className = 'voice-assistant-widget closed';
        widget.innerHTML = `
            <div class="voice-widget-header">
                <span class="voice-widget-title">🎤 Asistente de Voz</span>
                <button class="voice-widget-toggle" title="Minimizar/Maximizar">─</button>
            </div>
            <div class="voice-widget-chat" id="voiceChat"></div>
            <div class="voice-widget-controls">
                <button class="voice-mic-btn" id="voiceMicBtn" title="Presiona para hablar">🎤</button>
                <input type="text" class="voice-input" id="voiceInput" placeholder="Escribe o habla...">
                <button class="voice-send-btn" id="voiceSendBtn" title="Enviar">➤</button>
            </div>
            <div class="voice-status" id="voiceStatus"></div>
        `;

        document.body.appendChild(widget);

        // Add styles dynamically
        addWidgetStyles();

        // Initialize voice recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.continuous = true;
        recognition.interimResults = true;

        // Get elements
        const micBtn = widget.querySelector('#voiceMicBtn');
        const input = widget.querySelector('#voiceInput');
        const sendBtn = widget.querySelector('#voiceSendBtn');
        const chatArea = widget.querySelector('#voiceChat');
        const status = widget.querySelector('#voiceStatus');
        const toggleBtn = widget.querySelector('.voice-widget-toggle');

        // State
        let isListening = false;
        let isProcessing = false;
        let conversationId = generateUUID();

        // Toggle widget
        toggleBtn.addEventListener('click', () => {
            widget.classList.toggle('closed');
            toggleBtn.textContent = widget.classList.contains('closed') ? '▲' : '─';
            // Guardar el estado en localStorage
            localStorage.setItem('voiceWidgetState', widget.classList.contains('closed') ? 'closed' : 'open');
        });

        // Restaurar el estado del widget
        const savedState = localStorage.getItem('voiceWidgetState');
        if(savedState === 'open'){
            widget.classList.remove('closed');
            toggleBtn.textContent = '─';
            // Iniciar escucha automáticamente si estaba abierto
            setTimeout(() => {
                isListening = true;
                micBtn.classList.add('listening');
                setStatus('Escuchando...');
                recognition.start();
            }, 500);
        }

        // Add initial message
        addMessage('Hola! Presiona 🎤 para hablar o escribe un comando', false);

        // Microphone button
        micBtn.addEventListener('click', () => {
            if(isListening){
                recognition.stop();
                isListening = false;
                micBtn.classList.remove('listening');
                setStatus('Parado');
            } else {
                isListening = true;
                micBtn.classList.add('listening');
                setStatus('Escuchando...');
                recognition.start();
            }
        });

        // Send button
        sendBtn.addEventListener('click', sendMessage);
        input.addEventListener('keypress', (e) => {
            if(e.key === 'Enter'){
                sendMessage();
            }
        });

        // Speech recognition events
        recognition.onstart = () => {
            isListening = true;
            micBtn.classList.add('listening');
        };

        recognition.onend = () => {
            isListening = false;
            micBtn.classList.remove('listening');
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            let isFinal = false;

            for(let i = event.resultIndex; i < event.results.length; i++){
                const transcript = event.results[i][0].transcript;
                if(event.results[i].isFinal){
                    interimTranscript += transcript + ' ';
                    isFinal = true;
                } else {
                    interimTranscript += transcript;
                }
            }

            input.value = interimTranscript.trim();

            if(isFinal){
                setStatus('Procesando...');
                setTimeout(() => {
                    sendMessage();
                }, 300);
            }
        };

        recognition.onerror = (event) => {
            setStatus(`Error: ${event.error}`);
            isListening = false;
            micBtn.classList.remove('listening');
        };

        // Send message function
        async function sendMessage(){
            const text = input.value.trim();
            if(!text || isProcessing) return;

            isProcessing = true;
            input.disabled = true;
            sendBtn.disabled = true;

            addMessage(text, true);
            input.value = '';

            try {
                setStatus('Procesando...');

                const response = await fetch('/api/voice-assistant/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json; charset=utf-8'
                    },
                    body: JSON.stringify({
                        text: text,
                        conversation_id: conversationId
                    })
                });

                if(!response.ok){
                    throw new Error('Error al procesar el comando');
                }

                const data = await response.json();
                conversationId = data.conversation_id;

                addMessage(data.message, false);
                setStatus(`Intent: ${data.intent}`);

                // Execute action if needed
                if(data.action){
                    executeAction(data.action, data.action_params);
                }

                // Keep listening for next command
                setStatus('Escuchando...');
                recognition.start();

            } catch(error){
                addMessage(`Error: ${error.message}`, false);
                setStatus('Error');
            } finally {
                isProcessing = false;
                input.disabled = false;
                sendBtn.disabled = false;
                input.focus();
            }
        }

        // Add message to chat
        function addMessage(text, isUser){
            const msgDiv = document.createElement('div');
            msgDiv.className = `voice-message ${isUser ? 'user' : 'bot'}`;
            msgDiv.textContent = text;
            chatArea.appendChild(msgDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        // Set status
        function setStatus(message){
            status.textContent = message;
        }

        // Execute actions
        function executeAction(action, params = {}){
            switch(action){
                case 'navigate':
                    const destination = params.destination || 'dashboard';
                    window.location.href = `/app/${destination}`;
                    break;
                case 'open_form':
                    const entity = params.entity_type || 'producto';
                    window.location.href = `/app/${entity}?mode=crear`;
                    break;
                case 'show_help':
                    addMessage(
                        '📍 Puedo ayudarte a:\n' +
                        '🔍 Buscar productos\n' +
                        '📍 Navegar secciones\n' +
                        '➕ Crear registros\n' +
                        '📊 Ver reportes\n' +
                        '🔧 Filtrar datos\n' +
                        '✏️ Editar registros\n' +
                        '🗑️ Eliminar registros',
                        false
                    );
                    break;
            }
        }
    }

    // Add widget styles
    function addWidgetStyles(){
        const style = document.createElement('style');
        style.textContent = `
            .voice-assistant-widget {
                position: fixed;
                bottom: 80px;
                left: 18px;
                width: 380px;
                height: 500px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 5px 30px rgba(0, 0, 0, 0.3);
                display: flex;
                flex-direction: column;
                z-index: 9998;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                transition: all 0.3s ease;
            }

            .voice-assistant-widget.closed {
                height: 50px;
                width: 50px;
                bottom: 20px;
            }

            .voice-assistant-widget.closed .voice-widget-chat,
            .voice-assistant-widget.closed .voice-widget-controls,
            .voice-assistant-widget.closed .voice-status {
                display: none;
            }

            .voice-widget-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 16px;
                border-radius: 12px 12px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                cursor: pointer;
            }

            .voice-widget-title {
                font-weight: 600;
                font-size: 0.95em;
            }

            .voice-widget-toggle {
                background: none;
                border: none;
                color: white;
                font-size: 1.2em;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: transform 0.3s;
            }

            .voice-widget-toggle:hover {
                transform: scale(1.1);
            }

            .voice-widget-chat {
                flex: 1;
                overflow-y: auto;
                padding: 16px 12px;
                display: flex;
                flex-direction: column;
                gap: 10px;
                background: #f9f9f9;
                min-height: 300px;
            }

            .voice-widget-chat::-webkit-scrollbar {
                width: 6px;
            }

            .voice-widget-chat::-webkit-scrollbar-track {
                background: #f1f1f1;
            }

            .voice-widget-chat::-webkit-scrollbar-thumb {
                background: #667eea;
                border-radius: 3px;
            }

            .voice-message {
                padding: 10px 14px;
                border-radius: 8px;
                word-wrap: break-word;
                line-height: 1.4;
                font-size: 0.95em;
                animation: slideIn 0.3s ease-out;
                max-width: 90%;
            }

            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .voice-message.user {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                align-self: flex-end;
                border-radius: 8px 0px 8px 8px;
            }

            .voice-message.bot {
                background: white;
                color: #333;
                border: 1px solid #ddd;
                align-self: flex-start;
                border-radius: 0px 8px 8px 8px;
            }

            .voice-widget-controls {
                display: flex;
                gap: 8px;
                padding: 12px;
                background: white;
                border-top: 1px solid #e0e0e0;
            }

            .voice-mic-btn {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                border: 2px solid #667eea;
                background: white;
                cursor: pointer;
                font-size: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s;
                flex-shrink: 0;
            }

            .voice-mic-btn:hover {
                background: #f0f0f0;
            }

            .voice-mic-btn.listening {
                background: #667eea;
                border-color: #764ba2;
                animation: pulse 1s infinite;
            }

            @keyframes pulse {
                0%, 100% {
                    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
                }
                50% {
                    box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
                }
            }

            .voice-input {
                flex: 1;
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 0.9em;
                font-family: inherit;
            }

            .voice-input:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
            }

            .voice-send-btn {
                width: 40px;
                height: 40px;
                border-radius: 6px;
                border: none;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                cursor: pointer;
                font-size: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: transform 0.2s;
                flex-shrink: 0;
            }

            .voice-send-btn:hover {
                transform: scale(1.05);
            }

            .voice-send-btn:active {
                transform: scale(0.95);
            }

            .voice-status {
                padding: 6px 12px;
                font-size: 0.8em;
                color: #667eea;
                background: #f0f4ff;
                border-top: 1px solid #e0e0e0;
                min-height: 20px;
            }

            @media (max-width: 600px) {
                .voice-assistant-widget {
                    width: 100%;
                    height: 100%;
                    bottom: 0;
                    right: 0;
                    border-radius: 0;
                }

                .voice-assistant-widget.closed {
                    width: 50px;
                    height: 50px;
                    bottom: 20px;
                    right: 20px;
                    border-radius: 50%;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Generate UUID
    function generateUUID(){
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c){
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
})();
