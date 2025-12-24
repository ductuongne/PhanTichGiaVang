import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from matplotlib.ticker import MultipleLocator, FuncFormatter



def plot_gold_simple(df, company, data_type):
    fig, ax = plt.subplots(figsize=(12, 5))

    if data_type == "History":
        # ===== AREA (Buy) =====
        ax.fill_between(
            df["date"],
            df["Buy"],
            alpha=0.25,
            label="Buy"
        )

        # ===== LINE (Sell) =====
        ax.plot(
            df["date"],
            df["Sell"],
            linewidth=2.5,
            label="Sell"
        )

        max_price = df["Sell"].max()
        min_price = df["Sell"].min()

        max_row = df.loc[df["Sell"].idxmax()]
        min_row = df.loc[df["Sell"].idxmin()]

        ax.scatter(max_row["date"], max_price, zorder=5)
        ax.scatter(min_row["date"], min_price, zorder=5)

        ax.annotate(
            f"High: {int(max_price):,}",
            (max_row["date"], max_price),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center"
        )

        ax.annotate(
            f"Low: {int(min_price):,}",
            (min_row["date"], min_price),
            xytext=(0, -12),
            textcoords="offset points",
            ha="center"
        )



        ax.set_xlabel("Date")
        ax.set_ylabel("Price (VND)")
        
        ax.yaxis.set_major_locator(MultipleLocator(120000))


        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda x, _: f"{int(x):,}")
        )




    ax.legend()
    ax.grid(alpha=0.3)

    st.pyplot(fig)
