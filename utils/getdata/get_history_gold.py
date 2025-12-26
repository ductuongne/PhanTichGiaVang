import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# Đặt BASE_DIR là thư mục gốc project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

API_URL = "https://edge-api.pnj.io/ecom-frontend/v1/get-gold-price-history"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}

CSV_PATH_HISTORY_SJC = os.path.join(BASE_DIR, "data", "sjc", "gold_sjc_history.csv")
CSV_PATH_HISTORY_PNJ = os.path.join(BASE_DIR, "data", "pnj", "gold_pnj_history.csv")


def _to_float(x):
    """Chuyển đổi giá trị sang float, xử lý format số Việt Nam."""
    if x is None:
        return None
    return float(str(x).replace(".", "").replace(",", ""))


def _parse_history_data(data: dict, gold_type: str) -> pd.DataFrame:
    """
    Parse dữ liệu từ API history response.
    
    Args:
        data: Response JSON từ API
        gold_type: "PNJ" hoặc "SJC"
    
    Returns:
        DataFrame chứa dữ liệu đã parse
    """
    rows = []
    
    for loc in data.get("locations", []):
        region = loc.get("name")
        
        # Bỏ qua "Giá vàng nữ trang" vì chỉ lấy PNJ và SJC chính
        if region == "Giá vàng nữ trang":
            continue
            
        for item in loc.get("gold_type", []):
            if item.get("name") != gold_type:
                continue
            
            # Lấy tất cả các bản ghi trong data array
            for record in item.get("data", []):
                sell = _to_float(record.get("gia_ban"))
                buy = _to_float(record.get("gia_mua"))
                time_str = record.get("updated_at")
                
                # Parse datetime từ format "04/01/2024 08:19:25"
                date_parsed = pd.to_datetime(time_str, format="%d/%m/%Y %H:%M:%S", errors="coerce")
                
                rows.append({
                    "TypeName": gold_type,
                    "BranchName": region,
                    "Buy": buy,
                    "Sell": sell,
                    "date": date_parsed,
                })
    
    return pd.DataFrame(rows)


def _get_date_range(years: int = 3) -> tuple[list[str], datetime, datetime]:
    """
    Tạo danh sách ngày trong khoảng thời gian (từ hôm nay trở về trước).
    
    Args:
        years: Số năm cần lấy (mặc định 3 năm)
    
    Returns:
        Tuple (danh sách ngày dạng YYYYMMDD, start_date, end_date)
    """
    dates = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime("%Y%m%d"))
        current_date += timedelta(days=1)
    
    return dates, start_date, end_date


def get_history_for_date(date_str: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Lấy lịch sử giá vàng cho một ngày cụ thể.
    
    Args:
        date_str: Ngày dạng YYYYMMDD
    
    Returns:
        Tuple (df_pnj, df_sjc)
    """
    params = {"date": date_str}
    
    try:
        res = requests.get(API_URL, params=params, headers=DEFAULT_HEADERS, timeout=15)
        res.raise_for_status()
        data = res.json()
        
        df_pnj = _parse_history_data(data, "PNJ")
        df_sjc = _parse_history_data(data, "SJC")
        
        return df_pnj, df_sjc
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu ngày {date_str}: {e}")
        return pd.DataFrame(), pd.DataFrame()


def save_history_data(df: pd.DataFrame, csv_path: str) -> None:
    """
    Lưu dữ liệu vào file history (append mode).
    
    Args:
        df: DataFrame cần lưu
        csv_path: Đường dẫn file CSV
    """
    if df.empty:
        return
    
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    # Chọn các cột cần thiết
    df_out = df[["TypeName", "BranchName", "Buy", "Sell", "date"]].copy()
    
    # Append vào file history (không có header)
    df_out.to_csv(csv_path, mode="a", header=False, index=False)


def get_history_batch(years: int = 3, delay: float = 0.5) -> None:
    """
    Lấy lịch sử giá vàng cho nhiều ngày (3 năm gần nhất).
    
    Args:
        years: Số năm cần lấy (mặc định 3)
        delay: Thời gian delay giữa các request (giây) để tránh rate limit
    """
    dates, start_date, end_date = _get_date_range(years)
    total_dates = len(dates)
    
    print("=" * 60)
    print(f"PHẠM VI LẤY DỮ LIỆU:")
    print(f"  Từ ngày: {start_date.strftime('%d/%m/%Y')}")
    print(f"  Đến ngày: {end_date.strftime('%d/%m/%Y')}")
    print(f"  Tổng số ngày: {total_dates} ngày")
    print("=" * 60)
    print(f"\nBắt đầu lấy lịch sử...\n")
    
    for idx, date_str in enumerate(dates, 1):
        print(f"[{idx}/{total_dates}] Đang xử lý ngày {date_str}...", end=" ")
        
        df_pnj, df_sjc = get_history_for_date(date_str)
        
        if not df_pnj.empty:
            save_history_data(df_pnj, CSV_PATH_HISTORY_PNJ)
            print(f"PNJ: {len(df_pnj)} records", end=" ")
        
        if not df_sjc.empty:
            save_history_data(df_sjc, CSV_PATH_HISTORY_SJC)
            print(f"SJC: {len(df_sjc)} records", end=" ")
        
        print("✓")
        
        # Delay để tránh rate limit
        if idx < total_dates:
            time.sleep(delay)
    
    print(f"\nHoàn thành! Đã lấy dữ liệu cho {total_dates} ngày.")
    
    # Deduplicate sau khi hoàn thành
    from save_data import deduplicate_history
    print("Đang xóa dữ liệu trùng lặp...")
    deduplicate_history(CSV_PATH_HISTORY_PNJ, ["TypeName", "BranchName", "date"])
    deduplicate_history(CSV_PATH_HISTORY_SJC, ["TypeName", "BranchName", "date"])
    print("Hoàn thành!")


if __name__ == "__main__":
    get_history_batch(years=3, delay=0.5)

