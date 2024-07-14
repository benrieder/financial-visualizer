# Importing required libraries
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys

# Specify the path to your local "All NASDAQ Stocks.txt" file
file_path = 'All NASDAQ Stocks.txt'

# Extracting NASDAQ stock symbols from the provided file
nasdaq_symbols = []
with open(file_path, 'r') as file:
    next(file)  # Skip the header row
    for line in file:
        symbol = line.split('|')[0]
        nasdaq_symbols.append(symbol)


class FinancialDataVisualizer:
    def __init__(self, ticker_symbol, start_date, end_date):
        self.symbol = ticker_symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.font = fm.FontProperties(family='Arial', size=12)

    def fetch_data(self):
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date, interval='3mo')

    def plot_closing_price(self):
        plt.style.use('dark_background')
        plt.plot(self.data['Close'], label='Closing Price')
        plt.xlabel('Year', fontproperties=self.font)
        plt.ylabel('Closing Price (USD)')
        plt.title(f'{self.symbol} Closing Price Chart for {self.start_date[:4]}-{datetime.today().year}')
        plt.xticks(rotation=35)
        plt.grid(True, linestyle='dotted')
        plt.legend()
        plt.savefig(f"figs/closingPrice_{self.symbol}_{self.start_date[:4]}_{self.end_date[:4]}.png")
        plt.show()

    def plot_volume(self):
        plt.style.use('seaborn-v0_8-white')
        plt.bar(self.data.index, self.data['Volume'], color='darkblue', width=45)
        plt.xlabel('Year')
        plt.xticks(rotation=35)
        plt.ylabel('Trade Volume')
        plt.title(f'{self.symbol} Trade Volume in {self.start_date[:4]}-{datetime.today().year}')
        plt.savefig(f"figs/tradeVolume_{self.symbol}_{self.start_date[:4]}_{self.end_date[:4]}.png")
        plt.show()

    def plot_price_distribution(self):
        plt.hist(self.data['Close'].pct_change(), bins=50, color='#FF7F0E')
        plt.xlabel('Daily Return')
        plt.ylabel('Frequency')
        plt.title(f'{self.symbol} Daily Returns Distribution in {self.start_date[:4]}-{datetime.today().year}')
        plt.savefig(f"figs/dailyReturnDist_{self.symbol}_{self.start_date[:4]}_{self.end_date[:4]}.png")
        plt.show()

    def plot_correlation_heatmap(self):
        corr = self.data[['Open', 'High', 'Low', 'Close']].corr()
        plt.imshow(corr, cmap='coolwarm', interpolation='nearest')
        plt.colorbar()
        plt.xticks(range(len(corr)), corr.columns, rotation=35)
        plt.yticks(range(len(corr)), corr.columns)
        plt.title(f'{self.symbol} Price Correlation in {self.start_date[:4]}-{datetime.today().year}')
        plt.savefig(f"figs/priceCorrelation_{self.symbol}_{self.start_date[:4]}_{self.end_date[:4]}.png")
        plt.show()

    def plot_moving_averages(self):
        self.data['MA50'] = self.data['Close'].rolling(window=50).mean()
        self.data['MA200'] = self.data['Close'].rolling(window=200).mean()
        plt.plot(self.data['Close'], label='Closing Price')
        plt.plot(self.data['MA50'], label='50-Day Moving Average')
        plt.plot(self.data['MA200'], label='200-Day Moving Average')
        plt.xlabel('Year', fontproperties=self.font)
        plt.ylabel('Price (USD)')
        plt.title(f'{self.symbol} Moving Averages')
        plt.legend()
        plt.xticks(rotation=35)
        plt.grid(True)
        plt.savefig(f"figs/movingAverages_{self.symbol}_{self.start_date[:4]}_{self.end_date[:4]}.png")
        plt.show()


def run_visualization(symbol, start_date, end_date):
    visualizer = FinancialDataVisualizer(symbol, start_date, end_date)
    visualizer.fetch_data()
    visualizer.plot_closing_price()
    visualizer.plot_volume()
    visualizer.plot_price_distribution()
    visualizer.plot_correlation_heatmap()
    visualizer.plot_moving_averages()


def play_game():
    # Start the happy_humblebee.py script
    subprocess.run([sys.executable, 'happy_humblebee.py'])


def on_submit():
    symbol = symbol_combo.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    if symbol and start_date and end_date:
        root.destroy()  # Close the GUI window
        run_visualization(symbol, start_date, end_date)
    else:
        messagebox.showwarning("Input Error", "Please enter valid values for all fields.")


# Setting up the GUI
root = tk.Tk()
root.title("Financial Data Visualizer")

# Adding a custom icon
root.iconphoto(False, tk.PhotoImage(file='icon.png'))

# Adding a title label
title_label = tk.Label(root, text="Welcome to the Financial Data Visualizer", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Adding instructions
instructions = (
    "This application allows you to visualize financial data for any NASDAQ stock.\n"
    " \n"
    "To use the financial data visualization tool:\n\n"
    "1. Select the stock symbol from the dropdown menu.\n"
    "2. Enter the start and end dates for the data you wish to analyze.\n"
    "3. Click 'Submit' to generate various financial charts including:\n\n"
    "   - Closing Price Chart\n"
    "   - Trade Volume Chart\n"
    "   - Daily Returns Distribution\n"
    "   - Price Correlation Heatmap\n"
    "   - Moving Averages\n\n\n"
    "Alternatively, you can click the 'Just play a game instead' button to play a fun game."
)
instructions_label = tk.Label(root, text=instructions, justify="left", wraplength=500)
instructions_label.pack(pady=30)

# Default dates
default_start_date = '2019-01-01'
default_end_date = datetime.today().strftime('%Y-%m-%d')

# Stock symbols list
tk.Label(root, text="Select the stock symbol:").pack(pady=5)
symbol_combo = ttk.Combobox(root, values=nasdaq_symbols)
symbol_combo.set(nasdaq_symbols[0])  # Set default value
symbol_combo.pack(pady=5)

tk.Label(root, text="Enter the start date (YYYY-MM-DD):").pack(pady=5)
start_date_entry = tk.Entry(root)
start_date_entry.insert(0, default_start_date)  # Set default start date
start_date_entry.pack(pady=5)

tk.Label(root, text="Enter the end date (YYYY-MM-DD):").pack(pady=5)
end_date_entry = tk.Entry(root)
end_date_entry.insert(0, default_end_date)  # Set default end date
end_date_entry.pack(pady=5)

submit_button = tk.Button(root, text="Submit", command=on_submit, bg="lightblue", font=("Helvetica", 12, "bold"))
submit_button.pack(pady=20)

game_button = tk.Button(root, text="Just play a game instead", command=play_game, bg="lightgreen",
                        font=("Helvetica", 12, "bold"))
game_button.pack(pady=10)

root.mainloop()
