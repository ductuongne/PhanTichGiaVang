import streamlit as st
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui
from datetime import datetime
import base64
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Convert Gold", layout="wide")
render_navbar()
clean_streamlit_ui()


# =========================
# LOAD CSS FROM FILE
# =========================
def load_css(file_path):
    """Đọc file CSS và trả về nội dung"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f"<style>{f.read()}</style>"
    except FileNotFoundError:
        st.error(f"Không tìm thấy file CSS: {file_path}")
        return ""


# Load CSS từ file
css_content = load_css("assets/styles/congcu.css")
st.markdown(css_content, unsafe_allow_html=True)


# =========================
# LOAD IMAGES
# =========================
def img_to_data_uri(path: str) -> str:
    """Chuyển ảnh thành base64 để hiển thị trong HTML"""
    try:
        with open(path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode("utf-8")
        ext = path.split(".")[-1].lower()
        mime = "png" if ext == "png" else "jpeg"
        return f"data:image/{mime};base64,{b64}"
    except FileNotFoundError:
        st.error(f"Không tìm thấy ảnh: {path}")
        return ""


img_chi = img_to_data_uri("assets/images/chi_vang.png")
img_luong = img_to_data_uri("assets/images/luong_vang.png")
img_tygia = img_to_data_uri("assets/images/ty_gia.png")

# =========================
# CONSTANTS
# =========================
CHI_TO_GRAM = 3.75  # 1 chỉ = 3.75g
LUONG_TO_CHI = 10  # 1 lượng = 10 chỉ
OZ_TO_GRAM = 31.1035  # 1 oz = 31.1035g
LUONG_TO_GRAM = 37.5  # 1 lượng = 37.5g
USD_TO_VND = 25000  # Tỷ giá cố định


# =========================
# LOAD GOLD PRICES FROM CSV
# =========================
@st.cache_data
def load_gold_prices():
    """Đọc giá vàng từ file PNJ và SJC realtime"""
    try:
        # Đọc PNJ
        df_pnj = pd.read_csv("data/pnj/gold_pnj_realtime.csv")
        pnj_price = df_pnj.iloc[0]['Sell']  # Lấy giá bán dòng đầu

        # Đọc SJC
        df_sjc = pd.read_csv("data/sjc/gold_sjc_realtime.csv")
        sjc_price = df_sjc.iloc[0]['Sell']  # Lấy giá bán dòng đầu

        return pnj_price, sjc_price
    except Exception as e:
        st.error(f"Lỗi đọc file CSV: {e}")
        return 15650000, 15900000  # Giá mặc định nếu lỗi


# Load giá vàng
price_pnj, price_sjc = load_gold_prices()


# =========================
# CONVERSION FUNCTIONS
# =========================
def vnd_per_luong_to_usd_per_oz(vnd_luong):
    """Chuyển VND/lượng sang USD/oz
    Công thức: USD/oz = VND/lượng / (USD_TO_VND × (LUONG_TO_GRAM / OZ_TO_GRAM))
    """
    usd_oz = vnd_luong / (USD_TO_VND * (LUONG_TO_GRAM / OZ_TO_GRAM))
    return usd_oz


def usd_per_oz_to_vnd_per_luong(usd_oz):
    """Chuyển USD/oz sang VND/lượng
    Công thức: VND/lượng = USD/oz × USD_TO_VND × (LUONG_TO_GRAM / OZ_TO_GRAM)
    """
    vnd_luong = usd_oz * USD_TO_VND * (LUONG_TO_GRAM / OZ_TO_GRAM)
    return vnd_luong


# =========================
# SESSION STATE
# =========================
if "luong" not in st.session_state:
    st.session_state.luong = 1.0
if "chi" not in st.session_state:
    st.session_state.chi = 10.0
if "usd_oz" not in st.session_state:
    # Tính USD/oz từ giá SJC
    st.session_state.usd_oz = vnd_per_luong_to_usd_per_oz(price_sjc)


# =========================
# UPDATE FUNCTIONS
# =========================
def update_from_luong():
    """Khi user nhập Lượng"""
    luong = st.session_state.luong
    st.session_state.chi = luong * LUONG_TO_CHI


def update_from_chi():
    """Khi user nhập Chỉ"""
    chi = st.session_state.chi
    st.session_state.luong = chi / LUONG_TO_CHI


def update_from_usd_oz():
    """Khi user nhập USD/oz - tính lại số lượng vàng"""
    usd_oz = st.session_state.usd_oz
    # Tính giá VND/lượng từ USD/oz người dùng nhập
    vnd_per_luong = usd_per_oz_to_vnd_per_luong(usd_oz)
    # Giữ nguyên số lượng vàng (không thay đổi)
    pass


# =========================
# FORMAT FUNCTION
# =========================
def fmt_vnd(x: float) -> str:
    """Format số tiền VND"""
    return f"{int(round(x, 0)):,}".replace(",", ".")


def fmt_usd(x: float) -> str:
    """Format USD"""
    return f"{x:,.0f}"


# =========================
# UI
# =========================
st.markdown('<div class="pill-title">Convert Gold</div>', unsafe_allow_html=True)

# Tính USD/oz từ giá SJC và PNJ
usd_oz_sjc = vnd_per_luong_to_usd_per_oz(price_sjc)
usd_oz_pnj = vnd_per_luong_to_usd_per_oz(price_pnj)

with st.container():
    # Top row: 3 blocks + arrows
    c1, a1, c2, a2, c3 = st.columns([5, 1, 5, 1, 5], vertical_alignment="center")

    with c1:
        st.markdown('<div class="unit-label"><span class="unit-dot"></span>Lượng ▾</div>', unsafe_allow_html=True)
        st.number_input(
            "luong_input",
            min_value=0.0,
            value=float(st.session_state.luong),
            step=0.01,
            key="luong",
            on_change=update_from_luong,
            format="%.2f",
            label_visibility="collapsed"
        )

        # Hiển thị giá VND theo số lượng
        total_vnd_sjc = st.session_state.luong * price_sjc
        st.markdown(
            f'<div class="small-under">{fmt_vnd(total_vnd_sjc)} VND (SJC)</div>',
            unsafe_allow_html=True
        )

    with a1:
        st.markdown('<div class="arrow-col"><div class="arrow">↔</div></div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="unit-label"><span class="unit-dot"></span>Chỉ ▾</div>', unsafe_allow_html=True)
        st.number_input(
            "chi_input",
            min_value=0.0,
            value=float(st.session_state.chi),
            step=0.10,
            key="chi",
            on_change=update_from_chi,
            format="%.2f",
            label_visibility="collapsed"
        )

        # Hiển thị giá VND theo số lượng
        total_vnd_chi = (st.session_state.chi / LUONG_TO_CHI) * price_sjc
        st.markdown(
            f'<div class="small-under">{fmt_vnd(total_vnd_chi)} VND (SJC)</div>',
            unsafe_allow_html=True
        )

    with a2:
        st.markdown('<div class="arrow-col"><div class="arrow">↔</div></div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="unit-label"><span class="unit-dot"></span>USD/oz ▾</div>', unsafe_allow_html=True)

        st.number_input(
            "usd_oz_input",
            min_value=0.0,
            value=float(st.session_state.usd_oz),
            step=1.0,
            key="usd_oz",
            on_change=update_from_usd_oz,
            format="%.0f",
            label_visibility="collapsed"
        )

        st.markdown(
            f'<div class="small-under">Giá thị trường vàng thế giới</div>',
            unsafe_allow_html=True
        )

    # Note line với giá vàng hiện tại
    today = datetime.now().strftime("%d/%m/%Y")
    st.markdown(
        f'<div class="note">* Giá vàng SJC: {fmt_vnd(price_sjc)} VND/lượng | PNJ: {fmt_vnd(price_pnj)} VND/lượng (ngày {today})</div>',
        unsafe_allow_html=True
    )

    # Info cards
    st.markdown(
        f"""
<div class="info-row">

  <div class="info-card">
    <div class="info-icon"><img src="{img_luong}"/></div>
    <div class="info-text">1 Lượng = 10 Chỉ</div>
    <div class="info-sub">Quy đổi đơn vị vàng Việt Nam</div>
  </div>

  <div class="info-card">
    <div class="info-icon"><img src="{img_chi}"/></div>
    <div class="info-text">1 Chỉ ≈ {CHI_TO_GRAM:.2f} grams</div>
    <div class="info-sub">Khối lượng quy ước phổ biến</div>
  </div>

  <div class="info-card">
    <div class="info-icon"><img src="{img_tygia}"/></div>
    <div class="info-text">SJC: ${fmt_usd(usd_oz_sjc)}/oz | PNJ: ${fmt_usd(usd_oz_pnj)}/oz</div>
    <div class="info-sub">$1 = {fmt_vnd(USD_TO_VND)} VND</div>
  </div>

</div>
""",
        unsafe_allow_html=True
    )