def calc_volatility_agg(df, price_col="Buy"):
    """
    Tính biến động theo thời gian (aggregate theo date)
    """
    df = (
        df.groupby("date")[price_col]
          .mean()
          .reset_index()
          .sort_values("date")
    )

    if len(df) < 2:
        return None

    current = df.iloc[-1][price_col]
    previous = df.iloc[-2][price_col]

    delta = current - previous
    delta_pct = delta / previous * 100

    high = df[price_col].max()
    low = df[price_col].min()

    return {
        "current": current,
        "delta": delta,
        "delta_pct": delta_pct,
        "high": high,
        "low": low,
    }
