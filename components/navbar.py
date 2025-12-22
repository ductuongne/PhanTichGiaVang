import streamlit as st

def render_navbar():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("biểu đồ", use_container_width=True):
            st.switch_page("pages/BieuDoGia.py")

    with col2:
        if st.button("Xu hướng", use_container_width=True):
            st.switch_page("pages/DuDoanXuHuong.py")

    with col3:
        if st.button("Biến động", use_container_width=True):
            st.switch_page("pages/BienDongGia.py")
    with col4:
        if st.button("Công cụ", use_container_width=True):
            st.switch_page("pages/CongCu.py")