import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import san
#san.ApiConfig.api_key = "your key"

"""
To Do:

- transaction costs
- Portfolio analysis

"""

class Backtest:
    
    def __init__(self, returns, trades, lagged=True, transaction_cost = 0, percent_invested_per_trade = 1):
        """ Initializing Backtesting function
        
        Init function generates performance of the test and several risk metrics. The object lets
        you specify wether you want to lag the trades to avoid overfitting, the transaction costs
        and the percentage of the portfolio to be invested per trade (50% as 0.5).
        """
        
        if lagged:
            trades = trades.shift(1)
            trades.iloc[0] = False
            
        else:
            pass
        
        self.strategy_returns = ((returns * percent_invested_per_trade) * trades)
        
        if transaction_cost != 0:
            for index, trade in enumerate(trades):
                if (trade != 0) & (trades[index - 1] == 0):
                    self.strategy_returns.iloc[index + 1] = self.strategy_returns.iloc[index + 1] - transaction_cost
                elif (trade == 0) & (trades[index - 1] != 0):
                    self.strategy_returns.iloc[index + 1] = self.strategy_returns.iloc[index + 1] - transaction_cost
                else:
                    pass
        
        self.performance = ((self.strategy_returns * percent_invested_per_trade) * trades + 1).cumprod() -1
            
        self.benchmark = (returns + 1).cumprod() -1
        self.sharpe_ratio = (self.strategy_returns.mean() * 365) / (self.strategy_returns.std() * np.sqrt(365))
        
        max_draw = 0  # Maximum drawdown
        try:
            running_value = np.array(self.performance)
            a = np.argmax(np.maximum.accumulate(running_value) - running_value)  # end of the period
            b = np.argmax(running_value[:a])  # start of period
            max_draw = ((running_value[a]-running_value[b])/running_value[b]) * 100  # Maximum Drawdown
        except Exception as e:
            print(e)
        
        self.maximum_drawdown = max_draw
        
        
    def get_sharpe_ratio(self):
        return round(self.sharpe_ratio, 2)
    
    
    def get_value_at_risk(self, percentile=5):
        sorted_rets = sorted(self.strategy_returns)
        var = np.percentile(sorted_rets, percentile)
        return round(var * 100, 2)


    def plot_backtest(self):
        plt.figure(figsize=(15,8))
        plt.plot(self.performance,label="performance")
        plt.plot(self.benchmark,label="holding")
        plt.legend()
        plt.show()
    
    
    def get_maximum_drawdown(self):
        return round(self.maximum_drawdown, 2)
    
    
    def get_return(self):
        return round(((self.performance.iloc[-1] + 1) / (self.performance.iloc[0] + 1) - 1) * 100, 2)
    
    
    def get_annualized_return(self):
        return round((((self.performance.iloc[-1] + 1)** (1/len(self.performance))) - 1) *365 * 100, 2)
        
    
    def summary(self):
        print("Returns in Percent: ", self.get_return())
        print("Annualized Returns in Percent: ", self.get_annualized_return())
        print("Annualized Sharpe Raito: ", self.get_sharpe_ratio())
        print("Maximum Drawdown: ", self.get_maximum_drawdown())
        self.plot_backtest()
    
    
    def monte_carlo_simulation(self, simulation_number, simulation_range):
        mu = self.strategy_returns.mean()
        sd = self.strategy_returns.std()

        plt.figure(figsize=(15,8))
        plt.hist(self.strategy_returns, 15)

        simulation_data = pd.DataFrame()
        plt.figure(figsize=(15,8))
        for simulation in range(simulation_number):
            simulation_data[str(simulation)] = np.random.normal(mu, sd, simulation_range)

        simulation_data = (simulation_data + 1).cumprod() - 1
        plt.plot(simulation_data, color="grey")
        plt.show()
        print("Max: ", round(simulation_data.iloc[-1].max() * 100, 2), "%")
        print("Min: ", round(simulation_data.iloc[-1].min() * 100, 2), "%")
        
        
class Portfolio:
    
    def __init__(self, start_date="2017-01-01", end_date=datetime.datetime.now().strftime("%Y-%m-%d"), asset_list=[]):
        """ Takes in list of project slugs"""
        
        self.start_date = start_date
        self.end_date = end_date
        self.asset_list = asset_list
        self.portfolio = pd.DataFrame()
        self.benchmark = san.get("ohlcv/bitcoin", from_date=start_date,
                                 to_date=end_date).closePriceUsd.pct_change()
        
        for portfolio_asset in asset_list:
            self.portfolio[portfolio_asset] = san.get("ohlcv/" + portfolio_asset,
                                                      from_date=start_date,
                                                      to_date=end_date).closePriceUsd.pct_change()
            self.portfolio = self.portfolio.replace([np.inf, -np.inf], 0)
            self.metrics = dict()
        
    
    def add_project(self, project):
        self.asset_list.append(project)
        self.portfolio[project] = san.get("ohlcv/" + project, from_date=self.start_date,
                                          to_date=self.end_date).closePriceUsd.pct_change()
        self.portfolio = self.portfolio.replace([np.inf, -np.inf], 0)
        
    def remove_project(self, project):
        self.portfolio = self.portfolio.drop([project], axis=1)
        self.asset_list.remove(project)
        
    
    def all_assets(self):
        print(self.asset_list)
        return self.asset_list
    
    
    def metrics(self, metric):
        metric_data = pd.DataFrame()
        for asset in self.asset_list:
            metric_data[asset] =  san.get(metric + "/" + asset, 
                                          from_date=self.start_date, to_date=self.end_date).iloc[:,0]
        
        self.metrics[metric] = metric_data
        return metric_data
    
    
    def show_portfolio(self):
        return self.portfolio
    
    
    def plot_portfolio(self):
        perf = (self.portfolio.mean(axis=1, skipna=True) + 1).cumprod() - 1
        plt.figure(figsize=(15,8))
        plt.plot(perf, label="Portfolio")
        plt.plot((self.benchmark + 1).cumprod() - 1, label="Benchmark (BTC)")
        plt.legend()
        plt.show()
    
    
    def portfolio_summary(self):
        #  Bunch of metrics here #####
        self.plot_portfolio()
    


    
# Additional simple event study
    
def eventstudy(price, event, observed_interval, market_returns=0):
    """The function takes in the price of an asset, an array of booleans that mark the events 
    and an integer that describes the size of the event window.
    - as price the opening price is required
    
    """
    
    event_counter = 0
    eventdata = pd.DataFrame()
    returns = price.pct_change() 
    
    returns = returns - market_returns # Calculate the deviation of returns from the market
        

    #print(returns)
    
    plt.figure(figsize=[18,8])
    plt.plot(price)
    
    
    for eventindex, time in enumerate(returns):  # If you find an event take the x times before and after the event and store them
        
        if event[eventindex]:
            if eventindex > observed_interval:
                event_counter += 1
                eventdata[str(returns.index[eventindex])] = pd.DataFrame(returns.iloc[eventindex - observed_interval : eventindex + observed_interval + 1]).reset_index().iloc[:,1]
            
                plt.axvline(price.index[eventindex], color="grey")
            
        else:
            pass
        
    
    cumulative_returns = eventdata.mean(axis=1)
    
    
    # VISUALIZATION:
    
    print("Here are the found events: ")
    
    plt.show()
    print("\n\nThe specified event uccurred {} times\n\n".format(event_counter))
    display(eventdata)
    
    y_labels = ["Event (t)"]
    
    for i in range(observed_interval):
        y_labels.append("t+" + str(i + 1))
        y_labels = ["t-" + str(i+1)] + y_labels
    
    print("\n\nThese are the cumulative returns for the time of the event and the {} time periods before and after the event:".format(observed_interval))
    plt.figure(figsize=[18,8])
    cumulative_returns = (pd.DataFrame(cumulative_returns)[0] + 1).cumprod() - 1
    plt.plot(y_labels, cumulative_returns)
    plt.axvline("Event (t)", color="grey")
    plt.show()
    
    
if __name__ == '__main__':
    data = san.get("ohlcv/bitcoin")
    data["returns"]= data.closePriceUsd.pct_change()
    data["ma50"] = data.closePriceUsd.rolling(50).mean()
    data["ma200"] = data.closePriceUsd.rolling(200).mean()
    data = data.dropna()
    
    trades = data["ma50"] > data["ma200"]
    
    bt = Backtest(data.returns.dropna(),trades, percent_invested_per_trade=0.8)
    bt.summary()
