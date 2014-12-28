import Quandl
import pandas as pd
import json
import signal
from contextlib import contextmanager
from time import time

class TimeoutException(Exception): pass
def timeout(fun, limit, *args ):
    @contextmanager
    def time_limit(seconds):
        def signal_handler(signum, frame):
            raise TimeoutException, "Timed out!"
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
        try: yield
        finally: signal.alarm(0)
    try:
        with time_limit(limit):
            return fun(*args)
    except TimeoutException, msg:
        return None

def get_stock(ticker):
    return Quandl.get('WIKI/%s' % ticker, collapse='daily', column=4)

def update_db(temp_df):
    main_df = pd.read_hdf('stocks_db.h5','df')
    new_df = pd.concat([main_df, temp_df], axis=1)
    new_df.to_hdf('stocks_db.h5','df')

def make_db(tickers):
    start_time = time()
    num_updated = 0
    # get list of tickers already in db
    tics_in_db = pd.read_hdf('stocks_db.h5','df').columns
    # make a temporary df to hold 10 stocks before updating db
    temp_df = pd.DataFrame()

    for num_in_db, tic in enumerate(tickers):
        # update db after every 10 iterations
        if num_updated%10 == 0 and num_updated!=0:
            update_db(temp_df)
            temp_df = pd.DataFrame()
            print '\nUpdating database. Updated: %d, Stocks in db: %d' % (num_updated, num_in_db)
            elapsed_time = time() - start_time
            print 'Time since last update: %.1fs\n' % elapsed_time
            start_time = time()

        # get stock if not already in db
        if tic in tics_in_db:
            # stock is in db
            print '%s already in db' % tic
        else:
            # get stock if it doesn't take too long
            stock = timeout(get_stock, 10, tic)
            if isinstance(stock, pd.DataFrame):
                # update temporary df
                stock.columns = [tic]
                temp_df = pd.concat([temp_df, stock], axis=1)
                num_updated += 1
                print 'Added %s to db' % tic
            else:
                # Timed out
                print "\nFunction timed out on ticker: %s\n" % tic


def main():
    # load tickers and file
    with open('tickers_dict.json', "rb") as f:
        tickers = json.loads(f.read()).keys()
    # get stock prices from quandl
    make_db(tickers)

main()