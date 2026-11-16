import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(page_title="Dummy Math | Chapter 01: Trigonometry", layout="wide")

st.title("📐 Chapter 01: The Circle and the Shadows")
st.markdown(
    "Move the angle slider to watch how a rotating radius projects horizontal (**Cosine**) "
    "and vertical (**Sine**) shadows, unfolding into continuous waves over time."
)

# Panel de control lateral
st.sidebar.header("🎛️ Controls")
grados = st.sidebar.slider("Angle (Degrees)", min_value=0, max_value=360, value=45, step=1)
mostrar_tan = st.sidebar.checkbox("Show Tangent Wave (tan θ)", value=True)

radianes = np.deg2rad(grados)
cos_val = np.cos(radianes)
sin_val = np.sin(radianes)
tan_val = np.tan(radianes) if not np.isclose(cos_val, 0, atol=1e-2) else np.nan

# Métricas en vivo
col1, col2, col3, col4 = st.columns(4)
col1.metric("Angle (Radians)", f"{radianes:.2f} rad", f"{radianes/np.pi:.2f} π")
col2.metric("Cosine (X Shadow)", f"{cos_val:.3f}")
col3.metric("Sine (Y Shadow)", f"{sin_val:.3f}")
col4.metric("Tangent (sin / cos)", f"{tan_val:.3f}" if not np.isnan(tan_val) else "∞ (Undefined)")

# Crear figura doble: Círculo Unitario + Ondas
fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.4, 0.6],
    subplot_titles=("Unit Circle & Shadows", "Unfolded Waves Over Time")
)

# --- 1. CÍRCULO UNITARIO ---
theta_circ = np.linspace(0, 2 * np.pi, 200)
fig.add_trace(go.Scatter(x=np.cos(theta_circ), y=np.sin(theta_circ), mode="lines",
                         line=dict(color="#8b949e", width=2), name="Unit Circle", showlegend=False), row=1, col=1)

# Radio giratorio
fig.add_trace(go.Scatter(x=[0, cos_val], y=[0, sin_val], mode="lines+markers",
                         line=dict(color="#f0883e", width=3), marker=dict(size=8), name="Radius (1)"), row=1, col=1)

# Sombra Coseno (Horizontal - Azul)
fig.add_trace(go.Scatter(x=[0, cos_val], y=[0, 0], mode="lines",
                         line=dict(color="#58a6ff", width=4), name="Cosine (X)"), row=1, col=1)

# Sombra Seno (Vertical - Verde)
fig.add_trace(go.Scatter(x=[cos_val, cos_val], y=[0, sin_val], mode="lines",
                         line=dict(color="#3fb950", width=4, dash="dot"), name="Sine (Y)"), row=1, col=1)

# --- 2. ONDAS EN EL TIEMPO ---
x_deg = np.linspace(0, 360, 361)
x_rad = np.deg2rad(x_deg)

# Onda Coseno
fig.add_trace(go.Scatter(x=x_deg, y=np.cos(x_rad), mode="lines",
                         line=dict(color="#58a6ff", width=2.5), name="Cosine Wave"), row=1, col=2)
fig.add_trace(go.Scatter(x=[grados], y=[cos_val], mode="markers",
                         marker=dict(color="#58a6ff", size=10), showlegend=False), row=1, col=2)

# Onda Seno
fig.add_trace(go.Scatter(x=x_deg, y=np.sin(x_rad), mode="lines",
                         line=dict(color="#3fb950", width=2.5), name="Sine Wave"), row=1, col=2)
fig.add_trace(go.Scatter(x=[grados], y=[sin_val], mode="markers",
                         marker=dict(color="#3fb950", size=10), showlegend=False), row=1, col=2)

# Onda Tangente (con corte en asíntotas 90° y 270°)
if mostrar_tan:
    y_tan = np.tan(x_rad)
    y_tan[np.abs(y_tan) > 5] = np.nan  # Evita líneas verticales falsas al cruzar el infinito
    fig.add_trace(go.Scatter(x=x_deg, y=y_tan, mode="lines",
                             line=dict(color="#f85149", width=2, dash="dash"), name="Tangent Wave"), row=1, col=2)
    if not np.isnan(tan_val) and abs(tan_val) <= 5:
        fig.add_trace(go.Scatter(x=[grados], y=[tan_val], mode="markers",
                                 marker=dict(color="#f85149", size=10), showlegend=False), row=1, col=2)

# Línea vertical marcando el ángulo actual en las ondas
fig.add_vline(x=grados, line_width=1.5, line_dash="dash", line_color="#f0883e", row=1, col=2)

# Ajustes de ejes y diseño oscuro
fig.update_xaxes(range=[-1.3, 1.3], zeroline=True, zerolinecolor="#30363d", row=1, col=1)
fig.update_yaxes(range=[-1.3, 1.3], scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="#30363d", row=1, col=1)

fig.update_xaxes(title_text="Angle (Degrees)", range=[0, 360], tickvals=[0, 90, 180, 270, 360], row=1, col=2)
fig.update_yaxes(title_text="Value", range=[-2.5, 2.5], zeroline=True, zerolinecolor="#30363d", row=1, col=2)

fig.update_layout(template="plotly_dark", height=500, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig, use_container_width=True)
