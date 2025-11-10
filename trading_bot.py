import yfinance as yf


#getting market data from SPY from the last month and printing
data = yf.download("SPY", start="2025-11-06", end="2025-11-08")  # last 1 month of data
data.columns = data.columns.get_level_values(0)
print(data)


#getting the last closing price
last_close = data['Close']
print(last_close)



#calculating daily percentage change and printing
data['pct_change'] = data['Close'].pct_change()  
print(data)

#percent change over the entire period
first = data["Close"].iat[0]     # first closing price
last = data["Close"].iat[-1]     # last closing price


# if the last closing price is more than the first closing price , print market going up
if last > first:
    print("The market is going up!")
else:
    print("The market is going down!")


percent_change = ((last - first) / first) * 100 #percentage change
absolute_change = last - first     # dollar change
# tells you how much the market went up or down in percentage and dollar terms
if percent_change > 0:
    print(f"The market went UP {percent_change:.2f}% (${absolute_change:.2f}).")
else:
    print(f"The market went DOWN {abs(percent_change):.2f}% (${abs(absolute_change):.2f}).")

print(percent_change)


