# --------------------------------------------------------------------

# JDA Backtesting Engine
# /python/user.py
# JohnDavid Abe

# --------------------------------------------------------------------

# Import the bound engine
import sys, os
sys.path.append(os.path.abspath("PATH_TO_SO_FILE"))
import backtest_python










# Step 1: Configure Options

# Set the following options in the options class
class Options:

    # Starting cash for the Portfolio operating the backtest
    cash = 5000

    # The Engine will simulate the implemented trading strategy in steps of bars
    # The following bar sizes are available:
    # Option            Bar Length          Max Historical Date Available

    # "1m"              1 Minute            7 Days
    # "2m"              2 Minutes           60 Days
    # "60m"             60 Minutes          730 Days
    # "1d"              1 Day               ~50 Years
    barSize = "1d"

    # Array with each symbol utilized in the strategy
    symbols = ["AAPL"]

    # The start and end date for which the backtest will run
    start = "2020-01-01"
    end = "2022-01-01"










# Step 2: Implement Strategy

# The user defined Strategy will subclass the exposed cpp Strategy class and then override the "on_data" method
class MyStrategy(backtest_python.Strategy):
    def __int__(self, order_m):
        super().init_(order_m)



    # This method controls the Strategy response to each new bar of data
    # Implement trading Strategy here
    def on_data(self, bars, portfolio):
        # The user has the following actions available for the Strategy to perform:

        # self.buy(symbol, # contracts)                       -->     Market Orders
        # self.sell(symbol, # contracts)

        # self.limit_buy(symbol, # contracts, price)          -->     Limit Orders
        # self.limit_sell(symbol, # contracts, price)

        # self.stop_buy(symbol, # contracts, price)           -->     Stop Orders
        # self.stop_sell(symbol, # contracts, price)


        # The user can also access each symbol's data for the current bar via:

        # aapl_bar = bars["AAPL"]       -->     Get the current bar data for the symbol "AAPL"

        # aapl_bar.open                 -->     Retrieve data from the bar
        # aapl_bar.close
        # aapl_bar.high
        # aapl_bar.low
        # aapl_bar.bid                  -->     Simulated bid/ask prices with 0.02% spread
        # aapl_bar.ask
        # aapl_bar.volume
        # aapl_bar.timestamp


        # Finally, the user can also access the current state on their Portfolio:

        # portfolio.get_cash()              -->     Get cash on hand
        # portfolio.get_equity(bars)        -->     Get current equity based on some bar data
        # portfolio.get_position("AAPL")    -->     Get Portfolio's position on a particular symbol


        # Example Strategy (buying and selling Apple):
        if bars["AAPL"].ask < 100 and portfolio.get_cash() > 500:
            self.buy("AAPL", 5)
        elif bars["AAPL"].bid > 120 and portfolio.get_position("AAPL") > 5:
            self.sell("AAPL", 5)
