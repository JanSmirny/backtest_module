# Backtesting Module

This python module was designed to test trading strategies in a quick and easy way.
It was designed with an emphasis on speed and easy to understand functionality.

## 

A simple backtest can be done by creating a Backtest object:

```python
import testing

bt = testing.backtest.Backtest(price, trades)
```

The format for both the price and the trades should be a pandas dataframe time series.
The trades can be booleans with True for every time interval traded and False for not traded.
Three True values in a row would therefore represent holding the asset for three time periods.
Alternative the values can also be:
* 1 for Buy
* 0 for not being invested
* -1 for selling short
* floats > 1 for a leveraged position
* floats < 1 for reduced exposure (0.5 for 50% of the money invested)


After that a summary can be created by the summary() method:


```python
bt.summary()
```

#

A more detailed tutorial can be found in the jupyter notebook under /examples
