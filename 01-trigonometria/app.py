
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Dummy Math | Chapter 01: Trigonometry", layout="wide")

st.title("📐 Chapter 01: The Circle and the Shadows")
st.info(
    "💡 **Fundamental Rule:** Because the unit circle has a fixed radius of **1**, "
    "**Sine** and **Cosine** are permanently trapped between **-1** and **1**. "
    "Their reciprocals (**Secant** and **Cosecant**) live completely outside that `[-1, 1]` corridor."
)

# ==========================================
# SECCIÓN 1: BANNER DE ONDAS EN MOVIMIENTO CONTINUO
# ==========================================
st.subheader("🌊 1. Continuous Wave Banner (Oscilloscope View)")

col_b1, col_b2 = st.columns([2, 1])
with col_b1:
    foco = st.selectbox(
        "🔍 Highlight Wave Intensity:",
        ["All Equal", "Sine (sin)", "Cosine (cos)", "Tangent (tan)", "Cosecant (1/sin)", "Secant (1/cos)", "Cotangent (1/tan)"]
    )
with col_b2:
    st.write("")
    st.write("")
    mostrar_rec = st.checkbox("Include Reciprocals (sec, csc, cot)", value=True)

def get_style(name, base_w=2.5):
    if foco == "All Equal":
        return 1.0, base_w
    return (1.0, base_w + 2.2) if foco == name else (0.15, base_w)

op_sin, lw_sin = get_style("Sine (sin)")
op_cos, lw_cos = get_style("Cosine (cos)")
op_tan, lw_tan = get_style("Tangent (tan)", 2.0)
op_csc, lw_csc = get_style("Cosecant (1/sin)", 2.0)
op_sec, lw_sec = get_style("Secant (1/cos)", 2.0)
op_cot, lw_cot = get_style("Cotangent (1/tan)", 2.0)

def clean_inf(arr, limit=3.5):
    c = arr.copy()
    c[np.abs(c) > limit] = np.nan
    return c

# Eje X espacial para el banner (0 a 4*pi = 2 ciclos completos)
x_banner = np.linspace(0, 4 * np.pi, 300)

def calcular_ondas(fase):
    s = np.sin(x_banner - fase)
    c = np.cos(x_banner - fase)
    t = clean_inf(np.tan(x_banner - fase))
    csc = clean_inf(1.0 / np.where(np.isclose(s, 0, atol=1e-2), np.nan, s))
    sec = clean_inf(1.0 / np.where(np.isclose(c, 0, atol=1e-2), np.nan, c))
    cot = clean_inf(c / np.where(np.isclose(s, 0, atol=1e-2), np.nan, s))
    return s, c, t, csc, sec, cot

s0, c0, t0, csc0, sec0, cot0 = calcular_ondas(0)

fig_banner = go.Figure()

# Líneas límite [-1, 1]
fig_banner.add_hline(y=1, line_width=1, line_dash="dot", line_color="#8b949e", opacity=0.4)
fig_banner.add_hline(y=-1, line_width=1, line_dash="dot", line_color="#8b949e", opacity=0.4)

# Trazos iniciales
fig_banner.add_trace(go.Scatter(x=x_banner, y=s0, mode="lines", line=dict(color="#3fb950", width=lw_sin), opacity=op_sin, name="Sine (sin)"))
fig_banner.add_trace(go.Scatter(x=x_banner, y=c0, mode="lines", line=dict(color="#58a6ff", width=lw_cos), opacity=op_cos, name="Cosine (cos)"))
fig_banner.add_trace(go.Scatter(x=x_banner, y=t0, mode="lines", line=dict(color="#f85149", width=lw_tan, dash="dash"), opacity=op_tan, name="Tangent (tan)"))

if mostrar_rec:
    fig_banner.add_trace(go.Scatter(x=x_banner, y=csc0, mode="lines", line=dict(color="#56d364", width=lw_csc, dash="dot"), opacity=op_csc, name="Cosecant (1/sin)"))
    fig_banner.add_trace(go.Scatter(x=x_banner, y=sec0, mode="lines", line=dict(color="#79c0ff", width=lw_sec, dash="dot"), opacity=op_sec, name="Secant (1/cos)"))
    fig_banner.add_trace(go.Scatter(x=x_banner, y=cot0, mode="lines", line=dict(color="#d2a8ff", width=lw_cot, dash="dashdot"), opacity=op_cot, name="Cotangent (1/tan)"))

# Generar 60 frames donde las ondas completas avanzan, suben y bajan suavemente
frames = []
fases = np.linspace(0, 2 * np.pi, 60, endpoint=False)
for idx, f in enumerate(fases):
    sf, cf, tf, cscf, secf, cotf = calcular_ondas(f)
    frame_data = [
        go.Scatter(y=sf),
        go.Scatter(y=cf),
        go.Scatter(y=tf)
    ]
    if mostrar_rec:
        frame_data.extend([
            go.Scatter(y=cscf),
            go.Scatter(y=secf),
            go.Scatter(y=cotf)
        ])
    frames.append(go.Frame(data=frame_data, name=str(idx)))

fig_banner.frames = frames

fig_banner.update_xaxes(
    range=[0, 4 * np.pi],
    tickvals=[0, np.pi, 2*np.pi, 3*np.pi, 4*np.pi],
    ticktext=["0", "π", "2π", "3π", "4π"],
    fixedrange=True, showgrid=True, gridcolor="#21262d"
)
fig_banner.update_yaxes(range=[-2.8, 2.8], fixedrange=True, zeroline=True, zerolinecolor="#30363d", gridcolor="#21262d")

fig_banner.update_layout(
    template="plotly_dark",
    height=320,
    margin=dict(l=20, r=20, t=40, b=20),
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        x=0.01, y=1.18,
        direction="left",
        buttons=[
            dict(label="▶️ Play Waves", method="animate",
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

    # Cuadrícula de las 6 métricas
    m1, m2, m3 = st.columns(3)
    m1.metric("Cosine (X)", f"{c_val:.4f}")
    m2.metric("Sine (Y)", f"{s_val:.4f}")
    m3.metric("Tangent", f"{t_val:.4f}" if not np.isnan(t_val) else "∞")

    m4, m5, m6 = st.columns(3)
    m4.metric("Secant (1/cos)", f"{sec_v:.4f}" if not np.isnan(sec_v) else "∞")
    m5.metric("Cosecant (1/sin)", f"{csc_v:.4f}" if not np.isnan(csc_v) else "∞")
    m6.metric("Cotangent (1/tan)", f"{cot_v:.4f}" if not np.isnan(cot_v) else "∞")

with col_calc_right:
    theta_c = np.linspace(0, 2 * np.pi, 200)
    fig_circle = go.Figure()
    
    # Círculo unitario fijo
    fig_circle.add_trace(go.Scatter(x=np.cos(theta_c), y=np.sin(theta_c), mode="lines",
                                    line=dict(color="#8b949e", width=2), name="Unit Circle (R=1)"))
    # Radio
    fig_circle.add_trace(go.Scatter(x=[0, c_val], y=[0, s_val], mode="lines+markers",
                                    line=dict(color="#f0883e", width=3), marker=dict(size=10), name=f"Radius ({angulo_libre}°)"))
    # Sombra Coseno
    fig_circle.add_trace(go.Scatter(x=[0, c_val], y=[0, 0], mode="lines",
                                    line=dict(color="#58a6ff", width=4), name="Cosine Shadow (X)"))
    # Sombra Seno
    fig_circle.add_trace(go.Scatter(x=[c_val, c_val], y=[0, s_val], mode="lines",
                                    line=dict(color="#3fb950", width=4, dash="dot"), name="Sine Shadow (Y)"))

    fig_circle.update_xaxes(range=[-1.3, 1.3], fixedrange=True, zeroline=True, zerolinecolor="#30363d")
    fig_circle.update_yaxes(range=[-1.3, 1.3], fixedrange=True, scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="#30363d")
    fig_circle.update_layout(template="plotly_dark", height=360, margin=dict(l=10, r=10, t=10, b=10))
    
    st.plotly_chart(fig_circle, use_container_width=True)
