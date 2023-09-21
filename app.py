import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import plotly.express as px
import plotly.graph_objects as go  # Import this module

# Page title and description
st.title("Real-Time Stock Data Visualization")

# Input for stock symbol
symbol = st.text_input("Enter the stock symbol (Example: AAPL for Apple Inc.):").upper()

if symbol:
    # Fetch stock data
    try:
        stock_data = yf.Ticker(symbol)
        stock_info = stock_data.info
        
        # Display labeled stock information
        st.subheader(f"Stock Information for {symbol}")
        st.write(f"**State:** {stock_info.get('state')}")
        st.write(f"**Country:** {stock_info.get('country')}")
        st.write(f"**Sector:** {stock_info.get('sector')}")
        st.write(f"**Business Summary:** {stock_info.get('longBusinessSummary')}")

        # Fetch historical data for a specific date range (e.g., 1 year)
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)
        end_date = datetime.datetime.now()
        historical_data = yf.download(symbol, start=start_date, end=end_date)
        
        # Display historical data
        st.subheader(f"Historical Data for {symbol}")
        st.write(historical_data)

        # Plot historical data
        st.subheader(f"Historical Data Plot for {symbol}")
        plt.figure(figsize=(10, 6))
        plt.title(f"{symbol} Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.plot(historical_data.index, historical_data['Close'], label="Closing Price")
        plt.legend()
        st.pyplot(plt)

        # Add date and time of information fetch
        st.write(f"Data last fetched on: {datetime.datetime.now()}")

        # Additional Visualizations
        st.write("**Moving Average Plot (50-Day and 200-Day)**")
        moving_average_50 = historical_data['Close'].rolling(window=50).mean()
        moving_average_200 = historical_data['Close'].rolling(window=200).mean()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(historical_data.index, historical_data['Close'], label="Closing Price")
        ax.plot(historical_data.index, moving_average_50, label="50-Day Moving Avg")
        ax.plot(historical_data.index, moving_average_200, label="200-Day Moving Avg")
        ax.set_title(f"{symbol} Stock Price with Moving Averages")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        st.pyplot(fig)

        # Visualization 2 - Volume Chart
        st.write("**Volume Chart**")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(historical_data.index, historical_data['Volume'], color='royalblue', label="Volume")
        ax.set_title(f"{symbol} Stock Volume")
        ax.set_xlabel("Date")
        ax.set_ylabel("Volume")
        ax.legend()
        st.pyplot(fig)

        # Visualization 3 - Scatter Plot (using Plotly)
        st.write("**Scatter Plot**")
        fig = px.scatter(historical_data, x=historical_data.index, y='Close', labels={'y': 'Closing Price'})
        fig.update_layout(title=f"{symbol} Closing Price Scatter Plot")
        st.plotly_chart(fig)

        # Visualization 4 - Candlestick Chart (using Plotly)
        st.write("**Candlestick Chart**")
        fig = go.Figure(data=[go.Candlestick(x=historical_data.index,
                                             open=historical_data['Open'],
                                             high=historical_data['High'],
                                             low=historical_data['Low'],
                                             close=historical_data['Close'])])
        fig.update_layout(title=f"{symbol} Candlestick Chart")
        st.plotly_chart(fig)

        # Visualization 5 - Histogram (using Plotly)
        st.write("**Histogram of Closing Prices**")
        fig = px.histogram(historical_data, x='Close', nbins=30, labels={'x': 'Closing Price'})
        fig.update_layout(title=f"{symbol} Closing Price Histogram")
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error: {e}")
