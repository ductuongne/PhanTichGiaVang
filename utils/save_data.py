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

    df_out = df[["TypeName", "BranchName", "Buy", "Sell", "date"]]
    df_out.to_csv(CSV_PATH_REALTIME_SJC, mode="w", header=True, index=False)
    df_out.to_csv(CSV_PATH_HISTORY_SJC, mode="a", header=False, index=False)
    # Xóa trùng lịch sử theo TypeName + BranchName + date
    deduplicate_history(CSV_PATH_HISTORY_SJC, ["TypeName", "BranchName", "date"])


def save_data_pnj():
    df = get_pnj_realtime()
    os.makedirs(os.path.dirname(CSV_PATH_REALTIME_PNJ), exist_ok=True)
    os.makedirs(os.path.dirname(CSV_PATH_HISTORY_PNJ), exist_ok=True)

    df_out = df[["TypeName", "BranchName", "Buy", "Sell", "date"]]
    df_out.to_csv(CSV_PATH_REALTIME_PNJ, mode="w", header=True, index=False)
    df_out.to_csv(CSV_PATH_HISTORY_PNJ, mode="a", header=False, index=False)
    # Xóa trùng lịch sử theo TypeName + BranchName + date
    deduplicate_history(CSV_PATH_HISTORY_PNJ, ["TypeName", "BranchName", "date"])


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


if __name__ == "__main__":
    save_data_sjc()
    save_data_pnj() 
