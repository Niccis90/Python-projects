# Backtester Class Usage Guide
(SOMETHING IS CLEARLY WRONG WITH THE BACKTESTING LOGIC OR STRATEGIES: SEE RESULT)
## Overview
The `backtester` class is a Python tool designed for backtesting trading strategies. It allows users to test trading strategies on historical data to evaluate their performance. This class supports various functionalities including adding data, adding strategies, running backtests, and generating a summary of the backtest results.

## Features
- **Data Management**: Add and manage historical price data for backtesting.
- **Strategy Integration**: Add custom trading strategies and select them for backtesting.
- **Backtesting**: Run backtests over specified periods with the chosen strategy.
- **Performance Analysis**: Generate a tear sheet with key performance metrics.

## How to Use
**Initialization**: Create an instance of the `backtester` class.
   ```python
   engine = backtester()

## Adding Data: Use add_data(name, data) to add historical price data. Data should be in the form of a Pandas Series.

import pandas as pd
data = pd.Series(...)


engine.add_data("MSFT", data)


## Adding Strategy: Use add_strategy(strategy) to add a trading strategy. The strategy should be a function that takes in price data and returns a signal vector.

def my_strategy(data, max_leverage, capital_size):
    # strategy implementation
    return signals


engine.add_strategy(my_strategy)

## Running Backtest: Use run_backtest(start_date, end_date, max_leverage, tx_costs, slippage) to run the backtest.

engine.select_data("MSFT")
engine.select_strategy(0)
engine.add_new_capital_size(100000)
engine.run_backtest("2020-01-01", "2023-01-01", 2, 0.001, 0.001)

## Reviewing Results: After running a backtest, you can view the results and generate a tear sheet for performance analysis.

engine.create_tear_sheet()

NOTE:: the strategies themselves are unrealistic and the information provided by the tear sheet
