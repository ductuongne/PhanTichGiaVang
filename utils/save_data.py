import os
import pandas as pd
from utils.getdata.get_data_sjc import get_sjc_realtime
from utils.getdata.get_data_pnj import get_pnj_realtime

CSV_PATH_REALTIME_SJC = "../../data/sjc/gold_sjc_realtime.csv"
CSV_PATH_HISTORY_SJC = "../../data/sjc/gold_sjc_history.csv"
CSV_PATH_REALTIME_PNJ = "../../data/pnj/gold_pnj_realtime.csv"
CSV_PATH_HISTORY_PNJ = "../../data/pnj/gold_pnj_history.csv"

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

    df_out = df[["date", "region", "gold_type", "buy_value", "sell_value"]]
    df.to_csv(CSV_PATH_REALTIME_PNJ, mode="w", header=True, index=False)
    df_out.to_csv(CSV_PATH_HISTORY_PNJ, mode="a", header=False, index=False)

# if __name__ == "__main__":
#     save_data_sjc()