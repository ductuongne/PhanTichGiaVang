import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator, FuncFormatter


FIG_BG = "none"  
AX_BG = "none"


GRID_COLOR = "rgba(156, 163, 175, 0.2)"
TEXT_MAIN = "#f9fafb"
TEXT_SUB = "#d1d5db"
TEXT_MUTED = "#9ca3af"

BUY_COLOR = "#60a5fa"  
SELL_COLOR = "#fbbf24" 

def _apply_dark_style(ax, title, xlabel, ylabel):
    ax.set_facecolor(AX_BG)

    ax.set_title(title, color=TEXT_MAIN)
    ax.set_xlabel(xlabel, color=TEXT_SUB)
    ax.set_ylabel(ylabel, color=TEXT_SUB)

    ax.tick_params(colors=TEXT_MUTED)

    for spine in ax.spines.values():
        spine.set_edgecolor(TEXT_MUTED)
        spine.set_alpha(0.3)

    ax.grid(alpha=0.1, color=TEXT_MUTED, linestyle='--')

    ax.legend(
        facecolor="none",
        edgecolor="none",
        labelcolor=TEXT_SUB
    )

def plot_gold_simple(df, company):
    fig, ax = plt.subplots(
        figsize=(12, 5),
        facecolor=FIG_BG
    )

    ax.fill_between(
        df["date"],
        df["Buy"],
        alpha=0.35,
        color=BUY_COLOR,
        label="Buy"
    )

    ax.plot(
        df["date"],
        df["Sell"],
        color=SELL_COLOR,
        linewidth=2.5,
        label="Sell"
    )

    if not df.empty:
        max_idx = df["Sell"].idxmax()
        min_idx = df["Sell"].idxmin()

        if pd.notna(max_idx) and pd.notna(min_idx):
            max_row = df.loc[max_idx]
            min_row = df.loc[min_idx]

            ax.scatter(max_row["date"], max_row["Sell"], color=SELL_COLOR, zorder=5, s=60, edgecolors='white', linewidths=1.5)
            ax.scatter(min_row["date"], min_row["Sell"], color=BUY_COLOR, zorder=5, s=60, edgecolors='white', linewidths=1.5)

            ax.annotate(
                f"High: {int(max_row['Sell']):,}",
                (max_row["date"], max_row["Sell"]),
                xytext=(0, 10),
                textcoords="offset points",
                ha="center",
                color=TEXT_MAIN,
                fontweight='bold',
                fontsize=9
            )

            ax.annotate(
                f"Low: {int(min_row['Sell']):,}",
                (min_row["date"], min_row["Sell"]),
                xytext=(0, -15),
                textcoords="offset points",
                ha="center",
                color=TEXT_MAIN,
                fontweight='bold',
                fontsize=9
            )

    ax.yaxis.set_major_locator(MultipleLocator(120_000))
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, _: f"{int(x):,}")
    )

    _apply_dark_style(
        ax,
        title=f"Lịch sử giá vàng {company}",
        xlabel="Thời gian",
        ylabel="Giá (VND)"
    )

    st.pyplot(fig, use_container_width=True, transparent=True)


def plot_realtime_bar(df, company):
    branches = df["BranchName"].tolist()
    buy = df["Buy"].values
    sell = df["Sell"].values

    x = np.arange(len(branches))
    width = 0.36

    fig, ax = plt.subplots(
        figsize=(12, 5),
        facecolor=FIG_BG
    )

    ax.bar(
        x - width / 2,
        buy,
        width,
        color=BUY_COLOR,
        label="Buy",
        alpha=0.9
    )

    ax.bar(
        x + width / 2,
        sell,
        width,
        color=SELL_COLOR,
        label="Sell",
        alpha=0.9
    )

    ax.set_xticks(x)
    ax.set_xticklabels(branches, rotation=30, ha="right", color=TEXT_SUB)

    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, _: f"{int(x):,}")
    )

    _apply_dark_style(
        ax,
        title=f"Giá vàng trực tiếp tại các chi nhánh – {company}",
        xlabel="Chi nhánh",
        ylabel="Giá (VND)"
    )

    st.pyplot(fig, use_container_width=True, transparent=True)