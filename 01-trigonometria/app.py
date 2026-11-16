import json
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from textostri import TEXTOS

st.set_page_config(page_title="Dummy Math | Trigonometry", layout="wide")

col_t, col_lang = st.columns([0.85, 0.15])
with col_lang:
    idioma = st.selectbox("🌐", ["Español", "English", "Italiano"], label_visibility="collapsed")

T = TEXTOS[idioma]
with col_t:
    st.title(T["title"])

with st.expander(T["exp_title"], expanded=False):
    st.markdown(T["defs"])

st.caption(T["cap"])

# ==========================================
# PARTE 1: ANIMACIÓN PERPETUA (NO SE TOCA)
# ==========================================
c1, c2, c3, c4, c5, c6 = st.columns(6)
active_waves = {
    "sin": c1.toggle(f"🟢 {T['sin']}", value=True),
    "cos": c2.toggle(f"🔵 {T['cos']}", value=True),
    "tan": c3.toggle(f"🔴 {T['tan']}", value=False),
    "csc": c4.toggle(f"🟩 {T['csc']}", value=False),
    "sec": c5.toggle(f"🟦 {T['sec']}", value=False),
    "cot": c6.toggle(f"🟣 {T['cot']}", value=False),
}

ruta_html = Path(__file__).parent / "animacion.html"
html_code = ruta_html.read_text(encoding="utf-8")
html_code = html_code.replace("__ACTIVE_JSON__", json.dumps(active_waves))
html_code = html_code.replace("__BTN_PAUSE__", T["pause"])
html_code = html_code.replace("__BTN_PLAY__", T["play"])

components.html(html_code, height=400)

st.divider()

# ==========================================
# PARTE 2: CALCULADORA MANUAL DEL CÍRCULO
# ==========================================
st.subheader(T["calc_title"])

col_left, col_right = st.columns([1.1, 1.3])

with col_left:
    angulo = st.number_input(T["calc_input"], value=45.0, step=15.0)
    rad = np.deg2rad(angulo)

    c_val = np.cos(rad)
    s_val = np.sin(rad)
    t_val = np.tan(rad) if not np.isclose(c_val, 0, atol=1e-4) else np.nan
    csc_v = 1.0 / s_val if not np.isclose(s_val, 0, atol=1e-4) else np.nan
    sec_v = 1.0 / c_val if not np.isclose(c_val, 0, atol=1e-4) else np.nan
    cot_v = c_val / s_val if not np.isclose(s_val, 0, atol=1e-4) else np.nan

    st.caption(f"{T['calc_rad']} **{rad:.4f} rad** ({rad/np.pi:.2f} π)")

    m1, m2, m3 = st.columns(3)
    m1.metric(T["cos"], f"{c_val:.4f}")
    m2.metric(T["sin"], f"{s_val:.4f}")
    m3.metric(T["tan"], f"{t_val:.4f}" if not np.isnan(t_val) else T["inf"])

    m4, m5, m6 = st.columns(3)
    m4.metric(T["sec"], f"{sec_v:.4f}" if not np.isnan(sec_v) else T["inf"])
    m5.metric(T["csc"], f"{csc_v:.4f}" if not np.isnan(csc_v) else T["inf"])
    m6.metric(T["cot"], f"{cot_v:.4f}" if not np.isnan(cot_v) else T["inf"])

with col_right:
    theta_c = np.linspace(0, 2 * np.pi, 200)
    fig = go.Figure()

    # Círculo base
    fig.add_trace(go.Scatter(x=np.cos(theta_c), y=np.sin(theta_c), mode="lines",
                             line=dict(color="#8b949e", width=2), name="Unit Circle"))
    # Radio
    fig.add_trace(go.Scatter(x=[0, c_val], y=[0, s_val], mode="lines+markers",
                             line=dict(color="#f0883e", width=3), marker=dict(size=10), name=f"{angulo}°"))
    # Sombra Coseno (Horizontal Azul)
    fig.add_trace(go.Scatter(x=[0, c_val], y=[0, 0], mode="lines",
                             line=dict(color="#58a6ff", width=4), name=T["cos"]))
    # Sombra Seno (Vertical Verde)
    fig.add_trace(go.Scatter(x=[c_val, c_val], y=[0, s_val], mode="lines",
                             line=dict(color="#3fb950", width=4, dash="dot"), name=T["sin"]))

    fig.update_xaxes(range=[-1.3, 1.3], fixedrange=True, zeroline=True, zerolinecolor="#30363d")
    fig.update_yaxes(range=[-1.3, 1.3], fixedrange=True, scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="#30363d")
    fig.update_layout(template="plotly_dark", height=360, margin=dict(l=10, r=10, t=10, b=10))

    st.plotly_chart(fig, use_container_width=True)
