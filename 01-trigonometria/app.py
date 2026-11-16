import time
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(page_title="Dummy Math | Chapter 01: Trigonometry", layout="wide")

st.title("📐 Chapter 01: The Circle and the Shadows (All 6 Functions)")
st.markdown(
    "Explore how a rotating radius inside a unit circle generates the **3 primary functions** "
    "(Sine, Cosine, Tangent) and their **3 reciprocal twins** (Cosecant, Secant, Cotangent)."
)

# Cartel pedagógico
st.info(
    "💡 **The Boundary Rule:** **Sine** and **Cosine** are trapped inside the `[-1, 1]` corridor. "
    "Their reciprocals (**Cosecant** = `1/sin` and **Secant** = `1/cos`) live completely **outside** that corridor, "
    "bouncing away toward infinity."
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

# Interruptores de visibilidad
mostrar_tan = st.sidebar.checkbox("Show Tangent (tan θ)", value=True)
mostrar_reciprocas = st.sidebar.checkbox("Show Reciprocals (sec, csc, cot)", value=True)

# Selector de intensidad / enfoque de onda
opciones_foco = [
    "All Equal",
    "Sine (sin)",
    "Cosine (cos)",
    "Tangent (tan)",
    "Cosecant (csc = 1/sin)",
    "Secant (sec = 1/cos)",
    "Cotangent (cot = 1/tan)"
]
foco_onda = st.sidebar.radio("🔍 Highlight Wave Intensity:", options=opciones_foco, index=0)

st.sidebar.divider()

# Control de animación continua
animar = st.sidebar.toggle("▶️ Auto-Rotate (Continuous Motion)", value=False)
velocidad = st.sidebar.select_slider("Rotation Speed", options=["Slow", "Normal", "Fast"], value="Normal")

# Cálculos exactos para el ángulo actual
grados = st.session_state.angulo_deg
radianes = np.deg2rad(grados)

cos_val = np.cos(radianes)
sin_val = np.sin(radianes)
tan_val = np.tan(radianes) if not np.isclose(cos_val, 0, atol=1e-2) else np.nan
csc_val = 1.0 / sin_val if not np.isclose(sin_val, 0, atol=1e-2) else np.nan
sec_val = 1.0 / cos_val if not np.isclose(cos_val, 0, atol=1e-2) else np.nan
cot_val = cos_val / sin_val if not np.isclose(sin_val, 0, atol=1e-2) else np.nan

# Fila 1 de Métricas: Principales
col1, col2, col3, col4 = st.columns(4)
col1.metric("Angle (Radians)", f"{radianes:.2f} rad", f"{radianes/np.pi:.2f} π")
col2.metric("Cosine (cos θ)", f"{cos_val:.3f}")
col3.metric("Sine (sin θ)", f"{sin_val:.3f}")
col4.metric("Tangent (tan θ)", f"{tan_val:.3f}" if not np.isnan(tan_val) else "∞")

# Fila 2 de Métricas: Recíprocas
rcol1, rcol2, rcol3, rcol4 = st.columns(4)
rcol1.metric("Degrees", f"{grados}°")
rcol2.metric("Secant (1 / cos)", f"{sec_val:.3f}" if not np.isnan(sec_val) else "∞")
rcol3.metric("Cosecant (1 / sin)", f"{csc_val:.3f}" if not np.isnan(csc_val) else "∞")
rcol4.metric("Cotangent (cos / sin)", f"{cot_val:.3f}" if not np.isnan(cot_val) else "∞")

# Función auxiliar para definir estilo según el foco seleccionado
def estilo_onda(nombre_clave, grosor_base=2.5):
    if foco_onda == "All Equal":
        return 1.0, grosor_base
    elif foco_onda == nombre_clave:
        return 1.0, grosor_base + 2.0
    else:
        return 0.15, grosor_base

op_sin, lw_sin = estilo_onda("Sine (sin)")
op_cos, lw_cos = estilo_onda("Cosine (cos)")
op_tan, lw_tan = estilo_onda("Tangent (tan)", 2.0)
op_csc, lw_csc = estilo_onda("Cosecant (csc = 1/sin)", 2.0)
op_sec, lw_sec = estilo_onda("Secant (sec = 1/cos)", 2.0)
op_cot, lw_cot = estilo_onda("Cotangent (cot = 1/tan)", 2.0)

# Crear figura doble: Círculo Unitario + Ondas
fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.38, 0.62],
    subplot_titles=("Unit Circle & Projections", "All Trigonometric Waves Over Time")
)

# --- 1. CÍRCULO UNITARIO ---
theta_circ = np.linspace(0, 2 * np.pi, 200)
fig.add_trace(go.Scatter(x=np.cos(theta_circ), y=np.sin(theta_circ), mode="lines",
                         line=dict(color="#8b949e", width=2), showlegend=False), row=1, col=1)

# Radio giratorio
fig.add_trace(go.Scatter(x=[0, cos_val], y=[0, sin_val], mode="lines+markers",
                         line=dict(color="#f0883e", width=3), marker=dict(size=8), name="Radius (1)"), row=1, col=1)

# Sombra Coseno (Azul)
fig.add_trace(go.Scatter(x=[0, cos_val], y=[0, 0], mode="lines",
                         line=dict(color="#58a6ff", width=lw_cos + 1.5), opacity=op_cos, name="Cosine (X)"), row=1, col=1)

# Sombra Seno (Verde)
fig.add_trace(go.Scatter(x=[cos_val, cos_val], y=[0, sin_val], mode="lines",
                         line=dict(color="#3fb950", width=lw_sin + 1.5, dash="dot"), opacity=op_sin, name="Sine (Y)"), row=1, col=1)

# --- 2. ONDAS EN EL TIEMPO ---
x_deg = np.linspace(0, 360, 721)
x_rad = np.deg2rad(x_deg)

# Bandas límite [-1, 1]
fig.add_hline(y=1, line_width=1, line_dash="dot", line_color="#8b949e", opacity=0.4, row=1, col=2)
fig.add_hline(y=-1, line_width=1, line_dash="dot", line_color="#8b949e", opacity=0.4, row=1, col=2)

# Coseno (Azul)
fig.add_trace(go.Scatter(x=x_deg, y=np.cos(x_rad), mode="lines",
                         line=dict(color="#58a6ff", width=lw_cos), opacity=op_cos, name="Cosine (cos)"), row=1, col=2)
fig.add_trace(go.Scatter(x=[grados], y=[cos_val], mode="markers",
                         marker=dict(color="#58a6ff", size=9), opacity=op_cos, showlegend=False), row=1, col=2)

# Seno (Verde)
fig.add_trace(go.Scatter(x=x_deg, y=np.sin(x_rad), mode="lines",
                         line=dict(color="#3fb950", width=lw_sin), opacity=op_sin, name="Sine (sin)"), row=1, col=2)
fig.add_trace(go.Scatter(x=[grados], y=[sin_val], mode="markers",
                         marker=dict(color="#3fb950", size=9), opacity=op_sin, showlegend=False), row=1, col=2)

# Función para recortar asíntotas infinitas
def limpiar_asintotas(arr, limite=5.0):
    copia = arr.copy()
    copia[np.abs(copia) > limite] = np.nan
    return copia

# Tangente (Rojo)
if mostrar_tan:
    y_tan = limpiar_asintotas(np.tan(x_rad))
    fig.add_trace(go.Scatter(x=x_deg, y=y_tan, mode="lines",
                             line=dict(color="#f85149", width=lw_tan, dash="dash"), opacity=op_tan, name="Tangent (tan)"), row=1, col=2)
    if not np.isnan(tan_val) and abs(tan_val) <= 5:
        fig.add_trace(go.Scatter(x=[grados], y=[tan_val], mode="markers",
                                 marker=dict(color="#f85149", size=9), opacity=op_tan, showlegend=False), row=1, col=2)

# Las 3 Recíprocas
if mostrar_reciprocas:
    # Secante (Cian claro)
    y_sec = limpiar_asintotas(1.0 / np.where(np.isclose(np.cos(x_rad), 0, atol=1e-3), np.nan, np.cos(x_rad)))
    fig.add_trace(go.Scatter(x=x_deg, y=y_sec, mode="lines",
                             line=dict(color="#79c0ff", width=lw_sec, dash="dot"), opacity=op_sec, name="Secant (1/cos)"), row=1, col=2)
    if not np.isnan(sec_val) and abs(sec_val) <= 5:
        fig.add_trace(go.Scatter(x=[grados], y=[sec_val], mode="markers",
                                 marker=dict(color="#79c0ff", size=9), opacity=op_sec, showlegend=False), row=1, col=2)

    # Cosecante (Verde menta)
    y_csc = limpiar_asintotas(1.0 / np.where(np.isclose(np.sin(x_rad), 0, atol=1e-3), np.nan, np.sin(x_rad)))
    fig.add_trace(go.Scatter(x=x_deg, y=y_csc, mode="lines",
                             line=dict(color="#56d364", width=lw_csc, dash="dot"), opacity=op_csc, name="Cosecant (1/sin)"), row=1, col=2)
    if not np.isnan(csc_val) and abs(csc_val) <= 5:
        fig.add_trace(go.Scatter(x=[grados], y=[csc_val], mode="markers",
                                 marker=dict(color="#56d364", size=9), opacity=op_csc, showlegend=False), row=1, col=2)

    # Cotangente (Morado)
    y_cot = limpiar_asintotas(np.cos(x_rad) / np.where(np.isclose(np.sin(x_rad), 0, atol=1e-3), np.nan, np.sin(x_rad)))
    fig.add_trace(go.Scatter(x=x_deg, y=y_cot, mode="lines",
                             line=dict(color="#d2a8ff", width=lw_cot, dash="dashdot"), opacity=op_cot, name="Cotangent (cos/sin)"), row=1, col=2)
    if not np.isnan(cot_val) and abs(cot_val) <= 5:
        fig.add_trace(go.Scatter(x=[grados], y=[cot_val], mode="markers",
                                 marker=dict(color="#d2a8ff", size=9), opacity=op_cot, showlegend=False), row=1, col=2)

# Línea vertical marcando el ángulo actual
fig.add_vline(x=grados, line_width=1.5, line_dash="dash", line_color="#f0883e", row=1, col=2)

# Ajustes de ejes y diseño oscuro
fig.update_xaxes(range=[-1.3, 1.3], zeroline=True, zerolinecolor="#30363d", row=1, col=1)
fig.update_yaxes(range=[-1.3, 1.3], scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="#30363d", row=1, col=1)

fig.update_xaxes(title_text="Angle (Degrees)", range=[0, 360], tickvals=[0, 45, 90, 135, 180, 225, 270, 315, 360], row=1, col=2)
fig.update_yaxes(title_text="Value", range=[-3.5, 3.5], zeroline=True, zerolinecolor="#30363d", row=1, col=2)

fig.update_layout(template="plotly_dark", height=540, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig, use_container_width=True)

# Motor de animación continua
if animar:
    paso = {"Slow": 2, "Normal": 5, "Fast": 10}[velocidad]
    st.session_state.angulo_deg = (st.session_state.angulo_deg + paso) % 361
    time.sleep(0.05)
    st.rerun()
