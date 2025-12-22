import os
import requests
import pandas as pd

SJC_REALTIME_URL = "https://sjc.com.vn/GoldPrice/Services/PriceService.ashx"
CSV_PATH_REALTIME = "../../data/sjc/gold_sjc_realtime.csv"
CSV_PATH_HISTORY = "../../data/sjc/gold_sjc_history.csv"


def get_sjc_realtime():

    response = requests.get(SJC_REALTIME_URL, timeout=15)

    data = response.json()

    # DataFrame từ trường "data"
    df = pd.DataFrame(data["data"])

    # Chỉ lấy vàng miếng SJC 1L, 10L, 1KG
    scj = df["TypeName"] == "Vàng SJC 1L, 10L, 1KG"
    df = df[scj]

    # Chuyển latestDate thành cột date (kiểu datetime)
    date_str = data.get("latestDate")
    date_parsed = pd.to_datetime(date_str, format="%H:%M %d/%m/%Y", errors="coerce")
    df["date"] = date_parsed

    # Chỉ lấy các cột yêu cầu
    df_selected = df[["date", "TypeName", "BranchName", "BuyValue", "SellValue"]].reset_index(drop=True)

    # Lưu (append) vào CSV lịch sử
    df_out = df_selected[["TypeName", "BranchName", "BuyValue", "SellValue", "date"]]

    # Đảm bảo thư mục 'data' tồn tại trước khi ghi file
    os.makedirs(os.path.dirname(CSV_PATH_REALTIME), exist_ok=True)
    os.makedirs(os.path.dirname(CSV_PATH_HISTORY), exist_ok=True)

    df_out.to_csv(CSV_PATH_REALTIME, mode="w", header=True, index=False)
    df_out.to_csv(CSV_PATH_HISTORY, mode="a", header=False, index=False)

if __name__ == "__main__":
    get_sjc_realtime()