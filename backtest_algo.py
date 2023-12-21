import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class backtester:

    def __init__(self):
        self.data = {}
        self.strategies = []
        self.selected_data = None
        self.selected_strategy = None
        self.capital_size = None
        self.results = None

    def add_data(self,name ,data):
        assert isinstance(data, pd.Series), "Data must be a pandas Series"
        self.data[name] = data
        print("Data has been appended.")

    def add_strategy(self, strategy):
       
        assert callable(strategy), "Strategy must be callable"
        self.strategies.append(strategy)
        print("Strategy has been appended.")

    def get_strategies(self):
        if self.strategies:
            print("Here are your strategies:")
            for strategy in self.strategies:
                print(strategy)
        else:
            print("You have not added any strategies")

    def get_data(self):
        if self.data:
            print("Here is your data:")
            for name, data_series in self.data.items():
                print(f"Data set '{name}':\n{data_series}")
        else:
            print("You have not added any data")

    def select_data(self, x):
        """Select the preferred data by name"""
        try:
            self.selected_data = self.data[x]
        except IndexError:
            print(f"No data found at index {x}.")

    def select_strategy(self, x: int):
        """Select the preferred strategy by index."""
        try:
            self.selected_strategy = self.strategies[x]
        except IndexError:
            print(f"No strategy found at index {x}.")

    def remove_data(self, x: int):
        """Remove the preferred data by index."""
        try:
            self.data.pop(x)
        except IndexError:
            print(f"No data found at index {x}.")

    def remove_strategy(self, x: int):
        """Remove the preferred strategy by index."""
        try:
            self.strategies.pop(x)
        except IndexError:
            print(f"No strategy found at index {x}.")

    def plot_data(self, name, start_date=None, end_date=None, to_plot=None):
        """Plot specific time series data. name = is the key for target data"""
        if name not in self.data:
            print(f"No data found for name '{name}'.")
            return
        data = self.data[name]
        if start_date is not None and end_date is not None:
            data = data[start_date:end_date]
        if to_plot is not None:
            data = data[to_plot]
        plt.plot(data.index, data)
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title(f'Time Series Data: {name}')
        plt.show()


    def add_new_capital_size(self, num):
        self.capital_size = num

    def run_backtest(self, start_date=None, end_date=None, max_leverage=None, tx_costs=None, slippage=None):
        if self.selected_data is None or self.selected_strategy is None:
            raise Exception("Selected data or strategy is not available")
        if self.capital_size is None:
            raise Exception("Please define the capital size!")
        if start_date and end_date:
            data = self.selected_data[start_date:end_date]
        else:
            data = self.selected_data
        try:
            signal_vector = self.selected_strategy(data, max_leverage, self.capital_size)
        except Exception as e:
            raise Exception(f"Error in strategy function: {e}")
        if signal_vector.empty:
            raise Exception("Signal Vector is empty, strategy function is faulty")
        aligned_signal_vector = signal_vector.reindex(data.index).fillna(0)
        price_change = data.diff()
        results = aligned_signal_vector.shift(1) * price_change
        if tx_costs:
            trade_amounts = aligned_signal_vector.diff().abs()
        results -= trade_amounts * tx_costs
        if slippage:
            trade_occurred = aligned_signal_vector.diff().abs() != 0
        results[trade_occurred] -= slippage
        
        self.results = pd.Series(self.capital_size, index=data.index).add(results.cumsum(), fill_value=0)
        return self.results


    def create_tear_sheet(self):
        if self.results is None or self.results.dropna().empty:
            raise Exception("No valid backtest results to analyze")
        initial_capital = self.capital_size if self.capital_size is not None else 0
        equity_curve = initial_capital + self.results.cumsum()
        backtest_length_years = len(equity_curve.dropna()) / 252
        total_return = (equity_curve.iloc[-1] - equity_curve.iloc[0]) /equity_curve.iloc[0]
        cagr = ((1 + total_return) ** (1 / backtest_length_years)) - 1 if backtest_length_years > 0 else np.nan
        daily_returns = equity_curve.pct_change().dropna()
        max_drawdown = (daily_returns.cummin() - daily_returns.cummax()).min()
        volatility = daily_returns.std() * np.sqrt(252)
        sharpe_ratio = daily_returns.mean() / volatility 
        skewness = daily_returns.skew()
        tear_sheet_data = {
            'Backtest length': f'{backtest_length_years:.2f} years',
            'Total return': f'{total_return:.2%}',
            'CAGR': f'{cagr:.2%}',
            'Max drawdown': f'{max_drawdown:.2%}',
            'Volatility': f'{volatility:.2%}',
            'Sharpe ratio': f'{sharpe_ratio:.2f}',
            'Skewness': f'{skewness:.2f}'
            }
        print("\nTear Sheet:")
        for k, v in tear_sheet_data.items():
            print(f"{k:<20}: {v}")






































































        


    


    









