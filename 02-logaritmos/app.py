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
# SECCIÓN 1: ANIMACIÓN ESPEJO (EXPONENCIAL VS LOGARITMO)
# ==========================================
st.subheader(T["sec1"])
ruta_html = Path(__file__).parent / "animacion.html"
html_code = ruta_html.read_text(encoding="utf-8")
html_code = html_code.replace("__BTN_PAUSE__", T["pause"]).replace("__BTN_PLAY__", T["play"])
components.html(html_code, height=340)

st.divider()

# ==========================================
# SECCIÓN 2: EL COMPRESOR DE GIGANTES (ESCALA LINEAL VS LOG)
# ==========================================
st.subheader(T["sec2"])
st.caption(T["desc2"])

usar_log = st.toggle(T["toggle_log"], value=False)

categorias = ["User A", "User B", "User C", "User D", "User E", "Viral Giant"]
valores = [15, 45, 120, 350, 900, 10000000]

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=categorias,
    y=valores,
    text=[f"{v:,}" for v in valores],
    textposition="outside",
    marker_color=["#58a6ff", "#58a6ff", "#58a6ff", "#58a6ff", "#58a6ff", "#f85149"]
))

fig_bar.update_layout(
    template="plotly_dark",
    height=380,
    yaxis_type="log" if usar_log else "linear",
    yaxis_title="Logarithmic Scale (Powers of 10)" if usar_log else "Linear Scale (Raw Numbers)",
    margin=dict(l=20, r=20, t=30, b=20)
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ==========================================
# SECCIÓN 3: CALCULADORA DE PASOS (CUALQUIER NÚMERO)
# ==========================================
st.subheader(T["sec3"])

col_c1, col_c2 = st.columns([1.1, 1.3])

with col_c1:
    numero = st.number_input(T["input_num"], min_value=0.0001, value=1000.0, step=100.0, format="%.2f")
    base_opcion = st.radio(T["select_base"], ["Base 10 (Standard)", "Base 2 (Binary / Bits)", "Base e (Natural ~2.718)"], horizontal=True)

with col_c2:
    if "10" in base_opcion:
        pasos = np.log10(numero)
        base_str = "10"
    elif "2" in base_opcion:
        pasos = np.log2(numero)
        base_str = "2"
    else:
        pasos = np.log(numero)
        base_str = "e"

    st.metric(T["res_steps"], f"{pasos:.4f}")
    st.info(f"🔄 **{T['res_exp']}** ${base_str}^{{{pasos:.4f}}} = {numero:,.2f}$")
