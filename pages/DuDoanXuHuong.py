import streamlit as st
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui

st.set_page_config(page_title="Phân tích", layout="wide")

render_navbar()
clean_streamlit_ui()