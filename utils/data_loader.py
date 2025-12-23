import pandas as pd

def load_gold_price():
    print("LOADING CSV...")
    df = pd.read_csv("data/gold_price.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

def load_sjc_data():
    df = pd.read_csv("data/sjc/gold_sjc_history.csv")
    df["date"] = pd.to_datetime(df["date"])
    # Take average of BuyValue and SellValue, group by date
    df["price"] = (df["Buy"] + df["Sell"]) / 2
    df = df.groupby("date")["price"].mean().reset_index()
    return df
