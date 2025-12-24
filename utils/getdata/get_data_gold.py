import requests
import pandas as pd

API_URL = "https://edge-api.pnj.io/ecom-frontend/v3/get-gold-price"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}

def _to_float(x):
    if x is None:
        return None
    return float(str(x).replace(".", "").replace(",", ""))

def get_data_gold(type_gold):
    res = requests.get(API_URL, timeout=15, headers=DEFAULT_HEADERS)
    res.raise_for_status()
    data = res.json()
    updated_text = data.get("updated_text")
    rows = []

    for loc in data.get("locations", []):
        region = loc.get("name")
        for item in loc.get("gold_type", []):
            # Chỉ lấy PNJ
            if item.get("name") != type_gold:
                continue

            sell = _to_float(item.get("gia_ban"))
            buy = _to_float(item.get("gia_mua"))

            time_str = item.get("updated_at") or updated_text
            if time_str and " " in time_str and ":" in time_str and "Giá vàng" in time_str:
                time_str = time_str.split(":", maxsplit=1)[-1].strip()

            date_parsed = pd.to_datetime(time_str, format="%d/%m/%Y %H:%M:%S", errors="coerce")

            rows.append(
                {
                    "TypeName": type_gold,
                    "BranchName": region,
                    "Buy": buy,
                    "Sell": sell,
                    "date": date_parsed, 
                }
            )

    return pd.DataFrame(rows)

