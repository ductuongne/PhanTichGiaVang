import streamlit as st
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui
# Import hàm từ file data_loader (giả sử file đó nằm cùng thư mục hoặc trong python path)
from utils.data_loader import get_gold_predictions 

st.set_page_config(page_title="Phân tích Xu hướng", layout="wide")

render_navbar()
clean_streamlit_ui()

st.title("📊 Dự đoán Xu hướng Giá Vàng")
st.markdown("Mô hình sử dụng **Linear Regression** để xác định trend dài hạn.")

# --- Gọi hàm để lấy dữ liệu ---
with st.spinner("Đang tải dữ liệu và phân tích..."):
    fig_price, fig_profit, info = get_gold_predictions()

# --- Hiển thị các chỉ số (Metric) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Giá hiện tại", f"{info['today_price']:.2f} $")

with col2:
    delta_color = "normal"
    if info['trend'] == "Tăng": delta_color = "off" # Streamlit auto màu xanh
    
    st.metric(
        "Dự đoán ngày mai", 
        f"{info['predicted_tomorrow']:.2f} $", 
        delta=info['trend'],
        delta_color="inverse" if info['trend'] == "Giảm" else "normal"
    )

with col3:
    st.metric("Xu hướng dự báo", info['trend'])

with col4:
    st.metric("Lợi nhuận mô phỏng (1 năm)", f"{info['cumulative_profit']:.2f} $")

st.divider()

# --- Hiển thị biểu đồ 1: Giá ---
st.subheader("1. So sánh Giá thực tế & Dự đoán")
st.pyplot(fig_price)

# --- Hiển thị biểu đồ 2: Lợi nhuận ---
st.subheader("2. Hiệu quả đầu tư (Backtest)")
st.pyplot(fig_profit)