import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Dummy Math | Chapter 01: Trigonometry", layout="wide")

st.title("📐 Chapter 01: The Circle and the Shadows")
st.info(
    "💡 **Fundamental Rule:** Because the unit circle has a fixed radius of **1**, "
    "**Sine** and **Cosine** are permanently trapped between **-1** and **1**. "
    "Their reciprocals (**Secant** and **Cosecant**) live completely outside that `[-1, 1]` corridor."
)

# ==========================================
# SECCIÓN 1: BANNER SINCRONIZADO CON SELECCIÓN MÚLTIPLE
# ==========================================
st.subheader("🌊 1. Synchronized Circle & Wave Banner")
st.caption("Toggle one or more functions below to highlight them simultaneously:")

# Fila de 6 interruptores independientes para selección múltiple inmediata
c1, c2, c3, c4, c5, c6 = st.columns(6)
hi_sin = c1.toggle("🟢 Sine (sin)", value=True)
hi_cos = c2.toggle("🔵 Cosine (cos)", value=True)
hi_tan = c3.toggle("🔴 Tangent (tan)", value=False)
hi_csc = c4.toggle("🟩 Cosecant (1/sin)", value=False)
hi_sec = c5.toggle("🟦 Secant (1/cos)", value=False)
hi_cot = c6.toggle("🟣 Cotangent (1/tan)", value=False)

# Si el usuario apaga todos, mantenemos todos visibles tenues para no dejar el gráfico vacío
def get_style(is_active, base_w=2.5):
    if is_active:
        return 1.0, base_w + 1.2
    return 0.12, base_w - 0.5

op_sin, lw_sin = get_style(hi_sin)
op_cos, lw_cos = get_style(hi_cos)
op_tan, lw_tan = get_style(hi_tan, 2.2)
op_csc, lw_csc = get_style(hi_csc, 2.2)
op_sec, lw_sec = get_style(hi_sec, 2.2)
op_cot, lw_cot = get_style(hi_cot, 2.2)

def clean_inf(arr, limit=3.2):
    c = arr.copy()
    c[np.abs(c) > limit] = np.nan
    return c

# Eje X para el banner de ondas (0 a 4*pi = 2 ciclos completos)
x_banner = np.linspace(0, 4 * np.pi, 240)

def calcular_ondas(fase):
    s = np.sin(fase - x_banner)
    c = np.cos(fase - x_banner)
    t = clean_inf(np.tan(fase - x_banner))
    csc = clean_inf(1.0 / np.where(np.isclose(s, 0, atol=1e-2), np.nan, s))
    sec = clean_inf(1.0 / np.where(np.isclose(c, 0, atol=1e-2), np.nan, c))
    cot = clean_inf(c / np.where(np.isclose(s, 0, atol=1e-2), np.nan, s))
    return s, c, t, csc, sec, cot

# Figura doble sincronizada
fig_banner = make_subplots(
    rows=1, cols=2,
    column_widths=[0.28, 0.72],
    horizontal_spacing=0.06,
    subplot_titles=("Rotating Unit Circle", "Waves Flowing From Circle")
)

# 1. Círculo fijo de fondo (Trazo 0)
theta_c = np.linspace(0, 2 * np.pi, 150)
fig_banner.add_trace(go.Scatter(x=np.cos(theta_c), y=np.sin(theta_c), mode="lines",
                                line=dict(color="#8b949e", width=2), showlegend=False), row=1, col=1)

# Estado inicial
s0, c0, t0, csc0, sec0, cot0 = calcular_ondas(0)

# Trazos dinámicos del círculo (Trazos 1, 2, 3)
fig_banner.add_trace(go.Scatter(x=[0, 1], y=[0, 0], mode="lines+markers",
                                line=dict(color="#f0883e", width=3), marker=dict(size=8), name="Radius"), row=1, col=1)
fig_banner.add_trace(go.Scatter(x=[0, 1], y=[0, 0], mode="lines",
                                line=dict(color="#58a6ff", width=lw_cos + 1.5), opacity=op_cos, showlegend=False), row=1, col=1)
fig_banner.add_trace(go.Scatter(x=[1, 1], y=[0, 0], mode="lines",
                                line=dict(color="#3fb950", width=lw_sin + 1.5, dash="dot"), opacity=op_sin, showlegend=False), row=1, col=1)

# Trazos dinámicos de las 6 ondas (Trazos 4, 5, 6, 7, 8, 9)
fig_banner.add_trace(go.Scatter(x=x_banner, y=s0, mode="lines", line=dict(color="#3fb950", width=lw_sin), opacity=op_sin, name="Sine (sin)"), row=1, col=2)
fig_banner.add_trace(go.Scatter(x=x_banner, y=c0, mode="lines", line=dict(color="#58a6ff", width=lw_cos), opacity=op_cos, name="Cosine (cos)"), row=1, col=2)
fig_banner.add_trace(go.Scatter(x=x_banner, y=t0, mode="lines", line=dict(color="#f85149", width=lw_tan, dash="dash"), opacity=op_tan, name="Tangent (tan)"), row=1, col=2)
fig_banner.add_trace(go.Scatter(x=x_banner, y=csc0, mode="lines", line=dict(color="#56d364", width=lw_csc, dash="dot"), opacity=op_csc, name="Cosecant (1/sin)"), row=1, col=2)
fig_banner.add_trace(go.Scatter(x=x_banner, y=sec0, mode="lines", line=dict(color="#79c0ff", width=lw_sec, dash="dot"), opacity=op_sec, name="Secant (1/cos)"), row=1, col=2)
fig_banner.add_trace(go.Scatter(x=x_banner, y=cot0, mode="lines", line=dict(color="#d2a8ff", width=lw_cot, dash="dashdot"), opacity=op_cot, name="Cotangent (1/tan)"), row=1, col=2)

indices_animados = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Líneas límite [-1, 1]
fig_banner.add_hline(y=1, line_width=1, line_dash="dot", line_color="#8b949e", opacity=0.4, row=1, col=2)
fig_banner.add_hline(y=-1, line_width=1, line_dash="dot", line_color="#8b949e", opacity=0.4, row=1, col=2)

# Generar 60 frames sincronizados
frames = []
fases = np.linspace(0, 2 * np.pi, 60, endpoint=False)
for idx, f in enumerate(fases):
    cx, cy = np.cos(f), np.sin(f)
    sf, cf, tf, cscf, secf, cotf = calcular_ondas(f)
    
    frame_data = [
        go.Scatter(x=[0, cx], y=[0, cy]),
        go.Scatter(x=[0, cx], y=[0, 0]),
        go.Scatter(x=[cx, cx], y=[0, cy]),
        go.Scatter(y=sf),
        go.Scatter(y=cf),
        go.Scatter(y=tf),
        go.Scatter(y=cscf),
        go.Scatter(y=secf),
        go.Scatter(y=cotf)
    ]
    frames.append(go.Frame(data=frame_data, traces=indices_animados, name=str(idx)))

fig_banner.frames = frames

# Ejes fijos
fig_banner.update_xaxes(range=[-1.25, 1.25], fixedrange=True, zeroline=True, zerolinecolor="#30363d", row=1, col=1)
fig_banner.update_yaxes(range=[-1.25, 1.25], fixedrange=True, scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="#30363d", row=1, col=1)

fig_banner.update_xaxes(
    range=[0, 4 * np.pi],
    tickvals=[0, np.pi, 2*np.pi, 3*np.pi, 4*np.pi],
    ticktext=["0 (Now)", "π", "2π", "3π", "4π"],
    fixedrange=True, gridcolor="#21262d", row=1, col=2
)
fig_banner.update_yaxes(range=[-2.5, 2.5], fixedrange=True, zeroline=True, zerolinecolor="#30363d", gridcolor="#21262d", row=1, col=2)

fig_banner.update_layout(
    template="plotly_dark",
    height=350,
    margin=dict(l=20, r=20, t=45, b=20),
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        x=0.0, y=1.18,
        direction="left",
        buttons=[
            dict(label="▶️ Play Motion", method="animate",
                 args=[None, dict(frame=dict(duration=35, redraw=False), fromcurrent=True, mode="immediate", loop=True)]),
            dict(label="⏸️ Pause", method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])
        ]
    )]
)

st.plotly_chart(fig_banner, use_container_width=True)

st.divider()

# ==========================================
# SECCIÓN 2: CALCULADORA MANUAL DEL CÍRCULO UNITARIO
# ==========================================
st.subheader("🧮 2. Unit Circle & Trigonometric Calculator")

col_calc_left, col_calc_right = st.columns([1.1, 1.3])

with col_calc_left:
    angulo_libre = st.number_input("Type any angle in degrees (e.g., 30, 45, 90, -60, 720):", value=45.0, step=15.0)
    
    rad_libre = np.deg2rad(angulo_libre)
    c_val = np.cos(rad_libre)
    s_val = np.sin(rad_libre)
    t_val = np.tan(rad_libre) if not np.isclose(c_val, 0, atol=1e-4) else np.nan
    csc_v = 1.0 / s_val if not np.isclose(s_val, 0, atol=1e-4) else np.nan
    sec_v = 1.0 / c_val if not np.isclose(c_val, 0, atol=1e-4) else np.nan
    cot_v = c_val / s_val if not np.isclose(s_val, 0, atol=1e-4) else np.nan

    st.caption(f"Equivalent in Radians: **{rad_libre:.4f} rad** ({rad_libre/np.pi:.2f} π)")

    m1, m2, m3 = st.columns(3)
    m1.metric("Cosine (X)", f"{c_val:.4f}")
    m2.metric("Sine (Y)", f"{s_val:.4f}")
    m3.metric("Tangent", f"{t_val:.4f}" if not np.isnan(t_val) else "∞")

    m4, m5, m6 = st.columns(3)
    m4.metric("Secant (1/cos)", f"{sec_v:.4f}" if not np.isnan(sec_v) else "∞")
    m5.metric("Cosecant (1/sin)", f"{csc_v:.4f}" if not np.isnan(csc_v) else "∞")
    m6.metric("Cotangent (1/tan)", f"{cot_v:.4f}" if not np.isnan(cot_v) else "∞")

with col_calc_right:
    fig_circle = go.Figure()
    
    fig_circle.add_trace(go.Scatter(x=np.cos(theta_c), y=np.sin(theta_c), mode="lines",
                                    line=dict(color="#8b949e", width=2), name="Unit Circle (R=1)"))
    fig_circle.add_trace(go.Scatter(x=[0, c_val], y=[0, s_val], mode="lines+markers",
                                    line=dict(color="#f0883e", width=3), marker=dict(size=10), name=f"Radius ({angulo_libre}°)"))
    fig_circle.add_trace(go.Scatter(x=[0, c_val], y=[0, 0], mode="lines",
                                    line=dict(color="#58a6ff", width=4), name="Cosine Shadow (X)"))
    fig_circle.add_trace(go.Scatter(x=[c_val, c_val], y=[0, s_val], mode="lines",
                                    line=dict(color="#3fb950", width=4, dash="dot"), name="Sine Shadow (Y)"))

    fig_circle.update_xaxes(range=[-1.3, 1.3], fixedrange=True, zeroline=True, zerolinecolor="#30363d")
    fig_circle.update_yaxes(range=[-1.3, 1.3], fixedrange=True, scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="#30363d")
    fig_circle.update_layout(template="plotly_dark", height=360, margin=dict(l=10, r=10, t=10, b=10))
    
    st.plotly_chart(fig_circle, use_container_width=True)
