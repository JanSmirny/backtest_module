# Backtesting Module

This python module was designed to test trading strategies in a quick and easy way.
It was designed with an emphasis on speed and easy to understand functionality. 
While the main focus is cryptocurrency analysis, most of the content can also be used 
for any other asset.

The module contains a simple backtest for single assets, a portfolio backtesting tool, 
as well as some additional functions for time series analysis like event studies etc.


## Table of contents

- [Table of contents](#table-of-content)
  - [Short Intro](#short-intro)
  - [Detailed Description](#detailed-description)

## Short Intro

A simple backtest can be done by creating a Backtest object:

```python
import testing

bt = testing.backtest.Backtest(price, trades)
```

The format for both the price and the trades should be a pandas dataframe time series.
The trades can be booleans with True for every time interval traded and False for not traded.

Therefore, given a pandas dataframe `data` with the columns `price, moving_average_50, moving_average_200`, 
defining a strategy can be as easy as:

```python
trades = data.moving_average_50 > data.moving_average_200
```

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

## Detailed Description

A more detailed tutorial can be found in the jupyter notebook under /examples
