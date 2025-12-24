import streamlit as st
import pandas as pd
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui
from utils.volatility import calc_volatility_agg

st.set_page_config(page_title="Biến động", layout="wide")
render_navbar()
st.title("Biến động giá vàng")

DATA_FILES = {
    "PNJ": {
        "Hà Nội": "data/pnj/gold_pnj_history.csv",
        "TP.HCM": "data/pnj/gold_pnj_history.csv",
    },
    "SJC": {
        "Hà Nội": "data/sjc/gold_sjc_history.csv",
        "TP.HCM": "data/sjc/gold_sjc_history.csv",
    }
}

cols = st.columns(2)

# pnj
with cols[0]:
    st.subheader("PNJ")

    branch_pnj = st.selectbox(
        "Chi nhánh PNJ",
        list(DATA_FILES["PNJ"].keys()),
        key="pnj_branch"
    )

    df_pnj = pd.read_csv(DATA_FILES["PNJ"][branch_pnj])
    df_pnj["date"] = pd.to_datetime(df_pnj["date"])

    result = calc_volatility_agg(df_pnj)

    if result:
        st.metric(
            "Giá hiện tại (Buy)",
            f"{result['current']:,.0f} VND",
            f"{result['delta']:,.0f} ({result['delta_pct']:.2f}%)"
        )
        st.write(f"🔺 Cao nhất: {result['high']:,.0f} VND")
        st.write(f"🔻 Thấp nhất: {result['low']:,.0f} VND")
    else:
        st.warning("Không đủ dữ liệu")

# sjc
with cols[1]:
    st.subheader("SJC")

    branch_sjc = st.selectbox(
        "Chi nhánh SJC",
        list(DATA_FILES["SJC"].keys()),
        key="sjc_branch"
    )

    df_sjc = pd.read_csv(DATA_FILES["SJC"][branch_sjc])
    df_sjc["date"] = pd.to_datetime(df_sjc["date"])

    result = calc_volatility_agg(df_sjc)

    if result:
        st.metric(
            "Giá hiện tại (Buy)",
            f"{result['current']:,.0f} VND",
            f"{result['delta']:,.0f} ({result['delta_pct']:.2f}%)"
        )
        st.write(f"🔺 Cao nhất: {result['high']:,.0f} VND")
        st.write(f"🔻 Thấp nhất: {result['low']:,.0f} VND")
    else:
        st.warning("Không đủ dữ liệu")

clean_streamlit_ui()
