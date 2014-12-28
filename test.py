"""
This Python script demonstrates the use of the pandas package to read and
process stock data.  You can choose your own list of stock symbols (these are
all T. Rowe Price Mutual Funds). The script reads the daily price data from
Yahoo finance, extracts just the adjusted closing prices, calculates continuosly
compounded returns and does some statistical plotting.

When we first read in the stock data it comes in as a 3D table (a Panel in panda).
One dimension is the date (this is daily data), another dimension is the stock
symbol, and the third dimension is the data type downloaded from Yahoo. You
need pandas v 0.11.0, for this to work since the get_data_yahoo method was only
updated to read multiple stocks at once in that version.

One of the first things that we do is pull out just the adjusted close data.  This
is now a 2D table (a DataFrame in pandas), which is much easier to deal with. The
continuously compounded daily returns are calculated from the adjusted close data.

"""

from pylab import *
from pandas.io.data import *
from pandas import *
from pandas.tools.plotting import *

# 1. Data Gathering


print 'Reading stock data from Yahoo Finance'

symbols = ['TRBCX', 'CMTFX', 'TREMX', 'PRFDX', 'PEXMX', 'PRITX', 'PRLAX',
           'RPMGX', 'TRMCX', 'PRASX', 'PRNHX', 'OPGSX', 'TRREX', 'PRSCX',
           'PRSVX', 'PRSGX', 'PSILX', 'PRHYX', 'PTTRX', 'RPSIX', 'PRTIX',
           'TRRFX', 'TRRAX', 'TRRGX', 'TRRBX', 'TRRHX', 'TRRCX', 'TRRJX',
           'TRRDX', 'TRRKX', 'TRRMX', 'TRRNX', 'TRRIX'] # List of all stock symbols to download


stock_data = get_data_yahoo(symbols,start='1/1/1900') # Download data from YAHOO as a pandas Panel object

# 2. Extract and plot data

print 'Extracting and plotting Adjusted Closing Prices'

adj_close  = stock_data['Adj Close']                  # Pull out adjusted closing prices as pandas DataFrane object
adj_close.plot(title='Daily Adjusted Closing Prices for 401K Funds')
show()

print 'Extracting and plotting Daily Returns'

returns    = log(adj_close/adj_close.shift(1))        # Calculate continuously compounded returns
returns.plot(title='Daily Returns for 401K Funds')
show()

# 3. Plot return vs. volatility

print 'Plotting data'

mean_ret   = returns.mean() # Returns a pandas DataFrame with mean values indexed by stock symbol
std_ret    = returns.std()  # Returns a pandas DataFrame with standard deviations (volatility) indexed by stock symbol

"""
Create a scatter plot of mean return vs. standard deviation (a measure of volatility)
for each stock. We would expect that the mean return would increase with volatility,
but this is not always the case.

"""

plot(std_ret,mean_ret,'ro')
for ii in range(len(symbols)):
    annotate(mean_ret.index[ii],(std_ret[ii],mean_ret[ii])) # Annotate the markers with the stock symbol
title('Mean Daily Return vs. Standard Deviation for 401K Funds')
xlabel('Standard Deviation of Daily Returns')
ylabel('Mean of Daily Returns')
show()

#4. Analyze selected set of funds

sel_symbols = ['PRSVX','PRLAX','TRMCX','PRHYX','RPSIX','PRTIX'] # This is a subset of stocks to study in greater depth
sel_returns = returns[sel_symbols] # Extract columns of return data for selected subset of stocks

mean_ret   = sel_returns.mean() # Returns a pandas DataFrame with mean values indexed by stock symbol
std_ret    = sel_returns.std()  # Returns a pandas DataFrame with standard deviations (volatility) indexed by stock symbol

"""
Create the same scatter plot for only the selected stock symbols

"""

plot(std_ret,mean_ret,'ro')
for ii in range(len(sel_symbols)):
    annotate(mean_ret.index[ii],(std_ret[ii],mean_ret[ii]))
title('Mean Daily Return vs. Standard Deviation for Selected 401K Funds')
xlabel('Standard Deviation of Daily Returns')
ylabel('Mean of Daily Returns')
show()

"""
Now create a boxplot as another means to visualize volatility in a stock. Note that the 
boxplot gets pretty busy for more than a handful of stocks

"""

sel_returns.boxplot()
title('Selected 401K Funds Daily Returns')
show()

"""
Finally calculate the correlation matrix between the various stocks. This returns a DataFrame
object with rows and columns labeled with the stock symbols.  It's actually fairly clever
because it automatically handles the fact that not all the symbols have data available on the
same day.

The values method returns just the array of data

"""

sel_corr=sel_returns.corr()     # Calculate correlation
sel_corr_values=sel_corr.values # Return just the array of correlation data (no labels)

"""
Now create a scatter plot matrix. This shows a probability density on each diagonal and
a scatter plot indicating correlation on the off-diagonals

"""

scatter_matrix(sel_returns, alpha=0.2, figsize=(6,6), diagonal='kde')
show()
