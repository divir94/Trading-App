import csv
import pickle

tickers_dict = {}

with open('WIKI_tickers.csv', 'rU') as f:
    reader = csv.reader(f)
    next(reader)  # skip the header
    for row in reader:
        ticker = row[0].split('/')[1]
        tickers_dict[ticker] = 1

pickle.dump( tickers_dict, open( "tickers_dict.p", "wb" ) )