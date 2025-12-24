import os
import pandas as pd
from get_data_gold import get_data_gold
from get_data_usd import get_data_usd

# Đặt BASE_DIR là thư mục gốc project (utils/getdata/save_data.py -> utils/getdata -> utils -> ..)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

CSV_PATH_REALTIME_SJC = os.path.join(BASE_DIR, "data", "sjc", "gold_sjc_realtime.csv")
CSV_PATH_HISTORY_SJC = os.path.join(BASE_DIR, "data", "sjc", "gold_sjc_history.csv")
CSV_PATH_REALTIME_PNJ = os.path.join(BASE_DIR, "data", "pnj", "gold_pnj_realtime.csv")
CSV_PATH_HISTORY_PNJ = os.path.join(BASE_DIR, "data", "pnj", "gold_pnj_history.csv")
CSV_PATH_USD_RATE = os.path.join(BASE_DIR, "data", "usd", "usd_vnd_rate.csv")

def save_data_gold(data, PATH_REALTIME, PATH_HISTORY):
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(os.path.dirname(PATH_REALTIME), exist_ok=True)
    os.makedirs(os.path.dirname(PATH_HISTORY), exist_ok=True)
    
    data.to_csv(PATH_REALTIME, mode="w", header=True, index=False)
    data.to_csv(PATH_HISTORY, mode="a", header=False, index=False)
    deduplicate_history(PATH_HISTORY, ["TypeName", "BranchName", "date"])


def deduplicate_history(csv_path: str, subset_cols: list[str]) -> None:
    """
    Xóa các dòng trùng trong file lịch sử theo các cột trong subset_cols.
    Giữ lại dòng xuất hiện cuối cùng (mới nhất).
    """
    if not os.path.exists(csv_path):
        return

    df = pd.read_csv(csv_path, header=None)
    # Gán tên cột tạm để dễ xử lý
    n_cols = df.shape[1]
    df.columns = [f"col_{i}" for i in range(n_cols)]

    # Map subset_cols sang index tương ứng
    col_index = {name: idx for idx, name in enumerate(["TypeName", "BranchName", "Buy", "Sell", "date"])}
    subset_idx = [col_index[c] for c in subset_cols if c in col_index]

    if not subset_idx:
        return

    # drop_duplicates: keep="last" để giữ bản ghi mới nhất
    df = df.drop_duplicates(subset=[f"col_{i}" for i in subset_idx], keep="last")

    # Ghi đè lại file, không header, không index
    df.to_csv(csv_path, header=False, index=False)

def save_data_usd(data, PATH_USD_RATE):
    os.makedirs(os.path.dirname(PATH_USD_RATE), exist_ok=True)
    data.to_csv(PATH_USD_RATE, mode='w', header=True, index=False)

def save_data():
    df_pnj = get_data_gold("PNJ")
    save_data_gold(df_pnj, CSV_PATH_REALTIME_PNJ, CSV_PATH_HISTORY_PNJ)
    df_sjc = get_data_gold("SJC")
    save_data_gold(df_sjc, CSV_PATH_REALTIME_SJC, CSV_PATH_HISTORY_SJC)
    df_usd = get_data_usd()
    save_data_usd(df_usd, CSV_PATH_USD_RATE)
if __name__ == "__main__":
    save_data()
