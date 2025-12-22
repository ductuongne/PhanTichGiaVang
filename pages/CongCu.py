import streamlit as st
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui

import streamlit as st
from datetime import datetime
import base64

def img_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    ext = path.split(".")[-1].lower()
    mime = "png" if ext == "png" else "jpeg"
    return f"data:image/{mime};base64,{b64}"

img_chi  = img_to_data_uri("pages/chi_vang.png")   # hoặc "chi_vang.png" tùy file bạn nằm đâu
img_luong = img_to_data_uri("pages/luong_vang.png")
img_tygia  = img_to_data_uri("pages/ty_gia.png")

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Convert Gold", layout="wide")
render_navbar()
clean_streamlit_ui()

st.markdown("""
<style>
/* Kill fake top pill / search bar */
.fake-search,
.search-bar,
.top-pill,
.header-pill,
.nav-search,
div:has(> input[type="search"]){
  display: none !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# THEME / CSS
# =========================
CSS = """
<style>
/* --- Page background --- */
.stApp{
  background: radial-gradient(1200px 600px at 50% 10%, #241a0c 0%, #0b0b0f 60%, #07070a 100%);
}

/* Remove default padding a bit */
.block-container{ padding-top: 24px; padding-bottom: 40px; }

/* --- Title pill --- */
.pill-title{
  display:inline-block;
  padding: 8px 14px;
  border-radius: 15px;
  background: linear-gradient(180deg, #9b0d0d 0%, #6f0a0a 100%);
  color: #fff;
  font-weight: 800;
  letter-spacing: .3px;
  box-shadow: 0 10px 24px rgba(155, 13, 13, .25);
  margin-bottom: 14px;
}

/* --- Main converter card --- */
.converter-wrap{
  background: linear-gradient(180deg, rgba(25,25,32,.65) 0%, rgba(10,10,14,.65) 100%);
  border: 1px solid rgba(255, 209, 102, .20);
  border-radius: 14px;
  padding: 18px 18px 16px 18px;
  box-shadow: 0 25px 60px rgba(0,0,0,.45);
  backdrop-filter: blur(6px);
}

/* --- Input blocks --- */
.unit-label{
  color: rgba(255, 209, 102, .92);
  font-weight: 700;
  font-size: 25px;
  margin-bottom: 6px;
  display:flex;
  align-items:center;
  gap: 6px;
  justify-content: center;
}
.unit-dot{
  width: 10px; height: 7px; border-radius: 99px;
  background: rgba(255, 209, 102, .85);
  box-shadow: 0 0 12px rgba(255, 209, 102, .35);
}

.block-box{
  border-radius: 12px;
  border: 1px solid rgba(255, 209, 102, .35);
  background: rgba(10, 10, 14, .55);
  padding: 10px 12px 8px 12px;
  box-shadow: inset 0 0 0 1px rgba(255, 209, 102, .06);
}

.small-under{
  margin-top: 10px;
  color: rgba(255, 255, 255, .75);
  font-size: 20px;
}

.arrow-col{
  display:flex;
  justify-content:center;
  align-items:center;
  height: 92px;
}
.arrow{
  font-size: 26px;
  color: rgba(255, 209, 102, .95);
  text-shadow: 0 0 16px rgba(255, 209, 102, .35);
}

/* --- Footer note --- */
.note{
  margin-top: 14px;
  color: rgba(255,255,255,.70);
  font-size: 13px;
}

/* --- Info cards --- */
.info-row{
  margin-top: 16px;
  display:flex;
  gap: 14px;
}
.info-card{
  flex: 1;
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(22,22,28,.65) 0%, rgba(10,10,14,.65) 100%);
  border: 1px solid rgba(255, 209, 102, .18);
  padding: 16px 14px;
  box-shadow: 0 18px 40px rgba(0,0,0,.35);
  min-height: 92px;
}
.info-emoji{
  font-size: 26px;
  margin-bottom: 8px;
}
.info-text{
  color: rgba(255,255,255,.88);
  font-weight: 700;
  font-size: 16px;
}
.info-sub{
  margin-top: 2px;
  color: rgba(255,255,255,.65);
  font-size: 12px;
}

/* --- Make streamlit widgets darker --- */
div[data-baseweb="select"] > div{
  background: rgba(10,10,14,.6) !important;
  border-color: rgba(255, 209, 102, .25) !important;
}
div[data-baseweb="input"] input{
  background: rgba(10,10,14,.0) !important;
  color: rgba(255,255,255,.92) !important;

}
label{ color: rgba(255,255,255,.75) !important; }

.info-icon{
  height: 90px;                 /* 👈 cùng chiều cao cho cả 3 card */
  display: flex;
  align-items: center;          /* canh giữa dọc */
  justify-content: center;      /* canh giữa ngang */
  margin-bottom: 10px;
}

.info-icon img{
  height: 80px;                 /* 👈 ép ảnh cùng chiều cao */
  width: auto;                  /* giữ tỉ lệ */
  object-fit: contain;          /* không méo */
  display: block;
}


/* Hide empty labels spacing */
div.stNumberInput label, div.stSelectbox label{ display:none !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =========================
# CONVERSION CONSTANTS
# =========================
CHI_TO_GRAM = 3.75               # ~3.75g
LUONG_TO_CHI = 10                # 1 lượng = 10 chỉ
OZ_TO_GRAM = 31.1035             # 1 troy oz

# =========================
# DEFAULT STATE
# =========================
if "active" not in st.session_state:
    st.session_state.active = "luong"

if "luong" not in st.session_state:
    st.session_state.luong = 0.50
if "chi" not in st.session_state:
    st.session_state.chi = st.session_state.luong * LUONG_TO_CHI
if "usd_oz" not in st.session_state:
    st.session_state.usd_oz = 1225.0

# rates (you can wire these to your data)
if "price_vnd_per_luong" not in st.session_state:
    st.session_state.price_vnd_per_luong = 18_275_000  # giống hình
if "usd_to_vnd" not in st.session_state:
    st.session_state.usd_to_vnd = 25_000

# =========================
# HELPERS
# =========================
def luong_to_grams(luong: float) -> float:
    return luong * LUONG_TO_CHI * CHI_TO_GRAM

def chi_to_grams(chi: float) -> float:
    return chi * CHI_TO_GRAM

def oz_to_grams(oz: float) -> float:
    return oz * OZ_TO_GRAM

def grams_to_luong(g: float) -> float:
    return g / (LUONG_TO_CHI * CHI_TO_GRAM)

def grams_to_chi(g: float) -> float:
    return g / CHI_TO_GRAM

def grams_to_oz(g: float) -> float:
    return g / OZ_TO_GRAM

def recalc_all():
    """Recalculate the other two fields based on the active one."""
    active = st.session_state.active

    # interpret the active value as "gold amount in grams"
    if active == "luong":
        g = luong_to_grams(st.session_state.luong)
    elif active == "chi":
        g = chi_to_grams(st.session_state.chi)
    else:  # usd_oz active means user is typing the "price", not quantity
        # If user edits usd/oz, we DON'T change amounts; we just keep price.
        return

    # update other amount fields
    st.session_state.chi = grams_to_chi(g)
    st.session_state.luong = grams_to_luong(g)

def on_change_luong():
    st.session_state.active = "luong"
    recalc_all()

def on_change_chi():
    st.session_state.active = "chi"
    recalc_all()

def on_change_usd_oz():
    st.session_state.active = "usd_oz"
    # no amount update needed (price-only field)

def fmt_vnd(x: float) -> str:
    return f"{int(round(x, 0)):,}".replace(",", ",")

# =========================
# UI
# =========================
st.markdown('<div class="pill-title">Convert Gold</div>', unsafe_allow_html=True)

with st.container():
   
    # Top row: 3 blocks + arrows
    c1, a1, c2, a2, c3 = st.columns([5, 1, 5, 1, 5], vertical_alignment="center")

    with c1:
        st.markdown('<div class="unit-label"><span class="unit-dot"></span>Lượng ▾</div>', unsafe_allow_html=True)
        st.number_input(
            "luong",
            min_value=0.0,
            value=float(st.session_state.luong),
            step=0.01,
            key="luong",
            on_change=on_change_luong,
            format="%.2f",
        )

        vnd_per_luong = st.session_state.price_vnd_per_luong
        st.markdown(
            f'<div class="small-under">{fmt_vnd(vnd_per_luong)} VND / Lượng</div>',
            unsafe_allow_html=True
        )

    with a1:
        st.markdown('<div class="arrow-col"><div class="arrow">↔</div></div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="unit-label"><span class="unit-dot"></span>Chỉ ▾</div>', unsafe_allow_html=True)
        st.number_input(
            "chi",
            min_value=0.0,
            value=float(st.session_state.chi),
            step=0.10,
            key="chi",
            on_change=on_change_chi,
            format="%.2f",
        )

        vnd_per_chi = st.session_state.price_vnd_per_luong / LUONG_TO_CHI
        st.markdown(
            f'<div class="small-under">{fmt_vnd(vnd_per_chi)} VND / Chỉ</div>',
            unsafe_allow_html=True
        )

    with a2:
        st.markdown('<div class="arrow-col"><div class="arrow">↔</div></div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="unit-label"><span class="unit-dot"></span>USD/oz ▾</div>', unsafe_allow_html=True)
        st.number_input(
            "usd_oz",
            min_value=0.0,
            value=float(st.session_state.usd_oz),
            step=1.0,
            key="usd_oz",
            on_change=on_change_usd_oz,
            format="%.0f",
        )
       

        # Show an extra line like in the screenshot (example)
        st.markdown(
            f'<div class="small-under">{fmt_vnd(st.session_state.usd_oz * 2)} USD / oz</div>',
            unsafe_allow_html=True
        )

    # note line
    today = datetime.now().strftime("%d/%m/%Y")
    st.markdown(f'<div class="note">* Giá vàng niêm yết ngày {today}</div>', unsafe_allow_html=True)

    # info cards
    usd_to_vnd = st.session_state.usd_to_vnd
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
    <div class="info-text">Tỷ giá: ${st.session_state.usd_oz:,.0f}/oz</div>
    <div class="info-sub">$1 = {fmt_vnd(usd_to_vnd)} VND</div>
  </div>

</div>
""",
unsafe_allow_html=True
)



# Optional: small debug for you
# st.write(st.session_state)
