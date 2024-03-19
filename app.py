import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

# Function to calculate expected stock price change
def calculate_expected_change(closing_price, beta, volatility, correlation, index_expectation):
    expected_change = beta * (index_expectation / index_data['Adj Close'].iloc[-1] - 1) + (volatility * correlation)
    return expected_change

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

            # User input for Nifty next day closing expectation
            nifty_expectation = st.number_input('Enter your expectation for the next day closing of Nifty:', step=0.01)

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

                # Calculate expected change in stock price
                closing_price = stock_data['Adj Close'].iloc[-1]
                expected_change = calculate_expected_change(closing_price, beta, volatility, correlation, nifty_expectation)
                st.write(f'Expected Change in {ticker} Price: {expected_change}')

                # Plot stock prices
                plt.figure(figsize=(10, 6))
                plt.plot(stock_data['Adj Close'], label=ticker)
                plt.xlabel('Date')
                plt.ylabel('Price')
                plt.title(f'{ticker} Closing Prices')
                plt.legend()
                st.pyplot(plt)

            # Display correlation matrix
            st.subheader('Correlation Matrix')
            correlation_matrix = pd.DataFrame(index=portfolio.keys(), columns=['^NSEI'])
            for ticker, _ in portfolio.items():
                stock_data = fetch_stock_data(ticker)
                stock_returns = stock_data['Adj Close'].pct_change().dropna()
                correlation_matrix.loc[ticker, '^NSEI'] = calculate_correlation(stock_returns, index_data['Returns'].iloc[1:])
            st.write(correlation_matrix)

if __name__ == "__main__":
    main()
