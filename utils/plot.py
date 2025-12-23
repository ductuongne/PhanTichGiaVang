import matplotlib.pyplot as plt
import streamlit as st

def plot_gold_pnj(df, branch):
    df = df[df["BranchName"] == branch]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date"], df["Buy"], label="Buy")
    ax.plot(df["date"], df["Sell"], label="Sell")

    ax.set_xlabel("Date")
    ax.set_ylabel("Price (VND)")
    ax.set_title(f"PNJ Gold Price - {branch}")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
