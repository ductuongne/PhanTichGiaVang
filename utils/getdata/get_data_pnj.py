import requests
import pandas as pd
from ._to_float import _to_float

PNJ_URL = "https://edge-api.pnj.io/ecom-frontend/v3/get-gold-price"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}


def get_pnj_realtime():
    """
    Lấy dữ liệu PNJ từ API PNJ, trả về DataFrame gồm:
    date, BranchName, TypeName, BuyValue, SellValue
    (chỉ giữ các bản ghi gold_type == "PNJ")
    """
    res = requests.get(PNJ_URL, timeout=15, headers=DEFAULT_HEADERS)
    res.raise_for_status()
    data = res.json()

    updated_text = data.get("updated_text")
    rows = []

    for loc in data.get("locations", []):
        region = loc.get("name")
        for item in loc.get("gold_type", []):
            # Chỉ lấy PNJ
            if item.get("name") != "PNJ":
                continue

            sell = _to_float(item.get("gia_ban"))
            buy = _to_float(item.get("gia_mua"))

            time_str = item.get("updated_at") or updated_text
            # Xử lý trường hợp updated_text có prefix "Giá vàng ngày:"
            if time_str and " " in time_str and ":" in time_str and "Giá vàng" in time_str:
                time_str = time_str.split(":", maxsplit=1)[-1].strip()

            date_parsed = pd.to_datetime(time_str, format="%d/%m/%Y %H:%M:%S", errors="coerce")

            rows.append(
                {
                    "date": date_parsed,
                    "BranchName": region,
                    "TypeName": "PNJ",
                    "Buy": buy,
                    "Sell": sell,
                }
            )

    return pd.DataFrame(rows)
