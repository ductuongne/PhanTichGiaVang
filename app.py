import streamlit as st
from utils.data_loader import load_gold_price

st.set_page_config(page_title="Phân tích giá vàng", layout="centered")

st.title("📈 Phân tích giá vàng")

df = load_gold_price()

st.subheader("Dữ liệu giá vàng")
st.dataframe(df)

st.subheader("Biểu đồ giá vàng")
st.line_chart(df.set_index("date")["price"])
