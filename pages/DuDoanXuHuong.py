import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from components.navbar import render_navbar
from components.clean_ui import clean_streamlit_ui
from utils.data_loader import load_gold_price, load_sjc_data

st.set_page_config(page_title="Dự đoán Xu hướng", layout="wide")

render_navbar()
clean_streamlit_ui()

st.markdown("<h1 style='color: gold;'>Dự đoán Xu hướng Giá Vàng 7 Ngày Tới</h1>", unsafe_allow_html=True)

# Load data
df_world = load_gold_price()
df_vn = load_sjc_data()

# Prepare data for prediction
def prepare_data(df):
    df = df.sort_values('date')
    df['days'] = (df['date'] - df['date'].min()).dt.days
    return df

df_world = prepare_data(df_world)
df_vn = prepare_data(df_vn)

# Fit models
model_world = LinearRegression()
model_world.fit(df_world[['days']], df_world['price'])

model_vn = LinearRegression()
model_vn.fit(df_vn[['days']], df_vn['price'])

# Predict next 7 days
last_date = max(df_world['date'].max(), df_vn['date'].max())
usd_vnd_rate = 23500  # Tỷ giá giả định
ounce_per_luong = 37.5 / 31.1035  # 1 lượng = 37.5g, 1 oz = 31.1035g
start_date = last_date
end_date = last_date + timedelta(days=6)
predictions = []
for i in range(7):
    pred_date = last_date + timedelta(days=i)
    days_world = (pred_date - df_world['date'].min()).days
    days_vn = (pred_date - df_vn['date'].min()).days
    pred_world_vnd = model_world.predict([[days_world]])[0]
    pred_vn = model_vn.predict([[days_vn]])[0]
    # Chuyển đổi vàng thế giới sang USD/oz
    pred_world_usd = (pred_world_vnd / ounce_per_luong) / usd_vnd_rate
    predictions.append({
        'Ngày': pred_date.strftime('%d/%m'),
        'Dự báo giá vàng thế giới (USD/oz)': f"{pred_world_usd:,.2f} USD",
        'Dự báo giá vàng Việt Nam (VND/lượng)': f"{pred_vn:,.0f} VND"
    })

df_pred = pd.DataFrame(predictions)

# Layout
col1, col2 = st.columns([7, 3])

with col1:
    title = f"BẢNG DỰ BÁO GIÁ VÀNG TUÂN TỚI THEO NGÀY ({start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m/%Y')})"
    st.subheader(title)
    
    df_show = df_pred.reset_index(drop=True)

    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: black;
        color: white;
    }
    .gold-table table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
        background-color: #333;
        color: white;
        border: 1px solid white;
    }
    .gold-table th {
        text-align: center;
        padding: 8px;
        background-color: #555;
        border-bottom: 1px solid white;
        border-right: 1px solid white;
        color: white;
    }
    .gold-table td {
        padding: 8px;
        border-bottom: 1px solid white;
        border-right: 1px solid white;
        background-color: #222;
        color: white;
    }
    /* Cột Ngày */
    .gold-table td:nth-child(1) {
        text-align: center;
    }
    /* Cột Giá */
    .gold-table td:nth-child(2),
    .gold-table td:nth-child(3) {
        text-align: right;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

    # Render bảng bằng HTML
    st.markdown(
        f"<div class='gold-table'>{df_show.to_html(index=False)}</div>",
        unsafe_allow_html=True
    )

with col2:
    st.subheader('Thông Tin Bổ Sung')
    # Some noise information
    st.markdown("""
    <div style="background-color: #333; color: white; padding: 10px; border-radius: 5px; border: 1px solid white;">
        <p><strong>Chỉ số Kinh tế:</strong> USD/VND: 23,500</p>
        <p><strong>Tin tức:</strong> Giá vàng thế giới ổn định.</p>
        <p><strong>Dự báo:</strong> Có thể tăng nhẹ do lạm phát.</p>
    </div>
    """, unsafe_allow_html=True)