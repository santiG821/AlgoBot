#!/usr/bin/env python
# coding: utf-8

# In[121]:


# imports
import numpy as np
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
#Gather BTC and ETH data
dataETH = yf.download('ETH-USD',interval="1m",period="7d")
dataBTC = yf.download('BTC-USD',interval="1m",period="7d")
#Create Subplots of BTC and ETH Price
fig, (ax1,ax2)=plt.subplots(2,sharex=True,figsize=(12,10))
ax1.plot(dataETH['Close'])
ax1.set_title('Eth Price')
ax2.plot(dataBTC['Close'])
ax2.set_title('BTC Price')
# Create bands for ETH
dataETH['short_sma'] = dataETH['Adj Close'].rolling(window=20).mean()
dataETH['std'] = dataETH['Adj Close'].rolling(window=20).std()
dataETH['upper_band'] = dataETH['short_sma'] + (2 * dataETH['std'])
dataETH['lower_band'] = dataETH['short_sma'] - (2 * dataETH['std'])
dataETH.drop(['Open','High','Low'],axis=1,inplace=True,errors='ignore')
dataETH.tail(5)
# Create Bands for BTC
dataBTC['short_sma'] = dataBTC['Adj Close'].rolling(window=20).mean()
dataBTC['std'] = dataBTC['Adj Close'].rolling(window=20).std()
dataBTC['upper_band'] = dataBTC['short_sma'] + (2 * dataBTC['std'])
dataBTC['lower_band'] = dataBTC['short_sma'] - (2 * dataBTC['std'])
dataBTC.drop(['Open','High','Low'],axis=1,inplace=True,errors='ignore')
dataBTC.tail(5)
#Plot BTC and ETH Bands
plot_dataETH = dataETH[-500:]
plot_dataBTC = dataBTC[-500:]
fig, (ax3,ax4)=plt.subplots(2,sharex=True,figsize=(12,10))
#ETH Chart
ax3.plot(plot_dataETH['Close'], label='Close')
ax3.plot(plot_dataETH['upper_band'],label='Upper Band')
ax3.plot(plot_dataETH['lower_band'],label='lower Band')
ax3.legend()
ax3.set_title('ETH Band Chart')
#BTC Chart
ax4.plot(plot_dataBTC['Close'], label='Close')
ax4.plot(plot_dataBTC['upper_band'],label='Upper Band')
ax4.plot(plot_dataBTC['lower_band'],label='lower Band')
ax4.set_title('BTC Band Chart')
ax4.legend()
# Take long positions
dataETH['long_positions'] = np.where(dataETH['lower_band'] < dataETH['Close'], 1, 0)
dataBTC['long_positions'] = np.where(dataBTC['lower_band'] < dataBTC['Close'], 1, 0)
# Take short positions
dataETH['short_positions'] = np.where(dataETH['upper_band'] > dataETH['Close'], -1, 0)
dataBTC['short_positions'] = np.where(dataBTC['upper_band'] > dataBTC['Close'], -1, 0)

dataETH['positions'] = dataETH['long_positions'] + dataETH['short_positions']
dataBTC['positions']= dataBTC['long_positions'] + dataBTC['short_positions']  
# Create Subplots for Signals
plot_dataETH = dataETH[-3000:]
plot_dataBTC =dataBTC[-3000:]
fig, (ax5,ax6)=plt.subplots(2,sharex=True,figsize=(12,10))
#Plot ETH Signals
ax5.plot(plot_dataETH['Close'], label='Close')
ax5.plot(plot_dataETH['upper_band'],label='Upper Band')
ax5.plot(plot_dataETH['lower_band'],label='lower Band')
ax5.plot(plot_dataETH[(plot_dataETH['long_positions'] == 1) &
                       (plot_dataETH['long_positions'].shift(1) == 0)]['short_sma'],
         '^', ms=15, label='Buy Signal', color='green')
ax5.plot(plot_dataETH[(plot_dataETH['short_positions'] == -1) &
                       (plot_dataETH['short_positions'].shift(1) == 0)]['short_sma'],
         '^', ms=15, label='Sell Signal', color='red')
ax5.legend()
ax5.set_title('Eth Signals')
#Plot BTC Signals
ax6.plot(plot_dataBTC['Close'], label='Close')
ax6.plot(plot_dataBTC['upper_band'],label='Upper Band')
ax6.plot(plot_dataBTC['lower_band'],label='lower Band')
ax6.plot(plot_dataBTC[(plot_dataBTC['long_positions'] == 1) &
                       (plot_dataBTC['long_positions'].shift(1) == 0)]['short_sma'],
         '^', ms=15, label='Buy Signal', color='green')
ax6.plot(plot_dataBTC[(plot_dataBTC['short_positions'] == -1) &
                       (plot_dataBTC['short_positions'].shift(1) == 0)]['short_sma'],
         '^', ms=15, label='Sell Signal', color='red')
ax6.legend()
ax6.set_title('BTC Signals')
# Calculate daily returns
dataETH['returns'] = dataETH['Close'].pct_change()
dataBTC['returns'] = dataBTC['Close'].pct_change()
# Calculate strategy returns
dataETH['strategy_returns'] = dataETH['returns'] * dataETH['positions'].shift(1)
dataBTC['strategy_returns'] = dataBTC['returns'] * dataBTC['positions'].shift(1)
# Calcualte cumulative returns
cumulative_returnsETH = (dataETH['strategy_returns'] +1).cumprod()
cumulative_returnsBTC= (dataBTC['strategy_returns'] +1).cumprod()
cumulative_returnsALL= (dataBTC['strategy_returns'] +1+dataETH['strategy_returns']).cumprod()
#Plot daily and cumulative returns
fig, (ax7,ax8,ax9,ax10,ax11)=plt.subplots(5, sharex=True,figsize=(10,10))
#Plot Eth
ax7.plot(dataETH['returns'])
ax7.set_title("ETH Daily Returns")
ax8.plot(cumulative_returnsETH)
ax8.set_title("ETH CUmulative Returns")
#Plot BTC
ax9.plot(dataBTC['returns'])
ax9.set_title("BTC Daily Returns")
ax10.plot(cumulative_returnsBTC)
ax10.set_title("BTC CUmulative Returns")
#Plot Both Combine
ax11.plot(cumulative_returnsALL)
ax11.set_title("Cumulative Returns")
# Total number of trading days
days = len(cumulative_returnsALL)
# Calculate compounded annual growth rate
# Use 252 instead oof 365, # of trading days in a year is 252
annualised_returns = (cumulative_returnsALL.iloc[-1]**(252/days)-1)*100
print('annualised returns %.2f' % annualised_returns + '%')


# In[ ]:




