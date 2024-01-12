# AI-Driven-Financial-Chatbot

The "AI-Driven Financial Chatbot" is a Python-based assistant enhanced by OpenAI's GPT-3.5, designed to deliver financial insights interactively 
through Streamlit. It sources real-time data from Yahoo Finance, offering features like stock price tracking, analysis of financial indicators 
(Moving Averages, RSI, MACD), and the latest market news. This tool is ideal for investors and financial analysts, merging GPT-3.5's natural 
language processing with financial analytics for accessible, up-to-date market intelligence.

# Set-Up and Installation (Docker)
To set up and run this project using Docker, follow these steps:

1. Clone the Repository:

```
git clone https://github.com/AbinilaSiva/AI-Driven-Financial-Chatbot.git
```

2. Navigate to the Project Directory:

```
cd AI-Driven-Financial-Chatbot
```
3. Configure the API Key:

* In main.py, locate the line 11: api_key (Note: Ensure you prepend 'sk-').
* Example: api_key = 'sk-EWIDVvyxEvg...'

4. Build the Docker Image:

```
docker build -t finance-chatbot .
```

5. Run the Container:

```
docker run -p 8501:8501 finance-chatbot
```
The application should now be running and accessible at http://localhost:8501

# Code Functionality

* get_stock_price: Fetches the latest stock price for a given ticker.
* calculate_SMA: Calculates the Simple Moving Average for a stock.
* calculate_EMA: Computes the Exponential Moving Average.
* calculate_RSI: Determines the Relative Strength Index.
* calculate_MACD: Calculates the Moving Average Convergence Divergence.
* plot_stock_price: Plots the stock price over the last year.
* get_market_news: Retrieves the latest market news based on a keyword or ticker symbol.

# Demo

A demonstration of the chatbot can be accessed by running the application as mentioned in the Set-Up section. Interact with the chatbot by inputting 
your queries about stock prices, market analysis, and news updates.

For a visual guide and overview of the chatbot's features and capabilities, check out the demo video:

https://github.com/AbinilaSiva/AI-Driven-Financial-Chatbot/assets/80882447/d3fe66fd-9889-4d2f-969f-76b0fd8a0880

