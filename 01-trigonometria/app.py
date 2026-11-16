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
