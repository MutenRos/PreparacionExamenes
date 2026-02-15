(function(){
  if(window.__erpAssistantLoaded) return; window.__erpAssistantLoaded=true;
  const ENABLE_TASKBAR = true;

  function ensureWidget(){
    if(document.getElementById('ai-widget-panel')) return;
    const panel=document.createElement('div'); panel.id='ai-widget-panel'; panel.className='ai-widget-panel hidden-taskbar'; panel.innerHTML=`
      <div class="ai-widget-header">
        <h3 style="margin:0;font-size:15px;font-weight:600;">💬 Soporte</h3>
        <div style="display:flex;gap:6px;align-items:center;">
          <button id="ai-widget-collapse" aria-label="Minimizar soporte" style="background:#fff;color:#111;padding:6px 8px;border-radius:6px;border:1px solid #e5e7eb;cursor:pointer;">_</button>
        </div>
      </div>
      <div class="ai-widget-body" id="ai-widget-body">
        <div class="ai-bubble bot">Hola, soy tu asistente de soporte. Pregúntame cómo usar el ERP.</div>
      </div>
      <div class="ai-widget-footer">
        <textarea id="ai-widget-input" placeholder="Escribe tu pregunta..."></textarea>
        <button id="ai-widget-send">Enviar</button>
      </div>`;
    document.body.appendChild(panel);
    const bodyChat=panel.querySelector('#ai-widget-body');
    const input=panel.querySelector('#ai-widget-input');
    const sendBtn=panel.querySelector('#ai-widget-send');
    const collapseBtn=panel.querySelector('#ai-widget-collapse');
    let sending=false;
    function appendBubble(text,type){ const div=document.createElement('div'); div.className=`ai-bubble ${type}`; div.textContent=text; bodyChat.appendChild(div); bodyChat.scrollTop=bodyChat.scrollHeight; }
    async function send(){
      if(sending) return; const msg=input.value.trim(); if(!msg) return; sending=true;
      appendBubble(msg,'user'); input.value=''; appendBubble('Pensando...','bot');
      try{
        const resp=await fetch('/api/ai/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})});
        if(!resp.ok){
          const detail=await resp.text();
          bodyChat.removeChild(bodyChat.lastChild);
          appendBubble(`Error ${resp.status}: ${detail||'No se pudo obtener respuesta'}`,'bot');
          return;
        }
        const data=await resp.json();
        if(bodyChat.lastChild) bodyChat.removeChild(bodyChat.lastChild);
        appendBubble(data.reply||'No se obtuvo respuesta','bot');
      }catch(err){
        if(bodyChat.lastChild) bodyChat.removeChild(bodyChat.lastChild);
        appendBubble('Error al conectar con el asistente.','bot');
      } finally { sending=false; }
    }
    sendBtn.addEventListener('click',send);
    input.addEventListener('keydown',e=>{ if(e.key==='Enter'&&!e.shiftKey){ e.preventDefault(); send(); }});
    if(collapseBtn){ collapseBtn.addEventListener('click',()=>{ panel.classList.toggle('collapsed'); }); }
  }
  if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded',ensureWidget); } else { ensureWidget(); }

  // Taskbar: botones flotantes que controlan visibilidad de los asistentes
  if (ENABLE_TASKBAR) {
    function ensureTaskbar(){
      if(document.getElementById('assistant-taskbar')) return;
      const bar=document.createElement('div');
      bar.id='assistant-taskbar';
      bar.className='assistant-taskbar';
      bar.innerHTML=`
        <button id="btn-basic" aria-label="Asistente básico">📋 Básico</button>
        <button id="btn-ai" aria-label="Mostrar soporte">🤖 Soporte</button>
        <button id="btn-voice" aria-label="Mostrar asistente de voz">🎙️ Voz</button>
        <button id="btn-tutorial" aria-label="Iniciar tutorial">❓ Tutorial</button>
        <button id="btn-close" class="danger" aria-label="Ocultar asistentes">✕ Ocultar</button>
      `;
      document.body.appendChild(bar);

      const basicBtn=bar.querySelector('#btn-basic');
      const aiBtn=bar.querySelector('#btn-ai');
      const voiceBtn=bar.querySelector('#btn-voice');
      const tutorialBtn=bar.querySelector('#btn-tutorial');
      const closeBtn=bar.querySelector('#btn-close');

      const hideAll = () => {
        const basic=document.getElementById('assistantPanel');
        const ai=document.getElementById('ai-widget-panel');
        const voice=document.getElementById('voice-widget-panel');
        if(basic) basic.classList.add('hidden-taskbar');
        if(ai) ai.classList.add('hidden-taskbar');
        if(voice) voice.classList.add('hidden-taskbar');
      };

      // Ensure start hidden
      hideAll();

      function toggle(id){
        const el=document.getElementById(id);
        if(!el) return;
        el.classList.toggle('hidden-taskbar');
      }

      basicBtn.addEventListener('click',()=>toggle('assistantPanel'));
      aiBtn.addEventListener('click',()=>toggle('ai-widget-panel'));
      voiceBtn.addEventListener('click',()=>toggle('voice-widget-panel'));
      tutorialBtn.addEventListener('click',()=>{
        if(window.tutorial && typeof window.tutorial.restartTutorial === 'function'){
          window.tutorial.restartTutorial();
        }
      });
      closeBtn.addEventListener('click',()=>{
        hideAll();
      });
    }

    // Esperar a que ambos widgets existan para asegurar botones funcionales
    const waitForWidgets=setInterval(()=>{
      const hasBasic=document.getElementById('assistantPanel');
      const hasAI=document.getElementById('ai-widget-panel');
      const hasVoice=document.getElementById('voice-widget-panel');
      if(hasBasic && hasAI && hasVoice){
        ensureTaskbar();
        clearInterval(waitForWidgets);
      }
    },200);
  }
})();
