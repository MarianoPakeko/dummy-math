import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Dummy Math | Chapter 01: Trigonometry", layout="wide")

st.title("📐 Chapter 01: The Circle and the Shadows")
st.info(
    "💡 **Fundamental Rule:** Because the unit circle has a fixed radius of **1**, "
    "**Sine** and **Cosine** can never exceed **1** or drop below **-1**. "
    "Their reciprocals (**Secant** and **Cosecant**) live completely outside the `[-1, 1]` corridor."
)

# Separamos en 2 pestañas claras: Animación Fluida vs Calculadora Manual
tab1, tab2 = st.tabs(["▶️ 1. Smooth Wave Animation", "🧮 2. Manual Angle Inspector"])

# ==========================================
# PESTAÑA 1: ANIMACIÓN FLUIDA NATIVA (60 FPS)
# ==========================================
with tab1:
    col_ctrl1, col_ctrl2 = st.columns([1, 2])
    with col_ctrl1:
        foco = st.selectbox(
            "🔍 Highlight Function:",
            ["All Equal", "Sine (sin)", "Cosine (cos)", "Tangent (tan)", "Cosecant (1/sin)", "Secant (1/cos)", "Cotangent (1/tan)"]
        )
    with col_ctrl2:
        mostrar_rec = st.checkbox("Include Reciprocals (Secant, Cosecant, Cotangent)", value=False)

    # Configurar opacidades y grosores según selección
    def get_style(name, base_w=2.5):
        if foco == "All Equal":
            return 1.0, base_w
        return (1.0, base_w + 2.0) if foco == name else (0.15, base_w)

    op_sin, lw_sin = get_style("Sine (sin)")
    op_cos, lw_cos = get_style("Cosine (cos)")
    op_tan, lw_tan = get_style("Tangent (tan)", 2.0)
    op_csc, lw_csc = get_style("Cosecant (1/sin)", 2.0)
    op_sec, lw_sec = get_style("Secant (1/cos)", 2.0)
    op_cot, lw_cot = get_style("Cotangent (1/tan)", 2.0)

    # Pre-calcular las ondas completas (0° a 360°)
    x_deg = np.linspace(0, 360, 361)
    x_rad = np.deg2rad(x_deg)
    y_sin = np.sin(x_rad)
    y_cos = np.cos(x_rad)

    def clean_inf(arr, limit=4.0):
        c = arr.copy()
        c[np.abs(c) > limit] = np.nan
        return c

    y_tan = clean_inf(np.tan(x_rad))
    y_csc = clean_inf(1.0 / np.where(np.isclose(y_sin, 0, atol=1e-2), np.nan, y_sin))
    y_sec = clean_inf(1.0 / np.where(np.isclose(y_cos, 0, atol=1e-2), np.nan, y_cos))
    y_cot = clean_inf(y_cos / np.where(np.isclose(y_sin, 0, atol=1e-2), np.nan, y_sin))

    fig_anim = make_subplots(
        rows=1, cols=2,
        column_widths=[0.38, 0.62],
        subplot_titles=("Fixed Unit Circle (Radius = 1)", "Waves Rising & Falling Over Time")
    )

    # Trazos estáticos de fondo (Círculo y ondas completas tenues)
    theta_c = np.linspace(0, 2 * np.pi, 180)
    fig_anim.add_trace(go.Scatter(x=np.cos(theta_c), y=np.sin(theta_c), mode="lines",
                                  line=dict(color="#8b949e", width=2), showlegend=False), row=1, col=1)

    # Ondas base
    fig_anim.add_trace(go.Scatter(x=x_deg, y=y_cos, mode="lines", line=dict(color="#58a6ff", width=lw_cos), opacity=op_cos, name="Cosine"), row=1, col=2)
    fig_anim.add_trace(go.Scatter(x=x_deg, y=y_sin, mode="lines", line=dict(color="#3fb950", width=lw_sin), opacity=op_sin, name="Sine"), row=1, col=2)
    fig_anim.add_trace(go.Scatter(x=x_deg, y=y_tan, mode="lines", line=dict(color="#f85149", width=lw_tan, dash="dash"), opacity=op_tan, name="Tangent"), row=1, col=2)

    if mostrar_rec:
        fig_anim.add_trace(go.Scatter(x=x_deg, y=y_csc, mode="lines", line=dict(color="#56d364", width=lw_csc, dash="dot"), opacity=op_csc, name="Cosecant"), row=1, col=2)
        fig_anim.add_trace(go.Scatter(x=x_deg, y=y_sec, mode="lines", line=dict(color="#79c0ff", width=lw_sec, dash="dot"), opacity=op_sec, name="Secant"), row=1, col=2)
        fig_anim.add_trace(go.Scatter(x=x_deg, y=y_cot, mode="lines", line=dict(color="#d2a8ff", width=lw_cot, dash="dashdot"), opacity=op_cot, name="Cotangent"), row=1, col=2)

    # Trazos dinámicos iniciales (se actualizarán en cada frame sin mover los ejes)
    # Índices de trazos dinámicos: los últimos 5 trazos
    idx_dinamicos = list(range(len(fig_anim.data), len(fig_anim.data) + 5))

    fig_anim.add_trace(go.Scatter(x=[0, 1], y=[0, 0], mode="lines+markers", line=dict(color="#f0883e", width=3), marker=dict(size=8), name="Radius"), row=1, col=1)
    fig_anim.add_trace(go.Scatter(x=[0, 1], y=[0, 0], mode="lines", line=dict(color="#58a6ff", width=4), showlegend=False), row=1, col=1)
    fig_anim.add_trace(go.Scatter(x=[1, 1], y=[0, 0], mode="lines", line=dict(color="#3fb950", width=4, dash="dot"), showlegend=False), row=1, col=1)
    fig_anim.add_trace(go.Scatter(x=[0], y=[1], mode="markers", marker=dict(color="#58a6ff", size=11), showlegend=False), row=1, col=2)
    fig_anim.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(color="#3fb950", size=11), showlegend=False), row=1, col=2)

    # Generar Frames cada 5 grados (73 frames súper fluidos en el navegador)
    frames = []
    for deg in range(0, 365, 5):
        rad = np.deg2rad(deg)
        c, s = np.cos(rad), np.sin(rad)
        frames.append(go.Frame(
            data=[
                go.Scatter(x=[0, c], y=[0, s]),
                go.Scatter(x=[0, c], y=[0, 0]),
                go.Scatter(x=[c, c], y=[0, s]),
                go.Scatter(x=[deg], y=[c]),
                go.Scatter(x=[deg], y=[s])
            ],
            traces=idx_dinamicos,
            name=str(deg)
        ))
    fig_anim.frames = frames

    # Límites fijos estrictos para que el círculo NUNCA cambie de tamaño
    fig_anim.update_xaxes(range=[-1.25, 1.25], fixedrange=True, zeroline=True, zerolinecolor="#30363d", row=1, col=1)
    fig_anim.update_yaxes(range=[-1.25, 1.25], fixedrange=True, scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="#30363d", row=1, col=1)

    fig_anim.update_xaxes(title_text="Angle (Degrees)", range=[0, 360], tickvals=[0, 90, 180, 270, 360], fixedrange=True, row=1, col=2)
    fig_anim.update_yaxes(title_text="Value", range=[-2.5, 2.5], fixedrange=True, zeroline=True, zerolinecolor="#30363d", row=1, col=2)

    fig_anim.add_hline(y=1, line_width=1, line_dash="dot", line_color="#8b949e", opacity=0.4, row=1, col=2)
    fig_anim.add_hline(y=-1, line_width=1, line_dash="dot", line_color="#8b949e", opacity=0.4, row=1, col=2)

    # Botones nativos Play / Pause en el navegador
    fig_anim.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            x=0.05, y=1.15,
            buttons=[
                dict(label="▶️ Play", method="animate", args=[None, dict(frame=dict(duration=40, redraw=False), fromcurrent=True, mode="immediate")]),
                dict(label="⏸️ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])
            ]
        )]
    )
    st.plotly_chart(fig_anim, use_container_width=True)

# ==========================================
# PESTAÑA 2: CALCULADORA MANUAL LIBRE
# ==========================================
with tab2:
    st.markdown("Type **any angle** (positive, negative, or larger than 360°) to inspect its exact position on the unit circle.")
    
    # Caja numérica libre sin topes
    angulo_libre = st.number_input("Enter any angle in degrees:", value=45.0, step=15.0)
    
    rad_libre = np.deg2rad(angulo_libre)
    c_val = np.cos(rad_libre)
    s_val = np.sin(rad_libre)
    t_val = np.tan(rad_libre) if not np.isclose(c_val, 0, atol=1e-4) else np.nan
    csc_v = 1.0 / s_val if not np.isclose(s_val, 0, atol=1e-4) else np.nan
    sec_v = 1.0 / c_val if not np.isclose(c_val, 0, atol=1e-4) else np.nan
    cot_v = c_val / s_val if not np.isclose(s_val, 0, atol=1e-4) else np.nan

    # Mostrar las 6 métricas exactas
    m1, m2, m3 = st.columns(3)
    m1.metric("Cosine (cos)", f"{c_val:.4f}")
    m2.metric("Sine (sin)", f"{s_val:.4f}")
    m3.metric("Tangent (tan)", f"{t_val:.4f}" if not np.isnan(t_val) else "∞ (Undefined)")

    m4, m5, m6 = st.columns(3)
    m4.metric("Secant (1 / cos)", f"{sec_v:.4f}" if not np.isnan(sec_v) else "∞ (Undefined)")
    m5.metric("Cosecant (1 / sin)", f"{csc_v:.4f}" if not np.isnan(csc_v) else "∞ (Undefined)")
    m6.metric("Cotangent (cos / sin)", f"{cot_v:.4f}" if not np.isnan(cot_v) else "∞ (Undefined)")

    # Círculo estático de tamaño fijo mostrando el ángulo ingresado
    fig_static = go.Figure()
    fig_static.add_trace(go.Scatter(x=np.cos(theta_c), y=np.sin(theta_c), mode="lines", line=dict(color="#8b949e", width=2), name="Unit Circle"))
    fig_static.add_trace(go.Scatter(x=[0, c_val], y=[0, s_val], mode="lines+markers", line=dict(color="#f0883e", width=3), marker=dict(size=10), name=f"Angle {angulo_libre}°"))
    fig_static.add_trace(go.Scatter(x=[0, c_val], y=[0, 0], mode="lines", line=dict(color="#58a6ff", width=4), name="Cosine (X)"))
    fig_static.add_trace(go.Scatter(x=[c_val, c_val], y=[0, s_val], mode="lines", line=dict(color="#3fb950", width=4, dash="dot"), name="Sine (Y)"))

    fig_static.update_xaxes(range=[-1.3, 1.3], zeroline=True, zerolinecolor="#30363d")
    fig_static.update_yaxes(range=[-1.3, 1.3], scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="#30363d")
    fig_static.update_layout(template="plotly_dark", height=420, width=420, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_static)
