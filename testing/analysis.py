import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import statsmodels.api as sm
import san
#san.ApiConfig.api_key = "your key"


    
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

    
def causality(data, lags):  # Data as dataframe with two columns. Tests if first is caused by second
    sm.tsa.stattools.grangercausalitytests(data,lags)
