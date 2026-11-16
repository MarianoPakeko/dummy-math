import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from textos import TEXTOS

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

c1, c2, c3, c4, c5, c6 = st.columns(6)
active_waves = {
    "sin": c1.toggle(f"🟢 {T['sin']}", value=True),
    "cos": c2.toggle(f"🔵 {T['cos']}", value=True),
    "tan": c3.toggle(f"🔴 {T['tan']}", value=False),
    "csc": c4.toggle(f"🟩 {T['csc']}", value=False),
    "sec": c5.toggle(f"🟦 {T['sec']}", value=False),
    "cot": c6.toggle(f"🟣 {T['cot']}", value=False),
}

# Cargar el archivo HTML limpio e inyectar variables
ruta_html = Path(__file__).parent / "animacion.html"
html_code = ruta_html.read_text(encoding="utf-8")
html_code = html_code.replace("__ACTIVE_JSON__", json.dumps(active_waves))
html_code = html_code.replace("__BTN_PAUSE__", T["pause"])
html_code = html_code.replace("__BTN_PLAY__", T["play"])

components.html(html_code, height=400)

