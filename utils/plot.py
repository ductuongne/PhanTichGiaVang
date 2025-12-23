import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from matplotlib.ticker import MultipleLocator, FuncFormatter



def plot_gold_simple(df, company, data_type):
    fig, ax = plt.subplots(figsize=(12, 5))

    # ======================
    # HISTORY → LINE CHART
    # ======================
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

        # ===== HIGH / LOW =====
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

        # ===== TITLE =====
        ax.set_title(f"{company} Gold Price Trend")

        ax.set_xlabel("Date")
        ax.set_ylabel("Price (VND)")
        
        # ===== Y AXIS STEP: 60,000 =====
        ax.yaxis.set_major_locator(MultipleLocator(120000))

        # Format cho dễ đọc: 1,234,000
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda x, _: f"{int(x):,}")
        )


    # ======================
    # REALTIME → BAR CHART
    # ======================
    else:
        branches = df["BranchName"]
        x = np.arange(len(branches))
        width = 0.35

        ax.bar(x - width / 2, df["Buy"], width, label="Buy")
        ax.bar(x + width / 2, df["Sell"], width, label="Sell")

        ax.set_xticks(x)
        ax.set_xticklabels(branches, rotation=45, ha="right")

        ax.set_xlabel("Branch")
        ax.set_ylabel("Price (VND)")
        ax.set_title(f"{company} Gold Price (Realtime)")

    ax.legend()
    ax.grid(alpha=0.3)

    st.pyplot(fig)
