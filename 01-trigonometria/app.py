import time
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(page_title="Dummy Math | Chapter 01: Trigonometry", layout="wide")

st.title("📐 Chapter 01: The Circle and the Shadows")
st.markdown(
    "Explore how a rotating radius inside a unit circle projects horizontal (**Cosine**) "
    "and vertical (**Sine**) shadows, unfolding into continuous waves over time."
)

# Cartel pedagógico sobre los límites [-1, 1]
st.info(
    "💡 **Fundamental Rule:** Because the unit circle has a fixed radius of **1**, "
    "neither **Sine** nor **Cosine** can ever be greater than **1** or less than **-1**. "
    "They are forever bounded inside the `[-1, 1]` corridor. Only **Tangent** can break free toward infinity."
)

# Sincronización entre el deslizador y la entrada numérica manual
if "angulo_deg" not in st.session_state:
    st.session_state.angulo_deg = 45

def actualizar_desde_slider():
    st.session_state.angulo_deg = st.session_state.slider_deg

def actualizar_desde_numero():
    st.session_state.angulo_deg = st.session_state.num_deg

# Panel de control lateral
st.sidebar.header("🎛️ Controls")

# 1. Entrada manual y deslizador sincronizados
st.sidebar.number_input(
    "Type Angle (0° to 360°)",
    min_value=0, max_value=360,
    value=st.session_state.angulo_deg,
    step=1, key="num_deg",
    on_change=actualizar_desde_numero
)

st.sidebar.slider(
    "Or Slide Angle (Degrees)",
    min_value=0, max_value=360,
    value=st.session_state.angulo_deg,
    step=1, key="slider_deg",
    on_change=actualizar_desde_slider
)

st.sidebar.divider()

# 2. Selector de intensidad / enfoque de onda
foco_onda = st.sidebar.radio(
    "🔍 Highlight Wave Intensity:",
    options=["All Equal", "Sine (Y - Green)", "Cosine (X - Blue)", "Tangent (Red)"],
    index=0
)

mostrar_tan = st.sidebar.checkbox("Include Tangent Wave (tan θ)", value=True)

st.sidebar.divider()

# 3. Control de animación continua
animar = st.sidebar.toggle("▶️ Auto-Rotate (Continuous Motion)", value=False)
velocidad = st.sidebar.select_slider("Rotation Speed", options=["Slow", "Normal", "Fast"], value="Normal")

grados = st.session_state.angulo_deg
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

# Configurar opacidades y grosores según el selector de intensidad
op_sin = 1.0 if foco_onda in ["All Equal", "Sine (Y - Green)"] else 0.2
lw_sin = 4.0 if foco_onda == "Sine (Y - Green)" else 2.5

op_cos = 1.0 if foco_onda in ["All Equal", "Cosine (X - Blue)"] else 0.2
lw_cos = 4.0 if foco_onda == "Cosine (X - Blue)" else 2.5

op_tan = 1.0 if foco_onda in ["All Equal", "Tangent (Red)"] else 0.2
lw_tan = 3.5 if foco_onda == "Tangent (Red)" else 2.0

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
                         line=dict(color="#58a6ff", width=lw_cos + 1.5), opacity=op_cos, name="Cosine (X)"), row=1, col=1)

# Sombra Seno (Vertical - Verde)
fig.add_trace(go.Scatter(x=[cos_val, cos_val], y=[0, sin_val], mode="lines",
                         line=dict(color="#3fb950", width=lw_sin + 1.5, dash="dot"), opacity=op_sin, name="Sine (Y)"), row=1, col=1)

# --- 2. ONDAS EN EL TIEMPO ---
x_deg = np.linspace(0, 360, 361)
x_rad = np.deg2rad(x_deg)

# Bandas límite [-1, 1] para demostrar visualmente que Seno y Coseno nunca pasan de 1
fig.add_hline(y=1, line_width=1, line_dash="dot", line_color="#8b949e", opacity=0.5, row=1, col=2)
fig.add_hline(y=-1, line_width=1, line_dash="dot", line_color="#8b949e", opacity=0.5, row=1, col=2)

# Onda Coseno
fig.add_trace(go.Scatter(x=x_deg, y=np.cos(x_rad), mode="lines",
                         line=dict(color="#58a6ff", width=lw_cos), opacity=op_cos, name="Cosine Wave"), row=1, col=2)
fig.add_trace(go.Scatter(x=[grados], y=[cos_val], mode="markers",
                         marker=dict(color="#58a6ff", size=10), opacity=op_cos, showlegend=False), row=1, col=2)

# Onda Seno
fig.add_trace(go.Scatter(x=x_deg, y=np.sin(x_rad), mode="lines",
                         line=dict(color="#3fb950", width=lw_sin), opacity=op_sin, name="Sine Wave"), row=1, col=2)
fig.add_trace(go.Scatter(x=[grados], y=[sin_val], mode="markers",
                         marker=dict(color="#3fb950", size=10), opacity=op_sin, showlegend=False), row=1, col=2)

# Onda Tangente
if mostrar_tan:
    y_tan = np.tan(x_rad)
    y_tan[np.abs(y_tan) > 5] = np.nan
    fig.add_trace(go.Scatter(x=x_deg, y=y_tan, mode="lines",
                             line=dict(color="#f85149", width=lw_tan, dash="dash"), opacity=op_tan, name="Tangent Wave"), row=1, col=2)
    if not np.isnan(tan_val) and abs(tan_val) <= 5:
        fig.add_trace(go.Scatter(x=[grados], y=[tan_val], mode="markers",
                                 marker=dict(color="#f85149", size=10), opacity=op_tan, showlegend=False), row=1, col=2)

# Línea vertical marcando el ángulo actual
fig.add_vline(x=grados, line_width=1.5, line_dash="dash", line_color="#f0883e", row=1, col=2)

# Ajustes de ejes y diseño oscuro
fig.update_xaxes(range=[-1.3, 1.3], zeroline=True, zerolinecolor="#30363d", row=1, col=1)
fig.update_yaxes(range=[-1.3, 1.3], scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="#30363d", row=1, col=1)

fig.update_xaxes(title_text="Angle (Degrees)", range=[0, 360], tickvals=[0, 90, 180, 270, 360], row=1, col=2)
fig.update_yaxes(title_text="Value", range=[-2.5, 2.5], zeroline=True, zerolinecolor="#30363d", row=1, col=2)

fig.update_layout(template="plotly_dark", height=520, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig, use_container_width=True)

# Motor de animación continua si el interruptor está activo
if animar:
    paso = {"Slow": 2, "Normal": 5, "Fast": 10}[velocidad]
    st.session_state.angulo_deg = (st.session_state.angulo_deg + paso) % 361
    time.sleep(0.05)
    st.rerun()
