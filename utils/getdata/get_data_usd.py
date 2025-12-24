import requests
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CSV_PATH_USD = os.path.join(BASE_DIR, "data", "usd", "usd_vnd_rate.csv")

# API key của CurrencyAPI public luôn vì free
CURRENTCY_KEY = 'cur_live_oLAQPXeWILkKt1Mvd4ImEigkUraypXPrn5r2IV4g' 
def get_data_usd():
    url = "https://api.currencyapi.com/v3/latest"
    headers = {
        'apikey': CURRENTCY_KEY
    }
    params = {
        'base_currency': 'USD',
        'currencies': 'VND'
    }
    response = requests.request("GET", url, headers=headers, params=params)
    
    usd_vnd_rate = response.json()['data']['VND']['value']
    date = response.json()['meta']['last_updated_at']
    date = pd.to_datetime(date)
    # Chuyển từ UTC (+00:00) sang UTC+7 (timezone Việt Nam) và bỏ timezone info
    date = date.tz_convert('Asia/Ho_Chi_Minh').tz_localize(None)
    df = pd.DataFrame({
        'usd_vnd_rate': [usd_vnd_rate], 
        'date': [date]
        })

    return df
    
if __name__ == "__main__":
    df = get_data_usd()
    print(df)