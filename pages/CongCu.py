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
LUONG_TO_GRAM = 37.5


# ==================================================
# LOAD USD/VND RATE
# ==================================================
@st.cache_data
def load_usd_vnd_rate():
    try:
        df = pd.read_csv("data/usd/usd_vnd_rate.csv")
        df = df.sort_values("date")
        return float(df.iloc[-1]["usd_vnd_rate"])
    except Exception as e:
        st.warning(f"Không đọc được tỷ giá USD/VND, dùng 25,000 VND: {e}")
        return 25_000.0


USD_TO_VND = load_usd_vnd_rate()


# ==================================================
# LOAD GOLD PRICES
# ==================================================
@st.cache_data
def load_gold_prices():
    try:
        df_pnj = pd.read_csv("data/pnj/gold_pnj_realtime.csv")
        df_sjc = pd.read_csv("data/sjc/gold_sjc_realtime.csv")

        return df_pnj.iloc[0]["Sell"] * 1000, df_sjc.iloc[0]["Sell"] * 1000
    except Exception as e:
        st.error(f"Lỗi đọc giá vàng: {e}")
        return 15_650_000, 15_900_000


price_pnj, price_sjc = load_gold_prices()


# ==================================================
# CONVERT FUNCTIONS
# ==================================================
def vnd_to_usd(vnd_value: float) -> float:
    return vnd_value / USD_TO_VND if USD_TO_VND else 0.0


def usd_to_vnd(usd_value: float) -> float:
    return usd_value * USD_TO_VND


# ==================================================
# SESSION STATE (canonical + widget keys)
# ==================================================
st.session_state.setdefault("luong", 1.0)
st.session_state.setdefault("chi", st.session_state.luong * LUONG_TO_CHI)

# tách key của widget input
st.session_state.setdefault("luong_input", st.session_state.luong)
st.session_state.setdefault("chi_input", st.session_state.chi)

st.session_state.setdefault("usd", vnd_to_usd(price_sjc))
st.session_state.setdefault("usd_input", st.session_state.usd)



# ==================================================
# UPDATE HANDLERS
# ==================================================
def update_from_luong():
    luong = float(st.session_state.luong_input)
    st.session_state.luong = luong

    st.session_state.chi = round(luong * LUONG_TO_CHI, 2)
    st.session_state.chi_input = st.session_state.chi  # cập nhật widget bên Chỉ

    # cập nhật USD theo giá SJC
    vnd_total = st.session_state.luong * price_sjc
    st.session_state.usd = vnd_to_usd(vnd_total)
    st.session_state.usd_input = st.session_state.usd


def update_from_chi():
    chi = float(st.session_state.chi_input)
    st.session_state.chi = chi

    st.session_state.luong = round(chi / LUONG_TO_CHI, 2)
    st.session_state.luong_input = st.session_state.luong  # cập nhật widget bên Lượng

    # cập nhật USD theo giá SJC
    vnd_total = st.session_state.luong * price_sjc
    st.session_state.usd = vnd_to_usd(vnd_total)
    st.session_state.usd_input = st.session_state.usd


def update_from_usd():
    usd_val = float(st.session_state.usd_input)
    st.session_state.usd = usd_val

    # quy đổi tổng giá trị USD sang VND theo tỷ giá, sau đó về lượng (theo giá SJC)
    vnd_total = usd_to_vnd(usd_val)
    new_luong = vnd_total / price_sjc if price_sjc else 0.0

    st.session_state.luong = round(new_luong, 2)
    st.session_state.chi = round(st.session_state.luong * LUONG_TO_CHI, 2)

    st.session_state.luong_input = st.session_state.luong
    st.session_state.chi_input = st.session_state.chi
    st.session_state.usd_input = st.session_state.usd



# ==================================================
# FORMATTERS
# ==================================================
fmt_vnd = lambda x: f"{int(round(x)):,}".replace(",", ".")
fmt_usd = lambda x: f"{x:,.0f}"


# ==================================================
# UI
# ==================================================
st.markdown('<div class="pill-title">Convert Gold</div>', unsafe_allow_html=True)


usd_sjc = vnd_to_usd(price_sjc)
usd_pnj = vnd_to_usd(price_pnj)

c1, a1, c2, a2, c3 = st.columns([5, 1, 5, 1, 5], vertical_alignment="top")

# ----- LUONG -----
with c1:
    st.markdown('<div class="unit-label"><span class="unit-dot"></span>Lượng</div>', unsafe_allow_html=True)
    st.number_input(
    "luong",
    min_value=0.0,
    value=float(st.session_state.luong_input),
    step=0.01,
    format="%.2f",
    key="luong_input",
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
    value=float(st.session_state.chi_input),
    step=0.1,
    format="%.2f",
    key="chi_input",
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


# ----- USD -----
with c3:
    st.markdown('<div class="unit-label"><span class="unit-dot"></span>USD</div>', unsafe_allow_html=True)
    st.number_input(
    "usd",
    min_value=0.0,
    value=float(st.session_state.usd_input),
    step=10.0,
    format="%.0f",
    key="usd_input",
    on_change=update_from_usd,
    label_visibility="collapsed"
    )

    st.markdown('<div class="small-under">Quy đổi tiền tệ theo tỷ giá USD/VND</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="small-under">1 USD = {fmt_vnd(USD_TO_VND)} VND</div>', unsafe_allow_html=True)

# ----- FOOTER -----
today = datetime.now().strftime("%d/%m/%Y")
st.markdown(
    f'<div class="note">* SJC: {fmt_vnd(price_sjc)} | PNJ: {fmt_vnd(price_pnj)} nghìn VND/lượng (ngày {today})</div>',
    unsafe_allow_html=True
)

# ----- INFO CARDS -----
st.markdown(
    f"""
<div class="info-row">
  <div class="info-card">
    <div class="info-icon"><img src="{IMG_LUONG}"/></div>
    <div class="info-text">1 Lượng = 1 Cây vàng = 10 Chỉ</div>
    <div class="info-sub">Đơn vị vàng Việt Nam</div>
  </div>

  <div class="info-card">
    <div class="info-icon"><img src="{IMG_CHI}"/></div>
    <div class="info-text">1 Chỉ ≈ {CHI_TO_GRAM} g</div>
    <div class="info-sub">Khối lượng quy ước</div>
  </div>

  <div class="info-card">
    <div class="info-icon"><img src="{IMG_TYGIA}"/></div>
        <div class="info-text">SJC: ${fmt_usd(usd_sjc)} | PNJ: ${fmt_usd(usd_pnj)}</div>
        <div class="info-sub">$1 = {fmt_vnd(USD_TO_VND)} VND</div>
  </div>
</div>
""",
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)
