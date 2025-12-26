import streamlit as st
import pandas as pd
import altair as alt


import numpy as np

def calc_volatility_agg(df, price_col="Buy", window=7):
    df = (
        df.groupby("date")[price_col]
          .mean()
          .reset_index()
          .sort_values("date")
    )

    if len(df) < window + 1:
        return None

    df["return"] = df[price_col].pct_change()
    df["volatility"] = df["return"].rolling(window).std()

    current = df.iloc[-1][price_col]
    previous = df.iloc[-2][price_col]
    delta = current - previous
    delta_pct = delta / previous * 100

    vol = df.iloc[-1]["volatility"]

    return {
        "current": current,
        "delta": delta,
        "delta_pct": delta_pct,
        "volatility": vol,
        "vol_level": (
            "High" if vol > df["volatility"].mean() * 1.5
            else "Low"
        )
    }


def prepare_timeseries(df, branch, freq="D"):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["BranchName"] == branch]

    df = (
        df.set_index("date")
          .resample(freq)[["Buy", "Sell"]]
          .mean()
          .reset_index()
          .sort_values("date")
    )
    return df


def render_company_card(
    col,
    name: str,
    csv_path: str,
    select_label: str,
    select_key: str,
    title_class: str,
):
    key_prefix = f"{name.lower()}_{select_key}"

    with col:
        with st.container():
            st.markdown(
                f'<div class="brand-title {title_class}">{name}</div>',
                unsafe_allow_html=True
            )

            df_all = pd.read_csv(csv_path)
            df_all["date"] = pd.to_datetime(df_all["date"])

            branches = sorted(df_all["BranchName"].dropna().unique())
            branch = st.selectbox(
                select_label,
                branches,
                key=f"{key_prefix}_branch"
            )

            freq = st.radio(
                "Độ chi tiết",
                ["Theo ngày", "Theo tháng"],
                horizontal=True,
                key=f"{key_prefix}_freq"
            )
            freq_map = {"Theo ngày": "D", "Theo tháng": "M"}

            df_branch = df_all[df_all["BranchName"] == branch]

            result = calc_volatility_agg(df_branch)
            if result:
                st.metric(
                    "Giá hiện tại (Buy)",
                    f"{result['current']:,.0f} VND",
                    f"{result['delta']:,.0f} ({result['delta_pct']:.2f}%)"
                )
            else:
                st.info("Không đủ dữ liệu")

            df_chart = prepare_timeseries(
                df_all,
                branch,
                freq=freq_map[freq]
            )

            df_long = df_chart.melt(
                id_vars="date",
                value_vars=["Buy", "Sell"],
                var_name="Type",
                value_name="Price"
            )

            chart = (
                alt.Chart(df_long)
                .mark_line()
                .encode(
                    x=alt.X("date:T", title="Thời gian"),
                    y=alt.Y("Price:Q", title="Giá (VND)"),
                    color=alt.Color(
                        "Type:N",
                        scale=alt.Scale(
                            domain=["Buy", "Sell"],
                            range=["green", "red"]
                        ),
                        legend=alt.Legend(title="Loại")
                    ),
                    tooltip=["date:T", "Type:N", "Price:Q"]
                )
                .properties(height=260)
            )

            st.altair_chart(chart, use_container_width=True)
