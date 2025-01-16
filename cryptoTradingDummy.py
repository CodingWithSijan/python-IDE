import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import random
import threading
import time


class CryptoTradingApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Crypto Trading App")
        self.window.geometry("1200x800")
        
        self.symbol = tk.StringVar(value="BTCUSDT")
        self.order_type = tk.StringVar(value="MARKET")
        self.amount = tk.DoubleVar()
        self.price = tk.DoubleVar()
        self.data_frame = None

        self.create_ui()
        self.load_dummy_data()

    def create_ui(self):
        """Create the UI components."""
        # Dropdown to select trading pair
        ttk.Label(self.window, text="Select Trading Pair:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.symbol_entry = ttk.Entry(self.window, textvariable=self.symbol, width=10)
        self.symbol_entry.grid(row=0, column=1, padx=10, pady=10)

        # Order Type Dropdown
        ttk.Label(self.window, text="Order Type:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        order_options = ["MARKET", "LIMIT"]
        ttk.OptionMenu(self.window, self.order_type, *order_options).grid(row=1, column=1, padx=10, pady=10)

        # Amount Entry
        ttk.Label(self.window, text="Amount:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(self.window, textvariable=self.amount).grid(row=2, column=1, padx=10, pady=10)

        # Price Entry (for LIMIT orders)
        ttk.Label(self.window, text="Price (Limit Order):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(self.window, textvariable=self.price).grid(row=3, column=1, padx=10, pady=10)

        # Submit Order Button
        ttk.Button(self.window, text="Place Order", command=self.place_order).grid(row=4, column=0, columnspan=2, pady=20)

        # Candlestick Chart
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.chart = FigureCanvasTkAgg(self.figure, self.window)
        self.chart.get_tk_widget().grid(row=0, column=2, rowspan=10, padx=20, pady=20)

        # Refresh Data Button
        ttk.Button(self.window, text="Refresh Chart", command=self.refresh_chart).grid(row=5, column=0, columnspan=2, pady=10)

        # Output Console
        ttk.Label(self.window, text="Console:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.console = tk.Text(self.window, height=10, width=50, bg="#1e1e1e", fg="white")
        self.console.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def load_dummy_data(self):
        """Generate dummy candlestick data."""
        timestamps = pd.date_range(start="2022-01-01", periods=100, freq="15T")
        opens = [random.uniform(40000, 50000) for _ in range(100)]
        closes = [open_ + random.uniform(-1000, 1000) for open_ in opens]
        highs = [max(open_, close_) + random.uniform(0, 500) for open_, close_ in zip(opens, closes)]
        lows = [min(open_, close_) - random.uniform(0, 500) for open_, close_ in zip(opens, closes)]

        self.data_frame = pd.DataFrame({
            "timestamp": timestamps,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
        })

        self.refresh_chart()

    def refresh_chart(self):
        """Refresh the candlestick chart with dummy data."""
        if self.data_frame is None:
            self.console.insert(tk.END, "No data to display.\n")
            return

        self.plot_chart(self.data_frame)

    def plot_chart(self, df):
        """Plot the candlestick chart."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(df["timestamp"], df["close"], label="Close Price", color="blue")
        ax.fill_between(df["timestamp"], df["low"], df["high"], alpha=0.2, label="High-Low Range")
        ax.set_title("Candlestick Chart")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price (USDT)")
        ax.legend()
        self.chart.draw()

    def place_order(self):
        """Simulate placing a crypto trade order."""
        threading.Thread(target=self.execute_order, daemon=True).start()

    def execute_order(self):
        """Simulate order execution."""
        try:
            symbol = self.symbol.get().upper()
            order_type = self.order_type.get()
            amount = self.amount.get()
            price = self.price.get()

            if order_type == "MARKET":
                self.console.insert(tk.END, f"Market Order: Bought {amount} {symbol} at market price.\n")
            elif order_type == "LIMIT":
                self.console.insert(tk.END, f"Limit Order: Placed an order to buy {amount} {symbol} at {price}.\n")
            else:
                messagebox.showerror("Error", "Unsupported order type.")
        except Exception as e:
            self.console.insert(tk.END, f"Error: {e}\n")

    def run(self):
        """Run the application."""
        self.window.mainloop()


if __name__ == "__main__":
    CryptoTradingApp().run()
