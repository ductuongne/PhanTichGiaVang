import pandas as pd

def load_pnj_history():
    df = pd.read_csv("data/pnj/gold_pnj_history.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df
