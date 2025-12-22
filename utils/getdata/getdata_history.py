import requests

# hàm này sử dụng thư viện requests để lấy dữ liệu giá vàng từ api của simplize (chỉ lấy 1 lần)
def get_data():
    url = "https://api2.simplize.vn/api/historical/prices/chart"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "authority": "api2.simplize.vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
    }
    params = {
        "ticker": "SJC:M1C:SELL",
        "period": "1y"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.text

def options_params():
    pass