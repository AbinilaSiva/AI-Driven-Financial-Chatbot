import json
import openai
import datetime
import pandas as pandas
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
from openai import OpenAI

# Read the API key from file
api_key = 'insert your openAI API key'

# Set the API key
openai.api_key = api_key

# Initialize the OpenAI client (if needed)
client = OpenAI(api_key=api_key)

def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period='1y').iloc[-1]['Close'])

def calculate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y')['Close']
    return str(data.rolling(window=window).mean().iloc[-1])

def calculate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y')['Close']
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])

def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period='1y')['Close']
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=14-1, adjust=False).mean()
    ema_down = down.ewm(com=14 - 1, adjust=False).mean()
    rs = ema_up / ema_down
    return str(100 - (100 / (1 + rs)).iloc[-1])

def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period='1y')['Close']
    short_EMA = data.ewm(span=12, adjust=False).mean()
    long_EMA = data.ewm(span=26, adjust=False).mean()

    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    MACD_histogram = MACD - signal
    return f'{MACD.iloc[-1]}, {signal.iloc[-1]}, {MACD_histogram.iloc[-1]}'

def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period='1y')
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data.Close)
    plt.title(f'{ticker} Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()

def get_market_news(keyword=None):
    try:
        if keyword:
            news = yf.Ticker(keyword).news
        else:
            # Fetch news using yfinance
            news = yf.Ticker("^GSPC").news  
        
        # Process and return the news
        if news:
            news_summary = []
            for item in news[:10]:  # Limit to first 10 news items for example
                news_item = {
                    'title': item.get('title', 'No Title'),
                    'link': item.get('link', 'No Link'),
                    'publisher': item.get('publisher', 'No Publisher'),
                    'published_date': datetime.datetime.fromtimestamp(item.get('providerPublishTime', 0)).strftime('%Y-%m-%d %H:%M:%S')
                }
                news_summary.append(news_item)
            return news_summary
        else:
            return "No news available currently."
    except Exception as e:
        return f"An error occurred while fetching news: {e}"

functions = [
    {
        'name': 'get_stock_price',
        'description': 'Gets the latest stock price given the ticker symbol of a company.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example AAPL for Apple).'
                }
            },
            'required': ['ticker']
        }   
    },    
    
    {
        "name": "calculate_SMA",
        "description": "Calculate the simple moving average for a given stock ticker and a window.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                "type": "string",
                "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)",
                },
                "window": {
                    "type": "integer",
                    "description": "The timeframe to consider when calculating the SMA",
                }
            },
            "required": ["ticker", "window"],
        },
    },
    
    {
        "name": "calculate_EMA",
        "description": "Calculate the exponential moving average for a given stock ticker and a window.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)",
                },
                "window": {
                    "type": "integer",
                    "description": "The timeframe to consider when calculating the EMA",
                }
            },
            "required": ["ticker", "window"],
        },
    },

    {
        "name": "calculate_RSI",
        "description": "Calculate the RSI for a given stock ticker.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)",
                },
            },
            "required": ["ticker"],
        },
    },

    {
        "name": "calculate_MACD",
        "description": "Calculate the MACD for a given stock ticker.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)",
                },
            },
            "required": ["ticker"],
        },
    },
    
    {
        "name": "plot_stock_price",
        "description": "Plot the stock price for the last year given the ticker sysmbol of a company.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)",
                },
            },
            "required": ["ticker"],
        },
    },
    {
        'name': 'get_market_news',
        'description': 'Fetches the latest market news based on a keyword, such as a ticker symbol.',
        'parameters': {
            'type': 'object',
            'properties': {
                'keyword': {
                    'type': 'string',
                    'description': 'A keyword for fetching news, such as a ticker symbol or a news topic.'
                }
            },
            'required': ['keyword']
        },
    }

]

available_functions = {
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_RSI': calculate_RSI,
    'calculate_MACD': calculate_MACD,
    'plot_stock_price': plot_stock_price,
    'get_market_news': get_market_news
}

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.title('Finance Analysis Chatbot Assistant')

user_input = st.text_input('Your input:')

if user_input:
    try:
        st.session_state['messages'].append({'role': 'user', 'content': f'{user_input}'})

        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=st.session_state['messages'],
            functions=functions,
            function_call='auto'
        )

        if response.choices and response.choices[0].message:
            response_message = response.choices[0].message

            if hasattr(response_message, 'function_call') and response_message.function_call:
                function_call = response_message.function_call
                function_name = function_call.name

                # Convert the string to a dictionary
                function_args = json.loads(function_call.arguments)

                if function_name in ['get_stock_price', 'calculate_RSI', 'calculate_MACD', 'plot_stock_price']:
                    args_dict = {'ticker': function_args['ticker']}
                    function_response = available_functions[function_name](**args_dict)

                elif function_name in ['calculate_SMA', 'calculate_EMA']:
                    args_dict = {'ticker': function_args['ticker'], 'window': function_args['window']}
                    function_response = available_functions[function_name](**args_dict)

                elif function_name == 'get_market_news':
                    args_dict = {'keyword': function_args.get('keyword')}
                    news_items = available_functions['get_market_news'](**args_dict)

                    # Convert the list of news items to a formatted string
                    if isinstance(news_items, list):
                        news_string = "\n".join([f"Title: {item['title']}\nLink: {item['link']}\nPublisher: {item['publisher']}\nDate: {item['published_date']}\n" for item in news_items])
                        function_response = news_string
                    else:
                        function_response = news_items

                if function_name == 'plot_stock_price':
                    st.image('stock.png')
                
                elif function_name == 'get_market_news':
                    # Check if news items were fetched
                    if isinstance(news_items, list) and news_items:
                        # Display each news item using Streamlit
                        for item in news_items:
                            st.markdown(f"**Title:** {item['title']}")
                            st.markdown(f"**Publisher:** {item['publisher']}")
                            st.markdown(f"**Date:** {item['published_date']}")
                            st.markdown(f"**Link:** [Read more]({item['link']})")
                            st.markdown("---")  # Adding a line for separation between news items
                    else:
                        # Display the message if no news items or an error occurred
                        st.write(function_response)

                else:
                    st.session_state['messages'].append({'role': 'function', 'name': function_name, 'content': function_response})
                    second_response = client.chat.completions.create(
                        model='gpt-3.5-turbo',
                        messages=st.session_state['messages']
                    )
                    st.markdown(second_response.choices[0].message.content)
                    st.session_state['messages'].append({'role': 'assistant', 'content': second_response.choices[0].message.content})
            else:
                st.markdown(response_message.content)

                # Check if the response indicates an inability to predict
                if any(phrase in response_message.content for phrase in ["As an AI language model", "As an AI", "I don't have real-time data", "the ability to predict future market trends"]):
                    # Use a default keyword to fetch related news
                    input_keywords = user_input.lower().split()
                    if "outlook" in input_keywords or "forecast" in input_keywords or "trend" in input_keywords:
                        default_keyword = " ".join(input_keywords) + " financial news"
                    else:
                        default_keyword = "stock market outlook" 
                    related_news = get_market_news(keyword=default_keyword)

                    # Display the related news articles
                    if related_news and isinstance(related_news, list):
                        st.write("Here are some related news articles that might provide insights:")
                        for news_item in related_news:
                            st.markdown(f"**Title:** {news_item['title']}")
                            st.markdown(f"**Link:** [Read more]({news_item['link']})")
                            st.markdown(f"**Publisher:** {news_item['publisher']}")
                            st.markdown(f"**Date:** {news_item['published_date']}")
                            st.markdown("---")
                    else:
                        st.write(related_news)

                st.session_state['messages'].append({'role': 'assistant', 'content': response_message.content})
    
    except Exception as e:
        st.error(f'An error occurred: {e}')
