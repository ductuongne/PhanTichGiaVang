# data_loader.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Hàm đọc dữ liệu từ file CSV Chuyển đổi cột date sang định dạng datetime và sắp xếp
def load_sjc_data(csv_path="data/sjc/gold_sjc_history.csv"):
    df = pd.read_csv(csv_path)
    
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df

# Hàm chính để lấy dữ liệu dự đoán giá vàng
def train_and_predict_by_region(df_region, display_years=1):
    """
    df_region: dữ liệu đã lọc theo BranchName
    """

    df = df_region.copy()
    df["time"] = np.arange(len(df))

    # Train model
    model = LinearRegression()
    model.fit(df[["time"]], df["Sell"])

    df["predicted"] = model.predict(df[["time"]])

    # Cắt dữ liệu hiển thị
    cutoff_date = df["date"].max() - pd.DateOffset(years=display_years)
    df_display = df[df["date"] >= cutoff_date].copy()

    # Dự đoán ngày tiếp theo
    next_time = df["time"].iloc[-1] + 1
    predicted_next = model.predict(np.array([[next_time]]))[0]

    return df_display, predicted_next
