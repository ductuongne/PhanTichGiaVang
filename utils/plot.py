import matplotlib.pyplot as plt

def plot_gold_price(df):
    plt.figure()
    plt.plot(df["date"], df["price"])
    plt.xlabel("Date")
    plt.ylabel("Gold Price (VND)")
    plt.title("Gold Price Over Time")
    plt.show()
