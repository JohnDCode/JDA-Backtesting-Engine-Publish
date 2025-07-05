# --------------------------------------------------------------------

# JDA Backtesting Engine
# /python/main.py
# JohnDavid Abe

# --------------------------------------------------------------------

# Import user configurations and strategy
from user import Options, MyStrategy

# Packages
import sys, os, pandas, yfinance

# Import the bound engine
sys.path.append(os.path.abspath("PATH_TO_SO_FILE"))
import backtest_python


# Create portfolio first
portfolio = backtest_python.Portfolio(Options.cash)

# Create market data feed
market_data = backtest_python.MarketDataFeed()

# Collect bar data
for symbol in Options.symbols:

    # Compile the file name for bar data
    file_name = symbol + "_" + Options.start + "_" + Options.end + "_" + Options.barSize

    # Check if the bar data already exists in the /data folder
    found = False
    for entry in os.listdir("../data"):
        if f"{file_name}.csv" == entry:
            found = True
            break
    if found:
        # If the data already exists in the data folder, just import the csv to the engine
        market_data.load_from_csv(symbol, f"../data/{file_name}.csv")
        continue

    # Retrieve the bar data from Yahoo finance (throw if args are wrong)
    try:
        # Ensure data filled
        data = yfinance.download(symbol, start=Options.start, end=Options.end, interval=Options.barSize)
        if data.empty:
            raise ValueError("Improper data request(s), see commented instructions.")

    except Exception:
        print("Improper data request(s), see commented instructions.")
        raise


    # Handle MultiIndex columns (e.g., ('Open', 'AAPL')) → 'Open'
    if isinstance(data.columns, pandas.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.reset_index(inplace=True)

    # Export the bar data to the appropriate csv
    data.to_csv(f"../data/{file_name}.csv", index=False)

    # Load bar data to market feed
    market_data.load_from_csv(symbol, f"../data/{file_name}.csv")


# Collect dividend/splits data
for symbol in Options.symbols:

    # Collect dividend/split data
    tick = yfinance.Ticker(symbol)
    div_series = tick.dividends
    split_series = tick.splits

    # Convert pandas Series to dictionaries that can be past to cpp methods
    dividend_map = {str(date.date()): float(value) for date, value in div_series.items()}
    split_map = {str(date.date()): float(ratio) for date, ratio in split_series.items()}

    # Load dividend data to market feed
    market_data.add_dividends(symbol, dividend_map)
    market_data.add_splits(symbol, split_map)




# Create other components of engine and run
order_manager = backtest_python.OrderManager()
strategy = MyStrategy(order_manager)
engine = backtest_python.Engine(market_data, order_manager, portfolio, strategy)
engine.run_backtest()
