import streamlit as st
import pandas as pd
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui
from utils.volatility import calc_volatility_agg
from utils.volatility import render_company_card

st.set_page_config(page_title="Biến động", layout="wide")
render_navbar()
clean_streamlit_ui()


def load_css(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Không tìm thấy CSS: {path}")
load_css("assets/styles/biendonggia.css")
load_css("assets/styles/base.css")



st.markdown('<div class="pill-title">Biến động giá vàng</div>', unsafe_allow_html=True)

cols = st.columns(2)

render_company_card(
    col=cols[0],
    name="PNJ",
    csv_path="data/pnj/gold_pnj_history.csv",
    select_label="Chi nhánh PNJ",
    select_key="pnj_branch",
    title_class="pnj",
)

render_company_card(
    col=cols[1],
    name="SJC",
    csv_path="data/sjc/gold_sjc_history.csv",
    select_label="Chi nhánh SJC",
    select_key="sjc_branch",
    title_class="sjc",
)
