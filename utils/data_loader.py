# data_loader.py
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st # Để dùng cache nếu cần

# Dùng cache để không phải tải lại dữ liệu mỗi lần reload trang
@st.cache_data
def get_gold_predictions():
    # 1. LẤY DỮ LIỆU
    df = yf.download("GC=F", period="3y", interval="1d")
    
    # Fix lỗi MultiIndex của yfinance phiên bản mới (nếu có)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    df = df.dropna()
    df["time"] = np.arange(len(df))

    # 2. TRAIN MODEL
    model = LinearRegression()
    model.fit(df[["time"]], df["Close"])
    df["predicted"] = model.predict(df[["time"]])

    # 3. CẮT 1 NĂM GẦN ĐÂY
    last_year = df[df.index >= (df.index[-1] - pd.DateOffset(years=1))].copy()

    # 4. TẠO BIỂU ĐỒ GIÁ & DỰ ĐOÁN
    sns.set_theme(style="darkgrid")
    
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(last_year.index, last_year["Close"], color="red", label="Giá vàng thực tế")
    ax1.plot(last_year.index, last_year["predicted"], color="blue", linestyle="--", label="Giá vàng dự đoán")
    ax1.set_title("Giá vàng thực tế và dự đoán (1 năm gần đây)")
    ax1.set_xlabel("Mốc thời gian (tháng - năm)")
    ax1.set_ylabel("Giá vàng ($)")
    ax1.legend()

    # 5. TÍNH LỢI NHUẬN TÍCH LŨY
    last_year["predicted_next"] = last_year["predicted"].shift(-1)
    last_year["signal"] = (last_year["predicted_next"] > last_year["Close"]).astype(int)
    last_year["daily_profit"] = (last_year["Close"].shift(-1) - last_year["Close"]) * last_year["signal"]
    last_year["cumulative_profit"] = last_year["daily_profit"].cumsum()

    # TẠO BIỂU ĐỒ LỢI NHUẬN (Lưu vào fig2)
    fig2, ax2 = plt.subplots(figsize=(12, 4))
    ax2.plot(last_year.index, last_year["cumulative_profit"], label="Lợi nhuận tích lũy (mô phỏng)", color="green")
    ax2.set_title("Lợi nhuận tích lũy (Chiến lược theo Linear Regression)")
    ax2.set_xlabel("Mốc thời gian (tháng - năm)")
    ax2.set_ylabel("Lợi nhuận ($)")
    ax2.legend()

    # 6. TÍNH TOÁN CÁC CHỈ SỐ UI
    today_price = df["Close"].iloc[-1]
    next_time = df["time"].iloc[-1] + 1
    # Reshape input để tránh warning của sklearn
    predicted_tomorrow = model.predict(np.array([[next_time]]))[0] 
    
    trend = "Tăng" if predicted_tomorrow > today_price else "Giảm"
    
    # Xử lý giá trị cumulative_profit cuối cùng
    cum_profit_final = last_year["cumulative_profit"].dropna().iloc[-1] if not last_year["cumulative_profit"].dropna().empty else 0

    ui_data = {
        "today_price": float(today_price),
        "predicted_tomorrow": float(predicted_tomorrow),
        "trend": trend,
        "cumulative_profit": float(cum_profit_final)
    }

    return fig1, fig2, ui_data
