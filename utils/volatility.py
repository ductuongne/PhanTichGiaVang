import streamlit as st
import pandas as pd

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

def render_company_card(
    col,
    name: str,
    csv_path: str,
    select_label: str,
    select_key: str,
    title_class: str,
):
    with col:
        container = st.container()

        with container:
            # Header
            st.markdown(
                f'<div class="company-card">',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="brand-title {title_class}">{name}</div>',
                unsafe_allow_html=True
            )

            # Data
            df_all = pd.read_csv(csv_path)
            df_all["date"] = pd.to_datetime(df_all["date"])

            branches = sorted(df_all["BranchName"].unique())
            branch = st.selectbox(select_label, branches, key=select_key)

            df = df_all[df_all["BranchName"] == branch]
            result = calc_volatility_agg(df)

            if result:
                st.metric(
                    "Giá hiện tại (Buy)",
                    f"{result['current']:,.0f} VND",
                    f"{result['delta']:,.0f} ({result['delta_pct']:.2f}%)"
                )

                st.markdown(
                    f"""
                    <div class="metric-extra">
                      <span>Cao nhất: <b>{result['high']:,.0f}</b></span>
                      <span>Thấp nhất: <b>{result['low']:,.0f}</b></span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.info("Không đủ dữ liệu")

            st.markdown("</div>", unsafe_allow_html=True)
