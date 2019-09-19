# Backtesting Module

This module was designed to test trading strategies in a quick and easy way.
It was designed with an emphasis on speed and easy to understand functionality.


A simple backtest can be done by creating a Backtest object:

```
import testing

bt = testing.backtest.Backtest(price, trades)

```

After that a summary can be created by the summary() method:


```
bt.summary()
```
