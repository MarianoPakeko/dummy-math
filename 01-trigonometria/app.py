import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Dummy Math | Trigonometry", layout="wide")

TEXTOS = {
    "Español": {
        "title": "📐 Capítulo 01: El Círculo y las Sombras",
        "cap": "Activa una o varias ondas para resaltarlas al mismo tiempo:",
        "pause": "⏸️ Pausar",
        "play": "▶️ Reanudar",
        "sin": "Seno (sen)",
        "cos": "Coseno (cos)",
        "tan": "Tangente (tan)",
        "csc": "Cosecante (1/sen)",
        "sec": "Secante (1/cos)",
        "cot": "Cotangente (1/tan)"
    },
    "English": {
        "title": "📐 Chapter 01: The Circle and the Shadows",
        "cap": "Toggle one or more waves to highlight them simultaneously:",
        "pause": "⏸️ Pause",
        "play": "▶️ Play",
        "sin": "Sine (sin)",
        "cos": "Cosine (cos)",
        "tan": "Tangent (tan)",
        "csc": "Cosecant (1/sin)",
        "sec": "Secant (1/cos)",
        "cot": "Cotangent (1/tan)"
    },
    "Italiano": {
        "title": "📐 Capitolo 01: Il Cerchio e le Ombre",
        "cap": "Attiva una o più onde per evidenziarle contemporaneamente:",
        "pause": "⏸️ Pausa",
        "play": "▶️ Riprendi",
        "sin": "Seno (sen)",
        "cos": "Coseno (cos)",
        "tan": "Tangente (tan)",
        "csc": "Cosecante (1/sen)",
        "sec": "Secante (1/cos)",
        "cot": "Cotangente (1/tan)"
    }
}

col_t, col_lang = st.columns([4, 1])
with col_lang:
    idioma = st.selectbox("🌐", ["Español", "English", "Italiano"], label_visibility="collapsed")

T = TEXTOS[idioma]
with col_t:
    st.title(T["title"])

st.caption(T["cap"])

# 6 interruptores independientes
c1, c2, c3, c4, c5, c6 = st.columns(6)
hi_sin = c1.toggle(f"🟢 {T['sin']}", value=True)
hi_cos = c2.toggle(f"🔵 {T['cos']}", value=True)
hi_tan = c3.toggle(f"🔴 {T['tan']}", value=False)
hi_csc = c4.toggle(f"🟩 {T['csc']}", value=False)
hi_sec = c5.toggle(f"🟦 {T['sec']}", value=False)
hi_cot = c6.toggle(f"🟣 {T['cot']}", value=False)

html_canvas = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{
    margin: 0;
    background-color: #0e1117;
    font-family: sans-serif;
    color: white;
    overflow: hidden;
  }}
  .toolbar {{
    padding: 6px 12px;
    background: #161b22;
    border-radius: 8px;
    margin-bottom: 8px;
    border: 1px solid #30363d;
  }}
  button {{
    background-color: #238636;
    color: white;
    border: none;
    padding: 6px 16px;
    font-size: 14px;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
  }}
  button.paused {{
    background-color: #d29922;
  }}
  canvas {{
    display: block;
    width: 100%;
    height: 340px;
    background-color: #0e1117;
    border-radius: 8px;
    border: 1px solid #21262d;
  }}
</style>
</head>
<body>
  <div class="toolbar">
    <button id="toggleBtn" onclick="togglePlay()">{T['pause']}</button>
  </div>
  <canvas id="trigCanvas"></canvas>

  <script>
    const canvas = document.getElementById('trigCanvas');
    const ctx = canvas.getContext('2d');
    const btn = document.getElementById('toggleBtn');

    let isPlaying = true;
    let angle = 0;

    const active = {{
      sin: {'true' if hi_sin else 'false'},
      cos: {'true' if hi_cos else 'false'},
      tan: {'true' if hi_tan else 'false'},
      csc: {'true' if hi_csc else 'false'},
      sec: {'true' if hi_sec else 'false'},
      cot: {'true' if hi_cot else 'false'}
    }};

    function togglePlay() {{
      isPlaying = !isPlaying;
      btn.innerText = isPlaying ? "{T['pause']}" : "{T['play']}";
      btn.classList.toggle("paused", !isPlaying);
    }}

    function resize() {{
      canvas.width = canvas.clientWidth * window.devicePixelRatio;
      canvas.height = 340 * window.devicePixelRatio;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    }}
    window.addEventListener('resize', resize);
    resize();

    function drawWave(fn, color, isHighlighted, startX, width, centerY, scaleY, isDashed=false) {{
      ctx.save();
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.globalAlpha = isHighlighted ? 1.0 : 0.12;
      ctx.lineWidth = isHighlighted ? 3.2 : 1.5;
      if (isDashed) ctx.setLineDash([5, 5]);

      let drawing = false;
      for (let px = 0; px <= width; px += 2) {{
        const theta = angle - (px / width) * 4 * Math.PI;
        const val = fn(theta);
        if (Math.abs(val) > 3.2 || isNaN(val)) {{
          drawing = false;
          continue;
        }}
        const py = centerY - val * scaleY;
        if (!drawing) {{
          ctx.moveTo(startX + px, py);
          drawing = true;
        }} else {{
          ctx.lineTo(startX + px, py);
        }}
      }}
      ctx.stroke();
      ctx.restore();
    }}

    function animate() {{
      const w = canvas.clientWidth;
      const h = 340;
      ctx.clearRect(0, 0, w, h);

      const circleCenterX = Math.min(150, w * 0.22);
      const centerY = h / 2;
      const radius = 85;
      const waveStartX = circleCenterX + radius + 55;
      const waveWidth = w - waveStartX - 20;

      // Ejes del círculo
      ctx.strokeStyle = '#30363d';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(circleCenterX - radius - 15, centerY);
      ctx.lineTo(circleCenterX + radius + 15, centerY);
      ctx.moveTo(circleCenterX, centerY - radius - 15);
      ctx.lineTo(circleCenterX, centerY + radius + 15);
      ctx.stroke();

      // Círculo Unitario
      ctx.strokeStyle = '#8b949e';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(circleCenterX, centerY, radius, 0, 2 * Math.PI);
      ctx.stroke();

      // Líneas límite [-1, 1]
      ctx.save();
      ctx.strokeStyle = '#8b949e';
      ctx.globalAlpha = 0.3;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(waveStartX, centerY - radius);
      ctx.lineTo(w - 20, centerY - radius);
      ctx.moveTo(waveStartX, centerY + radius);
      ctx.lineTo(w - 20, centerY + radius);
      ctx.stroke();
      ctx.restore();

      // Eje central de ondas
      ctx.strokeStyle = '#30363d';
      ctx.beginPath();
      ctx.moveTo(waveStartX, centerY);
      ctx.lineTo(w - 20, centerY);
      ctx.stroke();

      const cx = circleCenterX + Math.cos(angle) * radius;
      const cy = centerY - Math.sin(angle) * radius;

      // Sombra Coseno (Azul)
      ctx.save();
      ctx.strokeStyle = '#58a6ff';
      ctx.globalAlpha = active.cos ? 1.0 : 0.15;
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(circleCenterX, centerY);
      ctx.lineTo(cx, centerY);
      ctx.stroke();
      ctx.restore();

      // Sombra Seno (Verde)
      ctx.save();
      ctx.strokeStyle = '#3fb950';
      ctx.globalAlpha = active.sin ? 1.0 : 0.15;
      ctx.lineWidth = 4;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(cx, centerY);
      ctx.lineTo(cx, cy);
      ctx.stroke();
      ctx.restore();

      // Radio giratorio
      ctx.strokeStyle = '#f0883e';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(circleCenterX, centerY);
      ctx.lineTo(cx, cy);
      ctx.stroke();

      ctx.fillStyle = '#f0883e';
      ctx.beginPath();
      ctx.arc(cx, cy, 5, 0, 2 * Math.PI);
      ctx.fill();

      // Conector del Seno hacia la onda
      if (active.sin) {{
        ctx.save();
        ctx.strokeStyle = '#3fb950';
        ctx.globalAlpha = 0.45;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(waveStartX, cy);
        ctx.stroke();
        ctx.restore();
      }}

      // Dibujar las 6 ondas
      if (waveWidth > 50) {{
        drawWave(t => Math.sin(t), '#3fb950', active.sin, waveStartX, waveWidth, centerY, radius);
        drawWave(t => Math.cos(t), '#58a6ff', active.cos, waveStartX, waveWidth, centerY, radius);
        drawWave(t => Math.tan(t), '#f85149', active.tan, waveStartX, waveWidth, centerY, radius, true);
        drawWave(t => 1 / Math.sin(t), '#56d364', active.csc, waveStartX, waveWidth, centerY, radius, true);
        drawWave(t => 1 / Math.cos(t), '#79c0ff', active.sec, waveStartX, waveWidth, centerY, radius, true);
        drawWave(t => Math.cos(t) / Math.sin(t), '#d2a8ff', active.cot, waveStartX, waveWidth, centerY, radius, true);
      }}

      if (isPlaying) {{
        angle += 0.025;
      }}
      requestAnimationFrame(animate);
    }}

    animate();
  </script>
</body>
</html>
"""

components.html(html_canvas, height=400)
