import streamlit as st
import pandas as pd

from utils.plot import plot_realtime_bar
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui

from utils.plot import plot_gold_simple
from utils.volatility import prepare_timeseries, calc_volatility_agg


st.set_page_config(page_title="Biểu đồ giá", layout="wide")
render_navbar()


def load_css(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Không tìm thấy CSS: {path}")


load_css("assets/styles/base.css")
load_css("assets/styles/bieudogia.css")


col1, col2 = st.columns(2)

with col1:
    company = st.radio(
        "Doanh nghiệp",
        ["PNJ", "SJC"],
        horizontal=True
    )

with col2:
    data_type = st.radio(
        "Dữ liệu",
        ["History", "Realtime"],
        horizontal=True
    )


FILE_MAP = {
    ("PNJ", "History"): "data/pnj/gold_pnj_history.csv",
    ("PNJ", "Realtime"): "data/pnj/gold_pnj_realtime.csv",
    ("SJC", "History"): "data/sjc/gold_sjc_history.csv",
    ("SJC", "Realtime"): "data/sjc/gold_sjc_realtime.csv",
}

df_all = pd.read_csv(FILE_MAP[(company, data_type)])
df_all["date"] = pd.to_datetime(df_all["date"])


if data_type == "Realtime":
    plot_realtime_bar(df_all, company)
    clean_streamlit_ui()
    st.stop()


branches = sorted(df_all["BranchName"].dropna().unique())
branch = st.selectbox("Chi nhánh", branches)

freq_label = st.radio(
    "Độ chi tiết",
    ["Theo ngày", "Theo tháng"],
    horizontal=True
)

freq_map = {
    "Theo ngày": "D",
    "Theo tháng": "M"
}

df_chart = prepare_timeseries(
    df_all,
    branch,
    freq=freq_map[freq_label]
)

plot_gold_simple(df_chart, company)


vol = calc_volatility_agg(df_chart)

if vol:
    st.markdown(
        f"""
        <div class="volatility-box">
            <b>Biến động giá (Buy)</b><br>
            Giá hiện tại: {vol['current']:,.0f} VND<br>
            Thay đổi: {vol['delta']:,.0f} ({vol['delta_pct']:.2f}%)<br>
            Volatility: {vol['volatility']:.4f} ({vol['vol_level']})
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("Không đủ dữ liệu để tính biến động")


clean_streamlit_ui()
