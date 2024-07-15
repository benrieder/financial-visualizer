import yfinance as yf
import pandas as pd
from datetime import datetime
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
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

indices = {
    "S&P 500": "^GSPC",
    "NASDAQ Composite": "^IXIC"
}


class FinancialDataVisualizer:
    def __init__(self, ticker_symbol, start_date, end_date, index_symbol):
        self.symbol = ticker_symbol
        self.start_date = start_date
        self.end_date = end_date
        self.index_symbol = index_symbol
        self.data = None
        self.index_data = None

    def fetch_data(self):
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date, interval='3mo')
        self.index_data = yf.download(self.index_symbol, start=self.start_date, end=self.end_date, interval='3mo')

    def plot_closing_price(self):
        st.line_chart(self.data['Close'], use_container_width=True)

    def plot_volume(self):
        st.bar_chart(self.data['Volume'], use_container_width=True)

    def plot_price_distribution(self):
        fig, ax = plt.subplots()
        sns.histplot(self.data['Close'].pct_change().dropna(), bins=50, ax=ax)
        ax.set_xlabel('Daily Return')
        ax.set_ylabel('Frequency')
        ax.set_title(f'{self.symbol} Daily Returns Distribution in {self.start_date[:4]}-{datetime.today().year}')
        st.pyplot(fig)

    def plot_correlation_heatmap(self):
        combined_data = pd.DataFrame({
            self.symbol: self.data['Close'],
            self.index_symbol: self.index_data['Close']
        }).dropna()
        corr = combined_data.corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
        ax.set_title(f'{self.symbol} vs {self.index_symbol} Correlation in {self.start_date[:4]}-{datetime.today().year}')
        st.pyplot(fig)

    def plot_moving_averages(self):
        self.data['MA50'] = self.data['Close'].rolling(window=50).mean()
        self.data['MA200'] = self.data['Close'].rolling(window=200).mean()
        st.line_chart(self.data[['Close', 'MA50', 'MA200']], use_container_width=True)


def run_visualization(symbol, start_date, end_date, index_symbol):
    visualizer = FinancialDataVisualizer(symbol, start_date, end_date, index_symbol)
    visualizer.fetch_data()
    st.subheader(f'{symbol} Closing Price Chart')
    visualizer.plot_closing_price()
    st.subheader(f'{symbol} Trade Volume Chart')
    visualizer.plot_volume()
    st.subheader(f'{symbol} Daily Returns Distribution')
    visualizer.plot_price_distribution()
    st.subheader(f'{symbol} vs {index_symbol} Correlation Heatmap')
    visualizer.plot_correlation_heatmap()
    st.subheader(f'{symbol} Moving Averages')
    visualizer.plot_moving_averages()

def play_game():
    # Start the happy_humblebee.py script
    subprocess.run([sys.executable, 'happy_humblebee.py'])

st.title("Financial Data Visualizer")

instructions = (
    "This application allows you to visualize financial data for any NASDAQ stock.\n\n"
    "To use the financial data visualization tool:\n"
    "1. Select the stock symbol from the dropdown menu.\n"
    "2. Enter the start and end dates for the data you wish to analyze.\n"
    "3. Select the index for correlation analysis.\n"
    "4. Click 'Submit' to generate various financial charts including:\n"
    "- Closing Price Chart\n"
    "- Trade Volume Chart\n"
    "- Daily Returns Distribution\n"
    "- Price Correlation Heatmap\n"
    "- Moving Averages\n\n"
    "Alternatively, you can click the 'Just play a game instead' button to play a fun game."
)
st.write(instructions)

# Default dates
default_start_date = '2019-01-01'
default_end_date = datetime.today().strftime('%Y-%m-%d')

# Stock symbols list
symbol = st.selectbox("Select the stock symbol:", nasdaq_symbols)
start_date = st.date_input("Enter the start date (YYYY-MM-DD):", value=datetime.strptime(default_start_date, '%Y-%m-%d'))
end_date = st.date_input("Enter the end date (YYYY-MM-DD):", value=datetime.strptime(default_end_date, '%Y-%m-%d'))
index_symbol = st.selectbox("Select the index for correlation analysis:", list(indices.keys()))

if st.button("Submit"):
    run_visualization(symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), indices[index_symbol])

if st.button("Just play a game instead"):
    play_game()
