import os
import pandas as pd
from getdata.get_data_sjc import get_sjc_realtime
from getdata.get_data_pnj import get_pnj_realtime

# Đặt BASE_DIR là thư mục gốc project (utils/save_data.py -> utils -> ..)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CSV_PATH_REALTIME_SJC = os.path.join(BASE_DIR, "data", "sjc", "gold_sjc_realtime.csv")
CSV_PATH_HISTORY_SJC = os.path.join(BASE_DIR, "data", "sjc", "gold_sjc_history.csv")
CSV_PATH_REALTIME_PNJ = os.path.join(BASE_DIR, "data", "pnj", "gold_pnj_realtime.csv")
CSV_PATH_HISTORY_PNJ = os.path.join(BASE_DIR, "data", "pnj", "gold_pnj_history.csv")


def save_data_sjc():
    df = get_sjc_realtime()
    os.makedirs(os.path.dirname(CSV_PATH_REALTIME_SJC), exist_ok=True)
    os.makedirs(os.path.dirname(CSV_PATH_HISTORY_SJC), exist_ok=True)

    df_out = df[["TypeName", "BranchName", "BuyValue", "SellValue", "date"]]
    df.to_csv(CSV_PATH_REALTIME_SJC, mode="w", header=True, index=False)
    df_out.to_csv(CSV_PATH_HISTORY_SJC, mode="a", header=False, index=False)


def save_data_pnj():
    df = get_pnj_realtime()
    os.makedirs(os.path.dirname(CSV_PATH_REALTIME_PNJ), exist_ok=True)
    os.makedirs(os.path.dirname(CSV_PATH_HISTORY_PNJ), exist_ok=True)

    df_out = df[["TypeName", "BranchName", "BuyValue", "SellValue", "date"]]
    df_out.to_csv(CSV_PATH_REALTIME_PNJ, mode="w", header=True, index=False)
    df_out.to_csv(CSV_PATH_HISTORY_PNJ, mode="a", header=False, index=False)


if __name__ == "__main__":
    save_data_sjc()
    save_data_pnj()