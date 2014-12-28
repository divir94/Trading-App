import Quandl
import pandas as pd
import pickle

tickers  = ['IBM', 'AAPL', 'IBM']

# tickers = pickle.load(open( "tickers_dict.p", "rb" ))

#df = pd.DataFrame({"IBM": ibm.Close, "AAPL": apple.Close})

# df1 = pd.read_hdf('store.h5', 'df1')

df1 = pd.DataFrame()

for tic in tickers:
    if tic not in df1.columns:
        stock = Quandl.get('WIKI/%s' % tic, collapse='daily', column=4)
        stock.columns = [tic]
        df1 = pd.concat([df1, stock], axis=1)

# df1.to_hdf('store.h5','df1')
#print df.head()