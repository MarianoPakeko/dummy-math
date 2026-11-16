from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from textoslog import TEXTOS

st.set_page_config(page_title="Dummy Math | Logarithms", layout="wide")

col_t, col_lang = st.columns([0.85, 0.15])
with col_lang:
    idioma = st.selectbox("🌐", ["Español", "English", "Italiano"], label_visibility="collapsed")

T = TEXTOS[idioma]
with col_t:
    st.title(T["title"])

with st.expander(T["exp_title"], expanded=False):
    st.markdown(T["defs"])

# ==========================================
# SECCIÓN 1: ESCALERA DE PASOS + GRÁFICA
# ==========================================
st.subheader(T["sec1"])
ruta_html = Path(__file__).parent / "animacionlog.html"
html_code = ruta_html.read_text(encoding="utf-8")
html_code = html_code.replace("__BTN_PAUSE__", T["pause"]).replace("__BTN_PLAY__", T["play"])
components.html(html_code, height=360)

st.divider()

# ==========================================
# SECCIÓN 2: RESCATADOR DE DATOS REALES
# ==========================================
st.subheader(T["sec2"])

col_s1, col_s2 = st.columns([1, 1])
with col_s1:
    escenario_idx = st.radio(T["escenario_label"], range(len(T["escenarios"])), format_func=lambda i: T["escenarios"][i])
with col_s2:
    vista_idx = st.radio(T["vista_label"], range(len(T["vistas"])), format_func=lambda i: T["vistas"][i])

usar_log = (vista_idx == 1)

# Conjuntos de datos reales significativos
DATASETS = {
    0: {  # Riqueza Global
        "labels": ["Student Savings", "Used Car", "Family Home", "Millionaire", "Tech Billionaire"],
        "values":,
        "colors": ["#58a6ff", "#58a6ff", "#58a6ff", "#d29922", "#f85149"]
    },
    1: {  # Energía de Terremotos (Joules aproximados)
        "labels": ["Mag 2 (Unfelt)", "Mag 4 (Light)", "Mag 6 (Strong)", "Mag 8 (Great)", "Mag 9.5 (Valdivia)"],
        "values":,
        "colors": ["#3fb950", "#58a6ff", "#d29922", "#f0883e", "#f85149"]
    },
    2: {  # Tamaños en el Universo (Metros)
        "labels": ["Human", "Skyscraper", "Mount Everest", "Planet Earth", "The Sun"],
        "values": [1.7, 300, 8848, 12742000, 1392700000],
        "colors": ["#3fb950", "#58a6ff", "#58a6ff", "#d29922", "#f85149"]
    }
}

data_actual = DATASETS[escenario_idx]

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=data_actual["labels"],
    y=data_actual["values"],
    text=[f"{v:,.1f}" if v < 10 else f"{int(v):,}" for v in data_actual["values"]],
    textposition="outside",
    marker_color=data_actual["colors"]
))

fig_bar.update_layout(
    template="plotly_dark",
    height=380,
    yaxis_type="log" if usar_log else "linear",
    yaxis_title="Logarithmic Scale (Powers of 10)" if usar_log else "Raw Linear Scale",
    margin=dict(l=20, r=20, t=35, b=20)
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ==========================================
# SECCIÓN 3: CALCULADORA DE PASOS MULTI-BASE
# ==========================================
st.subheader(T["sec3"])

col_c1, col_c2 = st.columns([1.2, 1])

with col_c1:
    numero = st.number_input(T["input_num"], min_value=0.0001, value=256.0, step=10.0, format="%.2f")
    bases = [
        "Base 10 (Decimal / Zeros)",
        "Base 2 (Binary / Computer Bits)",
        "Base 16 (Hexadecimal / Memory & Colors)",
        "Base e ≈ 2.718 (Natural / Continuous Growth)",
        "Base φ ≈ 1.618 (Golden Ratio / Fibonacci)"
    ]
    base_sel = st.radio(T["select_base"], bases)

with col_c2:
    phi = (1 + np.sqrt(5)) / 2
    if "Base 10" in base_sel:
        pasos = np.log10(numero)
        b_sym, nota = "10", "Counts how many ×10 jumps (zeros) fit inside the number."
    elif "Base 2" in base_sel:
        pasos = np.log2(numero)
        b_sym, nota = "2", f"A computer needs **{int(np.ceil(pasos))} bits** of memory to store this integer."
    elif "Base 16" in base_sel:
        pasos = np.log(numero) / np.log(16)
        b_sym, nota = "16", f"Takes **{int(np.ceil(pasos))} hexadecimal digits** (0-9, A-F) to write this value."
    elif "Base e" in base_sel:
        pasos = np.log(numero)
        b_sym, nota = "e", "Time required to reach this size under 100% continuous compound growth."
    else:
        pasos = np.log(numero) / np.log(phi)
        b_sym, nota = "φ", "Number of Golden Ratio / Fibonacci spiral growth steps inside this value."

    st.metric(T["res_steps"], f"{pasos:.4f}")
    st.info(f"🔄 **{T['res_exp']}** ${b_sym}^{{{pasos:.4f}}} = {numero:,.2f}$\n\n💡 {nota}")
