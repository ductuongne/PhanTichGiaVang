import streamlit as st
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui
from utils.data_loader import load_pnj_history
from utils.plot import plot_gold_pnj

st.set_page_config(page_title="Biểu đồ giá", layout="wide")
render_navbar()

df = load_pnj_history()

branch = st.selectbox(
    "Chọn chi nhánh",
    df["BranchName"].unique()
)

plot_gold_pnj(df, branch)

clean_streamlit_ui()
