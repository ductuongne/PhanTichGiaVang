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

st.header('Dự đoán Xu hướng Giá Vàng 7 Ngày Tới')

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
predictions = []
for i in range(1, 8):
    pred_date = last_date + timedelta(days=i)
    days_world = (pred_date - df_world['date'].min()).days
    days_vn = (pred_date - df_vn['date'].min()).days
    pred_world_vnd = model_world.predict([[days_world]])[0]
    pred_vn = model_vn.predict([[days_vn]])[0]
    # Chuyển đổi vàng thế giới sang USD/oz
    pred_world_usd = (pred_world_vnd / ounce_per_luong) / usd_vnd_rate
    predictions.append({
        'Ngày': pred_date.strftime('%Y-%m-%d'),
        'Dự báo giá vàng thế giới (USD/oz)': f"{pred_world_usd:,.2f}",
        'Dự báo giá vàng Việt Nam (VND/lượng)': f"{pred_vn:,.0f}"
    })

df_pred = pd.DataFrame(predictions)

# Layout
col1, col2 = st.columns([7, 3])

with col1:
    st.subheader('Bảng Dự Báo')
    st.table(df_pred)

with col2:
    st.subheader('Thông Tin Bổ Sung')
    # Some noise information
    st.markdown("""
    <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
        <p><strong>Chỉ số Kinh tế:</strong> USD/VND: 23,500</p>
        <p><strong>Tin tức:</strong> Giá vàng thế giới ổn định.</p>
        <p><strong>Dự báo:</strong> Có thể tăng nhẹ do lạm phát.</p>
    </div>
    """, unsafe_allow_html=True)