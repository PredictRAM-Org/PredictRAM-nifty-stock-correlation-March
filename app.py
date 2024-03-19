import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

# Function to fetch stock data
def fetch_stock_data(ticker):
    stock_data = yf.download(ticker, start="2023-03-19", end="2024-03-19")
    return stock_data

# Function to calculate beta
def calculate_beta(stock_data, index_data):
    cov_matrix = np.cov(stock_data['Adj Close'], index_data['Adj Close'])
    beta = cov_matrix[0, 1] / np.var(index_data['Adj Close'])
    return beta

# Function to calculate volatility
def calculate_volatility(returns):
    volatility = np.std(returns) * np.sqrt(252)  # Annualized volatility
    return volatility

# Function to calculate correlation
def calculate_correlation(stock_returns, index_returns):
    correlation = np.corrcoef(stock_returns, index_returns)[0, 1]
    return correlation

# Main function
def main():
    st.title('Stock Portfolio Analysis')

    # User input for stock tickers and quantities
    st.subheader('Enter Stock Portfolio')
    portfolio = {}
    stock_tickers = st.text_input('Enter stock tickers separated by commas (e.g., AAPL, GOOGL):').upper()
    if stock_tickers:
        for ticker in stock_tickers.split(','):
            quantity = st.number_input(f'Enter quantity of {ticker}:', min_value=1, step=1)
            if quantity > 0:
                portfolio[ticker.strip()] = quantity

        if portfolio:
            # Fetch Nifty 50 index data
            index_data = yf.download('^NSEI', start="2023-03-19", end="2024-03-19")

            # Calculate index returns
            index_data['Returns'] = index_data['Adj Close'].pct_change()

            # Display portfolio
            st.subheader('Portfolio Summary')
            st.write(pd.DataFrame.from_dict(portfolio, orient='index', columns=['Quantity']))

            # Fetch and analyze data for each stock in the portfolio
            for ticker, quantity in portfolio.items():
                st.subheader(f'Analysis for {ticker}')
                stock_data = fetch_stock_data(ticker)

                # Calculate stock returns
                stock_data['Returns'] = stock_data['Adj Close'].pct_change()

                # Calculate beta
                beta = calculate_beta(stock_data, index_data)
                st.write(f'Beta: {beta}')

                # Calculate volatility
                volatility = calculate_volatility(stock_data['Returns'])
                st.write(f'Volatility: {volatility}')

                # Calculate correlation with index
                correlation = calculate_correlation(stock_data['Returns'].iloc[1:], index_data['Returns'].iloc[1:])
                st.write(f'Correlation with Nifty 50 Index: {correlation}')

if __name__ == "__main__":
    main()
