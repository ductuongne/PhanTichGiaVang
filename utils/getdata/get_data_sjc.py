import os
import requests
import pandas as pd

SJC_REALTIME_URL = "https://sjc.com.vn/GoldPrice/Services/PriceService.ashx"



def get_sjc_realtime():

    response = requests.get(SJC_REALTIME_URL, timeout=20)
    response.raise_for_status()
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

    return df_selected
