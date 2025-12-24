import streamlit as st
import pandas as pd
from datetime import datetime
import base64

from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui


# ==================================================
# CONFIG
# ==================================================
st.set_page_config(page_title="Convert Gold", layout="wide")
render_navbar()
clean_streamlit_ui()


# ==================================================
# LOAD CSS
# ==================================================
def load_css(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Không tìm thấy CSS: {path}")


# base + page css
load_css("assets/styles/base.css")
load_css("assets/styles/congcu.css")


# ==================================================
# LOAD IMAGES
# ==================================================
def img_to_data_uri(path: str) -> str:
    try:
        with open(path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        ext = path.split(".")[-1].lower()
        mime = "png" if ext == "png" else "jpeg"
        return f"data:image/{mime};base64,{b64}"
    except FileNotFoundError:
        st.error(f"Không tìm thấy ảnh: {path}")
        return ""


IMG_CHI = img_to_data_uri("assets/images/chi_vang.png")
IMG_LUONG = img_to_data_uri("assets/images/luong_vang.png")
IMG_TYGIA = img_to_data_uri("assets/images/ty_gia.png")


# ==================================================
# CONSTANTS
# ==================================================
CHI_TO_GRAM = 3.75
LUONG_TO_CHI = 10
OZ_TO_GRAM = 31.1035
LUONG_TO_GRAM = 37.5
USD_TO_VND = 25_000


# ==================================================
# LOAD GOLD PRICES
# ==================================================
@st.cache_data
def load_gold_prices():
    try:
        df_pnj = pd.read_csv("data/pnj/gold_pnj_realtime.csv")
        df_sjc = pd.read_csv("data/sjc/gold_sjc_realtime.csv")

        return df_pnj.iloc[0]["Sell"], df_sjc.iloc[0]["Sell"]
    except Exception as e:
        st.error(f"Lỗi đọc giá vàng: {e}")
        return 15_650_000, 15_900_000


price_pnj, price_sjc = load_gold_prices()


# ==================================================
# CONVERT FUNCTIONS
# ==================================================
def vnd_luong_to_usd_oz(vnd_luong: float) -> float:
    return vnd_luong / (USD_TO_VND * (LUONG_TO_GRAM / OZ_TO_GRAM))


def usd_oz_to_vnd_luong(usd_oz: float) -> float:
    return usd_oz * USD_TO_VND * (LUONG_TO_GRAM / OZ_TO_GRAM)


# ==================================================
# SESSION STATE
# ==================================================
st.session_state.setdefault("luong", 1.0)
st.session_state.setdefault("chi", 10.0)
st.session_state.setdefault("usd_oz", vnd_luong_to_usd_oz(price_sjc))


# ==================================================
# UPDATE HANDLERS
# ==================================================
def update_from_luong():
    st.session_state.chi = st.session_state.luong * LUONG_TO_CHI


def update_from_chi():
    st.session_state.luong = st.session_state.chi / LUONG_TO_CHI


def update_from_usd_oz():
    vnd_luong = usd_oz_to_vnd_luong(st.session_state.usd_oz)
    current_value = st.session_state.luong * price_sjc
    new_luong = current_value / vnd_luong

    st.session_state.luong = new_luong
    st.session_state.chi = new_luong * LUONG_TO_CHI


# ==================================================
# FORMATTERS
# ==================================================
fmt_vnd = lambda x: f"{int(round(x)):,}".replace(",", ".")
fmt_usd = lambda x: f"{x:,.0f}"


# ==================================================
# UI
# ==================================================
st.markdown('<div class="pill-title">Convert Gold</div>', unsafe_allow_html=True)

st.markdown('<div class="converter-wrap">', unsafe_allow_html=True)

usd_oz_sjc = vnd_luong_to_usd_oz(price_sjc)
usd_oz_pnj = vnd_luong_to_usd_oz(price_pnj)

c1, a1, c2, a2, c3 = st.columns([5, 1, 5, 1, 5], vertical_alignment="center")

# ----- LUONG -----
with c1:
    st.markdown('<div class="unit-label"><span class="unit-dot"></span>Lượng</div>', unsafe_allow_html=True)
    st.number_input(
        "luong",
        min_value=0.0,
        step=0.01,
        format="%.2f",
        on_change=update_from_luong,
        label_visibility="collapsed"
    )
    st.markdown(f'<div class="small-under">{fmt_vnd(st.session_state.luong * price_sjc)} VND (SJC)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="small-under">{fmt_vnd(st.session_state.luong * price_pnj)} VND (PNJ)</div>', unsafe_allow_html=True)


# ----- ARROW -----
with a1:
    st.markdown('<div class="arrow-col"><div class="arrow">↔</div></div>', unsafe_allow_html=True)


# ----- CHI -----
with c2:
    st.markdown('<div class="unit-label"><span class="unit-dot"></span>Chỉ</div>', unsafe_allow_html=True)
    st.number_input(
        "chi",
        min_value=0.0,
        step=0.1,
        format="%.2f",
        on_change=update_from_chi,
        label_visibility="collapsed"
    )
    vnd_chi_sjc = (st.session_state.chi / LUONG_TO_CHI) * price_sjc
    vnd_chi_pnj = (st.session_state.chi / LUONG_TO_CHI) * price_pnj
    st.markdown(f'<div class="small-under">{fmt_vnd(vnd_chi_sjc)} VND (SJC)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="small-under">{fmt_vnd(vnd_chi_pnj)} VND (PNJ)</div>', unsafe_allow_html=True)


# ----- ARROW -----
with a2:
    st.markdown('<div class="arrow-col"><div class="arrow">↔</div></div>', unsafe_allow_html=True)


# ----- USD/OZ -----
with c3:
    st.markdown('<div class="unit-label"><span class="unit-dot"></span>USD/oz</div>', unsafe_allow_html=True)
    st.number_input(
        "usd_oz",
        min_value=0.0,
        step=1.0,
        format="%.0f",
        on_change=update_from_usd_oz,
        label_visibility="collapsed"
    )
    st.markdown('<div class="small-under">Giá vàng thế giới</div>', unsafe_allow_html=True)


# ----- FOOTER -----
today = datetime.now().strftime("%d/%m/%Y")
st.markdown(
    f'<div class="note">* SJC: {fmt_vnd(price_sjc)} | PNJ: {fmt_vnd(price_pnj)} VND/lượng (ngày {today})</div>',
    unsafe_allow_html=True
)

# ----- INFO CARDS -----
st.markdown(
    f"""
<div class="info-row">
  <div class="info-card">
    <div class="info-icon"><img src="{IMG_LUONG}"/></div>
    <div class="info-text">1 Lượng = 10 Chỉ</div>
    <div class="info-sub">Đơn vị vàng Việt Nam</div>
  </div>

  <div class="info-card">
    <div class="info-icon"><img src="{IMG_CHI}"/></div>
    <div class="info-text">1 Chỉ ≈ {CHI_TO_GRAM} g</div>
    <div class="info-sub">Khối lượng quy ước</div>
  </div>

  <div class="info-card">
    <div class="info-icon"><img src="{IMG_TYGIA}"/></div>
    <div class="info-text">SJC: ${fmt_usd(usd_oz_sjc)} | PNJ: ${fmt_usd(usd_oz_pnj)}</div>
    <div class="info-sub">$1 = {fmt_vnd(USD_TO_VND)} VND</div>
  </div>
</div>
""",
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)
