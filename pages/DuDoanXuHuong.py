import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui

from utils.data_loader import load_sjc_data, train_and_predict_by_region

st.set_page_config(page_title="Phân tích Xu hướng", layout="wide")

render_navbar()
clean_streamlit_ui()

def load_css(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Không tìm thấy CSS: {path}")


load_css("assets/styles/dudoan.css")

st.title("📊 Dự đoán Xu hướng Giá Vàng SJC")
st.markdown("Mô hình sử dụng **Linear Regression** để xác định trend theo từng khu vực.")

# Load dữ liệu
with st.spinner("Đang tải dữ liệu..."):
    df = load_sjc_data()

# Dropdown chọn khu vực
regions = sorted(df["BranchName"].unique())

selected_region = st.selectbox(
    "📍 Chọn khu vực",
    regions
)

df_region = df[df["BranchName"] == selected_region]

# Train mô hình và dự đoán
df_region = df_region.sort_values("date")

with st.spinner("Đang huấn luyện mô hình và dự đoán..."):
    df_display, predicted_tomorrow = train_and_predict_by_region(df_region)

# Lấy giá của dòng cuối cùng sau khi đã lọc vùng
today_price = df_region["Sell"].iloc[-1]

# Tính toán xu hướng: So sánh giá dự đoán với giá thực tế cuối cùng
trend = "Tăng" if predicted_tomorrow > today_price else "Giảm"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Giá hôm nay", f"{today_price:,.0f} nghìn VNĐ")

with col2:
    # Tính toán chênh lệch (delta) để hiển thị mũi tên lên/xuống
    delta_val = predicted_tomorrow - today_price
    st.metric(
        "Dự đoán ngày tới",
        f"{predicted_tomorrow:,.0f} nghìn VNĐ",
        delta=f"{delta_val:,.0f} ({trend})",
        delta_color="normal" if trend == "Tăng" else "inverse"
    )

with col3:
    st.metric("Xu hướng dự báo", trend)

st.divider()

# Biểu đồ giá thực tế và dự đoán
st.subheader("1. So sánh Giá thực tế & Dự đoán")

sns.set_theme(style="darkgrid")

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(
    df_display["date"],
    df_display["Sell"],
    label="Giá thực tế",
    color="gold"
)
ax1.plot(
    df_display["date"],
    df_display["predicted"],
    label="Giá dự đoán",
    linestyle="--",
    color="blue"
)

ax1.set_title(f"Giá vàng SJC – {selected_region}")
ax1.set_xlabel("Thời gian")
ax1.set_ylabel("Giá bán (nghìn VNĐ)")
ax1.legend()

st.pyplot(fig1)

# Biểu đồ lợi nhuận
st.subheader("2. Hiệu quả đầu tư (Backtest mô phỏng)")

df_bt = df_display.copy()
df_bt["predicted_next"] = df_bt["predicted"].shift(-1)
df_bt["signal"] = (df_bt["predicted_next"] > df_bt["Sell"]).astype(int)
df_bt["daily_profit"] = (df_bt["Sell"].shift(-1) - df_bt["Sell"]) * df_bt["signal"]
df_bt["cumulative_profit"] = df_bt["daily_profit"].cumsum()

fig2, ax2 = plt.subplots(figsize=(12, 4))
ax2.plot(
    df_bt["date"],
    df_bt["cumulative_profit"],
    label="Lợi nhuận tích lũy (mô phỏng)",
    color="green"
)

ax2.set_title("Lợi nhuận tích lũy (Chiến lược Linear Regression)")
ax2.set_xlabel("Thời gian")
ax2.set_ylabel("nghìn VNĐ")
ax2.legend()

st.pyplot(fig2)
