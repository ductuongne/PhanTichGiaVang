import pandas as pd

def load_gold_price():
    print("LOADING CSV...")
    df = pd.read_csv("data/gold_price.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df
