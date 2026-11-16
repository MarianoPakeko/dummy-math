import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Dummy Math | Trigonometry", layout="wide")

# ==========================================
# 🌐 DICCIONARIO MULTILINGÜE (EN / ES / IT)
# ==========================================
TEXTOS = {
    "English": {
        "title": "📐 Chapter 01: The Circle and the Shadows",
        "rule": "💡 **Fundamental Rule:** Because the unit circle has a fixed radius of **1**, **Sine** and **Cosine** are permanently trapped between **-1** and **1**. Their reciprocals (**Secant** and **Cosecant**) live completely outside that `[-1, 1]` corridor.",
        "sec1": "🌊 1. Perpetual Motion Banner (Circle & Waves)",
        "cap1": "Toggle one or more functions to highlight them simultaneously:",
        "btn_pause": "⏸️ Pause",
        "btn_play": "▶️ Play",
        "sin": "Sine (sin)",
        "cos": "Cosine (cos)",
        "tan": "Tangent (tan)",
        "csc": "Cosecant (1/sin)",
        "sec": "Secant (1/cos)",
        "cot": "Cotangent (1/tan)",
        "sec2": "🧮 2. Unit Circle & Trigonometric Calculator",
        "input_ang": "Type any angle in degrees (e.g., 30, 45, 90, -60, 720):",
        "rad_eq": "Equivalent in Radians:",
        "inf": "∞ (Undefined)"
    },
    "Español": {
        "title": "📐 Capítulo 01: El Círculo y las Sombras",
        "rule": "💡 **Regla Fundamental:** Como el círculo unitario tiene un radio fijo de **1**, el **Seno** y el **Coseno** están atrapados para siempre entre **-1** y **1**. Sus recíprocas (**Secante** y **Cosecante**) viven completamente fuera de ese pasillo `[-1, 1]`.",
        "sec1": "🌊 1. Banner de Movimiento Perpetuo (Círculo y Ondas)",
        "cap1": "Activa una o varias funciones para resaltarlas al mismo tiempo:",
        "btn_pause": "⏸️ Pausar",
        "btn_play": "▶️ Reanudar",
        "sin": "Seno (sen)",
        "cos": "Coseno (cos)",
        "tan": "Tangente (tan)",
        "csc": "Cosecante (1/sen)",
        "sec": "Secante (1/cos)",
        "cot": "Cotangente (1/tan)",
        "sec2": "🧮 2. Calculadora del Círculo Unitario",
        "input_ang": "Escribe cualquier ángulo en grados (ej. 30, 45, 90, -60, 720):",
        "rad_eq": "Equivalente en Radianes:",
        "inf": "∞ (Indefinido)"
    },
    "Italiano": {
        "title": "📐 Capitolo 01: Il Cerchio e le Ombre",
        "rule": "💡 **Regola Fondamentale:** Poiché il cerchio unitario ha un raggio fisso di **1**, **Seno** e **Coseno** sono intrappolati per sempre tra **-1** e **1**. Le loro reciproche (**Secante** e **Cosecante**) vivono completamente fuori dal corridoio `[-1, 1]`.",
        "sec1": "🌊 1. Banner a Moto Perpetuo (Cerchio e Onde)",
        "cap1": "Attiva una o più funzioni per evidenziarle contemporaneamente:",
        "btn_pause": "⏸️ Pausa",
        "btn_play": "▶️ Riprendi",
        "sin": "Seno (sen)",
        "cos": "Coseno (cos)",
        "tan": "Tangente (tan)",
        "csc": "Cosecante (1/sen)",
        "sec": "Secante (1/cos)",
        "cot": "Cotangente (1/tan)",
        "sec2": "🧮 2. Calcolatrice del Cerchio Unitario",
        "input_ang": "Inserisci qualsiasi angolo in gradi (es. 30, 45, 90, -60, 720):",
        "rad_eq": "Equivalente in Radianti:",
        "inf": "∞ (Indefinito)"
    }
}

# Selector de idioma en la parte superior derecha
col_t, col_lang = st.columns([4, 1])
with col_lang:
    idioma = st.selectbox("🌐 Language", ["Español", "English", "Italiano"], label_visibility="collapsed")

T = TEXTOS[idioma]

with col_t:
    st.title(T["title"])

st.info(T["rule"])

# ==========================================
# SECCIÓN 1: BANNER PERPETUO (HTML5 CANVAS 60 FPS)
# ==========================================
st.subheader(T["sec1"])
st.caption(T["cap1"])

c1, c2, c3, c4, c5, c6 = st.columns(6)
hi_sin = c1.toggle(f"🟢 {T['sin']}", value=True)
hi_cos = c2.toggle(f"🔵 {T['cos']}", value=True)
hi_tan = c3.toggle(f"🔴 {T['tan']}", value=False)
hi_csc = c4.toggle(f"🟩 {T['csc']}", value=False)
hi_sec = c5.toggle(f"🟦 {T['sec']}", value=False)
hi_cot = c6.toggle(f"🟣 {T['cot']}", value=False)

# Motor HTML5 Canvas con bucle infinito real (requestAnimationFrame) y 1 solo botón Play/Pause
html_canvas = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{
    margin: 0;
    background-color: #0e1117;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: white;
    overflow: hidden;
  }}
  .toolbar {{
    display: flex;
    align-items: center;
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
    transition: background 0.2s;
  }}
  button.paused {{
    background-color: #d29922;
  }}
  button:hover {{
    opacity: 0.9;
  }}
  canvas {{
    display: block;
    width: 100%;
    height: 300px;
    background-color: #0e1117;
    border-radius: 8px;
    border: 1px solid #21262d;
  }}
</style>
</head>
<body>
  <div class="toolbar">
    <button id="toggleBtn" onclick="togglePlay()">{T['btn_pause']}</button>
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
      if (isPlaying) {{
        btn.innerText = "{T['btn_pause']}";
        btn.classList.remove("paused");
      }} else {{
        btn.innerText = "{T['btn_play']}";
        btn.classList.add("paused");
      }}
    }}

    function resize() {{
      canvas.width = canvas.clientWidth * window.devicePixelRatio;
      canvas.height = 300 * window.devicePixelRatio;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    }}
    window.addEventListener('resize', resize);
    resize();

    function drawWave(fn, color, isHighlighted, startX, width, centerY, scaleY, isDashed=false) {{
      ctx.save();
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.globalAlpha = isHighlighted ? 1.0 : 0.14;
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
      const h = 300;
      ctx.clearRect(0, 0, w, h);

      const circleCenterX = Math.min(140, w * 0.22);
      const centerY = h / 2;
      const radius = 75;
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

      // Círculo Unitario fijo
      ctx.strokeStyle = '#8b949e';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(circleCenterX, centerY, radius, 0, 2 * Math.PI);
      ctx.stroke();

      // Líneas límite [-1, 1] en las ondas
      ctx.save();
      ctx.strokeStyle = '#8b949e';
      ctx.globalAlpha = 0.35;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(waveStartX, centerY - radius);
      ctx.lineTo(w - 20, centerY - radius);
      ctx.moveTo(waveStartX, centerY + radius);
      ctx.lineTo(w - 20, centerY + radius);
      ctx.stroke();
      ctx.restore();

      // Eje central de las ondas
      ctx.strokeStyle = '#30363d';
      ctx.beginPath();
      ctx.moveTo(waveStartX, centerY);
      ctx.lineTo(w - 20, centerY);
      ctx.stroke();

      // Posición actual en el círculo
      const cx = circleCenterX + Math.cos(angle) * radius;
      const cy = centerY - Math.sin(angle) * radius;

      // Sombra Coseno (Azul)
      ctx.save();
      ctx.strokeStyle = '#58a6ff';
      ctx.globalAlpha = active.cos ? 1.0 : 0.2;
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(circleCenterX, centerY);
      ctx.lineTo(cx, centerY);
      ctx.stroke();
      ctx.restore();

      // Sombra Seno (Verde)
      ctx.save();
      ctx.strokeStyle = '#3fb950';
      ctx.globalAlpha = active.sin ? 1.0 : 0.2;
      ctx.lineWidth = 4;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(cx, centerY);
      ctx.lineTo(cx, cy);
      ctx.stroke();
      ctx.restore();

      // Radio giratorio (Naranja)
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

      // Conector visual del círculo hacia el inicio de la onda Seno
      if (active.sin) {{
        ctx.save();
        ctx.strokeStyle = '#3fb950';
        ctx.globalAlpha = 0.4;
ctx.setLineDash([3, 3]);
ctx.beginPath();
ctx.moveTo(cx, cy);
ctx.lineTo(waveStartX, cy);
ctx.stroke();
ctx.restore();
}}
// Dibujar las 6 ondas en movimiento continuo
if (waveWidth > 50) {{
drawWave(t => Math.sin(t), '#3fb950', active.sin, waveStartX, waveWidth, centerY, radius);
drawWave(t => Math.cos(t), '#58a6ff', active.cos, waveStartX, waveWidth, centerY, radius);
drawWave(t => Math.tan(t), '#f85149', active.tan, waveStartX, waveWidth, centerY, radius, true);
drawWave(t => 1 / Math.sin(t), '#56d364', active.csc, waveStartX, waveWidth, centerY, radius, true);
drawWave(t => 1 / Math.cos(t), '#79c0ff', active.sec, waveStartX, waveWidth, centerY, radius, true);
drawWave(t => Math.cos(t) / Math.sin(t), '#d2a8ff', active.cot, waveStartX, waveWidth, centerY, radius, true);
}}
if (isPlaying) {{
angle += 0.025; // Velocidad perpetua suave
}}
requestAnimationFrame(animate);
}}
animate();


components.html(html_canvas, height=355)
st.divider()

==========================================


SECCIÓN 2: CALCULADORA MANUAL DEL CÍRCULO UNITARIO


==========================================

st.subheader(T["sec2"])
col_calc_left, col_calc_right = st.columns([1.1, 1.3])
with col_calc_left:
angulo_libre = st.number_input(T["input_ang"], value=45.0, step=15.0)
rad_libre = np.deg2rad(angulo_libre)
c_val = np.cos(rad_libre)
s_val = np.sin(rad_libre)
t_val = np.tan(rad_libre) if not np.isclose(c_val, 0, atol=1e-4) else np.nan
csc_v = 1.0 / s_val if not np.isclose(s_val, 0, atol=1e-4) else np.nan
sec_v = 1.0 / c_val if not np.isclose(c_val, 0, atol=1e-4) else np.nan
cot_v = c_val / s_val if not np.isclose(s_val, 0, atol=1e-4) else np.nan
st.caption(f"{T['rad_eq']} {rad_libre:.4f} rad ({rad_libre/np.pi:.2f} π)")
m1, m2, m3 = st.columns(3)
m1.metric(T["cos"], f"{c_val:.4f}")
m2.metric(T["sin"], f"{s_val:.4f}")
m3.metric(T["tan"], f"{t_val:.4f}" if not np.isnan(t_val) else T["inf"])
m4, m5, m6 = st.columns(3)
m4.metric(T["sec"], f"{sec_v:.4f}" if not np.isnan(sec_v) else T["inf"])
m5.metric(T["csc"], f"{csc_v:.4f}" if not np.isnan(csc_v) else T["inf"])
m6.metric(T["cot"], f"{cot_v:.4f}" if not np.isnan(cot_v) else T["inf"])
with col_calc_right:
theta_c = np.linspace(0, 2 * np.pi, 200)
fig_circle = go.Figure()
fig_circle.add_trace(go.Scatter(x=np.cos(theta_c), y=np.sin(theta_c), mode="lines",
line=dict(color="#8b949e", width=2), name="Unit Circle (R=1)"))
fig_circle.add_trace(go.Scatter(x=[0, c_val], y=[0, s_val], mode="lines+markers",
line=dict(color="#f0883e", width=3), marker=dict(size=10), name=f"{angulo_libre}°"))
fig_circle.add_trace(go.Scatter(x=[0, c_val], y=[0, 0], mode="lines",
line=dict(color="#58a6ff", width=4), name=T["cos"]))
fig_circle.add_trace(go.Scatter(x=[c_val, c_val], y=[0, s_val], mode="lines",
line=dict(color="#3fb950", width=4, dash="dot"), name=T["sin"]))
fig_circle.update_xaxes(range=[-1.3, 1.3], fixedrange=True, zeroline=True, zerolinecolor="#30363d")
fig_circle.update_yaxes(range=[-1.3, 1.3], fixedrange=True, scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="#30363d")
fig_circle.update_layout(template="plotly_dark", height=360, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig_circle, use_container_width=True)
