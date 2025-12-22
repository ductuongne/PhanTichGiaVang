def _to_float(x):
    if x is None:
        return None
    return float(str(x).replace(".", "").replace(",", ""))