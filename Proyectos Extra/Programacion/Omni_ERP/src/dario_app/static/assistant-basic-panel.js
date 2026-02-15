// Asistente básico persistente en todas las páginas
(function(){
  if (window.__assistantBasicLoaded) return; window.__assistantBasicLoaded = true;
  const PANEL_ID = 'assistantPanel';

  const style = document.createElement('style');
  style.textContent = `
    .assistant-panel {
      position: fixed;
      left: 12px;
      bottom: 16px;
      top: auto;
      width: min(340px, 38vw);
      max-height: 70vh;
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.15);
      border: 1px solid #e5e7eb;
      display: flex !important;
      flex-direction: column;
      z-index: 1100;
    }
    .assistant-header { display: flex; align-items: center; justify-content: space-between; padding: 14px 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; border-radius: 12px 12px 0 0; flex-shrink: 0; }
    .assistant-header h3 { margin: 0; font-size: 15px; font-weight: 600; }
    .assistant-body { padding: 0; overflow-y: auto; flex: 1; min-height: 150px; }
    .accordion-item { border-bottom: 1px solid #f0f0f0; }
    .accordion-trigger { width: 100%; text-align: left; padding: 12px 14px; background: none; border: none; display: flex; justify-content: space-between; align-items: center; cursor: pointer; font-weight: 600; color: #333; font-size: 14px; }
    .accordion-trigger:hover { background: #f9f9f9; }
    .accordion-trigger span { font-size: 12px; color: #999; font-weight: 400; }
    .accordion-content { padding: 0 14px 12px 14px; display: none; max-height: 300px; overflow-y: auto; }
    .accordion-content.open { display: block; }
    .accordion-content ul { list-style: none; padding-left: 0; margin: 0; }
    .accordion-content li { padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 12px; color: #555; line-height: 1.4; }
    .accordion-content li:last-child { border-bottom: none; }
    .assistant-footer { padding: 10px 14px; display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #888; border-top: 1px solid #f0f0f0; background: #fafafa; border-radius: 0 0 12px 12px; flex-shrink: 0; }
    .assistant-footer button { padding: 6px 10px; border-radius: 6px; border: none; background: #667eea; color: #fff; cursor: pointer; font-size: 12px; transition: background 0.2s; }
    .assistant-footer button:hover { background: #5568d3; }
    .assistant-panel.collapsed { max-height: 54px; overflow: hidden; }
    .assistant-panel.collapsed .assistant-body, .assistant-panel.collapsed .assistant-footer { display: none; }
    .assistant-panel.collapsed .assistant-header { border-radius: 12px; }
    @media (max-width: 1400px) { .assistant-panel { width: min(300px, 42vw); left: 12px; bottom: 14px; top: auto; } }
    @media (max-width: 1200px) { .assistant-panel { width: min(260px, 45vw); left: 10px; bottom: 14px; top: auto; } }
    @media (max-width: 992px) { .assistant-panel { width: min(240px, 48vw); left: 10px; bottom: 12px; top: auto; } }
    @media (max-width: 900px) { .assistant-panel { width: calc(100% - 24px); left: 12px; right: 12px; bottom: 12px; top: auto; max-height: 45vh; } }
  `;
  document.head.appendChild(style);

  function ensurePanel(){
    if (document.getElementById(PANEL_ID)) return;
    const panel = document.createElement('div');
    panel.id = PANEL_ID;
    panel.className = 'assistant-panel hidden-taskbar';
    panel.innerHTML = `
      <div class="assistant-header">
        <h3>Asistente básico</h3>
        <div style="display:flex;gap:8px;align-items:center;">
          <button style="background:#fff;color:#4f46e5;padding:6px 10px;border-radius:6px;border:none;cursor:pointer;" id="assistantRefresh">↻</button>
          <button style="background:#fff;color:#111;padding:6px 8px;border-radius:6px;border:1px solid #e5e7eb;cursor:pointer;" id="assistantCollapse" aria-label="Minimizar">_</button>
        </div>
      </div>
      <div class="assistant-body">
        <div class="accordion-item">
          <button class="accordion-trigger" data-target="acc-compras">Compras sugeridas <span id="tag-compras"></span></button>
          <div class="accordion-content" id="acc-compras"><ul id="acc-compras-list"></ul></div>
        </div>
        <div class="accordion-item">
          <button class="accordion-trigger" data-target="acc-recordatorios">Recordatorios <span id="tag-record"></span></button>
          <div class="accordion-content" id="acc-recordatorios"><ul id="acc-record-list"></ul></div>
        </div>
        <div class="accordion-item">
          <button class="accordion-trigger" data-target="acc-resumen">Resumen asistente</button>
          <div class="accordion-content" id="acc-resumen"><pre id="acc-resumen-text" style="white-space: pre-wrap; font-family: 'Segoe UI', sans-serif; font-size: 13px; color:#333; margin: 0;"></pre></div>
        </div>
      </div>
      <div class="assistant-footer">
        <span id="assistantStatus">Listo</span>
        <button id="assistantBtn">Actualizar</button>
      </div>`;
    document.body.appendChild(panel);
  }

  function toggleAccordion(id){
    const el = document.getElementById(id);
    if (!el) return;
    const isOpen = el.classList.contains('open');
    document.querySelectorAll('.accordion-content').forEach(c => c.classList.remove('open'));
    if (!isOpen) el.classList.add('open');
  }

  async function refreshAssistant(){
    const statusEl = document.getElementById('assistantStatus');
    const comprasList = document.getElementById('acc-compras-list');
    const recList = document.getElementById('acc-record-list');
    const resumenText = document.getElementById('acc-resumen-text');
    const tagCompras = document.getElementById('tag-compras');
    const tagRecord = document.getElementById('tag-record');
    if (!statusEl) return;
    statusEl.textContent = 'Cargando...';
    if (comprasList) comprasList.innerHTML = '';
    if (recList) recList.innerHTML = '';
    if (resumenText) resumenText.textContent = '';
    try {
        const resp = await fetch('/api/ai/sugerencias-basico');
        if (!resp.ok) throw new Error('No se pudo obtener sugerencias');
        const data = await resp.json();
        const compras = data.compras_sugeridas || [];
        if (tagCompras) tagCompras.textContent = compras.length ? `(${compras.length})` : '';
        if (comprasList){
          if (compras.length === 0) {
            comprasList.innerHTML = '<li style="color:#777;">Sin compras urgentes</li>';
          } else {
            comprasList.innerHTML = compras.map(c => `
              <li>
                <strong>${c.codigo}</strong> · ${c.nombre}<br>
                Proveedor: ${c.proveedor || '-'} · Stock ${c.stock_actual}/${c.stock_minimo} · Comprar: ${c.cantidad_sugerida}<br>
                ${c.motivo}
              </li>
            `).join('');
          }
        }
        const recs = data.recordatorios || [];
        if (tagRecord) tagRecord.textContent = recs.length ? `(${recs.length})` : '';
        if (recList){
          if (recs.length === 0) {
            recList.innerHTML = '<li style="color:#777;">Sin recordatorios</li>';
          } else {
            recList.innerHTML = recs.map(r => `
              <li><strong>${r.tipo}</strong> · ${r.entidad}: ${r.mensaje}</li>
            `).join('');
          }
        }
        if (resumenText) resumenText.textContent = data.resumen_llm || 'Sin resumen disponible.';
        
        // Añadir botones de feedback ML al final del resumen
        const feedbackDiv = document.createElement('div');
        feedbackDiv.style.cssText = 'margin-top:16px;padding-top:12px;border-top:1px solid #e5e7eb;display:flex;gap:10px;align-items:center;justify-content:center;';
        feedbackDiv.innerHTML = `
          <span style="font-size:13px;color:#666;">¿Lo he hecho bien?</span>
          <button class="feedback-btn" data-feedback="positive" style="padding:6px 14px;border-radius:6px;border:1px solid #10b981;background:#10b981;color:#fff;cursor:pointer;font-size:12px;transition:all 0.2s;">👍 Sí</button>
          <button class="feedback-btn" data-feedback="negative" style="padding:6px 14px;border-radius:6px;border:1px solid #ef4444;background:#ef4444;color:#fff;cursor:pointer;font-size:12px;transition:all 0.2s;">👎 No</button>
        `;
        resumenText.parentElement.appendChild(feedbackDiv);
        
        // Eventos de feedback
        feedbackDiv.querySelectorAll('.feedback-btn').forEach(btn => {
          btn.addEventListener('click', async (e) => {
            const feedback = e.target.dataset.feedback;
            console.log(`Feedback ML: ${feedback}`);
            // TODO: Enviar feedback al backend para ML/recompensa
            try {
              await fetch('/api/ai/feedback', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ feedback, timestamp: new Date().toISOString() })
              });
              e.target.textContent = feedback === 'positive' ? '✅ Gracias!' : '📝 Mejorando...';
              e.target.disabled = true;
              setTimeout(() => feedbackDiv.style.display = 'none', 2000);
            } catch (err) {
              console.error('Error enviando feedback:', err);
            }
          });
        });
        
        statusEl.textContent = 'Actualizado';
    } catch (err) {
        statusEl.textContent = 'Error: ' + err.message;
        if (comprasList) comprasList.innerHTML = '<li style="color:#e11d48;">Error al cargar</li>';
    }
  }

  function toggleCollapse(){
    const panel = document.getElementById(PANEL_ID);
    if (!panel) return;
    panel.classList.toggle('collapsed');
  }

  function attachEvents(){
    document.querySelectorAll('.accordion-trigger').forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-target');
        if (target) toggleAccordion(target);
      });
    });
    const btn = document.getElementById('assistantBtn');
    const btnRefresh = document.getElementById('assistantRefresh');
    const btnCollapse = document.getElementById('assistantCollapse');
    if (btn) btn.addEventListener('click', refreshAssistant);
    if (btnRefresh) btnRefresh.addEventListener('click', refreshAssistant);
    if (btnCollapse) btnCollapse.addEventListener('click', toggleCollapse);
  }

  function init(){
    ensurePanel();
    attachEvents();
    refreshAssistant();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
