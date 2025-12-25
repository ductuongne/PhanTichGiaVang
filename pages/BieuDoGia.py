import streamlit as st
import pandas as pd
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui
from utils.plot import plot_gold_simple

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
        ["Realtime", "History"],
        horizontal=True
    )

# ==== map file ====
FILE_MAP = {
    ("PNJ", "History"): "data/pnj/gold_pnj_history.csv",
    ("PNJ", "Realtime"): "data/pnj/gold_pnj_realtime.csv",
    ("SJC", "History"): "data/sjc/gold_sjc_history.csv",
    ("SJC", "Realtime"): "data/sjc/gold_sjc_realtime.csv",
}

file_path = FILE_MAP[(company, data_type)]

df = pd.read_csv(file_path)
# ==== filter branch (History only) ====
if data_type == "History":
    branches = df["BranchName"].unique()
    selected_branch = st.selectbox(
        "Chi nhánh",
        branches
    )

    df = df[df["BranchName"] == selected_branch]



if data_type == "History":
    plot_gold_simple(df, company, data_type)
else:
    st.dataframe(
        df[["Buy", "Sell"]], 
        use_container_width=True
    )
    
    row = df.iloc[0]




clean_streamlit_ui()
