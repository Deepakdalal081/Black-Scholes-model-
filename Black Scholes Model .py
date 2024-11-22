# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 21:05:16 2024

@author: Deepak Dalal
"""

# Import necessary libraries
import numpy as np
import pandas as pd
import datetime as dt 
import yfinance as yf
from scipy.stats import norm

import os

# Load the Eicher Motors data from a local CSV file
data = pd.read_csv('C:/Users/sdhan/Desktop/Eicher Moter 22 Nov.csv')

# Define the start and end dates for downloading stock data
end_date = dt.date.today()
start_date = end_date - dt.timedelta(days = 300)

# Download historical stock data for Eicher Motors from Yahoo Finance
eicher = yf.download("EICHERMOT.NS", start= start_date, end = end_date, interval= "1D")


# Define Black-Scholes function for call option

def black_scholes_call(S, X, r, T, volatility):
   # Parameters:
   # S : Current stock price
   # X : Strike price of the option
   # r : Risk-free interest rate
   # T : Time to expiration (in years)
   # volatility : Annualized volatility of the stock

    
    d1 = (np.log(S/X) + (r + volatility**2/2)*T)/(volatility * np.sqrt(T))
    
    d2 = d1 + volatility*np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - X*np.exp(-r*T)*norm.cdf(d2)
    
    return call_price


eicher["Adj Close"] = eicher["Adj Close"].dropna()
 
# Extract the current stock price
S = float(np.round(eicher["Adj Close"].iloc[-1],2))

# Extract the strike price 
X = float(data["Strike"][11])

# Define the risk-free interest rate
r = .03    # ( 3% )

# Calculate the time to expiration in years
T = (29 - 14 )/ 365

# Calculate the rolling 1-year (252 trading days) standard deviation
std = eicher['Adj Close'].iloc[-252:].std()/252

# Convert standard deviation to annualized volatility
volatility = np.round(std * np.sqrt(252),4)

# Calculate the call option price using the Black-Scholes model
call_price = black_scholes_call(S, X, r, T, volatility)


print("\n-------------------------------")

# Print the calculated call price
print(f"\nCall Price of {data["Strike"][11]} Strike  right now is :  {call_price}")

# Print the actual last traded price (LTP) of the strike
print(f"\nActual Price of {data["Strike"][11]} strike should be ", data["LTP"][11])

# Convert the LTP column to numeric for accurate comparisons
data["LTP"] = pd.to_numeric(data["LTP"], errors='coerce')
print("-------------------------------------------------")

# Compare the calculated call price with the actual market price

if data["LTP"].iloc[11] > call_price :
    print("Buy Call as it is undervalued by : ", np.round(data["LTP"][11] - call_price, 3) )
    
elif data["LTP"][11].values[0] <= call_price :
    print("Sell the Call Option as it is ivervaled by :", np.round(call_price - data["LTP"][11], 3)  )
    
else :
  pass     
    
