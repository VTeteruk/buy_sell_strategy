# Buy-Sell strategy

This Python project is a simple crypto trading bot that uses historical price data to make buy and sell decisions. It utilizes the CCXT library to access real-time cryptocurrency price data from the Binance exchange, analyzes the data, and executes buy and sell orders based on predefined trading strategies.
___
# Features
* Fetches historical price data for a specified cryptocurrency pair (e.g., BTC/USDT) and time frame (e.g., 1 minute).
* Implements a basic trading strategy with adjustable buying and selling thresholds.
* Logs trading actions, such as buying and selling, and provides information on successful trades and final balance.
* Displays a graphical representation of price movements with buy and sell points marked.

___
# Prerequisites
Before running the trading bot, make sure you have the following prerequisites installed:

* Python 3.x
* And install libraries: `pip install -r requirements.txt`

# Getting Started
Clone this repository to your local machine:

Run the bot using the following command:

`python main.py`

The bot will fetch historical price data, execute trades based on your configured strategy, and display a graph showing price movements with buy and sell points.

# Configuration
You can configure the trading parameters in the main.py file. Here are some key configuration options:

* symbol: The trading pair you want to trade (e.g., "BTC/USDT").
* timeframe: The time frame for historical price data (e.g., "1m" for 1-minute intervals).
* limit: The limit of data to be fetched
* balance: Initial balance in USDT for trading.
* division_coefficient: A coefficient used to adjust the buying and selling thresholds.
* buying_steps and selling_steps: Lists of thresholds for buying and selling.
___
# Results
After running the bot, you will see information about successful trades, total trades, final balance, and total profit printed to the console. Additionally, a graphical representation of price movements with buy and sell points will be displayed using Matplotlib.
