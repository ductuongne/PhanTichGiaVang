import streamlit as st
import sys
import os
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui

# st.set_page_config phải được gọi trước mọi lệnh Streamlit khác
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Thêm đường dẫn utils/getdata vào sys.path để import
getdata_path = os.path.join(os.path.dirname(__file__), "utils", "getdata")
if getdata_path not in sys.path:
    sys.path.insert(0, getdata_path)

# Khởi tạo dữ liệu khi app khởi động (chỉ chạy một lần)
if "data_initialized" not in st.session_state:
    try:
        # Import từ save_data (đã thêm vào sys.path)
        import save_data  # type: ignore
        save_data.save_data()
        st.session_state.data_initialized = True
    except Exception as e:
        # Nếu lỗi, vẫn cho app chạy nhưng ghi log
        st.session_state.data_initialized = False
        st.session_state.data_init_error = str(e)

render_navbar()
clean_streamlit_ui()