/* analytics.js
   Canvas charts (bar/line/donut) with:
   - responsive + crisp DPR rendering
   - hover tooltip + highlight
   - topN + sorting helpers
   - export PNG + CSV

   Fixes:
   - Boot waits for DOMContentLoaded (payload scripts + tooltip exist)
   - Tooltip is fetched lazily (no null crashes)
*/

(function () {

  function getTooltip() {
    return document.getElementById('tt');
  }

  function clamp(n, a, b) { return Math.max(a, Math.min(b, n)); }

  function niceNumber(n) {
    if (!isFinite(n)) return "0";
    if (n >= 1_000_000) return (n / 1_000_000).toFixed(2).replace(/\.00$/, '') + "M";
    if (n >= 1_000) return (n / 1_000).toFixed(2).replace(/\.00$/, '') + "k";
    return String(n);
  }

  // Deterministic palette (HSL steps). Returns CSS string.
  function colorForIndex(i) {
    const h = (i * 47) % 360;
    const s = 72;
    const l = 52;
    return `hsl(${h} ${s}% ${l}%)`;
  }

  function parsePayload(canvasId) {
  const node = document.querySelector(`script[data-payload="${CSS.escape(canvasId)}"]`);
  if (!node) {
    console.warn('Missing payload script for', canvasId);
    return null;
  }
  try {
    return JSON.parse(node.textContent || "{}");
  } catch (err) {
    console.warn('Bad JSON payload for', canvasId, err, node.textContent);
    return null;
  }
}


  function toXY(e, canvas) {
    const r = canvas.getBoundingClientRect();
    return { x: e.clientX - r.left, y: e.clientY - r.top, r };
  }

  function downloadText(filename, text) {
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function safeName(s) {
    return (s || 'chart')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .slice(0, 80);
  }

  function roundedRect(ctx, x, y, w, h, r) {
    r = Math.max(0, Math.min(r, Math.min(w, h) / 2));
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h);
    ctx.lineTo(x, y + h);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }

  class CanvasChart {
    constructor(canvas, payload) {
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');
      this.payload = payload;

      this.hits = [];
      this.hoverIndex = -1;
      this.data = [];

      this.ro = new ResizeObserver(() => this.render());
      this.ro.observe(this.canvas);

      this.canvas.addEventListener('mousemove', (e) => this.onMove(e));
      this.canvas.addEventListener('mouseleave', () => this.onLeave());

      this.render();
    }

    getTheme() {
      const t = document.documentElement.getAttribute('data-theme') || 'dark';
      if (t === 'light') {
        return {
          ink: '#0b1220',
          muted: 'rgba(11,18,32,.55)',
          stroke: 'rgba(11,18,32,.12)',
          grid: 'rgba(11,18,32,.08)'
        };
      }
      return {
        ink: '#eef1ff',
        muted: 'rgba(238,241,255,.55)',
        stroke: 'rgba(238,241,255,.14)',
        grid: 'rgba(238,241,255,.08)'
      };
    }

    normalizeData() {
      const raw = Array.isArray(this.payload.data) ? this.payload.data : [];
      let data = raw
        .map(d => ({
          clave: (d.clave ?? '').toString(),
          valor: Number(d.valor ?? 0)
        }))
        .filter(d => d.clave !== '' || d.valor !== 0);

      const opt = this.payload.options || {};

      // default sort: desc for bar/donut, none for line
      if (opt.sort === 'desc' || (opt.sort == null && this.payload.type !== 'line')) {
        data.sort((a, b) => b.valor - a.valor);
      } else if (opt.sort === 'asc') {
        data.sort((a, b) => a.valor - b.valor);
      }

      // topN
      if (opt.topN && Number.isFinite(+opt.topN) && data.length > +opt.topN) {
        const top = data.slice(0, +opt.topN);
        const rest = data.slice(+opt.topN);
        const restSum = rest.reduce((s, x) => s + x.valor, 0);
        top.push({ clave: '(other)', valor: restSum });
        data = top;
      }

      return data;
    }

    setupCanvas() {
      const dpr = window.devicePixelRatio || 1;
      const rect = this.canvas.getBoundingClientRect();
      const w = Math.max(300, rect.width);
      const h = Math.max(260, rect.height);

      this.canvas.width = Math.round(w * dpr);
      this.canvas.height = Math.round(h * dpr);

      this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      return { w, h };
    }

    clear(w, h) {
      this.ctx.clearRect(0, 0, w, h);
      this.ctx.fillStyle = 'rgba(0,0,0,0)';
      this.ctx.fillRect(0, 0, w, h);
    }

    render() {
      const theme = this.getTheme();
      const { w, h } = this.setupCanvas();
      this.hits = [];
      this.hoverIndex = -1;

      const data = this.normalizeData();
      this.data = data;

      this.clear(w, h);

      const pad = 14;
      const left = pad;
      const top = pad;
      const right = w - pad;
      const bottom = h - pad;

      if (!data.length) {
        this.ctx.fillStyle = theme.muted;
        this.ctx.font = '600 13px system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('No data for these filters', w / 2, h / 2);
        return;
      }

      if (this.payload.type === 'donut') {
        this.drawDonut(theme, left, top, right, bottom, data);
      } else if (this.payload.type === 'line') {
        this.drawLine(theme, left, top, right, bottom, data);
      } else {
        this.drawBars(theme, left, top, right, bottom, data);
      }
    }

    drawAxes(theme, x0, y0, x1, y1) {
      const ctx = this.ctx;

      ctx.strokeStyle = theme.stroke;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(x0, y1);
      ctx.lineTo(x1, y1);
      ctx.stroke();

      ctx.strokeStyle = theme.grid;
      const steps = 4;
      for (let i = 1; i <= steps; i++) {
        const y = y1 - (i / steps) * (y1 - y0);
        ctx.beginPath();
        ctx.moveTo(x0, y);
        ctx.lineTo(x1, y);
        ctx.stroke();
      }
    }

    drawBars(theme, left, top, right, bottom, data) {
      const ctx = this.ctx;

      const plotTop = top + 6;
      const plotBottom = bottom - 26;
      const plotLeft = left + 8;
      const plotRight = right - 8;

      const max = Math.max(...data.map(d => d.valor), 1);

      this.drawAxes(theme, plotLeft, plotTop, plotRight, plotBottom);

      // y labels
      ctx.fillStyle = theme.muted;
      ctx.font = '600 11px system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif';
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';
      for (let i = 0; i <= 4; i++) {
        const v = (i / 4) * max;
        const y = plotBottom - (i / 4) * (plotBottom - plotTop);
        ctx.fillText(niceNumber(Math.round(v)), plotLeft - 6, y);
      }

      const n = data.length;
      const gap = 6;
      const barW = ((plotRight - plotLeft) - gap * (n - 1)) / n;
      const radius = 10;

      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';

      for (let i = 0; i < n; i++) {
        const d = data[i];
        const x = plotLeft + i * (barW + gap);
        const barH = (d.valor / max) * (plotBottom - plotTop);
        const y = plotBottom - barH;

        const isHover = (i === this.hoverIndex);
        const col = colorForIndex(i);

        ctx.fillStyle = col;
        roundedRect(ctx, x, y, barW, barH, radius);
        ctx.fill();

        if (isHover) {
          ctx.strokeStyle = 'rgba(255,255,255,.65)';
          ctx.lineWidth = 2;
          roundedRect(ctx, x, y, barW, barH, radius);
          ctx.stroke();
        }

        ctx.fillStyle = theme.muted;
        const label = d.clave.length > 12 ? d.clave.slice(0, 12) + '…' : d.clave;
        ctx.fillText(label, x + barW / 2, plotBottom + 6);

        this.hits.push({
          type: 'bar',
          i,
          x, y, w: barW, h: barH,
          label: d.clave,
          value: d.valor,
          color: col
        });
      }
    }

    drawLine(theme, left, top, right, bottom, data) {
      const ctx = this.ctx;

      const plotTop = top + 6;
      const plotBottom = bottom - 26;
      const plotLeft = left + 34;
      const plotRight = right - 10;

      // Ensure chronological order for ISO-like keys
      data = data.slice().sort((a, b) => a.clave.localeCompare(b.clave));

      const max = Math.max(...data.map(d => d.valor), 1);
      this.drawAxes(theme, plotLeft, plotTop, plotRight, plotBottom);

      // y labels
      ctx.fillStyle = theme.muted;
      ctx.font = '600 11px system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif';
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';
      for (let i = 0; i <= 4; i++) {
        const v = (i / 4) * max;
        const y = plotBottom - (i / 4) * (plotBottom - plotTop);
        ctx.fillText(niceNumber(Math.round(v)), plotLeft - 8, y);
      }

      const n = data.length;
      const dx = (plotRight - plotLeft) / Math.max(1, n - 1);

      // line
      ctx.strokeStyle = colorForIndex(0);
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let i = 0; i < n; i++) {
        const d = data[i];
        const x = plotLeft + i * dx;
        const y = plotBottom - (d.valor / max) * (plotBottom - plotTop);
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();

      // points
      for (let i = 0; i < n; i++) {
        const d = data[i];
        const x = plotLeft + i * dx;
        const y = plotBottom - (d.valor / max) * (plotBottom - plotTop);

        const isHover = (i === this.hoverIndex);
        ctx.fillStyle = colorForIndex(0);
        ctx.beginPath();
        ctx.arc(x, y, isHover ? 5 : 3.5, 0, Math.PI * 2);
        ctx.fill();

        if (isHover) {
          ctx.strokeStyle = 'rgba(255,255,255,.65)';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.arc(x, y, 8, 0, Math.PI * 2);
          ctx.stroke();
        }

        this.hits.push({
          type: 'point',
          i,
          cx: x,
          cy: y,
          r: 10,
          label: d.clave,
          value: d.valor,
          color: colorForIndex(0)
        });
      }

      // x labels (sparse)
      ctx.fillStyle = theme.muted;
      ctx.font = '600 11px system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';

      const step = Math.ceil(n / 6);
      for (let i = 0; i < n; i += step) {
        const x = plotLeft + i * dx;
        ctx.fillText(data[i].clave, x, plotBottom + 6);
      }
    }

    drawDonut(theme, left, top, right, bottom, data) {
      const ctx = this.ctx;

      const w = right - left;
      const h = bottom - top;

      const cx = left + w * 0.38;
      const cy = top + h * 0.52;
      const r = Math.min(w, h) * 0.30;
      const r2 = r * 0.62;

      const total = data.reduce((s, x) => s + x.valor, 0) || 1;
      let a0 = -Math.PI / 2;

      for (let i = 0; i < data.length; i++) {
        const d = data[i];
        const frac = d.valor / total;
        const a1 = a0 + frac * Math.PI * 2;
        const col = colorForIndex(i);
        const isHover = (i === this.hoverIndex);

        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.arc(cx, cy, r, a0, a1);
        ctx.closePath();
        ctx.fillStyle = col;
        ctx.fill();

        if (isHover) {
          ctx.strokeStyle = 'rgba(255,255,255,.65)';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.arc(cx, cy, r + 2, a0, a1);
          ctx.stroke();
        }

        this.hits.push({
          type: 'slice',
          i,
          cx, cy,
          rOuter: r,
          rInner: r2,
          a0, a1,
          label: d.clave,
          value: d.valor,
          color: col
        });

        a0 = a1;
      }

      // hole
      ctx.globalCompositeOperation = 'destination-out';
      ctx.beginPath();
      ctx.arc(cx, cy, r2, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalCompositeOperation = 'source-over';

      // center label
      ctx.fillStyle = theme.ink;
      ctx.font = '800 18px system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(niceNumber(total), cx, cy - 4);

      ctx.fillStyle = theme.muted;
      ctx.font = '600 12px system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif';
      ctx.fillText('total', cx, cy + 16);

      // legend
      const lx = left + w * 0.70;
      let ly = top + 16;

      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.font = '600 12px system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif';

      const maxLegend = Math.min(10, data.length);
      for (let i = 0; i < maxLegend; i++) {
        const d = data[i];
        const col = colorForIndex(i);
        const pct = ((d.valor / total) * 100).toFixed(1);

        ctx.fillStyle = col;
        ctx.fillRect(lx, ly - 6, 12, 12);

        ctx.fillStyle = theme.ink;
        const name = d.clave.length > 18 ? d.clave.slice(0, 18) + '…' : d.clave;
        ctx.fillText(`${name} · ${pct}%`, lx + 18, ly);

        ly += 18;
      }
    }

    onMove(e) {
      const { x, y, r } = toXY(e, this.canvas);
      const hit = this.findHit(x, y);
      const tooltip = getTooltip();

      if (!hit) {
        this.hoverIndex = -1;
        if (tooltip) tooltip.style.display = 'none';
        this.render();
        return;
      }

      this.hoverIndex = hit.i;
      this.render();

      if (tooltip) {
        tooltip.style.display = 'block';
        tooltip.textContent = `${hit.label} — ${hit.value}`;
        tooltip.style.left = `${r.left + x}px`;
        tooltip.style.top = `${r.top + y}px`;
      }
    }

    onLeave() {
      this.hoverIndex = -1;
      const tooltip = getTooltip();
      if (tooltip) tooltip.style.display = 'none';
      this.render();
    }

    findHit(x, y) {
      for (const h of this.hits) {
        if (h.type === 'bar') {
          if (x >= h.x && x <= h.x + h.w && y >= h.y && y <= h.y + h.h) return h;
        }
        if (h.type === 'point') {
          const dx = x - h.cx, dy = y - h.cy;
          if ((dx * dx + dy * dy) <= (h.r * h.r)) return h;
        }
        if (h.type === 'slice') {
          const dx = x - h.cx, dy = y - h.cy;
          const rr = Math.sqrt(dx * dx + dy * dy);
          if (rr < h.rInner || rr > h.rOuter) continue;

          let ang = Math.atan2(dy, dx);
          while (ang < h.a0) ang += Math.PI * 2;
          while (ang > h.a1) ang -= Math.PI * 2;
          if (ang >= h.a0 && ang <= h.a1) return h;
        }
      }
      return null;
    }

    exportPNG() {
      const a = document.createElement('a');
      a.download = `${safeName(this.payload.title)}.png`;
      a.href = this.canvas.toDataURL('image/png');
      a.click();
    }

    exportCSV() {
      const rows = [["clave", "valor"], ...this.data.map(d => [d.clave, String(d.valor)])];
      const csv = rows.map(r => r.map(cell => {
        const s = String(cell).replace(/"/g, '""');
        return `"${s}"`;
      }).join(",")).join("\n");
      downloadText(`${safeName(this.payload.title)}.csv`, csv);
    }
  }

  // -----------------------
  // Boot (after DOM ready)
  // -----------------------
  const charts = new Map();

  function boot() {
    document.querySelectorAll('canvas[data-chart="1"]').forEach((canvas) => {
      const payload = parsePayload(canvas.id);
      if (!payload) return;
      charts.set(canvas.id, new CanvasChart(canvas, payload));
    });

    document.querySelectorAll('button[data-export]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-target');
        const kind = btn.getAttribute('data-export');
        const ch = charts.get(target);
        if (!ch) return;
        if (kind === 'png') ch.exportPNG();
        if (kind === 'csv') ch.exportCSV();
      });
    });

    const mo = new MutationObserver(() => {
      charts.forEach(ch => ch.render());
    });
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

})();

