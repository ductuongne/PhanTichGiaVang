import streamlit as st
import pandas as pd
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui
from utils.volatility_upgrade import render_company_row

st.set_page_config(page_title="Phân tích Biến động", layout="wide")

render_navbar()
clean_streamlit_ui()

def load_css(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Thiếu file CSS: {path}")

load_css("assets/styles/base.css")    
load_css("assets/styles/biendonggia.css") 

st.markdown('<div class="pill-title">Biến động giá & Cảnh báo rủi ro</div>', unsafe_allow_html=True)

render_company_row(
    name="PNJ",
    csv_path="data/pnj/gold_pnj_history.csv",
    title_class="pnj"
)

render_company_row(
    name="SJC",
    csv_path="data/sjc/gold_sjc_history.csv",
    title_class="sjc"
)