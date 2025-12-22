import requests
import pandas as pd

PNJ_URL = "https://edge-api.pnj.io/ecom-frontend/v3/get-gold-price"


def _to_float(x):
    if x is None:
        return None
    return float(str(x).replace(".", "").replace(",", ""))


def get_pnj_realtime():
    """
    Lấy dữ liệu PNJ từ API PNJ, trả về DataFrame gồm:
    date, region, gold_type, buy_value, sell_value
    (chỉ giữ các bản ghi gold_type == "PNJ")
    """
    res = requests.get(PNJ_URL, timeout=15)
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
            date_parsed = pd.to_datetime(time_str, format="%d/%m/%Y %H:%M:%S", errors="coerce")

            rows.append(
                {
                    "date": date_parsed,
                    "BranchName": region,
                    "TypeName": "PNJ",
                    "BuyValue": buy,
                    "SellValue": sell,
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(get_pnj_realtime().head())

