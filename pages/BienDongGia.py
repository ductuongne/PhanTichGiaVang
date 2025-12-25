import streamlit as st
import pandas as pd
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui
from utils.volatility import calc_volatility_agg

st.set_page_config(page_title="Biến động", layout="wide")
render_navbar()
clean_streamlit_ui()


def load_css(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Không tìm thấy CSS: {path}")

load_css("assets/styles/base.css")
load_css("assets/styles/biendonggia.css")


st.markdown('<div class="pill-title">Biến động giá vàng</div>', unsafe_allow_html=True)

cols = st.columns(2)


# ===== PNJ =====
with cols[0]:
    st.markdown('<div class="brand-title pnj">PNJ</div>', unsafe_allow_html=True)

    df_pnj_all = pd.read_csv("data/pnj/gold_pnj_history.csv")
    df_pnj_all["date"] = pd.to_datetime(df_pnj_all["date"])

    branches_pnj = sorted(df_pnj_all["BranchName"].unique())

    branch_pnj = st.selectbox("Chi nhánh PNJ", branches_pnj, key="pnj_branch")

    df_pnj = df_pnj_all[df_pnj_all["BranchName"] == branch_pnj]
    result = calc_volatility_agg(df_pnj)

    if result:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)

        st.metric(
            "Giá hiện tại (Buy)",
            f"{result['current']:,.0f} VND",
            f"{result['delta']:,.0f} ({result['delta_pct']:.2f}%)"
        )

        st.markdown(
            f"""
            <div class="metric-extra">
              <span>🔺 Cao nhất: <b>{result['high']:,.0f}</b></span>
              <span>🔻 Thấp nhất: <b>{result['low']:,.0f}</b></span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Không đủ dữ liệu")


# ===== SJC =====
with cols[1]:
    st.markdown('<div class="brand-title sjc">SJC</div>', unsafe_allow_html=True)

    df_sjc_all = pd.read_csv("data/sjc/gold_sjc_history.csv")
    df_sjc_all["date"] = pd.to_datetime(df_sjc_all["date"])

    branches_sjc = sorted(df_sjc_all["BranchName"].unique())

    branch_sjc = st.selectbox("Chi nhánh SJC", branches_sjc, key="sjc_branch")

    df_sjc = df_sjc_all[df_sjc_all["BranchName"] == branch_sjc]
    result = calc_volatility_agg(df_sjc)

    if result:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)

        st.metric(
            "Giá hiện tại (Buy)",
            f"{result['current']:,.0f} VND",
            f"{result['delta']:,.0f} ({result['delta_pct']:.2f}%)"
        )

        st.markdown(
            f"""
            <div class="metric-extra">
              <span>🔺 Cao nhất: <b>{result['high']:,.0f}</b></span>
              <span>🔻 Thấp nhất: <b>{result['low']:,.0f}</b></span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Không đủ dữ liệu")
